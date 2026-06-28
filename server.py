from Server.aguardar_conexao import aguardar_conexao
from Server.menu import menu

def main():
    
    while True:
        try:
            conn = aguardar_conexao()
            
            while True:
                senha = input('\nDigite a senha: ')
                conn.send(str(senha).encode())    
                
                resultado = conn.recv(1024).decode()
                if resultado == '0':
                    print('acesso concedido!')
                    break
                
                elif resultado == '1':
                    print('senha errada!')
                
                elif resultado == '2':
                    print('Limite de tentava excedido!')
                    print('Encerrando programa...')
                    exit()
                

            while True:
                menu(conn)
        
        except (ConnectionRefusedError, ConnectionAbortedError, BrokenPipeError):
            print('\nClient desconectou')

        except KeyboardInterrupt:
            print('\nFechando Programa...')
            break
        
        finally:
            try:
                conn.close()
            except:
                pass

if __name__ == '__main__':
    main()