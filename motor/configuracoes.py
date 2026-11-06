# Minha Engine - configuracoes.py
# imports, tamanhos da tela, pastas, cores e fontes
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

import copy
import importlib.util
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys

import pygame

# =====================================================================
# CONFIGURACOES
# =====================================================================
LARGURA, ALTURA = 1280, 720
PAINEL_ESQ = 200
PAINEL_DIR = 270
TOPO = 46
ABAS_H = 30
RODAPE = 26
VIEW = pygame.Rect(PAINEL_ESQ, TOPO + ABAS_H, LARGURA - PAINEL_ESQ - PAINEL_DIR,
                   ALTURA - TOPO - ABAS_H - RODAPE)
TELA_INTEIRA = pygame.Rect(0, 0, LARGURA, ALTURA)
GRADE = 20
if getattr(sys, "frozen", False):          # jogo exportado como .exe
    PASTA = os.path.dirname(sys.executable)
else:
    PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA, "projeto.json")
PASTA_IMAGENS = os.path.join(PASTA, "imagens")
PASTA_PLUGINS = os.path.join(PASTA, "plugins")
PASTA_SONS = os.path.join(PASTA, "sons")
ARQUIVO_AUTOSAVE = os.path.join(PASTA, "projeto_autosave.json")
ARQUIVO_SAVEGAME = os.path.join(PASTA, "savegame.json")
PASTA_PROJETOS = os.path.join(PASTA, "projetos")
ARQUIVO_CONFIG = os.path.join(PASTA, "config.json")
VERSAO = "19"
EXT_SONS = (".wav", ".ogg", ".mp3")
EXT_IMAGENS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")

C_FUNDO_UI = (32, 34, 40)
C_PAINEL = (42, 45, 53)
C_BORDA = (65, 68, 80)
C_TEXTO = (225, 225, 230)
C_TEXTO2 = (150, 152, 165)
C_DESTAQUE = (70, 140, 255)
C_BOTAO = (58, 62, 74)
C_VERDE = (60, 170, 95)
C_VERMELHO = (205, 70, 70)
C_CAMPO = (28, 30, 36)
C_QUANDO = (140, 80, 200)
C_SE = (200, 130, 40)
C_FACA = (50, 120, 210)
C_FUNCAO = (30, 150, 140)
C_MODELO = (200, 120, 40)

# Fontes (familias que o pygame procura no computador, em ordem)
FONTES_UI = {"Segoe UI": "segoeui,arial,dejavusans,liberationsans", "Arial": "arial,liberationsans,dejavusans",
             "Verdana": "verdana,dejavusans", "Tahoma": "tahoma,arial,dejavusans", "Calibri": "calibri,arial,dejavusans",
             "Trebuchet": "trebuchetms,arial,dejavusans"}
FONTES_CODIGO = {"Consolas": "consolas,dejavusansmono,liberationmono,couriernew,monospace",
                 "Cascadia Code": "cascadiacode,cascadiamono,consolas,dejavusansmono,monospace",
                 "Courier New": "couriernew,liberationmono,dejavusansmono,monospace",
                 "Lucida Console": "lucidaconsole,consolas,dejavusansmono,monospace"}
FONTES_JOGO = {"Arial": "arial,liberationsans,dejavusans", "Segoe UI": "segoeui,arial,dejavusans",
               "Verdana": "verdana,dejavusans", "Times New Roman": "timesnewroman,liberationserif,dejavuserif",
               "Georgia": "georgia,dejavuserif", "Courier New": "couriernew,liberationmono,dejavusansmono",
               "Comic Sans": "comicsansms,comicsans,arial", "Impact": "impact,arialblack,arial",
               "Trebuchet": "trebuchetms,arial", "Consolas": "consolas,dejavusansmono"}
