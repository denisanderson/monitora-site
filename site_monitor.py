#!/usr/bin/env python
 
import os, sys, requests, smtplib
from time import sleep
from decouple import config
from datetime import datetime
from email.mime.text import MIMEText

# ler informações a partir de arquivo .env localizado no mesmo dir do script
try:
    EMAIL_ADDRESS = config('EMAIL_ADDR')
    EMAIL_PASS = config('EMAIL_PASSWD')
except Exception as e:
    print(f'[x] Falha: {e}')
    sys.exit(1) # aborta a execução do script se não conseguir obter as credenciais

DEBUG_LEVEL = 0 # 0: Off / 1: On

# TODO: ler a partir de arquivo os destinatarios do email
EMAIL_RCPT = "denisranderson@gmail.com"

now = datetime.now()
data_hora_execucao = now.strftime("%d/%m/%Y %H:%M:%S")

def envia_email(user_email, user_passwd, recipients, msg):
    SMTP_SERVER_NAME = 'smtp.gmail.com'
    SMTP_SERVER_PORT = 465

    server = smtplib.SMTP_SSL(SMTP_SERVER_NAME, SMTP_SERVER_PORT)
    server.ehlo()
    server.login(user_email, user_passwd)
    server.set_debuglevel(DEBUG_LEVEL)

    print(f'[OK] Enviando email para: {recipients}')
    server.sendmail(user_email, recipients, msg)

    server.close()
    print(f'[OK] {data_hora_execucao}, Email enviado')

# TODO: gerar log da execução do script
def log():
    pass

print(f'[OK] {data_hora_execucao}, Processamento iniciado')

# TODO: ler de arquivo as urls a monitorar
url_monitorada = 'https://www.uol.com.br/'

# TODO: corrigir problema que o destinatario da msg vai no campo CCo
MSG_BODY = MIMEText('{}\nServidor {} não respondeu.'.format(data_hora_execucao, url_monitorada))
MSG_BODY['Subject'] = 'Falha: {}'.format(url_monitorada)
MSG_BODY['From'] = 'Monitora Site Test Script'

try:
    # TODO: testar se url responde em 5 tentativas a cada 1 seg
    envia_email(EMAIL_ADDRESS, EMAIL_PASS, EMAIL_RCPT, MSG_BODY.as_string())
except Exception as e:
    print('[x] Falha: {}'.format(e))
