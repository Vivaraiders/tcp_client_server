import ast
from PIL import Image

def capturar_tela_em_video(conn):
    parar = 'nao'
    comparacao_frames = b''
    try:
        
        while True:
            conn.send(parar.encode())#envia confirmação se para while ou não - No momento só para com CRTL C
            tamanho_screenshot_rgb = int(conn.recv(1024).decode())
            conn.send(b'ok') #Handshake
            tamanho_screenshot_size = int(conn.recv(1024).decode())
            conn.send(b'ok1')#Handshake

            bytes_recebidos = 0 #contador de bytes recebidos no while
            screenshot_rgb = b''
            dados = b''
            while bytes_recebidos < tamanho_screenshot_rgb: #loop pra verificar se todos os bytes do obj da imagem ja chegou
                dados = conn.recv(1024)
                screenshot_rgb += dados
                bytes_recebidos += len(dados)
            
            if bytes_recebidos == tamanho_screenshot_rgb:
                conn.send(b'ok2')

                bytes_recebidos = 0
                dados = b'' #resetar ele pra zero porque ele foi usado no screenshot_rgb e ainda contem dados
                while bytes_recebidos < tamanho_screenshot_size: #loop pra verificar se o tamanho do obj da imagem ja chegou para converter em imagem  
                    a = conn.recv(1024)
                    dados += a
                    bytes_recebidos += len(a)
                if bytes_recebidos == tamanho_screenshot_size:
                    #ast.literal_eval é porque o que ta sendo recebido é um tupla em formato de string, isso converte de volta para tupla
                    print(dados)
                    screenshot_size = ast.literal_eval(dados.decode())

            imagem_convertida = Image.frombytes(
                "RGB",
                screenshot_size,
                screenshot_rgb
            )
            
            if screenshot_rgb != comparacao_frames:
                imagem_convertida.show()
            comparacao_frames = screenshot_rgb
    
    except KeyboardInterrupt:
        parar = 'sim'
        print('Operação Cancelada!')
        conn.send(parar.encode())
        return
