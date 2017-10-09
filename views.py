# -*- coding: utf-8 -*-
'''Views customizadas utilizadas neste projeto
São as funcões que geram o conteúdo para a submissão à
API que o Usuário acessa.
'''
import json
import urllib.request


def two_tokens(text):
    '''Receives a text string, splits on first space, return
    first word of list/original sentence and the rest of the sentence
    '''
    lista = text.split(' ')
    return lista[0], " ".join(lista[1:])


def consulta_conteiner(message):
    '''Acessa a API da Aplicação LACRE em pythonanywhere'''
    try:
        _, conteiner = two_tokens(message.text)
        response_text = urllib.request.urlopen(
            "http://brasilico.pythonanywhere.com/_lacre/container/" +
            conteiner).read()
        resposta = response_text.decode("utf-8")
        json_resposta = json.loads(resposta)
        str_resposta = ""
        for key, value in json_resposta[0].items():
            str_resposta = str_resposta + key + ': ' + value + ' - '
    except Exception as err:
        print(err)
    return str_resposta


def help_text(message):
    '''Retorna a lista de Patterns/ disponíveis'''
    # TODO Fazer modo automatizado
    return 'cc <Nº contêiner>'


def say_help(message):
    '''Se comando não reconhecido'''
    return 'Digite help'


def works(message):
    '''Mensagem simples para teste automático se
    a aplicação está no ar'''
    return 'works'
