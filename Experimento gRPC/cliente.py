import grpc
import experimento_pb2
import experimento_pb2_grpc
import time
import csv
from datetime import datetime

def run_benchmark(host='localhost'):
    tamanhos = [1, 10000, 100000, 1000000]
    repeticoes = 20
    
    with grpc.insecure_channel(f'{host}:50051') as channel:
        stub = experimento_pb2_grpc.ExperimentoServiceStub(channel)
        
        with open('benchmark.log', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp', 'tamanho_bytes', 'indice_chamada', 'rtt_ms'])
            
            for tamanho in tamanhos:
                print(f"Iniciando testes para {tamanho} bytes...")
                payload = b'a' * tamanho 
                
                for i in range(repeticoes):
                    msg = experimento_pb2.Mensagem(payload=payload)
                    
                    start_time = time.perf_counter()
                    response = stub.Enviar(msg)
                    end_time = time.perf_counter()
                    
                    rtt_ms = (end_time - start_time) * 1000
                    ts_local = datetime.now().isoformat()
                    
                    writer.writerow([ts_local, tamanho, i+1, rtt_ms])
    print("Benchmark concluído! Arquivo benchmark.log gerado.")

if __name__ == '__main__':
    run_benchmark('localhost') 