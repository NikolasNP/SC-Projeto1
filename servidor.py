import socket
import VigenereTable

cypher_table = VigenereTable.CypherTable()
map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Configurações do servidor
HOST = 'localhost'  # ou '0.0.0.0' para aceitar de qualquer IP
PORT = 5000        # Porta que será usada

# Criar o socket TCP (SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar o socket ao endereço e porta
server_socket.bind((HOST, PORT))

# Colocar o socket em modo de escuta
server_socket.listen()
print(f"Servidor ouvindo em {HOST}:{PORT}...")

try:
    while True:
        # Aceitar nova conexão
        conn, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")
        dado = []

        with conn:
            buffer = ""
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                buffer += data
        
                # Verifica se temos duas mensagens separadas por '\n'
                if buffer.count('\n') >= 2:
                    partes = buffer.split('\n')
                    chave_expandida = partes[0]
                    cypher = partes[1]
        
                    print(f"Chave recebida: {chave_expandida}\n")
                    print(f"Mensagem cifrada recebida: {cypher}\n")

                    decode = ""

                    #Decodificação
                    for i in range(len(cypher)):
                        index_tabela = map.index(chave_expandida[i])
                        linha = cypher_table.final_table[index_tabela]
                        coluna = linha.index(cypher[i])
                        tamanho = len(linha[:coluna+1])
                        decode += map[tamanho-1]
                        
                    resposta = f"Mensagem: {decode}"
                    conn.sendall(resposta.encode())
                    break  # <- SAI DO LOOP DE LEITURA
except KeyboardInterrupt:
    print("\nServidor encerrado manualmente.")
finally:
    server_socket.close()