import grpc
import jornais_pb2
import jornais_pb2_grpc

def assinar(nome, topico):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = jornais_pb2_grpc.JornalServiceStub(channel)
        request = jornais_pb2.AssinaturaRequest(nome_cliente=nome, topico=topico)
        
        print(f"--- Aguardando notícias do {topico} ---")
        try:
            # O loop abaixo fica "preso" aguardando novas mensagens do servidor
            for noticia in stub.AssinarJornal(request):
                print(f"\n[{noticia.timestamp}] NOVO ARTIGO NO {noticia.jornal}")
                print(f"Título: {noticia.titulo}")
                print(f"Resumo: {noticia.conteudo}")
        except grpc.RpcError as e:
            print(f"Erro na conexão: {e}")

if __name__ == '__main__':
    # Você pode rodar vários clientes em terminais diferentes com tópicos diferentes
    meu_topico = input("Qual jornal deseja assinar? ")
    assinar("Usuario_Teste", meu_topico)