import grpc
from concurrent import futures
import jornais_pb2
import jornais_pb2_grpc
import time
from datetime import datetime

class JornalServicer(jornais_pb2_grpc.JornalServiceServicer):
    def AssinarJornal(self, request, context):
        print(f"[Servidor] {request.nome_cliente} assinou o jornal: {request.topico}")
        
        # Simulação de um loop que envia notícias quando elas "acontecem"
        noticias_enviadas = 0
        try:
            while context.is_active():
                # Aqui você integraria com um banco de dados ou fila real
                # Por enquanto, vamos simular o envio de uma notícia a cada 5 segundos
                time.sleep(5)
                
                noticia = jornais_pb2.Noticia(
                    jornal=request.topico,
                    titulo=f"Edição Extra #{noticias_enviadas + 1}",
                    conteudo=f"Conteúdo exclusivo para assinantes do {request.topico}.",
                    timestamp=datetime.now().strftime("%H:%M:%S")
                )
                
                yield noticia
                noticias_enviadas += 1
        except Exception as e:
            print(f"Conexão encerrada para {request.nome_cliente}: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    jornais_pb2_grpc.add_JornalServiceServicer_to_server(JornalServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor de Notícias rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()