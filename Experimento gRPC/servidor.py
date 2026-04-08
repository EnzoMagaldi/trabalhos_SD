import grpc
from concurrent import futures
import experimento_pb2
import experimento_pb2_grpc
from datetime import datetime, timezone

class ExperimentoServicer(experimento_pb2_grpc.ExperimentoServiceServicer):
    def Enviar(self, request, context):
        tamanho = len(request.payload)
        timestamp = datetime.now(timezone.utc).isoformat() + 'Z'
        
        print(f"[servidor] Recebido payload de {tamanho} bytes em {timestamp}")
        
        return experimento_pb2.Confirmacao(
            tamanho_recebido=tamanho,
            timestamp_servidor=timestamp
        )

def servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    experimento_pb2_grpc.add_ExperimentoServiceServicer_to_server(ExperimentoServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    servidor()