#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 09:18:39 2017

@author: ivan
"""
from bottery.message import Message
from patterns import FuncPattern
from views import two_tokens, consulta_conteiner


ptest = FuncPattern('cc', consulta_conteiner, two_tokens)

print(two_tokens("duas palavras"))
print(two_tokens("tres simples palavras"))
