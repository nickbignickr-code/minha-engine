# Minha Engine - objetos.py
# tipos de objeto, comportamentos e o catálogo da programação visual
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Tipos de objeto
# ---------------------------------------------------------------------
MODELOS = {
    # ---- BASICO ----
    "Peça":      {"w": 80, "h": 80, "cor": [163, 162, 165], "solido": True, "gravidade": False, "material": "Plástico",
                  "forma": "Retângulo", "contorno": 2, "cor_contorno": [90, 90, 96]},
    # ---- MUNDO ----
    "Bloco":     {"w": 120, "h": 40, "cor": [90, 200, 120], "solido": True, "gravidade": False, "material": "Grama"},
    "Player":    {"w": 32, "h": 48, "cor": [80, 170, 255], "solido": False, "gravidade": True,
                  "velocidade": 320, "pulo": 720, "aceleracao": 3000, "pulos_extras": 0, "pulo_variavel": True,
                  "anim_andando": "", "anim_pulando": ""},
    "Moeda":     {"w": 20, "h": 20, "cor": [255, 210, 50], "solido": False, "gravidade": False, "valor": 1},
    "Inimigo":   {"w": 32, "h": 32, "cor": [230, 70, 70], "solido": False, "gravidade": True,
                  "velocidade": 100, "distancia": 160},
    "Espinho":   {"w": 40, "h": 20, "cor": [200, 200, 215], "solido": False, "gravidade": False},
    "Bandeira":  {"w": 20, "h": 80, "cor": [220, 220, 220], "solido": False, "gravidade": False,
                  "ir_para_fase": ""},
    "Caixa":     {"w": 40, "h": 40, "cor": [160, 105, 55], "solido": True, "gravidade": True, "empurravel": True,
                  "material": "Madeira"},
    "Plataforma Movel": {"w": 120, "h": 20, "cor": [90, 160, 220], "solido": True, "gravidade": False,
                         "vel_x": 100, "vel_y": 0, "distancia": 200},
    "Trampolim": {"w": 60, "h": 20, "cor": [240, 110, 200], "solido": True, "gravidade": False, "forca": 1100},
    "Checkpoint": {"w": 20, "h": 60, "cor": [150, 150, 150], "solido": False, "gravidade": False},
    "Lava":      {"w": 120, "h": 30, "cor": [255, 90, 20], "solido": False, "gravidade": False},
    "Portal":    {"w": 40, "h": 60, "cor": [170, 80, 255], "solido": False, "gravidade": False, "destino": ""},
    "NPC":       {"w": 32, "h": 48, "cor": [240, 180, 90], "solido": False, "gravidade": True,
                  "fala": "Olá, aventureiro!|Use as setas para andar e Espaço para pular.|Boa sorte!"},
    "Item":      {"w": 24, "h": 24, "cor": [80, 230, 230], "solido": False, "gravidade": False, "item": "chave"},
    "Zona":      {"w": 120, "h": 120, "cor": [255, 230, 0], "solido": False, "gravidade": False},
    "Decoracao": {"w": 60, "h": 60, "cor": [110, 110, 150], "solido": False, "gravidade": False,
                  "material": "Plástico", "forma": "Retângulo"},
    # ---- INTERFACE (UI) ----
    "Texto":     {"w": 220, "h": 32, "cor": [255, 255, 255], "texto": "Pontos: {global.pontos}",
                  "tamanho_fonte": 24, "fonte": "Segoe UI", "negrito": False, "italico": False,
                  "alinhamento": "Esquerda", "sombra_texto": True, "na_tela": True},
    "Botao":     {"w": 160, "h": 44, "cor": [70, 140, 255], "texto": "Clique aqui", "tamanho_fonte": 20,
                  "fonte": "Segoe UI", "negrito": True, "italico": False,
                  "cor_texto": [255, 255, 255], "arredondado": 8, "na_tela": True},
    "Barra":     {"w": 200, "h": 20, "cor": [80, 220, 100], "cor_fundo": [50, 50, 60],
                  "valor_de": "global.vida", "maximo": 100, "na_tela": True},
    "Painel":    {"w": 240, "h": 120, "cor": [30, 30, 40], "opacidade": 210, "arredondado": 10, "na_tela": True},
    "Imagem":    {"w": 100, "h": 100, "cor": [255, 255, 255], "imagem": ""},
}
GRUPOS_TIPOS = [
    ("BÁSICO", ["Peça", "Bloco", "Decoracao", "Zona"]),
    ("PERSONAGENS", ["Player", "NPC", "Inimigo"]),
    ("COLETÁVEIS", ["Moeda", "Item", "Checkpoint", "Bandeira"]),
    ("PERIGOS", ["Espinho", "Lava"]),
    ("MECÂNICAS", ["Caixa", "Plataforma Movel", "Trampolim", "Portal"]),
    ("EFEITOS", ["preset:Tocha", "preset:Luz", "preset:Chuva", "preset:Neve", "preset:Fogueira", "preset:Brilhos"]),
    ("INTERFACE (UI)", ["Texto", "Botao", "Barra", "Painel", "Imagem"]),
]
MATERIAIS = ["Plástico", "Madeira", "Tijolo", "Pedra", "Metal", "Grama", "Areia", "Gelo", "Neon", "Vidro",
             "Borracha", "Tecido"]
