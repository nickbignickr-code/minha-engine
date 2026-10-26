# Minha Engine - auxiliares.py
# funções auxiliares e config.json (atalhos, controles, aparência)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# FUNCOES AUXILIARES
# =====================================================================
def nova_entidade(tipo, x, y, nome=None, **extra):
    d = {"tipo": tipo, "nome": nome or tipo, "x": int(x), "y": int(y)}
    d.update(copy.deepcopy(MODELOS[tipo]))
    for k, v in COMUNS.items():
        d.setdefault(k, copy.deepcopy(v))
    d.update(extra)
    d.setdefault("valores", {})
    d.setdefault("comportamentos", [])
    d.setdefault("eventos", [])
    d.setdefault("script", "")
    return d


def params_padrao(spec):
    return {nome: str(padrao) for nome, padrao, _ in spec}


def cena_padrao():
    return {"fundo": [25, 28, 45], "imagem_fundo": "", "parallax_fundo": 0.0, "musica": "",
            "gravidade": 1800, "visao_de_cima": False, "limitar_camera": False, "mostrar_moedas": True,
            "zoom_camera": 1.0, "olhar_a_frente": 60, "esticar_ao_pousar": True, "escuridao": 0,
            "titulo": "Meu Jogo", "largura_tela": 960, "altura_tela": 540, "tela_cheia": False,
            "eventos": [], "script": "", "funcoes": []}


def fase_padrao(com_chao=True):
    objs = [nova_entidade("Bloco", 0, 460, "Chao", w=800, h=80)] if com_chao else []
    return {"cena": cena_padrao(), "objetos": objs}


def projeto_padrao():
    evento_exemplo = {
        "gatilho": "Tecla apertada", "gp": {"tecla": "e"},
        "condicoes": [],
        "acoes": [{"t": "Mostrar texto", "p": {"texto": "Oi! Estou em x = {eu.x}", "seg": "2"}}],
    }
    objs = [
        nova_entidade("Bloco", 0, 460, "Chao", w=800, h=80),
        nova_entidade("Bloco", 300, 360, "Plataforma", w=140, h=20),
        nova_entidade("Moeda", 360, 320),
        nova_entidade("Player", 80, 400, eventos=[evento_exemplo], valores={"vida": 100}),
        nova_entidade("Texto", 12, 40, "Placar", texto="Vida: {player.vida}"),
    ]
    return {"fases": {"Fase 1": {"cena": cena_padrao(), "objetos": objs}},
            "fase_atual": "Fase 1", "fase_inicial": "Fase 1", "modelos": {}}


def comp(nome, **params):
    """Atalho para montar um comportamento com alguns campos trocados."""
    p = params_padrao(COMPORTAMENTOS[nome])
    p.update({k: str(v) for k, v in params.items()})
    return {"t": nome, "p": p}


def ui_vida(maximo):
    return [nova_entidade("Texto", 16, 40, "TextoVida", texto="Vida: {player.vida}", w=160),
            nova_entidade("Barra", 16, 72, "BarraVida", valor_de="player.vida", maximo=maximo, w=160, h=14)]


