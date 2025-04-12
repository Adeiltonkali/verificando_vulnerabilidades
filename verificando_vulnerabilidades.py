import socket
import requests

# Função para verificar se é possível se conectar ao host e porta informados
def verificar_conexao(host, porta=80, timeout=3):
    try:
        # Converte o domínio em um endereço IP
        ip = socket.gethostbyname(host)
        print(f'[INFO] IP de destino {ip}')

        # Tenta estabelecer uma conexão com o host na porta especificada
        socket.create_connection((ip, porta), timeout=timeout)
        print(f'[OK] Conexão com {host}:{porta} estabelecida com sucesso!')
        return True, ip

    # Tratamento de erro para host inválido
    except socket.gaierror:
        print(f"[ERRO] Host {host} inválido ou não encontrado.")
        return False, None

    # Tratamento de erro para conexão que excede o tempo limite
    except socket.timeout:
        print(f'[ERRO] Tempo esgotado ao tentar se conectar em {host}:{porta}.')
        return False, None

    # Tratamento para outros tipos de falhas na conexão
    except Exception as e:
        print(f'[ERRO] Falha na conexão com {host}:{porta} → {e}')
        return False, None

# Função que escaneia uma porta específica e tenta identificar qual serviço está nela
def scan_port(ip, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)  # Tempo máximo de espera para cada porta

        code = client.connect_ex((ip, port))

        if code == 0:
            # Tenta descobrir o nome do serviço que usa essa porta
            try:
                servico = socket.getservbyport(port, 'tcp')
            except:
                servico = "desconhecido"

            print(f"[✔] Porta {port:<5} aberta  | Serviço identificado: {servico}")

        client.close()

    except Exception as e:
        print(f"[ERRO] Falha ao verificar porta {port}: {e}")

# Execução principal do programa
if __name__ == "__main__":
    # Entrada do usuário
    destino = input('Digite o domínio ou IP de destino: ')

    # Verifica a conexão com o host informado
    status, ip = verificar_conexao(destino)

    # Se a conexão for bem-sucedida, inicia o scan das portas
    if status:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]  # Lista de portas comuns
        print('\n[INFO] Iniciando o scan de portas...\n')
        for port in ports:
            scan_port(ip, port)