DESC_MATERIAIS = {"Gelo": "escorrega", "Areia": "deixa lento", "Borracha": "quica", "Neon": "brilha",
                  "Vidro": "transparente"}
FORMAS = ["Retângulo", "Círculo", "Triângulo", "Losango", "Rampa ◢", "Rampa ◣"]
OPCOES_PROPS = {"material": MATERIAIS, "forma": FORMAS, "fonte": list(FONTES_JOGO),
                "alinhamento": ["Esquerda", "Centro", "Direita"]}


def preset_objeto(nome):
    """Objetos prontos da categoria EFEITOS (sao Pecas com comportamentos)."""
    def c(nome_c, **p):
        base = params_padrao(COMPORTAMENTOS[nome_c])
        base.update({k: str(v) for k, v in p.items()})
        return {"t": nome_c, "p": base}
    if nome == "Tocha":
        return nova_entidade("Decoracao", 0, 0, "Tocha", w=14, h=40, cor=[120, 80, 50], material="Madeira",
                             comportamentos=[c("Luz", raio=150), c("Emissor de partículas", estilo="fogo", por_seg=25)])
    if nome == "Luz":
        return nova_entidade("Zona", 0, 0, "Luz", w=30, h=30, cor=[255, 240, 150], comportamentos=[c("Luz", raio=200)])
    if nome == "Chuva":
        return nova_entidade("Zona", 0, 0, "Chuva", w=40, h=40, cor=[120, 160, 255],
                             comportamentos=[c("Emissor de partículas", estilo="chuva", por_seg=80)])
    if nome == "Neve":
        return nova_entidade("Zona", 0, 0, "Neve", w=40, h=40, cor=[240, 240, 255],
                             comportamentos=[c("Emissor de partículas", estilo="neve", por_seg=25)])
    if nome == "Fogueira":
        return nova_entidade("Decoracao", 0, 0, "Fogueira", w=50, h=20, cor=[110, 70, 40], material="Madeira",
                             comportamentos=[c("Luz", raio=220), c("Emissor de partículas", estilo="fogo", por_seg=60),
                                             c("Emissor de partículas", estilo="fumaca", por_seg=8)])
    if nome == "Brilhos":
        return nova_entidade("Zona", 0, 0, "Brilhos", w=60, h=60, cor=[255, 240, 120],
                             comportamentos=[c("Emissor de partículas", estilo="brilho", por_seg=15, r=255, g=240,
                                               b=120)])
    return nova_entidade("Peça", 0, 0)


DESC_PRESETS = {"Tocha": "Tocha com fogo e luz.", "Luz": "Uma luz invisível (precisa de Escuridão na cena).",
                "Chuva": "Faz chover na tela toda.", "Neve": "Faz nevar na tela toda.",
                "Fogueira": "Fogo, fumaça e muita luz.", "Brilhos": "Brilhinhos subindo (tesouros, magia)."}