def exemplo_plataforma():
    f1 = [
        nova_entidade("Bloco", 0, 460, "Chao", w=1400, h=80),
        nova_entidade("Bloco", 1500, 460, "Chao2", w=900, h=80),
        nova_entidade("Bloco", 320, 360, "Plataforma1", w=160, h=20),
        nova_entidade("Bloco", 560, 280, "Plataforma2", w=160, h=20),
        nova_entidade("Bloco", 820, 340, "Nuvem", w=160, h=16, cor=[230, 235, 245],
                      comportamentos=[comp("Plataforma atravessável")]),
        nova_entidade("Espinho", 1000, 440, w=120),
        nova_entidade("Checkpoint", 1180, 400),
        nova_entidade("Inimigo", 700, 428, velocidade=90, distancia=200),
        nova_entidade("Inimigo", 1650, 428, "Inimigo2", velocidade=120, distancia=250),
        nova_entidade("NPC", 160, 412, "Guia",
                      fala="Bem-vindo à Minha Engine!|Setas ou A/D andam, Espaço pula (dá pra pular 2 vezes).|"
                           "Pule em cima dos inimigos e pegue as moedas.|A bandeira leva para a Fase 2!"),
        nova_entidade("Bandeira", 2300, 380, ir_para_fase="Fase 2"),
        nova_entidade("Player", 60, 400, pulos_extras=1, comportamentos=[comp("Vida", vida=3)]),
    ] + [nova_entidade("Moeda", 360 + i * 40, 320, comportamentos=[comp("Senoide (vai e volta)", distancia=6)])
         for i in range(3)] + [nova_entidade("Moeda", 600 + i * 40, 240) for i in range(3)] + ui_vida(3)
    chefe = nova_entidade("Inimigo", 1400, 400, "Chefe", w=64, h=64, cor=[170, 40, 60], velocidade=140, distancia=300,
                          comportamentos=[comp("Vida", vida=3, invencivel_seg=0.5)])
    f2 = [
        nova_entidade("Bloco", 0, 460, "Chao", w=500, h=80),
        nova_entidade("Lava", 500, 470, w=500, h=70),
        nova_entidade("Plataforma Movel", 520, 400, vel_x=120, distancia=300),
        nova_entidade("Bloco", 1000, 460, "Chao2", w=1000, h=80),
        nova_entidade("Trampolim", 1150, 440),
        nova_entidade("Bloco", 1100, 200, "Alto", w=200, h=20),
        nova_entidade("Moeda", 1180, 160, valor=5, cor=[120, 230, 255]),
        chefe,
        nova_entidade("Zona", 0, 0, "Chuva", w=40, h=40,
                      comportamentos=[comp("Emissor de partículas", estilo="chuva", por_seg=70)]),
        nova_entidade("Bandeira", 1900, 380),
        nova_entidade("Player", 60, 400, pulos_extras=1, comportamentos=[comp("Vida", vida=3)]),
    ] + ui_vida(3)
    c2 = cena_padrao()
    c2["fundo"] = [40, 44, 70]
    return {"fases": {"Fase 1": {"cena": cena_padrao(), "objetos": f1}, "Fase 2": {"cena": c2, "objetos": f2}},
            "fase_atual": "Fase 1", "fase_inicial": "Fase 1", "modelos": {}}


def exemplo_aventura():
    cena = cena_padrao()
    cena.update({"visao_de_cima": True, "fundo": [40, 70, 50], "olhar_a_frente": 0, "titulo": "Aventura"})
    paredes = [(0, 0, 1200, 30), (0, 770, 1200, 30), (0, 0, 30, 800), (1170, 0, 30, 800),
               (400, 200, 30, 400), (750, 30, 30, 350), (750, 500, 30, 270)]
    objs = [nova_entidade("Bloco", x, y, f"Parede{i + 1}", w=w, h=h, cor=[90, 90, 110], material="Pedra")
            for i, (x, y, w, h) in enumerate(paredes)]
    for i, (x, y) in enumerate([(550, 300), (950, 200), (950, 600)]):
        objs.append(nova_entidade("Inimigo", x, y, f"Slime{i + 1}", gravidade=False, velocidade=0, distancia=0,
                                  cor=[120, 200, 90], grupo="Inimigos",
                                  comportamentos=[comp("Perseguir", alcance=260, velocidade=90),
                                                  comp("Vida", vida=2, dano_de="Tiros", invencivel_seg=0.2)]))
    objs += [
        nova_entidade("Item", 1050, 380, "Chave", item="chave"),
        nova_entidade("NPC", 150, 120, "Velho", gravidade=False,
                      fala="Os slimes roubaram a chave!|Atire com Espaço (ou botão A do controle).|"
                           "Pegue a chave e encoste no portal."),
        nova_entidade("Portal", 120, 650, "Saida",
                      eventos=[{"gatilho": "Ao tocar em", "gp": {"alvo": "Player"}, "nome": "Sair com a chave",
                                "condicoes": [{"t": "Tem item", "p": {"item": "chave"}}],
                                "acoes": [{"t": "Vencer o jogo", "p": {}}]}]),
        nova_entidade("Player", 120, 380, velocidade=230, gravidade=False, comportamentos=[comp("Vida", vida=5)],
                      script="""# Atira na direcao em que o heroi esta olhando
var dir_x = 1
var dir_y = 0

quando frame:
    se tecla("d") ou tecla("direita"):
        dir_x = 1
        dir_y = 0
    se tecla("a") ou tecla("esquerda"):
        dir_x = -1
        dir_y = 0
    se tecla("w") ou tecla("cima"):
        dir_x = 0
        dir_y = -1
    se tecla("s") ou tecla("baixo"):
        dir_x = 0
        dir_y = 1

quando tecla "espaco":
    lancar("Tiro", 500 * dir_x, 500 * dir_y)
"""),
    ] + ui_vida(5)
    tiro = nova_entidade("Decoracao", 0, 0, "Tiro", w=12, h=12, cor=[255, 230, 90], grupo="Tiros",
                         comportamentos=[comp("Bala", velocidade=500), comp("Destruir fora da tela")])
    return {"fases": {"Fase 1": {"cena": cena, "objetos": objs}}, "fase_atual": "Fase 1", "fase_inicial": "Fase 1",
            "modelos": {"Tiro": tiro}}


