import string
from collections import Counter
import textwrap

# Parte I – Cifrador e Decifrador
def vigenere_cifrar(texto, key):
    texto = texto.upper().replace(" ", "")
    key = key.upper()
    cifrado = ""
    key_index = 0

    for char in texto:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            cifrado += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            key_index += 1
        else:
            cifrado += char
    return cifrado

def vigenere_decifrar(texto_cifrado, key):
    texto_cifrado = texto_cifrado.upper().replace(" ", "")
    key = key.upper()
    decifrado = ""
    key_index = 0

    for char in texto_cifrado:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            decifrado += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            key_index += 1
        else:
            decifrado += char
    return decifrado

# Parte II – Análise de Frequência

# Frequência de letras no português
freq_portugues = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57, 'F': 1.02,
    'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40, 'K': 0.02, 'L': 2.78,
    'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 'Q': 1.20, 'R': 6.53,
    'S': 7.81, 'T': 4.74, 'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21,
    'Y': 0.01, 'Z': 0.47
}

# Frequência de letras no inglês
freq_ingles = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70, 'F': 2.23,
    'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03,
    'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.10, 'R': 5.99,
    'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
    'Y': 1.97, 'Z': 0.07
}

def analise_de_freq(texto):
    texto = ''.join(filter(str.isalpha, texto.upper()))
    total = len(texto)
    counter = Counter(texto)
    freq = {letter: (counter.get(letter, 0) / total) * 100 for letter in string.ascii_uppercase}
    return freq

def qui_quadrado(observado, esperado):
    qui = 0.0
    for letter in string.ascii_uppercase:
        o = observado.get(letter, 0)
        e = esperado.get(letter, 0)
        qui += ((o - e) ** 2) / e if e > 0 else 0
    return qui

def calcular_tamanho_chave(texto_cifrado, max_key_length=20):
    def ic(texto):
        freq = Counter(texto)
        N = len(texto)
        return sum(f*(f-1) for f in freq.values()) / (N*(N-1)) if N > 1 else 0

    texto_cifrado = ''.join(filter(str.isalpha, texto_cifrado.upper()))
    avg_ics = []
    for key_len in range(1, max_key_length+1):
        ics = []
        for i in range(key_len):
            seq = texto_cifrado[i::key_len]
            ics.append(ic(seq))
        avg_ics.append((key_len, sum(ics)/len(ics)))
    return max(avg_ics, key=lambda x: x[1])[0]

def descobrir_chave(texto_cifrado, freq_esperada):
    key_len = calcular_tamanho_chave(texto_cifrado)
    texto_cifrado = ''.join(filter(str.isalpha, texto_cifrado.upper()))
    key = ""

    for i in range(key_len):
        block = texto_cifrado[i::key_len]
        min_qui = float('inf')
        best_shift = 0
        for shift in range(26):
            decifrado = ''.join(chr(((ord(c) - ord('A') - shift) % 26) + ord('A')) for c in block)
            freq = analise_de_freq(decifrado)
            qui = qui_quadrado(freq, freq_esperada)
            if qui < min_qui:
                min_qui = qui
                best_shift = shift
        key += chr((best_shift % 26) + ord('A'))
    return key

# Função auxiliar para imprimir blocos com quebra de linha
def print_block(label, texto):
    print(f"{label}:\n")
    print(textwrap.fill(texto, width=80))
    print()

# Testes e demonstração
if __name__ == "__main__":
    print("Parte I: cifrador / decifrador:")

    mensagem = "ATTACKATDAWN"
    senha = "LEMON"

    print(f"Mensagem original: {mensagem}")
    print(f"Senha: {senha}")

    cifrado = vigenere_cifrar(mensagem, senha)
    print(f"Texto cifrado: {cifrado}")
    print(f"Texto decifrado: {vigenere_decifrar(cifrado, senha)}")

    print("\n" + "="*80)
    print("Parte II: ataque de recuperação de senha por análise de frequência:")
    print("="*80)

    # Exemplo em português
    mensagem_pt = (
        "AO VERME QUE PRIMEIRO ROEU AS FRIAS CARNES DO MEU CADAVER DEDICO"
        " COMO SAUDOSA LEMBRANCA ESTAS MEMORIAS POSTUMAS DE UMA RAPOSA RAPIDA E"
        " DE COR MARROM QUE SALTOU SOBRE O CAO PREGUICOSO CHAMADO BOB"
    )

    senha_pt = "LIMAO"
    cifrado_pt = vigenere_cifrar(mensagem_pt, senha_pt)

    print("\n--- Mensagem em Português ---")
    print_block("Texto cifrado", cifrado_pt)

    senha_descoberta_pt = descobrir_chave(cifrado_pt, freq_portugues)
    print(f"Senha descoberta: {senha_descoberta_pt}\n")

    mensagem_recuperada_pt = vigenere_decifrar(cifrado_pt, senha_descoberta_pt)
    print_block("Mensagem decifrada", mensagem_recuperada_pt)

    # Exemplo em inglês
    mensagem_en = (
        "INFORMATION SECURITY IS IMPORTANT TO ENSURE THE CONFIDENTIALITY INTEGRITY AND AVAILABILITY OF DATA"
        "IN THE MODERN WORLD WHERE DATA IS TRANSMITTED ANALYZED AND STORED ON MULTIPLE SYSTEMS AND NETWORKS"
        "STRONG PASSWORDS AND ENCRYPTION TECHNIQUES HELP SECURE COMMUNICATION AGAINST CYBER ATTACKS"
    )
    senha_en = "LEMON"
    cifrado_en = vigenere_cifrar(mensagem_en, senha_en)

    print("\n--- Mensagem em Inglês ---")
    print_block("Texto cifrado", cifrado_en)

    senha_descoberta_en = descobrir_chave(cifrado_en, freq_ingles)
    print(f"Senha descoberta: {senha_descoberta_en}\n")

    mensagem_recuperada_en = vigenere_decifrar(cifrado_en, senha_descoberta_en)
    print_block("Mensagem decifrada", mensagem_recuperada_en)
