# TCP Client-Server — Projeto Educacional

Projeto desenvolvido em 3 dias com o objetivo de aprender na prática como funciona comunicação TCP, sockets em Python e arquitetura client-server.

> ⚠️ **Aviso:** Este projeto é estritamente educacional. Desenvolvido para estudo de redes e programação com sockets. Use apenas em ambientes controlados e com autorização explícita.

---

## 📌 O que o projeto faz e casos de uso

Um servidor aguarda conexão de um cliente via TCP. Após conectado, o servidor pode:

- Executar comandos remotos na máquina do cliente
- Enviar e receber arquivos
- Capturar a tela do cliente *(BETA)*
- 
O projeto simula um Agente de Gerenciamento Remoto Centralizado (Arquitetura de Gestão de TI). Ele permite que um administrador gerencie dispositivos de forma centralizada (por exemplo, para automatizar a instalação de softwares em background em computadores de funcionários ou coletar diagnósticos do sistema).

Para garantir a segurança e o consentimento do dispositivo gerenciado (Cliente), o sistema implementa uma autenticação invertida: o Cliente valida a identidade do Servidor através de uma credencial local (.env) antes de aceitar qualquer comando.

---

## 🧠 O que aprendi

- Como funciona o handshake TCP na prática
- Uso da biblioteca `socket` do Python (AF_INET, SOCK_STREAM)
- Envio e recebimento de dados com `send` e `recv`
- Transferência de arquivos convertendo para bytes e reconstruindo no destino
- Verificação de integridade de arquivos com SHA-256 (hashlib)
- Encoding com base64
- Comunicação bidirecional entre processos em máquinas diferentes
- Tratamento de erros de conexão e reconexão automática
- Organização de projeto Python em módulos

---

## 🗂️ Estrutura

```
├── client.py          # Ponto de entrada do cliente
├── server.py          # Ponto de entrada do servidor
├── Client/
│   ├── procurar_conexao.py          # Conexão com o servidor
│   ├── executar_cmd.py              # Execução de comandos recebidos
│   ├── transferir_receber_arquivos.py
│   └── BETA/
│       └── enviar_captura_tela.py
└── Server/
    ├── aguardar_conexao.py          # Aguarda cliente conectar
    ├── menu.py                      # Interface de seleção de ação
    ├── mandar_cmd.py
    ├── tranferir_receber_arquivos.py
    └── BETA/
        └── captura_tela.py
```

---

## ▶️ Como usar

**Pré-requisitos:** Python 3.x
1.pip install -r requirements.txt
2.Crie um arquivo .env na raiz do projeto seguindo o modelo do .env.example e insira a sua senha de autenticação.
3. No arquivo `Client/procurar_conexao.py`, altere o IP para o IPv4 da máquina onde o servidor vai rodar
4. Rode o servidor: `python server.py`
5. Rode o cliente: `python client.py`

---

## 🛠️ Tecnologias

- Python 3
- `socket` — comunicação TCP
- `subprocess` — execução de comandos
- `Pillow` — captura de tela *(BETA)*

---

## 🚧 Em desenvolvimento

- Configuração de IP/porta via arquivo de config em vez de hardcoded
- Tratamento de erros mais robusto no servidor
- Criptografia na comunicação (SSL ou similar)
- Suporte a múltiplos clientes simultâneos
- Melhorias na captura de tela (BETA)