TIPOS_UI = {"Texto", "Botao", "Barra", "Painel"}
NOMES_CURTOS = {"Plataforma Movel": "Plat. Móvel", "Decoracao": "Decoração", "Botao": "Botão"}

# Propriedades que TODO objeto tem
COMUNS = {"imagem": "", "animacao": "", "fps_anim": 8, "opacidade": 255, "rotacao": 0, "espelhar": False,
          "camada": 0, "visivel": True, "na_tela": False, "grupo": ""}

# ---------------------------------------------------------------------
# Comportamentos prontos (como no GDevelop / Construct): ligue no painel direito
# ---------------------------------------------------------------------
COMPORTAMENTOS = {
    "Bala": [("velocidade", "500", "e"), ("angulo", "0", "e"), ("some_na_parede", "Sim", "sn")],
    "Senoide (vai e volta)": [("eixo", "y", "s"), ("distancia", "40", "e"), ("vezes_por_seg", "0.5", "e")],
    "Girar sempre": [("graus_por_seg", "90", "e")],
    "Perseguir": [("alvo", "Player", "s"), ("velocidade", "120", "e"), ("alcance", "400", "e")],
    "Vida": [("vida", "3", "e"), ("dano_de", "Inimigo", "s"), ("invencivel_seg", "1", "e"), ("barra", "Sim", "sn")],
    "Dano": [("quanto", "1", "e"), ("em", "Player", "s"), ("empurrar", "350", "e"), ("some_ao_acertar", "Não", "sn")],
    "Gerador": [("tipo", "Moeda", "s"), ("a_cada_seg", "2", "e"), ("maximo", "5", "e")],
    "Arrastável (mouse)": [],
    "Plataforma atravessável": [],
    "Destruir fora da tela": [("margem", "300", "e")],
    "Preso no mapa": [],
    "Sumir aos poucos": [("seg", "1", "e"), ("destruir", "Sim", "sn")],
    "8 direções (teclado)": [("velocidade", "200", "e")],
    "Luz": [("raio", "160", "e"), ("forca", "255", "e")],
    "Emissor de partículas": [("estilo", "fogo", "s"), ("por_seg", "30", "e"), ("r", "255", "e"), ("g", "140", "e"),
                              ("b", "40", "e")],
}
DESC_COMPORTAMENTOS = {
    "Bala": "Anda reto no ângulo (0 = direita, 90 = baixo, 180 = esquerda, 270 = cima). Some ao bater em algo sólido.",
    "Senoide (vai e volta)": "Balança suave no eixo x ou y. Ótimo para moedas, plataformas e inimigos voadores.",
    "Girar sempre": "Gira sem parar (graus por segundo, negativo gira ao contrário).",
    "Perseguir": "Vai atrás do alvo (nome, tipo ou grupo) quando ele chega perto (alcance).",
    "Vida": "Dá vida ao objeto. Perde 1 ao encostar em 'dano_de' (nome, tipo ou grupo) e pisca. Zerou: o "
            "objeto é destruído (o Player volta pro checkpoint com a vida cheia). No Player, inimigos, "
            "espinhos e lava tiram vida em vez de matar direto.",
    "Dano": "Machuca quem encostar: tira 'quanto' de vida de 'em' (nome, tipo ou grupo, ex: Player ou Inimigos) e "
            "empurra para trás. Quem tem o comportamento Vida perde vida; quem não tem é destruído (o Player volta "
            "pro checkpoint). Use em espadas, tiros, armadilhas, inimigos e chefões. 'some_ao_acertar' = Sim para "
            "tiros que somem quando acertam.",
    "Gerador": "Cria um objeto (tipo ou modelo) a cada X segundos na posição dele, até o máximo vivo.",
    "Arrastável (mouse)": "No jogo, dá para pegar e arrastar com o mouse.",
    "Plataforma atravessável": "Para objetos sólidos: dá para pular por baixo e ficar em cima (one-way).",
    "Destruir fora da tela": "Some quando sai da tela (bom para tiros e coisas criadas).",
    "Preso no mapa": "Não deixa o objeto sair da área do mapa.",
    "Sumir aos poucos": "Vai ficando transparente e (se quiser) é destruído no fim.",
    "8 direções (teclado)": "Anda com as setas/WASD para os lados e para cima/baixo (para qualquer objeto).",
    "Luz": "Ilumina em volta do objeto quando a cena tem 'Escuridão' maior que 0 (cavernas, noite, terror).",
    "Emissor de partículas": "Solta partículas sem parar. Estilos: fogo, fumaca, brilho, chuva, neve "
                             "(chuva e neve caem na tela toda).",
}

