import hashlib
import os

#função para transferir arquivos via socket
def transferir_arquivo(conn):
    #caminho do arquivo no computador server
    caminho_arquivo = input('Digite o caminho completo do arquivo: ')

    #sair da função
    if caminho_arquivo.lower() == 'sair':
        return

    #Nome do arquivo que vai ser enviado e o nome que ele receberá no client
    nome_arquivo = input('Digite o nome e a extenção do arquivo: ')
    conn.sendall(nome_arquivo.encode())

    if nome_arquivo.lower() == 'sair':
        return

    #variavel onde salva o caminho e o arquivo para que ele possa ser lido e transformado em bytes
    arquivo_para_tranferir = os.path.join(caminho_arquivo,nome_arquivo)

    #verificar se o arquivo existe
    try:
        with open(arquivo_para_tranferir, 'rb') as f:
          arquivo_bytes = f.read()
          conn.send(b'sim')

    except FileNotFoundError:
        print('\nArquivo ou pasta não existe')
        conn.send(b'nao')
        return

    except PermissionError:
        print('\nO usuário não tem permissão para acessar esse arquivo')
        conn.send(b'nao')
        return

    #pega o SHA256 do arquivo para comparar com o que vai chegar no client
    arquivo_hash = hashlib.sha256(arquivo_bytes).hexdigest()
    

    #confirmação de que o nome do arquivo ja chegou e ja posso mandar outra informação sem que haja conflito
    handshake = conn.recv(1024).decode()
    if handshake == 'ok':
        tamanho_arquivo = len(arquivo_bytes)
        conn.sendall(str(tamanho_arquivo).encode())

    #outra confirmação de que os dados ja chegaram e estão em variaveis
    handshake = conn.recv(1024).decode()
    if handshake == 'ok1':
        conn.sendall(arquivo_bytes)
    
    tamanho_arquivo_client = conn.recv(1024).decode()
    print(f'O tamanho do arquivo é {tamanho_arquivo} - Tamanho que chegou no Client: {tamanho_arquivo_client}')
    
    #recebe sha256 de como o arquivo chegou no client para que seja comparado com o que deveria ser
    sha256_client = conn.recv(1024).decode()
   
    if sha256_client == arquivo_hash:
        print(f'Arquivo chegou igual ao o que saiu!\nSHA256 CLIENT: {sha256_client}\nSHA256 SERVER: {arquivo_hash}')
    else:
        print(f'Arquivo teve um problema, não chegou todas as informações!\nSHA256 CLIENT: {sha256_client}\nSHA256 SERVER: {arquivo_hash}')

#função para pegar arquivos do computador Client
def pegar_arquivo(conn):
    caminho_arquivo = input('Caminho e o arquivo no computador do client(com extenção do arquivo): ')
    conn.sendall(str(caminho_arquivo).encode())
    if caminho_arquivo.lower() == 'sair':
        return
    salvar_arquivo = input('como quer que o arquivo seja salvo(colocar a extenção do arquivo): ')
    arquivo_existe = conn.recv(1024).decode()

    if arquivo_existe == '1':
        print('\nO arquivo não existe')
        return
    if arquivo_existe == '2':
        print('\nO usuário não tem permissão para acessar esse arquivo')
        return
    if arquivo_existe == '0':
        #tamanho de bytes que o arquivo tem
        tamanho_arquivo = int(conn.recv(4096).decode())
        conn.send(b"ok")#handshake porque o sendall está em linhas diferentes mas estão chegando juntos na mesma variavel

        #SHA256 do arquivo pra ver se chegou os mesmos bytes que saiu
        arquivo_sha256_client = conn.recv(2048).decode()
        conn.send(b"ok1")#handshake porque o sendall está em linhas diferentes mas estão chegando juntos na mesma variavel

        quantidade_bytes_chegaram = 0
        with open(salvar_arquivo, 'wb') as f:
            while quantidade_bytes_chegaram < tamanho_arquivo:
                arquivo_bytes = conn.recv(4096)
                f.write(arquivo_bytes)
                quantidade_bytes_chegaram += len(arquivo_bytes)
                print(f'\rCHEGARAM: {quantidade_bytes_chegaram} bytes    |    O arquivo tem: {tamanho_arquivo} bytes', end='')
        
        with open(salvar_arquivo, 'rb') as f:
            dados = f.read()
            arquivo_sha256_server = hashlib.sha256(dados).hexdigest()

        if quantidade_bytes_chegaram == tamanho_arquivo:
            print(f'Arquivo "{salvar_arquivo}" chegou com sucesso')
            
            if arquivo_sha256_server == arquivo_sha256_client:
                print(f'O conteúdo do arquivo chegou igual a quando saiu.\nSHA256 que saiu do Client:   {arquivo_sha256_client}\nSHA256 que chegou ao Server: {arquivo_sha256_server}')
            else:
                print(f'Houve uma alteração no conteúdo do arquivo.\nSHA256 que saiu do Client: {arquivo_sha256_client}\nSHA256 que chegou ao Server: {arquivo_sha256_server}')
