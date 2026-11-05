# Minha Engine - editor_dados.py
# cores do código, dicas dos botões, lista de atalhos e a API
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# EDITOR
# =====================================================================
RE_COR = re.compile(r"""(\#.*|//.*)|("(?:[^"\\]|\\.)*"?|'(?:[^'\\]|\\.)*'?)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_À-ÿ][\wÀ-ÿ]*)|(\s+)|(.)""")
RE_PALAVRA = re.compile(r"[A-Za-z_À-ÿ][\wÀ-ÿ]*")
NOMES_PRONTOS = {"escrever", "dizer", "destruir", "destruir_todos", "criar", "achar", "achar_todos", "tecla",
                 "apertou", "soltou", "mouse_x", "mouse_y", "mouse_segurado", "aleatorio", "distancia",
                 "vencer", "perder", "reiniciar", "voltar_inicio", "controles", "tela_cheia", "moedas",
                 "somar_moedas", "dar_item", "remover_item", "tem_item", "inventario",
                 "depois", "lancar", "hud", "apagar_hud", "tremer", "camera", "fundo", "gravidade", "texto",
                 "numero", "abs", "min", "max", "arredondar", "raiz", "tamanho", "adicionar", "chamar",
                 "ir_fase", "proxima_fase", "fase_atual", "tocar_som", "tocar_musica", "parar_musica",
                 "particulas", "animar", "piscar", "pausar", "salvar_jogo", "carregar_jogo",
                 "dano", "curar", "congelar", "flash", "esticar", "zoom", "linha_de_visao", "comportamento",
                 "no_grupo", "fps", "dialogo", "dialogo_aberto", "texto_flutuante", "escuridao",
                 "maiusculo", "minusculo", "contem", "dividir", "juntar", "substituir", "remover", "sortear",
                 "embaralhar", "inverter", "ordenar", "posicao", "lista_de", "piso", "teto", "seno", "cosseno",
                 "angulo_ate", "mirar",
                 "eu", "outro", "player", "global", "tempo", "dt"}
PROPS_OBJ = ["x", "y", "vx", "vy", "w", "h", "cor", "imagem", "animacao", "texto", "opacidade", "rotacao",
             "espelhar", "camada", "visivel", "solido", "gravidade", "no_chao", "nome", "tipo", "vivo",
             "grupo", "vida", "vida_max"]

ATALHOS = [
    ("GERAL", ""),
    ("F5", "Play (testar)"), ("F10", "Play em tela cheia"), ("F11", "Tela cheia"),
    ("Ctrl+S", "Salvar"), ("Ctrl+O", "Abrir"), ("Ctrl+Z", "Desfazer"), ("Ctrl+Y", "Refazer"),
    ("F1", "Mostrar/esconder esta ajuda"),
    ("CENA", ""),
    ("Clique", "Seleciona"), ("Shift+Clique", "Adiciona/tira da seleção"),
    ("Arrastar no vazio", "Caixa de seleção"), ("Ctrl+A", "Selecionar tudo"),
    ("Ctrl+C / X / V", "Copiar / Recortar / Colar (no mouse)"), ("Ctrl+D", "Duplicar"),
    ("Delete", "Apagar"), ("Setas", "Mover (Shift = 1 pixel)"),
    ("Botão direito", "Menu com mais opções"), ("Botão direito arrastando", "Mover a câmera"),
    ("Rodinha", "Zoom"), ("Ctrl+0", "Zoom 100%"), ("F", "Focar na seleção"),
    ("L / H", "Travar / Esconder no editor"), ("G", "Liga/desliga snap na grade"),
    ("E", "Borracha (apaga clicando/arrastando)"), ("M", "Mostrar/esconder o mini-mapa (clique nele para ir)"),
    ("Tipo + arrastar", "Pinta vários objetos (pincel)"), ("Esc", "Volta pro modo Selecionar"),
    ("SCRIPT", ""),
    ("Ctrl+C / X / V / A", "Copiar / Recortar / Colar / Tudo"), ("Shift+setas", "Selecionar texto"),
    ("Ctrl+D", "Duplicar linha"), ("Ctrl+/", "Comentar linhas"), ("Ctrl+F / F3", "Buscar / próximo"),
    ("Tab", "Aceita sugestão / indenta"), ("Shift+Tab", "Tira indentação"),
    ("NO JOGO", ""),
    ("A/D ou setas", "Andar"), ("Espaço / W", "Pular (segurar = pulo mais alto)"), ("E", "Falar com NPC"),
    ("P", "Pausar"), ("R", "Recomeçar depois de vencer/perder"), ("F2", "Modo debug (FPS e caixas)"),
    ("Controle (gamepad)", "Analógico anda, A pula, B fala, Start pausa"),
]