DESC_TIPOS = {
    "Peça": "A peça básica (como no Roblox): escolha forma, cor e material, e depois dê uma imagem, um desenho "
            "ou uma animação em APARÊNCIA. Comportamentos dão vida a ela.",
    "Bloco": "Chão e paredes. Sólido.",
    "Player": "O jogador. Anda com A/D ou setas e pula com Espaço/W. Tem pulo duplo (pulos_extras), "
              "aceleração e pulo variável (soltar cedo = pulo menor).",
    "Moeda": "O player pega e soma moedas.",
    "Inimigo": "Anda de um lado pro outro. Pular em cima mata ele; encostar do lado mata o player.",
    "Espinho": "Encostou, morreu (volta pro início ou checkpoint).",
    "Bandeira": "Encostou, venceu. Se 'ir_para_fase' tiver o nome de uma fase, vai pra ela.",
    "Caixa": "Sólida, cai com gravidade e o player pode empurrar.",
    "Plataforma Movel": "Plataforma que vai e volta (vel_x, vel_y, distancia). Carrega quem está em cima.",
    "Trampolim": "Quem cai em cima é jogado pra cima com a 'forca'.",
    "Checkpoint": "Encostou, o player passa a renascer aqui.",
    "Lava": "Encostou, morreu.",
    "Portal": "Leva o player até o objeto com o nome em 'destino'.",
    "NPC": "Personagem que fala quando o player aperta E perto dele. Separe as falas com | para virar uma "
           "conversa na caixa de diálogo (ex: Oi!|Cuidado com a lava.|Boa sorte!).",
    "Item": "Vai para o inventário (use as condições/ações de item).",
    "Zona": "Área invisível no jogo. Use 'Ao tocar em' para fazer gatilhos.",
    "Decoracao": "Só enfeite, sem colisão.",
    "Texto": "UI: texto na tela. Aceita {variaveis} como {global.pontos}.",
    "Botao": "UI: botão clicável. Use o evento 'Ao clicar no objeto'.",
    "Barra": "UI: barra de vida/progresso. 'valor_de' é uma conta (ex: player.vida).",
    "Painel": "UI: retângulo de fundo para menus e caixas de diálogo.",
    "Imagem": "Mostra uma imagem da pasta 'imagens'.",
}

