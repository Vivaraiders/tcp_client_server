import hashlib

#função que recebe arquivo do servidor via socket 
def receber_arquivo(conn):
    nome_arquivo = conn.recv(1024).decode()
    if nome_arquivo.lower() == 'sair':
        return
    
    arquivo_existe = conn.recv(1024).decode()

    if arquivo_existe == 'nao':
        return

    conn.send(b'ok')#para confirmar que chegou
    tamanho_arquivo = int(conn.recv(2048).decode())

    conn.send(b'ok1')#para confirmar que chegou

    quantidade_bytes_recebidos = 0
    with open(nome_arquivo, 'wb') as f:
        while quantidade_bytes_recebidos < tamanho_arquivo:
            arquivo_bytes = conn.recv(4096)
            f.write(arquivo_bytes)
            quantidade_bytes_recebidos += len(arquivo_bytes)    
    conn.send(str(quantidade_bytes_recebidos).encode())

    with open(nome_arquivo, 'rb') as f:
        dados = f.read()
        sha256_client = hashlib.sha256(dados).hexdigest()
    
    conn.send(sha256_client.encode())

def enviar_arquivo(conn):
    arquivo_enviar = conn.recv(2048).decode()
    if arquivo_enviar.lower() == 'sair':
        return
    try:
        with open(arquivo_enviar, 'rb') as f:
            arquivo_bytes = f.read()
            conn.send(b'0')
    except FileNotFoundError:
        conn.send(b'1')
        return
    except PermissionError:
        conn.send(b'2')
        return
    conn.sendall(str(len(arquivo_bytes)).encode())

    handshake = conn.recv(1024).decode()
    if handshake.lower() == "ok":
        hash_arquivo = hashlib.sha256(arquivo_bytes).hexdigest()
        conn.sendall(hash_arquivo.encode())

    handshake = conn.recv(1024).decode()
    if handshake.lower() == "ok1":
        conn.sendall(arquivo_bytes)
    