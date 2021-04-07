<h1 align="center">
  URL Monitor
</h1>
Script para verificar a resposta de uma requisição a uma URL. Caso a resposta seja diferente de OK (<i>http code 200</i>), um alerta será enviado por email para o admin cadastrado.

<p align="center"><br>
  <a href="#requisitos">Requisitos</a> •
  <a href="#usando-o-url-monitor">Usando o URL Monitor</a> •
  <a href="#contribuições">Contribuições</a> •
  <a href="#contato">Contato</a> •
  <a href="#licença">Licença</a>
</p>

---
## Requisitos

O script precisa do **Python versão 3.7** ou superior instalado, e também dos seguintes módulos:
- json
- logging
- smtplib
- email
- decouple
- traceback
- requests

Caso algum desses módulos não esteja instalado, você pode instalá-los utilizando a seguinte linha de comando:
```
pip install <nome_do_modulo>
```

## Usando o URL Monitor

Antes de utilizar o URL Monitor, configure os seguintes parâmetros:
1. Editar o arquivo **app_cfg.json** e alterar as seguintes chaves com a URL do site a monitorar, bem como o número de tentativas consecutivas antes de enviar o e-mail reportando a falha:
    "sites": [{
            "url": "https://www.site.com.br",
            "tentativas": 5
        }]
2. No mesmo arquivo, alterar o email do admin que receberá a notificação da falha:
    "destinatarios": [{
            "email": "email@email.com"
        }]
3. Salvar e fechar o arquivo
4. Editar o arquivo **log_cfg.json**. Alterar o o tamanho máximo (em bytes), a quantidade de arquivos de log a manter antes de iniciar a rotação e o nome para o arquivo de log:
"file": {
            "maxBytes": 10240,
            "backupCount": 5,
			"filename": "<nome_do_arquivo_de_log.log>",
        }

Ao ser criado um novo arquivo de log, após atingir o tamanho máximo definido, será acrescido suffixo com a sequencia até o número definido em **backupCount**, ex.: logfile.log.1, logfile.log.2...logfile.log.5

O arquivo de log será criado no mesmo diretório do arquivo json. Para mudar de local, deve incluir o caminho completo no campo **filename**.

5. Para utilizar o URL Monitor, execute:
```
python site_monitor.py
```
Se o executável do python não estiver no *path*, considere incluir o caminho da instalação do python no comando, assim:
```
"c:\program files\python37\python.exe" site_monitor.py
```

> O script não possui rotina de autoexecução programada, então é necessário incluir a linha de comando na rotina de algum agendadador de tarefas do seu sistema, como o **crontab** (no Linux) ou **Task Scheduler** (no Windows 10), e definir o intervalo de execução como preferir.

## Contribuições

Para contribuir com o projeto URL Monitor, siga os seguintes passos:

1. Faça um *Fork* do repositório
2. Crie uma *branch*: `git checkout -b <branch_name>`
3. Faça suas mudanças e depois realize um *commit*: `git commit -m '<commit_message>'`
4. Faça um *push* para a branch original: `git push origin <site-monitor>/<master>`
5. Submeta um *pull request* contendo os detalhes da mudança, incluindo o resultado/benefício esperado.

## Contato
[Denis Anderson](mailto:denisranderson@gmail.com)

## Licença
<!--- If you're not sure which open license to use see https://choosealicense.com/--->

[![MIT License](https://img.shields.io/github/license/denisanderson/site-monitor)](https://tldrlegal.com/license/mit-license)

Copyright © [DenisAnderson](https://github.com/denisanderson)


[[Voltar ao Topo]](#--url-monitor)
