import grpc
from concurrent import futures
import jornais_pb2
import jornais_pb2_grpc
from datetime import datetime
import queue
import threading

class JornalServicer(jornais_pb2_grpc.JornalServiceServicer):
    def __init__(self):
        # Dicionário para guardar as filas de mensagens: { "Topico": [fila1, fila2, ...] }
        self.topicos = {}
        # Trava para evitar problemas de concorrência (Thread-safety)
        self.lock = threading.Lock()

    def AssinarJornal(self, request, context):
        print(f"[Servidor] '{request.nome_cliente}' assinou o tópico: {request.topico}")
        
        # Cria uma fila exclusiva para este assinante
        fila_assinante = queue.Queue()

        with self.lock:
            if request.topico not in self.topicos:
                self.topicos[request.topico] = []
            self.topicos[request.topico].append(fila_assinante)

        try:
            # O stream fica aberto enquanto o cliente estiver conectado
            while context.is_active():
                try:
                    # Tenta pegar uma notícia da fila (espera até 1 segundo)
                    noticia = fila_assinante.get(timeout=1)
                    yield noticia # Envia a notícia pelo stream gRPC
                except queue.Empty:
                    # Se a fila estiver vazia, apenas continua o loop checando se o cliente está ativo
                    continue
        except Exception as e:
            print(f"[Servidor] Erro na conexão com {request.nome_cliente}: {e}")
        finally:
            # Quando o cliente desconecta (Ctrl+C), remove a fila dele do dicionário
            with self.lock:
                if request.topico in self.topicos:
                    self.topicos[request.topico].remove(fila_assinante)
                    if not self.topicos[request.topico]: # Se não sobrar ninguém, deleta a chave
                        del self.topicos[request.topico]
            print(f"[Servidor] '{request.nome_cliente}' cancelou a assinatura do tópico: {request.topico}")

    def PublicarNoticia(self, request, context):
        print(f"[Servidor] Recebida publicação para o tópico '{request.topico}': {request.titulo}")
        
        noticia = jornais_pb2.Noticia(
            jornal=request.topico,
            titulo=request.titulo,
            conteudo=request.conteudo,
            timestamp=datetime.now().strftime("%H:%M:%S")
        )

        # Distribui a notícia para todos os assinantes daquele tópico
        inscritos = 0
        with self.lock:
            if request.topico in self.topicos:
                for fila in self.topicos[request.topico]:
                    fila.put(noticia)
                inscritos = len(self.topicos[request.topico])
        
        mensagem_retorno = f"Notícia distribuída para {inscritos} assinante(s)."
        return jornais_pb2.PublicarResponse(sucesso=True, mensagem=mensagem_retorno)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jornais_pb2_grpc.add_JornalServiceServicer_to_server(JornalServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor (Pub/Sub) rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()