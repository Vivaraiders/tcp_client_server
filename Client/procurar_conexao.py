import socket

#função para conectar com o servidor
def procurar_conexao():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('192.168.0.177', 12345))#o ip tem que ser o ipv4 da maquina onde o server esta rodando

    mensagem = 'Conectado!'
    conn.send(mensagem.encode())

    return conn