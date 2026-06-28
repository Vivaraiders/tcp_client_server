from mss.windows import MSS

def enviar_captura_tela(conn):
    parar = 'nao'
    taxa_quadros = b''
    with MSS() as sct:
        while parar.lower() == 'nao':
            parar = conn.recv(1024).decode()

            screenshot = sct.grab(sct.monitors[1]) # captura de tela e armazenamento da imagem na variavel
            if taxa_quadros != screenshot.rgb: #se os bytes da imagem anterior for igual a aos byte da atual, ele envia uma foto nova
                conn.sendall(str(len(screenshot.rgb)).encode())

                #confirmação de que o tamanho da foto chegou
                hand = conn.recv(1024).decode()
                if hand == 'ok':
                    tamanho = (screenshot.width, screenshot.height)

                    #se n transformar o str antes, ele pega '2' por que é uma tupla com 2 valores, tem q transformar em str e encodar para pegar os bytes com len, depois encodar o len
                    conn.sendall(str(len(str(tamanho).encode())).encode())
                    hand = conn.recv(1024).decode()
                    if hand == 'ok1':
                        conn.sendall(screenshot.rgb)
                        hand = conn.recv(1024).decode()
                        if hand == 'ok2':
                            #tamanho do SCREENSHOT.SIZE: to usando a variavel 'tamanho' pq o screenshot.size retorna coisas alem da tupla, e eu so preciso da tupla
                            conn.sendall(str(tamanho).encode())
            taxa_quadros = screenshot.rgb
