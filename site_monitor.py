#!/usr/bin/env python

import logging
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from time import sleep

import decouple
import requests


def configura_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    log_formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s')

    log_file_handler = logging.FileHandler('site_monitor.log')
    log_file_handler.setFormatter(log_formatter)

    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setFormatter(log_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_stream_handler)  # Mostra log na tela

    return logger


def get_data_hora():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def envia_email(msg_contents):
    try:
        # Tenta obter credenciais a partir de arquivo .env
        EMAIL_ADDRESS = decouple.config('EMAIL_ADDR')
        EMAIL_PASSWORD = decouple.config('EMAIL_PASSWD')

    except decouple.UndefinedValueError as value_ex:
        logger.critical(f'{value_ex}')
        sys.exit(1)

    except Exception as ex:
        logger.critical(f'{repr(ex)}')
        raise

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        # TODO: Tratar exceções na rotina de envio de email #1
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg_contents)
        logger.info(f'email enviado')


def verifica_status_url(url, tentativas=5):
    TEMPO_SLEEP = 3
    mensagem = ''
    sem_resposta = False

    for _ in range(0, tentativas):
        try:
            requisicao = requests.get(url, timeout=5)

        except Exception as conn_ex:
#        except requests.exceptions.ConnectionError as conn_ex:
            # TODO: Enviar e-mail com o trace da exceção #2
            logger.critical(f'{conn_ex}')
            sys.exit(1)

        else:
            if requisicao.status_code != 200:
                sem_resposta = True
                mensagem = mensagem + \
                    f'{get_data_hora()}, {url}, {requisicao.status_code}, {requests.status_codes._codes[requisicao.status_code][0]}\n'
                logger.error(
                    f'{url},{requisicao.status_code},{requests.status_codes._codes[requisicao.status_code][0]}')
                sleep(TEMPO_SLEEP)

            else:
                sem_resposta = False
                mensagem = f'{url},{requisicao.status_code},{requests.status_codes._codes[requisicao.status_code][0]}'
                break

    return sem_resposta, mensagem


def prepara_msg(url, corpo_email):
    # TODO: Obter lista de destinatários do e-mail de um arquivo #3
    email_recipients = "denisranderson@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = f'Sem resposta: {url}'
    msg['From'] = 'Monitor de URL'
    msg['To'] = email_recipients
    msg.set_content(corpo_email)

    return msg


def main():
    # TODO: Obter nome dos arquivos de URL e e-mails na linha de comando #4
    # TODO: Obter URL a monitorar de arquivo #5
    url_monitorada = 'https://www.uol.com.br'

    url_monitorada_fora, mensagem = verifica_status_url(url_monitorada)

    if url_monitorada_fora:
        envia_email(prepara_msg(url_monitorada, mensagem))

    else:
        logger.info(mensagem)


if __name__ == "__main__":
    logger = configura_logger()
    main()
