"""
=====================================================================
  MINHA ENGINE - Editor de jogos 2D com linguagem propria (Brasa)
=====================================================================
Como rodar:
    1) pip install pygame
    2) python minha_engine.py
    No CELULAR (Android): app Pydroid 3 > Pip > pygame, copie a pasta e rode este arquivo
    (veja o LEIA-ME.txt). Toque = clique, segurar = botao direito, 2 dedos = mover/zoom,
    controles na tela durante o jogo.

TELA INICIO (abre primeiro, estilo Godot / Roblox Studio):
    Minhas criacoes - todos os seus projetos com miniatura: Editar, Jogar, Renomear,
                      Duplicar, Abrir pasta, Apagar (vai para a pasta lixeira)
    Novo projeto    - vazio ou a partir de um exemplo pronto
    Configuracoes   - atalhos, controles do jogo, EDITOR DE SCRIPT (fonte, tamanho e as
                      cores: funcoes em verde, palavras, textos, numeros...), APARENCIA
                      (fonte da interface, cor de destaque, resolucao, letras nitidas),
                      volume, salvamento automatico, grade, tela cheia, dicas...
    Cada projeto fica em projetos/<nome>/ com as suas imagens/ e sons/.
    No editor, o botao "Inicio" (Ctrl+I) volta para esta tela.

ABAS no meio da tela:
    CENA     - monta a fase (colocar, mover, redimensionar objetos)
    EVENTOS  - programacao VISUAL: QUANDO (evento) + SE (condicoes) + FACA (acoes)
    SCRIPT   - programacao em texto na linguagem BRASA
    API      - documentacao de TUDO da engine, com busca e botao "Usar"
    DESENHO  - editor de PIXEL ART e de ANIMACAO: lapis, borracha, balde, conta-gotas,
               linha, retangulo, circulo, espelho, paleta, quadros com "ver quadro anterior",
               previa animada. "Salvar e usar no objeto" coloca o desenho/animacao na peca.
    MODO     - botao "Modo: Plataforma / Top-down": visao de cima com 8 direcoes, espada (Espaco/J),
               animacao por direcao, sombras e quem esta mais embaixo aparece na frente.
    LOJA     - Creator Store: mais de 880 itens (28 personagens em plataforma/top-down/NPC, cenario
               top-down, inimigos de 10 elementos, chefoes, torres, plataformas, pocoes, pets,
               fases prontas, upgrades do Player, efeitos,
               interface "Voce prefere" com botoes, pixel arts e scripts). Clique em Inserir.

COMO CRIAR (estilo Roblox): coloque uma PECA (categoria Basico), escolha forma, cor e
    MATERIAL (Plastico, Madeira, Pedra, Metal, Gelo escorrega, Areia deixa lento,
    Borracha quica, Neon brilha, Vidro...) e no painel direito > APARENCIA escolha:
    Cor, Imagem, Desenhar (pixel art) ou Animar.
AMIGAVEL: guia "Primeiros passos" (marca sozinho o que voce ja fez), baloes de aviso
    coloridos (verde = deu certo, amarelo = atencao, vermelho = erro), fase vazia com
    botoes para comecar, botao Ajuda com menu e dica do dia na tela Inicio.
ONLINE (mundo todo): Inicio > clique no seu nome > Criar conta / Entrar (e-mail e senha).
    Com a conta online, os jogos publicados, likes, visitas, a carteira e os itens a venda na Loja
    ficam no servidor (Supabase) e aparecem para todo mundo. O codigo do servidor esta em
    servidor_supabase.sql (cole no SQL Editor do Supabase).
USUARIOS: cada pessoa deste computador tem a sua conta (Inicio > clique no seu nome > Novo usuario),
    com as suas Brasas, plano, compras e jogos. Senha (PIN) opcional.
BRASAS E PLANOS (moeda virtual, NAO e dinheiro de verdade):
    Ganhe: 150 de boas-vindas, recompensa SEMANAL (Gratis 10, Game Maker 35, Dev 75),
    +25 por VISITA e +50 por LIKE nos seus jogos publicados (1 vez por usuario), conquistas e vendas.
    Planos por mes: GAME MAKER 300 e DEV 800 Brasas (vender: Gratis 1 item, GM 10, Dev sem limite).
JOGOS PUBLICADOS: Inicio > Jogos publicados. Publique pelo ··· do projeto ou no editor
    (Exportar > Publicar). Todo mundo deste computador pode jogar e curtir.
VENDER NA LOJA: Loja > Vender. O item vira um arquivo .mepack (pasta loja_comunidade).
    Quem compra recebe um RECIBO (ME-XXXX...) e manda para voce resgatar em Loja > Resgatar venda.
SAIDA (F9): mostra erros, avisos e mensagens. Clique num erro para ir ate a linha.
STUDS: botao "Mover" escolhe de quantos em quantos pixels os objetos andam/encaixam;
       botao "Girar" escolhe o passo do giro (R / Shift+R).

PAINEL ESQUERDO:
    Objetos  - Mundo (Bloco, Player, Caixa, Portal...) e Interface/UI
               (Texto, Botao, Barra, Painel, Imagem)
    Modelos  - suas VARIANTES: objetos prontos para reutilizar
    Imagens  - todas as imagens do projeto: clique e depois na cena para criar uma Peca
               com ela, ou "Por na selecao" para trocar a imagem do objeto
    Lista    - tudo que tem na cena (Explorer)

FASES: botao "Fase: ..." em cima da cena (criar, renomear, duplicar, apagar).
       Moedas, itens e variaveis globais continuam de uma fase para outra.

PASTAS:
    projetos/<nome>/imagens/  - PNG/JPG para a propriedade "Imagem" ou "Animacao" (a1.png, a2.png)
    projetos/<nome>/sons/     - WAV/OGG/MP3 para "Tocar som" e a musica da fase
    plugins/                  - arquivos .py que criam funcoes novas para a linguagem (todos os projetos)
    config.json               - suas configuracoes e atalhos

ATALHOS (F1 mostra todos dentro do editor):
    F5 play | F10 play em tela cheia | F11 tela cheia | Ctrl+S salvar
    Ctrl+Z desfazer | Ctrl+Y refazer | Ctrl+C/X/V copiar/recortar/colar
    Ctrl+A selecionar tudo | Shift+clique selecao multipla | arrastar no vazio = caixa
    Ctrl+D duplicar | Delete apagar | Rodinha = zoom | F focar | L travar | H esconder
    Botao direito = menu com tudo | Tipo + arrastar = pincel

EXPORTAR: botao "Exportar" cria a pasta exportado/<titulo> com o jogo pronto
          (JOGAR.bat e instrucoes para virar .exe no LEIA-ME.txt) e atalhos na area de trabalho

SELETOR: + Evento / + Condição / + Ação / + Comportamento abrem uma janela com CATEGORIAS,
    BUSCA (digite: vida, pulo, tiro...), descrição de cada um e rolagem (rodinha ou barra).
COMPORTAMENTOS (painel direito > + Comportamento), sem programar:
    Bala, Senoide, Girar sempre, Perseguir, Vida, Gerador, Arrastavel, Plataforma atravessavel,
    Destruir fora da tela, Preso no mapa, Sumir aos poucos, 8 direcoes
    Luz, Emissor de particulas (fogo, fumaca, brilho, chuva, neve)
GRUPOS: escreva um grupo no objeto (ex: Inimigos). Onde pede nome ou tipo, o grupo tambem vale.
EXEMPLOS PRONTOS: botao Novo > plataforma (2 fases), aventura vista de cima, caverna escura
DIALOGOS: na fala do NPC separe as frases com | (ex: Oi!|Cuidado com a lava.)
ESCURIDAO: propriedade da Cena (0 a 255) + comportamento Luz nos objetos
NO JOGO: F2 = modo debug (FPS e caixas de colisao) | controle (gamepad) funciona sozinho

ARQUIVOS (a engine e dividida em partes, na pasta motor/):
    minha_engine.py      - ESTE arquivo: e ele que voce roda. Ele junta as partes.
    motor/*.py           - as partes da engine (a lista e a ordem estao em PARTES, abaixo).
    Todas as partes enxergam tudo umas das outras (funcionam como um arquivo so),
    entao da para mexer numa parte sem se preocupar com "import".
    Ao exportar um jogo, as partes sao juntadas num arquivo unico motor.py.

Rodar so o jogo (sem editor), depois de salvar:
    python minha_engine.py --jogar projeto.json
"""

