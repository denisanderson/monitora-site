#!/usr/bin/env python

import json
import logging
import logging.config
import os.path
import smtplib
import sys
import time
import traceback
from datetime import datetime
from email.message import EmailMessage

import decouple
import requests


def configura_logger(logging_config_file):
    try:
        # Tenta carregar configurações de logging
        with open(logging_config_file) as cfg_file:
            logging.config.dictConfig(json.load(cfg_file))

    except Exception as ex:
        print(f'[!] Falha na carga da configuração do logger: {repr(ex)}')
        sys.exit(1)

    else:
        # Cria logger
        logger = logging.getLogger(__name__)

        return logger


def get_data_hora():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def envia_email(msg_contents):

    try:
        # Tenta obter credenciais a partir de arquivo .env
        EMAIL_ADDRESS = decouple.config('EMAIL_ADDR')
        EMAIL_PASSWORD = decouple.config('EMAIL_PASSWD')

    except decouple.UndefinedValueError as ex:
        # Registra a falha e termina o programa
        logger.error(f'Falha em recuperar valor da variável de ambiente. {ex}')
        sys.exit(1)

    except Exception as ex:
        # Registra a falha e termina o programa
        logger.error(f'{repr(ex)}')
        sys.exit(1)

    else:

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            try:
                # Tenta fazer login no gmail e enviar a mensagem
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg_contents)

            except smtplib.SMTPAuthenticationError as auth_error:
                logger.error(f'Problema na autenticação. {auth_error}')
                sys.exit(1)

            except AttributeError as attr_error:
                logger.error(
                    f'Problema na preparação da mensagem. {attr_error}')
                sys.exit(1)

            except Exception as ex:
                logger.error(repr(ex))
                sys.exit(1)

            else:
                logger.debug(f'Notificação da falha enviada por email')


def verifica_status_url(url, tentativas=5):
    TEMPO_SLEEP = 3
    sem_resposta = False
    mensagem = ''

    for _ in range(tentativas):
        try:
            requisicao = requests.get(url, timeout=5)

        except requests.ConnectionError as ex:
            logger.critical(f'Falha de conexão. Verifique URL. {ex}')
            # Envia o trace do erro por email para o admin
            envia_email(prepara_msg(traceback.format_exc()))
            sys.exit(1)

        except Exception as ex:
            logger.critical(f'{repr(ex)}')
            # Envia o trace do erro por email para o admin
            envia_email(prepara_msg(traceback.format_exc()))
            sys.exit(1)

        else:
            # Prepara o texto do resultado
            # envia por email, se falha
            # grava no log, se sucesso
            if requisicao.status_code != 200:
                sem_resposta = True

                mensagem = mensagem + '{}:{}:{}\n'.format(
                    url, requisicao.status_code, requests.status_codes._codes[requisicao.status_code][0].upper())

                logger.error(
                    '{}:{}:{}'.format(
                        url, requisicao.status_code, requests.status_codes._codes[requisicao.status_code][0].upper()))

                time.sleep(TEMPO_SLEEP)
            else:
                sem_resposta = False

                mensagem = '{}:{}:{}'.format(
                    url, requisicao.status_code, requests.status_codes._codes[requisicao.status_code][0].upper())

                break

    return sem_resposta, mensagem


def prepara_msg(corpo_email):

    try:
        # Tenta carregar o endereço de email do destinatario
        with open(app_config_file) as json_cfg_file:
            app_config = json.load(json_cfg_file)

    except Exception as ex:
        # Grava erro no log e aborta o programa
        logger.critical(f'{repr(ex)}')
        sys.exit(1)

    else:
        # Carrega valor das variaveis a partir do arquivo de configuração json
        email_recipients = app_config['destinatarios'][0]['email']

        # Cria objeto
        msg = EmailMessage()

        # Prepara o cabeçalho da mensagem
        msg['Subject'] = f'Algo falhou'
        msg['From'] = 'Monitoramento URL'
        msg['To'] = email_recipients

        # Inclui texto no corpo do email
        msg.set_content(corpo_email)

        return msg


def main(app_config_file):

    try:
        # Tenta carregar configurações de URL para monitorar
        with open(app_config_file) as json_cfg_file:
            app_config = json.load(json_cfg_file)

    except Exception as ex:
        # Grava erro no log e aborta o programa
        logger.critical(f'{repr(ex)}')
        sys.exit(1)

    else:
        # Carrega valor das variaveis a partir do arquivo de configuração json
        url_monitorada = app_config['sites'][0]['url']
        tentativas = app_config['sites'][0]['tentativas']

        # Chama função que verifica se URL está respondendo ou não
        # Armazena o resultado da verificação em <url_monitorada_fora>
        # Armazena o texto com detalhes sobre o resultado em <mensagem>
        url_monitorada_fora, mensagem = verifica_status_url(
            url_monitorada, tentativas)

        if url_monitorada_fora:
            envia_email(prepara_msg(mensagem))
        else:
            logger.info(mensagem)


if __name__ == "__main__":
    # Marca o início da execução do programa
    tempo_inicio_execucao = time.perf_counter()

    # Nome dos arquivos de configuração
    logger_config_file = 'log_cfg.json'
    app_config_file = 'app_cfg.json'

    # Verifica se os arquivos de configuração estão no mesmo dir do sript
    if os.path.isfile(logger_config_file) & os.path.isfile(app_config_file):
        # Configura o Logger
        logger = configura_logger(logger_config_file)
        # Chama a função principal
        # Passa o nome do arquivo de configuração do programa
        main(app_config_file)

    else:
        # TODO: Executar o programa sem logar, se não encontrar o arquivo de configuração
        # Notifica o usuário que não foi possível configurar o Logger
        # Aborta o programa
        print(
            '[!] Arquivo de configuração não encontrado. Abortando execução.')

    # Marca o fim da execucação do programa
    tempo_fim_execucao = time.perf_counter()

    # Registra em log o tempo total de execucação
    logger.info(
        f'[i] Programa rodou em {(tempo_fim_execucao - tempo_inicio_execucao):.2f} segundos')
