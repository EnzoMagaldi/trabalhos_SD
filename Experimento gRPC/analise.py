import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico():
    df = pd.read_csv('benchmark.log')
    # Agrupa por tamanho e calcula a média do RTT
    media_rtt = df.groupby('tamanho_bytes')['rtt_ms'].mean()
    
    plt.figure(figsize=(10, 6))
    media_rtt.plot(kind='bar', color='skyblue')
    
    plt.title('RTT Médio gRPC por Tamanho de Mensagem')
    plt.xlabel('Tamanho da Mensagem (Bytes)')
    plt.ylabel('RTT Médio (ms)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('resultado_benchmark.png')
    plt.show()

if __name__ == '__main__':
    gerar_grafico()