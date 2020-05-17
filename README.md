# TM - The Messenger
Messaging system between friends

# Introduction
 - Brief introduction to the system.

# Requirements
 - Tests performed on Windows 10 with python (3.8.1)

## libraries
 - Django==3.0.3
 - python-decouple==3.3

 ## Adicionado Configurações para decouple
  - Adicionar arquivo .env na raiz do projeto
  - Colocar seguintes parametros:
  * SECRET_KEY=0atyt0aj^jy@w_*ylpmy9m$im4q_mahpiv8bkg&as-kh%6asg+
  * DEBUG=True
  * EMAIL_FROM=(e-mail para disparar msg do servidor)
  * PASS_EMAIL=(senha do e-mail)
  * SMTP_CONFIG=(configuraçao smtp do email do servidor)