ROTULOS = {
    "nome": "Nome", "x": "Posição X", "y": "Posição Y", "w": "Largura", "h": "Altura",
    "cor": "Cor (R G B)", "solido": "Sólido", "gravidade": "Gravidade",
    "velocidade": "Velocidade", "pulo": "Força do pulo", "valor": "Valor",
    "distancia": "Distância", "fundo": "Cor de fundo", "imagem": "Imagem", "opacidade": "Opacidade",
    "rotacao": "Rotação", "espelhar": "Espelhar", "camada": "Camada", "visivel": "Visível",
    "na_tela": "Fixo na tela (UI)", "empurravel": "Empurrável", "vel_x": "Veloc. X", "vel_y": "Veloc. Y",
    "forca": "Força", "destino": "Destino (nome)", "fala": "Fala", "item": "Nome do item", "texto": "Texto",
    "tamanho_fonte": "Tam. da fonte", "cor_texto": "Cor do texto", "cor_fundo": "Cor de fundo",
    "valor_de": "Valor de", "maximo": "Máximo", "arredondado": "Arredondado", "largura_tela": "Largura tela",
    "altura_tela": "Altura tela", "tela_cheia": "Tela cheia", "titulo": "Título do jogo",
    "imagem_fundo": "Imagem de fundo", "animacao": "Animação", "fps_anim": "Velocidade anim.",
    "aceleracao": "Aceleração", "pulos_extras": "Pulos no ar", "pulo_variavel": "Pulo variável",
    "anim_andando": "Anim. andando", "anim_pulando": "Anim. pulando", "ir_para_fase": "Ir para fase",
    "parallax_fundo": "Parallax fundo", "musica": "Música", "visao_de_cima": "Visão de cima",
    "limitar_camera": "Limitar câmera", "mostrar_moedas": "Mostrar moedas", "travado": "Travado (editor)",
    "grupo": "Grupo", "zoom_camera": "Zoom da câmera", "olhar_a_frente": "Câmera à frente",
    "material": "Material", "forma": "Forma", "contorno": "Contorno", "cor_contorno": "Cor do contorno",
    "fonte": "Fonte", "negrito": "Negrito", "italico": "Itálico", "alinhamento": "Alinhamento",
    "sombra_texto": "Sombra no texto",
    "esticar_ao_pousar": "Efeito ao pousar", "escuridao": "Escuridão (0-255)",
}
OCULTAS = {"tipo", "eventos", "script", "funcoes", "valores", "modelo", "oculto_editor", "comportamentos"}
CHAVES_FIXAS = {"tipo", "nome", "x", "y", "modelo", "eventos", "script"}

# ---------------------------------------------------------------------
# Catalogo da programacao visual
# Cada parametro: (nome, valor_padrao, tipo)
#   "s"   = texto literal        "e" = expressao Brasa (ex: eu.x + 10)
#   "cmp" = comparacao (==, <..) "atr" = operacao (=, +=, ...)
#   "sn"  = Sim / Nao
#   Onde pede "objeto", pode usar o NOME (Bloco1) ou o TIPO (Inimigo = todos)
# ---------------------------------------------------------------------
GATILHOS = {
    "Ao iniciar": [],
    "A cada frame": [],
    "A cada X segundos": [("seg", "1", "e")],
    "Tecla apertada": [("tecla", "e", "s")],
    "Tecla solta": [("tecla", "e", "s")],
    "Ao tocar em": [("alvo", "Moeda", "s")],
    "Ao parar de tocar em": [("alvo", "Bloco", "s")],
    "Ao cair no chão": [],
    "Ao clicar no objeto": [],
    "Clique em qualquer lugar": [],
    "Ao ser destruído": [],
    "Quando pegar moeda": [],
    "Quando pegar item": [],
    "Quando o player morrer": [],
    "Quando vencer": [],
    "Ao levar dano": [],
    "Quando a vida acabar": [],
    "Quando o diálogo terminar": [],
}
GATILHO_EVENTO = {
    "Ao iniciar": "iniciar", "A cada frame": "frame", "A cada X segundos": "cada",
    "Tecla apertada": "tecla", "Tecla solta": "soltar", "Ao tocar em": "tocar",
    "Ao parar de tocar em": "parar_tocar", "Ao cair no chão": "pousar",
    "Ao clicar no objeto": "clique", "Clique em qualquer lugar": "clique_tela",
    "Ao ser destruído": "destruido", "Quando pegar moeda": "moeda", "Quando pegar item": "item",
    "Quando o player morrer": "respawn", "Quando vencer": "vitoria",
    "Ao levar dano": "dano", "Quando a vida acabar": "sem_vida", "Quando o diálogo terminar": "fim_dialogo",
}