import os
import sys

PASTA_MOTOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "motor")

# A ordem importa: cada parte usa coisas das partes de cima.
PARTES_DA_ENGINE = [
    "configuracoes.py",
    "objetos.py",
    "api_docs.py",
    "linguagem_brasa.py",
    "auxiliares.py",
    "projetos.py",
    "midia.py",
    "desenho_objetos.py",
    "interface.py",
    "sistemas.py",
    "celular.py",
    "carteira.py",
    "publicados.py",
    "online.py",
    "jogo_objetos.py",
    "jogo_funcoes.py",
    "jogo_scripts.py",
    "jogo_tela.py",
    "logica_extra.py",
    "topdown.py",
    "jogo.py",
    "editor_dados.py",
    "editor_pixel.py",
    "loja.py",
    "loja_catalogo.py",
    "loja_personagens.py",
    "editor_base.py",
    "editor_objetos.py",
    "editor_eventos.py",
    "editor_script.py",
    "editor_entrada.py",
    "editor_tela.py",
    "editor_seletor.py",
    "editor.py",
    "inicio.py",
    "principal.py",
]


def codigo_unico():
    """Junta todas as partes num texto so (usado para exportar o jogo como motor.py)."""
    pedacos = ["# Minha Engine - motor unico (gerado automaticamente ao exportar)\n"]
    for nome in PARTES_DA_ENGINE:
        with open(os.path.join(PASTA_MOTOR, nome), encoding="utf-8") as f:
            pedacos.append(f"\n# {'=' * 69}\n# ARQUIVO motor/{nome}\n# {'=' * 69}\n" + f.read())
    return "\n".join(pedacos)


def _carregar_partes():
    if not os.path.isdir(PASTA_MOTOR):
        print("Não achei a pasta 'motor' ao lado do minha_engine.py.")
        print("Ela precisa ficar junto: minha_engine.py + motor/ (com os arquivos .py dentro).")
        sys.exit(1)
    for nome in PARTES_DA_ENGINE:
        caminho = os.path.join(PASTA_MOTOR, nome)
        if not os.path.isfile(caminho):
            print(f"Está faltando o arquivo motor/{nome}. Baixe a engine de novo.")
            sys.exit(1)
        with open(caminho, encoding="utf-8") as f:
            exec(compile(f.read(), caminho, "exec"), globals())


_carregar_partes()
