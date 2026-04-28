import grpc
import jornais_pb2
import jornais_pb2_grpc

def iniciar_publicador():
    print("=== PAINEL DO PUBLICANTE ===")
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = jornais_pb2_grpc.JornalServiceStub(channel)
        
        while True:
            print("\n--- Nova Notícia ---")
            topico = input("Tópico (ex: Esportes, Tecnologia): ")
            if not topico:
                break
                
            titulo = input("Título: ")
            conteudo = input("Conteúdo: ")
            
            request = jornais_pb2.PublicarRequest(
                topico=topico,
                titulo=titulo,
                conteudo=conteudo
            )
            
            try:
                # Faz a chamada RPC simples (Unary)
                resposta = stub.PublicarNoticia(request)
                print(f"Status: {resposta.mensagem}")
            except grpc.RpcError as e:
                print(f"Erro ao conectar com o Servidor: {e}")

if __name__ == '__main__':
    iniciar_publicador()