CONDICOES = {
    "Tecla segurada": [("tecla", "d", "s")],
    "Botão do mouse segurado": [],
    "Mouse em cima do objeto": [],
    "Está no chão": [],
    "Tocando em": [("alvo", "Bloco1", "s")],
    "Objeto existe": [("objeto", "Bloco1", "s")],
    "Quantidade de objetos": [("objeto", "Inimigo", "s"), ("op", "==", "cmp"), ("valor", "0", "e")],
    "Distância até objeto": [("objeto", "Player", "s"), ("op", "<", "cmp"), ("valor", "200", "e")],
    "Posição X": [("op", ">", "cmp"), ("valor", "500", "e")],
    "Posição Y": [("op", ">", "cmp"), ("valor", "500", "e")],
    "Está visível": [],
    "Tem item": [("item", "chave", "s")],
    "Fase atual é": [("fase", "Fase 1", "s")],
    "Existe progresso salvo": [],
    "Vida do objeto": [("op", "<=", "cmp"), ("valor", "0", "e")],
    "Vê o objeto (linha de visão)": [("objeto", "Player", "s"), ("alcance", "500", "e")],
    "Está no grupo": [("grupo", "Inimigos", "s")],
    "Tem comportamento ligado": [("comportamento", "Bala", "s")],
    "Diálogo aberto": [],
    "Variável do objeto": [("var", "vida", "s"), ("op", "==", "cmp"), ("valor", "0", "e")],
    "Variável de outro objeto": [("objeto", "Bloco1", "s"), ("var", "vida", "s"), ("op", "==", "cmp"),
                                 ("valor", "0", "e")],
    "Variável global": [("var", "pontos", "s"), ("op", ">=", "cmp"), ("valor", "10", "e")],
    "Moedas": [("op", ">=", "cmp"), ("valor", "5", "e")],
    "Tempo de jogo (seg)": [("op", ">=", "cmp"), ("valor", "10", "e")],
    "Comparar valores": [("a", "eu.vx", "e"), ("op", ">", "cmp"), ("b", "0", "e")],
    "Chance (%)": [("chance", "50", "e")],
    "Expressão": [("expr", "eu.x > 500", "e")],
}