def exemplo_caverna():
    cena = cena_padrao()
    cena.update({"escuridao": 235, "fundo": [30, 26, 34], "titulo": "Caverna Escura", "limitar_camera": True})
    objs = [nova_entidade("Bloco", 0, 460, "Chao", w=2200, h=80, cor=[80, 70, 75], material="Pedra"),
            nova_entidade("Bloco", 0, 0, "Teto", w=2200, h=40, cor=[80, 70, 75], material="Pedra")]
    for i in range(6):
        x = 250 + i * 330
        objs.append(nova_entidade("Bloco", x, 360 - (i % 2) * 90, f"Pedra{i + 1}", w=140, h=20, cor=[100, 90, 95],
                                  material="Pedra"))
        objs.append(nova_entidade("Decoracao", x + 60, 420, f"Tocha{i + 1}", w=16, h=40, cor=[120, 80, 50],
                                  comportamentos=[comp("Luz", raio=150, forca=230),
                                                  comp("Emissor de partículas", estilo="fogo", por_seg=25)]))
        objs.append(nova_entidade("Moeda", x + 60, 300 - (i % 2) * 90,
                                  comportamentos=[comp("Luz", raio=40, forca=160), comp("Girar sempre")]))
    objs += [nova_entidade("Inimigo", 900, 428, "Morcego", gravidade=False, w=30, h=20, cor=[60, 50, 70],
                           velocidade=0, distancia=0, comportamentos=[comp("Senoide (vai e volta)", distancia=60),
                                                                      comp("Perseguir", alcance=200, velocidade=80)]),
             nova_entidade("Bandeira", 2100, 380, comportamentos=[comp("Luz", raio=120)]),
             nova_entidade("Player", 60, 400, comportamentos=[comp("Luz", raio=190), comp("Vida", vida=3)])] + ui_vida(3)
    return {"fases": {"Fase 1": {"cena": cena, "objetos": objs}}, "fase_atual": "Fase 1", "fase_inicial": "Fase 1",
            "modelos": {}}


EXEMPLOS = {"Exemplo: plataforma (2 fases)": exemplo_plataforma,
            "Exemplo: aventura vista de cima": exemplo_aventura,
            "Exemplo: caverna escura (luzes)": exemplo_caverna}


def completar_entidade(d):
    tipo = d.get("tipo", "Bloco")
    if tipo in ("Bloco", "Caixa", "Decoracao") and "material" not in d:
        d["material"] = "Plástico"     # objetos de projetos antigos continuam com o mesmo visual
    if tipo in MODELOS:
        for k, v in MODELOS[tipo].items():
            d.setdefault(k, copy.deepcopy(v))
    for k, v in COMUNS.items():
        d.setdefault(k, v)
    d.setdefault("nome", tipo)
    d.setdefault("x", 0)
    d.setdefault("y", 0)
    d.setdefault("w", 40)
    d.setdefault("h", 40)
    d.setdefault("cor", [255, 255, 255])
    if not isinstance(d.get("valores"), dict):
        d["valores"] = {}
    if not isinstance(d.get("comportamentos"), list):
        d["comportamentos"] = []
    d.setdefault("eventos", [])
    d.setdefault("script", "")
    return d


