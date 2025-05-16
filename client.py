from socket import socket, AF_INET, SOCK_STREAM
import time
import VigenereTable

# Função para cifrar a mensagem usando Vigenère
def vigenere_encrypt(mensagem, chave, tabela):
    map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    chave_expandida = (chave * (len(mensagem) // len(chave) + 1))[:len(mensagem)]
    cypher = ""

    for i in range(len(mensagem)):
        linha = map.index(mensagem[i])
        coluna = map.index(chave_expandida[i])
        cypher += tabela.final_table[linha][coluna]

    return chave_expandida, cypher

# Configuração do cliente
HOST = 'localhost'
PORT = 5000

# Mensagem e chave
mensagem = "SECURITYISSAFE"
segredo =  "OBSCURESECRET"

# Geração da tabela
cypher_table = CypherTable()

# Cifrar a mensagem
chave_expandida, cypher = vigenere_encrypt(mensagem, segredo, cypher_table)

# Mostrar a tabela (opcional)
# for linha in cypher_table.final_table:
#     print(linha)

# Conexão com o servidor
with socket(AF_INET, SOCK_STREAM) as clientSocket:
    clientSocket.connect((HOST, PORT))
    

    clientSocket.sendall((chave_expandida + '\n').encode())
    time.sleep(0.05)
    clientSocket.sendall((cypher + '\n').encode())

    # Esperar resposta do servidor
    resposta = clientSocket.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")