ACOES = {
    # este objeto
    "Mover": [("dx", "0", "e"), ("dy", "0", "e")],
    "Ir para": [("x", "0", "e"), ("y", "0", "e")],
    "Ir até objeto": [("objeto", "Checkpoint", "s")],
    "Velocidade X": [("v", "200", "e")],
    "Velocidade Y (pulo)": [("v", "-600", "e")],
    "Pular (se no chão)": [("forca", "700", "e")],
    "Empurrar": [("fx", "300", "e"), ("fy", "0", "e")],
    "Parar movimento": [],
    "Seguir objeto": [("objeto", "Player", "s"), ("velocidade", "120", "e")],
    "Mudar tamanho": [("w", "40", "e"), ("h", "40", "e")],
    "Mudar cor": [("r", "255", "e"), ("g", "0", "e"), ("b", "0", "e")],
    "Mudar imagem": [("imagem", "heroi.png", "s")],
    "Mudar texto": [("texto", "Vida: {eu.vida}", "s")],
    "Mudar opacidade": [("valor", "128", "e")],
    "Girar": [("graus", "15", "e")],
    "Espelhar": [("espelhar", "Sim", "sn")],
    "Mudar animação": [("animacao", "andar1.png, andar2.png", "s")],
    "Mover suavemente para": [("x", "0", "e"), ("y", "0", "e"), ("seg", "1", "e")],
    "Animar propriedade": [("prop", "opacidade", "s"), ("valor", "0", "e"), ("seg", "1", "e")],
    "Piscar": [("seg", "1", "e")],
    "Partículas": [("qtd", "20", "e"), ("r", "255", "e"), ("g", "210", "e"), ("b", "80", "e")],
    "Esconder": [],
    "Mostrar": [],
    "Ligar/desligar sólido": [("solido", "Sim", "sn")],
    "Ligar/desligar gravidade": [("gravidade", "Sim", "sn")],
    "Destruir": [],
    "Destruir depois de": [("seg", "3", "e")],
    "Destruir quem tocou": [],
    # outros objetos (pelo nome ou tipo)
    "Destruir objeto": [("objeto", "Bloco1", "s")],
    "Mover objeto": [("objeto", "Bloco1", "s"), ("dx", "0", "e"), ("dy", "-20", "e")],
    "Teleportar objeto": [("objeto", "Bloco1", "s"), ("x", "0", "e"), ("y", "0", "e")],
    "Velocidade do objeto": [("objeto", "Bloco1", "s"), ("vx", "100", "e"), ("vy", "0", "e")],
    "Mudar cor do objeto": [("objeto", "Bloco1", "s"), ("r", "255", "e"), ("g", "0", "e"), ("b", "0", "e")],
    "Mudar texto do objeto": [("objeto", "Texto", "s"), ("texto", "Olá!", "s")],
    "Mudar imagem do objeto": [("objeto", "Imagem", "s"), ("imagem", "foto.png", "s")],
    "Esconder objeto": [("objeto", "Bloco1", "s")],
    "Mostrar objeto": [("objeto", "Bloco1", "s")],
    "Sólido no objeto": [("objeto", "Bloco1", "s"), ("solido", "Não", "sn")],
    "Variável de outro objeto": [("objeto", "Bloco1", "s"), ("var", "vida", "s"), ("op", "=", "atr"),
                                 ("valor", "1", "e")],
    # criar
    "Criar objeto": [("tipo", "Moeda", "s"), ("dx", "0", "e"), ("dy", "-40", "e")],
    "Criar objeto em": [("tipo", "Moeda", "s"), ("x", "0", "e"), ("y", "0", "e")],
    "Lançar objeto (tiro)": [("tipo", "Moeda", "s"), ("vx", "600", "e"), ("vy", "0", "e")],
    # variaveis, itens e logica
    "Variável do objeto": [("var", "vida", "s"), ("op", "=", "atr"), ("valor", "1", "e")],
    "Variável global": [("var", "pontos", "s"), ("op", "+=", "atr"), ("valor", "1", "e")],
    "Dar item": [("item", "chave", "s")],
    "Remover item": [("item", "chave", "s")],
    "Esperar (segundos)": [("seg", "1", "e")],
    "Chamar função": [("nome", "minha_funcao", "s")],
    "Executar código": [("codigo", "eu.vy = -900", "s")],
    # textos
    "Mostrar texto": [("texto", "Olá!", "s"), ("seg", "2", "e")],
    "Texto na tela": [("id", "placar", "s"), ("texto", "Pontos: {global.pontos}", "s"),
                      ("x", "12", "e"), ("y", "40", "e")],
    "Apagar texto da tela": [("id", "placar", "s")],
    "Escrever no console": [("texto", "x = {eu.x}", "s")],
    # jogo e camera
    "Somar moedas": [("n", "1", "e")],
    "Ir para fase": [("fase", "Fase 2", "s")],
    "Próxima fase": [],
    "Tocar som": [("som", "pulo.wav", "s"), ("volume", "1", "e")],
    "Tocar música": [("musica", "musica.ogg", "s")],
    "Parar música": [],
    "Pausar jogo": [],
    "Salvar progresso": [],
    "Carregar progresso": [],
    "Voltar ao início": [],
    "Vencer o jogo": [],
    "Perder o jogo": [],
    "Reiniciar fase": [],
    "Controles do player": [("ativo", "Sim", "sn")],
    "Mudar gravidade da cena": [("valor", "1800", "e")],
    "Mudar cor do fundo": [("r", "20", "e"), ("g", "20", "e"), ("b", "40", "e")],
    "Tremer câmera": [("forca", "8", "e"), ("seg", "0.5", "e")],
    "Câmera seguir objeto": [("objeto", "Player", "s")],
    "Zoom da câmera": [("zoom", "1.5", "e"), ("seg", "0.5", "e")],
    # efeitos de impacto (game feel)
    "Congelar tela (impacto)": [("seg", "0.06", "e")],
    "Flash branco": [("seg", "0.12", "e")],
    "Esticar (squash)": [],
    # vida
    "Dar dano": [("objeto", "Player", "s"), ("qtd", "1", "e")],
    "Curar": [("qtd", "1", "e")],
    "Mudar vida": [("vida", "3", "e")],
    # comportamentos
    "Ligar comportamento": [("comportamento", "Bala", "s")],
    "Desligar comportamento": [("comportamento", "Bala", "s")],
    "Mudar ângulo da bala": [("angulo", "180", "e")],
    # dialogos e textos
    "Mostrar diálogo": [("texto", "Oi!|Tudo bem?|Boa sorte na aventura!", "s"), ("nome", "", "s")],
    "Texto flutuante": [("texto", "+1", "s"), ("r", "255", "e"), ("g", "230", "e"), ("b", "80", "e")],
    "Mudar escuridão": [("valor", "200", "e")],
}
OPS_CMP = ["==", "!=", "<", ">", "<=", ">="]
OPS_ATR = ["=", "+=", "-=", "*=", "/="]
OPS_SN = ["Sim", "Não"]

