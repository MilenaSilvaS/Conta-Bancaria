import random
import threading
from ContaBancaria import ContaBancaria

def inicializar_contas(num_contas, saldo_min=100, saldo_max=1000):
    contas = []
    for i in range(1, num_contas + 1):
        saldo = random.randint(saldo_min, saldo_max)
        contas.append(ContaBancaria(i, saldo))
    return contas

def realizar_operacoes(contas, transacoes, num_operacoes):
    for _ in range(num_operacoes):
        origem = random.choice(contas)
        destino = random.choice([conta for conta in contas if conta != origem])
        valor = random.randint(1, 100)
        transacoes.transferir(origem, destino, valor)

def simular_transferencias(contas, transacoes, num_threads, num_operacoes):
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=realizar_operacoes, args=(contas, transacoes, num_operacoes))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