def lista_atalhos():
    """Lista para a tela de ajuda, montada com os atalhos configurados."""
    a = lambda acao: " / ".join(texto_atalho(c) for c in CONFIG["atalhos"].get(acao, [])[:2]) or "-"
    j = lambda acao: " / ".join(texto_atalho(c) for c in CONFIG["controles"].get(acao, [])[:2]) or "-"
    linhas = [("GERAL", "")]
    for acao in ("play", "play_cheio", "tela_cheia", "salvar", "inicio", "desfazer", "refazer", "ajuda"):
        linhas.append((a(acao), NOMES_ATALHOS[acao]))
    linhas.append(("CENA", ""))
    linhas += [("Clique / Shift+Clique", "Seleciona / adiciona na seleção"), ("Arrastar no vazio", "Caixa de seleção"),
               ("Botão direito", "Menu com mais opções"), ("Botão dir. arrastando", "Mover a câmera"),
               ("Rodinha", "Zoom"), ("Setas (Shift = 1px)", "Mover seleção")]
    for acao in ("copiar", "recortar", "colar", "duplicar", "selecionar_tudo", "apagar", "focar", "travar",
                 "esconder", "borracha", "minimapa", "snap", "zoom_100"):
        linhas.append((a(acao), NOMES_ATALHOS[acao]))
    linhas += [("SCRIPT", ""), ("Ctrl+C / X / V / A", "Copiar / Recortar / Colar / Tudo"),
               ("Ctrl+/  ·  Ctrl+F", "Comentar  ·  Buscar"), ("Tab / Shift+Tab", "Sugestão / indentação"),
               ("NO JOGO", "")]
    for acao in ("esquerda", "direita", "pular", "acao", "pausa", "debug"):
        linhas.append((j(acao), NOMES_CONTROLES[acao]))
    linhas.append(("Controle (gamepad)", "Analógico anda, A pula, B fala, Start pausa"))
    return linhas


DICAS_BOTOES = {
    "play": "Testa o jogo aqui dentro do editor (F5)",
    "playcheio": "Testa o jogo ocupando a tela toda (F10)",
    "novo": "Projeto novo vazio ou um exemplo pronto (plataforma, aventura, caverna)",
    "salvar": "Salva o projeto (Ctrl+S). O anterior vira projeto.bak.json",
    "abrir": "Abre o projeto.json salvo (Ctrl+O)",
    "desfazer": "Desfaz a última mudança (Ctrl+Z)",
    "refazer": "Refaz o que foi desfeito (Ctrl+Y)",
    "grade": "Mostra ou esconde a grade",
    "buscar": "Buscar qualquer coisa (Ctrl+K): comandos, objetos para colocar, objetos da fase e itens da Loja",
    "ajuda": "Ajuda: tour guiado, atalhos do teclado e primeiros passos",
    "modo": "Troca a fase entre PLATAFORMA (gravidade e pulo) e TOP-DOWN (visão de cima, 8 direções, espada)",
    "mover": "De quantos em quantos studs (pixels) os objetos andam quando você arrasta ou usa as setas",
    "girar": "Quantos graus a seleção gira com R (Shift+R gira ao contrário)",
    "saida": "Janela Saída: erros, avisos e mensagens do escrever() (F9)",
    "snap": "Prender os objetos na grade (G)",
    "telacheia": "Liga/desliga tela cheia (F11)",
    "exportar": "Exportar o jogo, ou criar atalhos com ícone na área de trabalho",
    "inicio": "Volta para a tela Início (suas criações e configurações)",
}


API_CATS = ["Todos", "Linguagem", "Eventos", "Funções", "Propriedades", "Objetos", "Comportamentos", "Gatilhos",
            "Condições", "Ações", "Plugins"]