def completar_projeto(p):
    # projetos antigos (sem fases) viram a "Fase 1"
    if not isinstance(p.get("fases"), dict) or not p["fases"]:
        p["fases"] = {"Fase 1": {"cena": p.pop("cena", {}), "objetos": p.pop("objetos", [])}}
    p.pop("cena", None)
    p.pop("objetos", None)
    for fase in p["fases"].values():
        if not isinstance(fase.get("cena"), dict):
            fase["cena"] = {}
        for k, v in cena_padrao().items():
            fase["cena"].setdefault(k, copy.deepcopy(v))
        if not isinstance(fase.get("objetos"), list):
            fase["objetos"] = []
        for d in fase["objetos"]:
            completar_entidade(d)
    if p.get("fase_atual") not in p["fases"]:
        p["fase_atual"] = next(iter(p["fases"]))
    if p.get("fase_inicial") not in p["fases"]:
        p["fase_inicial"] = next(iter(p["fases"]))
    if not isinstance(p.get("modelos"), dict):
        p["modelos"] = {}
    for m in p["modelos"].values():
        completar_entidade(m)
    return p


def num_seguro(v, padrao=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return padrao


def cor_ok(c):
    try:
        return tuple(max(0, min(255, int(v))) for v in list(c)[:3])
    except (TypeError, ValueError):
        return (255, 0, 255)


def clarear(c, n):
    return tuple(max(0, min(255, v + n)) for v in cor_ok(c))


def fmt(v):
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


def interpretar_valor(txt):
    """Texto digitado num VALOR do objeto -> numero, verdadeiro/falso ou texto."""
    s = txt.strip()
    if s.lower() in ("verdadeiro", "sim", "true"):
        return True
    if s.lower() in ("falso", "nao", "não", "false"):
        return False
    try:
        f = float(s.replace(",", "."))
        return int(f) if f.is_integer() else f
    except ValueError:
        return txt


def sobrepoe(a, b):
    return a.x < b.x + b.w and a.x + a.w > b.x and a.y < b.y + b.h and a.y + a.h > b.y


def encostando(a, b, m=1.0):
    """Igual sobrepoe, mas conta tambem quando esta so encostado (em cima de um bloco, por ex.)."""
    return a.x < b.x + b.w + m and a.x + a.w + m > b.x and a.y < b.y + b.h + m and a.y + a.h + m > b.y


def quebrar_texto(txt, fonte_, largura):
    linhas = []
    for paragrafo in str(txt).split("\n"):
        atual = ""
        for palavra in paragrafo.split(" "):
            teste = (atual + " " + palavra).strip()
            if fonte_.size(teste)[0] <= largura or not atual:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


NOMES_TECLAS = {
    "espaco": pygame.K_SPACE, "espaço": pygame.K_SPACE, "space": pygame.K_SPACE,
    "enter": pygame.K_RETURN, "esquerda": pygame.K_LEFT, "direita": pygame.K_RIGHT,
    "cima": pygame.K_UP, "baixo": pygame.K_DOWN, "shift": pygame.K_LSHIFT, "ctrl": pygame.K_LCTRL,
}


def codigo_tecla(nome):
    n = str(nome).strip().lower()
    if n in NOMES_TECLAS:
        return NOMES_TECLAS[n]
    if len(n) == 1:
        return ord(n)
    return None


# ---------------------------------------------------------------------
# Configuracoes (config.json): atalhos do editor, controles do jogo e opcoes gerais
# ---------------------------------------------------------------------
ATALHOS_PADRAO = {
    "play": ["f5"], "play_cheio": ["f10"], "tela_cheia": ["f11"], "ajuda": ["f1"],
    "salvar": ["ctrl+s"], "abrir": ["ctrl+o"], "inicio": ["ctrl+i"],
    "desfazer": ["ctrl+z"], "refazer": ["ctrl+y", "ctrl+shift+z"],
    "copiar": ["ctrl+c"], "recortar": ["ctrl+x"], "colar": ["ctrl+v"], "duplicar": ["ctrl+d"],
    "selecionar_tudo": ["ctrl+a"], "apagar": ["delete", "backspace"], "zoom_100": ["ctrl+0", "ctrl+[0]"],
    "zoom_mais": ["=", "+", "[+]"], "zoom_menos": ["-", "[-]"], "focar": ["f"], "snap": ["g"],
    "travar": ["l"], "esconder": ["h"], "borracha": ["e"], "minimapa": ["m"],
    "girar": ["r"], "girar_menos": ["shift+r"], "saida": ["f9"],
}
NOMES_ATALHOS = {
    "play": "Play (testar)", "play_cheio": "Play em tela cheia", "tela_cheia": "Tela cheia", "ajuda": "Ajuda / atalhos",
    "salvar": "Salvar", "abrir": "Recarregar o projeto salvo", "inicio": "Voltar para o Início",
    "desfazer": "Desfazer", "refazer": "Refazer", "copiar": "Copiar", "recortar": "Recortar", "colar": "Colar",
    "duplicar": "Duplicar", "selecionar_tudo": "Selecionar tudo", "apagar": "Apagar selecionados",
    "zoom_100": "Zoom 100%", "zoom_mais": "Mais zoom", "zoom_menos": "Menos zoom", "focar": "Focar na seleção",
    "snap": "Liga/desliga snap", "travar": "Travar / destravar", "esconder": "Esconder no editor",
    "borracha": "Borracha", "minimapa": "Mini-mapa", "girar": "Girar seleção", "girar_menos": "Girar ao contrário",
    "saida": "Mostrar/esconder a Saída (erros)",
}
CONTROLES_PADRAO = {
    "esquerda": ["a", "left"], "direita": ["d", "right"], "cima": ["w", "up"], "baixo": ["s", "down"],
    "pular": ["space", "w", "up"], "acao": ["e"], "pausa": ["p"], "reiniciar": ["r"], "debug": ["f2"],
}
NOMES_CONTROLES = {
    "esquerda": "Andar para a esquerda", "direita": "Andar para a direita", "cima": "Subir (visão de cima)",
    "baixo": "Descer (visão de cima)", "pular": "Pular", "acao": "Falar / avançar diálogo", "pausa": "Pausar",
    "reiniciar": "Recomeçar (depois de vencer/perder)", "debug": "Modo debug",
}
GERAL_PADRAO = {
    "autosave_seg": 90, "grade_padrao": 20, "volume_musica": 60, "volume_efeitos": 100,
    "tela_carregamento": True, "tela_cheia_ao_abrir": False, "minimapa": True, "dicas": True,
    "abrir_ultimo": False, "ultimo_projeto": "", "migrado": False, "primeiros_passos": True, "notificacoes": True,
}
NOMES_GERAL = {
    "autosave_seg": ("Salvar automático (segundos)", 15, 600, 15),
    "grade_padrao": ("Tamanho da grade", 4, 128, 4),
    "volume_musica": ("Volume da música (%)", 0, 100, 10),
    "volume_efeitos": ("Volume dos sons (%)", 0, 100, 10),
    "tela_carregamento": ("Mostrar tela de carregamento",), "tela_cheia_ao_abrir": ("Abrir em tela cheia",),
    "minimapa": ("Mini-mapa ligado",), "dicas": ("Mostrar dicas ao passar o mouse",),
    "abrir_ultimo": ("Abrir direto o último projeto (pular o Início)",),
    "primeiros_passos": ("Mostrar o guia 'Primeiros passos' no editor",),
    "notificacoes": ("Mostrar avisos em balões (canto da tela)",),
}
CORES_DESTAQUE = {"Azul": [70, 140, 255], "Verde": [46, 168, 98], "Roxo": [140, 92, 230], "Laranja": [232, 128, 40],
                  "Rosa": [222, 78, 148], "Ciano": [26, 168, 190], "Vermelho": [214, 72, 72]}
RESOLUCOES = ["1280x720", "1366x768", "1600x900", "1920x1080"]
APARENCIA_PADRAO = {"fonte_interface": "Segoe UI", "destaque": "Azul", "resolucao": "1280x720", "nitidez": "Suave"}
CORES_SCRIPT_PADRAO = {
    "palavras": [198, 120, 221], "suas_funcoes": [86, 214, 120], "funcoes_prontas": [97, 175, 239],
    "eventos": [229, 192, 123], "textos": [152, 195, 121], "numeros": [209, 154, 102],
    "comentarios": [110, 115, 130], "nomes": [220, 223, 228], "fundo": [22, 23, 28],
}
NOMES_CORES_SCRIPT = {
    "palavras": "Palavras da linguagem (se, var, quando...)", "suas_funcoes": "Suas funções (funcao pular...)",
    "funcoes_prontas": "Funções prontas (escrever, criar...)", "eventos": "Eventos (iniciar, tecla...)",
    "textos": "Textos \"entre aspas\"", "numeros": "Números", "comentarios": "Comentários # ...",
    "nomes": "Variáveis e o resto", "fundo": "Fundo do editor",
}
SCRIPT_PADRAO = {"tamanho": 15, "fonte": "Consolas", "cores": copy.deepcopy(CORES_SCRIPT_PADRAO)}
PALETA_CORES = [[255, 255, 255], [220, 223, 228], [150, 152, 165], [110, 115, 130], [60, 62, 70], [22, 23, 28],
                [255, 110, 110], [230, 70, 70], [255, 160, 80], [229, 192, 123], [255, 230, 100], [209, 154, 102],
                [152, 195, 121], [86, 214, 120], [46, 168, 98], [100, 230, 200], [97, 175, 239], [70, 140, 255],
                [130, 160, 255], [198, 120, 221], [240, 120, 200], [255, 180, 220], [40, 44, 70], [12, 14, 20]]
CONFIG = {"atalhos": copy.deepcopy(ATALHOS_PADRAO), "controles": copy.deepcopy(CONTROLES_PADRAO),
          "geral": dict(GERAL_PADRAO), "aparencia": dict(APARENCIA_PADRAO), "script": copy.deepcopy(SCRIPT_PADRAO)}
CODIGOS_JOGO = {}


def carregar_config():
    try:
        with open(ARQUIVO_CONFIG, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError):
        dados = {}
    for chave, padrao in (("atalhos", ATALHOS_PADRAO), ("controles", CONTROLES_PADRAO), ("geral", GERAL_PADRAO),
                          ("aparencia", APARENCIA_PADRAO), ("script", SCRIPT_PADRAO)):
        atual = dados.get(chave) if isinstance(dados.get(chave), dict) else {}
        CONFIG[chave] = {k: copy.deepcopy(atual.get(k, v)) for k, v in padrao.items()}
    cores = CONFIG["script"].get("cores") if isinstance(CONFIG["script"].get("cores"), dict) else {}
    CONFIG["script"]["cores"] = {k: list(cor_ok(cores.get(k, v))) for k, v in CORES_SCRIPT_PADRAO.items()}
    aplicar_controles(CONFIG["controles"])
    aplicar_aparencia()


def aplicar_aparencia():
    """Cor de destaque e fontes. Vale na hora (a resolucao vale quando abrir de novo)."""
    global C_DESTAQUE
    C_DESTAQUE = tuple(CORES_DESTAQUE.get(CONFIG["aparencia"].get("destaque"), CORES_DESTAQUE["Azul"]))
    _fontes.clear()
    _fontes_familia.clear()
    _cache_txt.clear()


def aplicar_resolucao():
    """Tamanho da interface (menos esticado = letras mais nitidas). Chamado antes de abrir a janela."""
    global LARGURA, ALTURA, VIEW, TELA_INTEIRA
    try:
        w, h = (int(v) for v in str(CONFIG["aparencia"].get("resolucao", "1280x720")).split("x"))
    except ValueError:
        w, h = 1280, 720
    LARGURA, ALTURA = max(1280, w), max(720, h)
    VIEW = pygame.Rect(PAINEL_ESQ, TOPO + ABAS_H, LARGURA - PAINEL_ESQ - PAINEL_DIR, ALTURA - TOPO - ABAS_H - RODAPE)
    TELA_INTEIRA = pygame.Rect(0, 0, LARGURA, ALTURA)
    os.environ["SDL_HINT_RENDER_SCALE_QUALITY"] = "0" if CONFIG["aparencia"].get("nitidez") == "Pixel" else "1"


def familia_ui():
    return FONTES_UI.get(CONFIG["aparencia"].get("fonte_interface"), FONTES_UI["Segoe UI"])


def fonte_ui(tam, negrito=False):
    return fonte_familia(familia_ui(), tam, negrito)


def fonte_codigo(tam=None):
    tam = tam or CONFIG["script"].get("tamanho", 15)
    return fonte_familia(FONTES_CODIGO.get(CONFIG["script"].get("fonte"), FONTES_CODIGO["Consolas"]), tam)


_fontes_familia = {}


def fonte_familia(familia, tam, negrito=False, italico=False):
    tam = max(6, min(200, int(num_seguro(tam, 16))))
    chave = (familia, tam, negrito, italico)
    f = _fontes_familia.get(chave)
    if f is None:
        try:
            f = pygame.font.SysFont(familia, tam, bold=negrito, italic=italico)
        except (pygame.error, TypeError):
            f = pygame.font.SysFont("arial", tam, bold=negrito)
        _fontes_familia[chave] = f
    return f


def salvar_config():
    try:
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(CONFIG, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def codigo_de_nome(nome):
    nome = str(nome).strip().lower()
    try:
        return pygame.key.key_code(nome)
    except (ValueError, AttributeError, pygame.error):
        pass
    especiais = {"space": pygame.K_SPACE, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP,
                 "down": pygame.K_DOWN, "return": pygame.K_RETURN, "escape": pygame.K_ESCAPE,
                 "backspace": pygame.K_BACKSPACE, "delete": pygame.K_DELETE, "tab": pygame.K_TAB}
    if nome in especiais:
        return especiais[nome]
    if nome.startswith("f") and nome[1:].isdigit():
        return getattr(pygame, "K_F" + nome[1:], None)
    if len(nome) == 1:
        return ord(nome)
    return None


def aplicar_controles(controles):
    """Converte os nomes das teclas do jogo (config ou projeto exportado) em codigos do pygame."""
    CODIGOS_JOGO.clear()
    for acao, padrao in CONTROLES_PADRAO.items():
        nomes = controles.get(acao, padrao) if isinstance(controles, dict) else padrao
        cods = [c for c in (codigo_de_nome(n) for n in nomes) if c is not None]
        CODIGOS_JOGO[acao] = cods or [c for c in (codigo_de_nome(n) for n in padrao) if c is not None]


def nome_da_tecla(key, mod=0, com_mods=True):
    try:
        nome = pygame.key.name(key)
    except (AttributeError, pygame.error, ValueError):
        nome = ""
    if not nome:
        nome = chr(key) if 32 < key < 127 else str(key)
    nome = nome.lower()
    if not com_mods:
        return nome
    partes = []
    if mod & pygame.KMOD_CTRL:
        partes.append("ctrl")
    if mod & pygame.KMOD_SHIFT:
        partes.append("shift")
    if mod & getattr(pygame, "KMOD_ALT", 0):
        partes.append("alt")
    return "+".join(partes + [nome])


def texto_atalho(combo):
    """'ctrl+shift+z' -> 'Ctrl+Shift+Z' para mostrar na tela."""
    bonitos = {"space": "Espaço", "left": "←", "right": "→", "up": "↑", "down": "↓", "return": "Enter",
               "escape": "Esc", "backspace": "Backspace", "delete": "Delete", "[0]": "Num0", "[+]": "Num+",
               "[-]": "Num-", "tab": "Tab"}
    return "+".join(bonitos.get(p, p.upper() if len(p) <= 3 else p.capitalize()) for p in str(combo).split("+"))


def atalho_de(acao):
    lista = CONFIG["atalhos"].get(acao) or ATALHOS_PADRAO.get(acao, [])
    return texto_atalho(lista[0]) if lista else ""


def evento_e(e, acao):
    """Verdadeiro se a tecla apertada (evento) bate com um atalho do editor."""
    combo = nome_da_tecla(e.key, e.mod)
    simples = nome_da_tecla(e.key, e.mod & pygame.KMOD_CTRL)   # ignora shift em atalhos com letras
    return combo in CONFIG["atalhos"].get(acao, ()) or simples in CONFIG["atalhos"].get(acao, ())


def acao_jogo(acao):
    return CODIGOS_JOGO.get(acao) or []


aplicar_controles(CONTROLES_PADRAO)
