import socket

#função para aguardar uma conexão do client
def aguardar_conexao():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('', 12345))
    print('aguardando conexão...')
    s.listen(1)

    
    conn, addr = s.accept()

    mensagem = conn.recv(2048).decode()
    print(f"\nClient: {mensagem}\n")

    return conn
