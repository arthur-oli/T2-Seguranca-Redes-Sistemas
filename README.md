# T2 - Segurança de Redes e Sistemas

## Descrição
Este repositório contém o **Trabalho 2** da disciplina de Segurança de Redes e Sistemas, que consiste na implementação de uma técnica de geração de tokens, através do algoritmo OTP de Lamport.
Os códigos client.py e server.py têm esse nome apenas pela didática, pois não são conectados, e rodam offline. Eles também possuem base de dados separada. (banco_client.db e banco_server.db)

## Conteúdo

### 1. client.py
- **Desconectado de server.py**
    - **Instruções**: 
    Rodar o código, cadastrar o nome de usuário (chave primária), senha semente e senha local (para acessar base de dados).
    Após isso, inserir nome de usuário e senha novamente para obter uma lista de 5 tokens.

### 2. server.py
- **Desconectado de client.py**
    - **Instruções**: 
    Rodar o código, cadastrar o nome de usuário (chave primária) e senha semente.
    Após isso, inserir nome de usuário e token obtido do cliente para validar.
    Se o token tiver sido utilizado, ele e todos os outros que dependiam dele (os posteriores na geração) não ficarão disponíveis para uso.
    Ao inserir o nome de usuário, os tokens que o sistema aceita vêm impressos na tela, com a mensagem de "DEBUG", para facilitar o entendimento.