EXEMPLO_SCRIPT = '''# Exemplo de script na linguagem Brasa
var vida = 3

quando iniciar:
    dizer("Oi! Eu tenho " + vida + " vidas", 2)

quando tecla "e":
    eu.cor = [255, 120, 120]
    dizer("Apertei E!", 1)

quando tocar "Moeda":
    global.pontos += 10
    escrever("Pontos: " + global.pontos)

quando cada 5:
    escrever("Ja se passaram " + arredondar(tempo) + " segundos")

funcao pular_alto():
    eu.vy = -1000
'''

AJUDA_SCRIPT = [
    "LINGUAGEM BRASA",
    "var x = 10            cria variável",
    "x += 1                = += -= *= /=",
    "se x > 5:   senao se ...:   senao:",
    "enquanto x < 10:     repetir 3:",
    "para i de 1 ate 10:   para cada x em lista:",
    "funcao nome(a, b):   retornar a + b",
    "e  ou  nao  verdadeiro  falso  nulo",
    "",
    "EVENTOS",
    "quando iniciar:      quando frame:",
    "quando cada 2:       quando pousar:",
    "quando tecla \"e\":    quando soltar \"e\":",
    "quando tocar \"Moeda\":  (tipo ou nome)",
    "quando parar_tocar \"Bloco1\":",
    "quando clique:       quando clique_tela:",
    "quando destruido:    quando moeda:",
    "quando item:   quando respawn:",
    "quando vitoria:   quando dano:",
    "quando sem_vida:",
    "",
    "OBJETOS",
    "eu.x eu.y eu.vx eu.vy eu.w eu.h",
    "eu.cor eu.imagem eu.texto eu.opacidade",
    "eu.rotacao eu.espelhar eu.visivel",
    "eu.vida (valores do objeto)",
    "@COLUNA",
    "FUNÇÕES PRONTAS (aba API tem tudo)",
    "dizer(\"oi\", 2)   escrever(x)",
    "destruir(achar(\"Bloco1\"))",
    "destruir_todos(\"Inimigo\")",
    "criar(\"Moeda\", x, y)   achar(\"Nome\")",
    "achar_todos(\"Inimigo\")   chamar(\"f\")",
    "lancar(\"Moeda\", vx, vy)   (tiro)",
    "depois(2, minha_funcao)  (espera)",
    "tecla(\"d\")  apertou(\"e\")  soltou(\"e\")",
    "mouse_x() mouse_y() mouse_segurado()",
    "aleatorio(1, 6)   distancia(a, b)",
    "dar_item(\"chave\")  tem_item(\"chave\")",
    "moedas()  somar_moedas(1)",
    "vencer() perder() reiniciar()",
    "voltar_inicio()  controles(falso)",
    "hud(\"id\", \"texto\", x, y)",
    "tremer(8, 0.5)  camera(achar(\"X\"))",
    "fundo(r, g, b)  gravidade(1800)",
    "dano(obj, 1)  curar(obj, 1)  congelar(0.06)",
    "flash(eu)  esticar(eu)  zoom(1.5, 0.5)",
    "linha_de_visao(eu, player)",
    "tela_cheia(verdadeiro)",
    "texto numero abs min max raiz",
    "arredondar tamanho adicionar",
]