def construir_api():
    itens = []

    def add(cat, titulo, desc, exemplo="", usavel=False):
        itens.append({"cat": cat, "titulo": titulo, "desc": desc, "exemplo": exemplo, "usavel": usavel})

    add("Linguagem", "var nome = valor", "Cria uma variável.", "var vida = 3", True)
    add("Linguagem", "se / senao se / senao", "Faz algo só se a condição for verdade.",
        "se vida <= 0:\n    dizer(\"Morri!\", 2)\nsenao:\n    dizer(\"Vivo\", 1)", True)
    add("Linguagem", "enquanto condição:", "Repete enquanto for verdade. Use 'parar' para sair.",
        "var i = 0\nenquanto i < 5:\n    i += 1", True)
    add("Linguagem", "repetir N:", "Repete N vezes.", "repetir 3:\n    criar(\"Moeda\", eu.x, eu.y - 40)", True)
    add("Linguagem", "para i de A ate B:", "Conta de A até B.", "para i de 1 ate 5:\n    escrever(i)", True)
    add("Linguagem", "funcao nome(a, b):", "Cria uma função. 'retornar' devolve um valor.",
        "funcao soma(a, b):\n    retornar a + b", True)
    add("Linguagem", "listas [1, 2, 3]", "Listas com [ ], posição com lista[0].",
        "var l = [10, 20]\nescrever(l[0])", True)
    add("Linguagem", "e  ou  nao", "Junta condições.", "se tecla(\"d\") e eu.no_chao:\n    eu.vx = 300", True)
    add("Linguagem", "# comentário", "Linhas com # são ignoradas.", "# isso é um comentário", True)
    exemplos_ev = {"cada": "2", "tecla": '"e"', "soltar": '"e"', "tocar": '"Moeda"', "parar_tocar": '"Bloco"'}
    for ev, precisa in EVENTOS_SCRIPT.items():
        arg = (" " + exemplos_ev.get(ev, '"x"')) if precisa else ""
        add("Eventos", f"quando {ev}{arg}:", DESC_EVENTOS.get(ev, ""),
            f"quando {ev}{arg}:\n    escrever(\"{ev}!\")", True)
    for assinatura, desc, ex in API_FUNCOES:
        add("Funções", assinatura, desc, ex, True)
    for nome, desc in API_PROPS:
        add("Propriedades", nome, desc)
    for nome, spec in COMPORTAMENTOS.items():
        add("Comportamentos", nome, DESC_COMPORTAMENTOS.get(nome, "") +
            ("  Campos: " + ", ".join(c[0] for c in spec) if spec else "") +
            "  Adicione no painel direito > + Comportamento.")
    for tipo, props in MODELOS.items():
        chaves = ", ".join(k for k in props if k not in ("w", "h"))
        add("Objetos", tipo, DESC_TIPOS.get(tipo, "") + "  Propriedades: " + chaves)
    for nome, spec in GATILHOS.items():
        add("Gatilhos", f"QUANDO {nome}", "Evento visual (aba Eventos). " +
            ("Campos: " + ", ".join(s[0] for s in spec) if spec else "Sem campos."))
    for nome, spec in CONDICOES.items():
        add("Condições", f"SE {nome}", "Condição visual. Clique no SE para virar SE NÃO. " +
            ("Campos: " + ", ".join(s[0] for s in spec) if spec else "Sem campos."))
    for nome, spec in ACOES.items():
        add("Ações", f"FAÇA {nome}", "Ação visual. " +
            ("Campos: " + ", ".join(s[0] for s in spec) if spec else "Sem campos."))
    add("Plugins", "Como criar um plugin", "Crie um arquivo .py na pasta 'plugins' com uma função "
        "registrar(api). Use api.funcao(nome, funcao_python, descrição). Reabra o editor e a função "
        "nova funciona na linguagem Brasa. Tem um exemplo pronto: plugins/exemplo_plugin.py")
    for nome, (fn, desc) in sorted(PLUGIN_FUNCOES.items()):
        add("Plugins", f"{nome}(...)", desc or "Função de plugin.", f"escrever({nome}(5))" if desc else "", bool(desc))
    for mat in MATERIAIS:
        add("Propriedades", f"material = \"{mat}\"", "Material da Peça/Bloco/Caixa" +
            (f" ({DESC_MATERIAIS[mat]})." if mat in DESC_MATERIAIS else "."), f'eu.material = "{mat}"', True)
    add("Propriedades", "eu.forma", "Forma da Peça: " + ", ".join(FORMAS) + ".", 'eu.forma = "Círculo"', True)
    add("Propriedades", "eu.animacao / eu.fps_anim", "Quadros da animação (imagens separadas por vírgula) e a "
        "velocidade. Faça os quadros na aba Desenho.", 'eu.animacao = "slime_1.png, slime_2.png"\neu.fps_anim = 6', True)
    add("Propriedades", "eu.fonte / eu.negrito / eu.italico", "Fonte do Texto/Botão: " + ", ".join(FONTES_JOGO) + ".",
        'eu.fonte = "Impact"\neu.negrito = verdadeiro', True)
    return itens
