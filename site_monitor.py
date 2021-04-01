#!/usr/bin/env python

# TODO: [ ] Cria função para preparar a mensagem de email
# TODO: [ ] Implementa logging
# TODO: [ ] Obtem lista de URL de arquivo
# TODO: [ ] Obtem lista de destinatários do email de arquivo
# TODO: [ ] Implementa chamada main()
# TODO: [ ] Obtem nome dos arquivos de URL e destinários do email na linha de comando
# TODO: [ ] Envia email com o trace da exceção nas falhas
# TODO: [ ] Inclui bloco Try/Except na rotina de envio de email

import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from time import sleep

import decouple
import requests


def get_data_hora():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def envia_email(msg_contents):
    try:
        # Tenta obter credenciais a partir de arquivo .env
        EMAIL_ADDRESS = decouple.config('EMAIL_ADDR')
        EMAIL_PASSWORD = decouple.config('EMAIL_PASSWD')

    except decouple.UndefinedValueError as value_ex:
        print(f'{get_data_hora()}, {value_ex}')  # log
        sys.exit(1)

    except Exception as ex:
        print(f'{get_data_hora()}, {repr(ex)}')  # log
        raise

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg_contents)
        print(f'{get_data_hora()}, email enviado')  # log


def verifica_status_url(url, tentativas=5):
    TEMPO_SLEEP = 2
    mensagem = ''
    sem_resposta_ok = False

    for _ in range(0, tentativas):
        try:
            requisicao = requests.get(url, timeout=5)

        except requests.exceptions.ConnectionError as conn_ex:
            mensagem = f'{get_data_hora()}, {conn_ex}'
            print(mensagem)  # log
            sys.exit(1)

        else:
            if requisicao.status_code != 200:
                sem_resposta_ok = True
                mensagem = mensagem + \
                    f'{get_data_hora()}, {url}, {requisicao.status_code}, {requests.status_codes._codes[requisicao.status_code][0]}\n'
                sleep(TEMPO_SLEEP)

            else:
                sem_resposta_ok = False
                mensagem = f'{get_data_hora()}, {url}, {requisicao.status_code}, {requests.status_codes._codes[requisicao.status_code][0]}'
                break

    return sem_resposta_ok, mensagem


def prepara_msg():
    pass


url_monitorada = 'https://www.uol1.com.br'

url_monitorada_fora, mensagem_verificacao = verifica_status_url(url_monitorada)

if url_monitorada_fora:
    email_recipients = "denisranderson@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = f'Sem resposta: {url_monitorada}'
    msg['From'] = 'Monitor de URL'
    msg['To'] = email_recipients
    msg.set_content(mensagem_verificacao)

    # prepara_msg()
    envia_email(msg)
else:
    print(mensagem_verificacao)  # log
