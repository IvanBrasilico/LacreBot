# -*- coding: utf-8 -*-
'''Views customizadas utilizadas neste projeto
São as funcões que geram o conteúdo para a submissão à
API que o Usuário acessa.
'''
import json
import urllib.request
import asyncio
import aiohttp
from aiohttp import web


ULRAPP = 'http://brasilico.pythonanywhere.com/_lacre/'
STATUS = ['OK', 'Divergente', 'Sem Lacre']
'''
def http_async_access(url):
    ''Default function for assincronous http access''
    async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as client:
        async with client.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 404:
                raise web.HTTPNotFound()
            else:
                raise aiohttp.HttpProcessingError(
                    code=resp.status, message=resp.reason,
                    headers=resp.headers)

'''
def two_tokens(text):
    '''Receives a text string, splits on first space, return
    first word of list/original sentence and the rest of the sentence
    '''
    lista = text.split(' ')
    return lista[0], " ".join(lista[1:])

def consulta_conteiner(message):
    return consulta_api(message, 'container')

def consulta_lacre(message):
    return consulta_api(message, 'lacre')

def consulta_api(message, resource):
    '''Acessa a API da Aplicação LACRE em pythonanywhere'''
    try:
        _, conteiner = two_tokens(message.text)
        if conteiner == "":
            # TODO See best way to stay on a conversation
            # Now it is responsability of the caller Pattern to initiate hook
            # The hook will remain until the view return False as second parameter
            # or no value (use try: Except ValueError to assume a False default)
            # Maybe needs some change in core architeture to allow more control
            # and more explicit behavior
            return 'Informe o número do Contêiner', True
        response_text = urllib.request.urlopen(
            ULRAPP + resource + '/' +
            conteiner).read()
        resposta = response_text.decode('utf-8')
        json_resposta = json.loads(resposta)
        str_resposta = ""
        for key, value in json_resposta[0].items():
            str_resposta = str_resposta + key + ': ' + value + ' \n '
    except Exception as err:
        print(err)
    return str_resposta, False


class HookView():

    def __init__(self, view):
        self.view = view
        self.hook = False
 
    def exec_view(self, message):
        try:
            response, hook = self.view(message)
        except ValueError:
            hook = False
        return response, hook
        

def report_api(message):
    '''Acessa a API da Aplicação LACRE em pythonanywhere'''
    try:
        _, conteiner = two_tokens(message.text)
        conteiner, status = two_tokens(conteiner)
        lstatus = STATUS[int(status)]
        response_text = urllib.request.urlopen(
            ULRAPP + 'add/report?' +
            'container=' + conteiner +
            'status=' + lstatus).read()
        resposta = response_text.decode('utf-8')
        json_resposta = json.loads(resposta)
        str_resposta = ""
        if len(json_resposta) > 0:
            for key, value in json_resposta[0].items():
                str_resposta = str_resposta + key + ': ' + value + ' \n '
        else:
            str_resposta = conteiner + "Adicionado ao relatório."
    except Exception as err:
        print(err)
    return str_resposta


def list_log(message):
    '''Acessa a API da Aplicação LACRE em pythonanywhere'''
    try:
        print('log')
        response_text = urllib.request.urlopen(
            ULRAPP + 'list/log').read()
        resposta = response_text.decode('utf-8')
        json_resposta = json.loads(resposta)
        print(json_resposta)
        str_resposta = ""
        for line in json_resposta:
            for key, value in line.items():
                str_resposta = str_resposta + key + ': ' + value + ' \n '
    except Exception as err:
        print(err)
    return str_resposta


def help_text(message):
    '''Retorna a lista de Patterns/ disponíveis'''
    # TODO Fazer modo automatizado
    lstatus = [str(key) + ': ' + value + ' ' for key, value in list(enumerate(STATUS))]
    return  ('cc <Nº contêiner> \n'
             'll <nº lacre> \n'
             'report <nº conteiner> <status> (status = ' + " ".join(lstatus) + ')')


def say_help(message):
    '''Se comando não reconhecido'''
    return 'Não entendi o pedido. \n Digite help para uma lista de comandos.'


def works(message):
    '''Mensagem simples para teste automático se
    a aplicação está no ar'''
    return 'works'
