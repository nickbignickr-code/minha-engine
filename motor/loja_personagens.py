# Minha Engine - loja_personagens.py
# MAIS PERSONAGENS (28, cada um com versão plataforma, top-down com 4 direções e NPC), inimigos top-down,
# cenário top-down (chão, muros, água, arbustos, vasos...), kits top-down e o exemplo "RPG top-down"
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# GERADOR DE PERSONAGENS EM PIXEL ART
# Letras dos moldes: H cabelo/chapéu, h cabelo escuro, S pele, C roupa, c roupa escura, P calça,
# B sapato, A detalhe (cinto, capa, coroa), V visor, k preto (olhos), w branco
# =====================================================================
CABECAS_LADO = {
    "curto": ["...HHHH...", "..HHHHHH..", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..", "...SSSS..."],
    "longo": ["...HHHH...", "..HHHHHH..", ".HHSSSSS..", ".HHSSSkS..", ".HHSSSSS..", ".HH.SSSS.."],
    "careca": ["..........", "...SSSS...", "..SSSSSS..", "..SSSSkS..", "..SSSSSS..", "...SSSS..."],
    "bone": ["...HHHH...", "..HHHHHHHH", "..hSSSSS..", "..SSSSkS..", "..SSSSSS..", "...SSSS..."],
    "capacete": ["...HHHH...", "..HHHHHH..", "..HHhhhh..", "..HHhhkh..", "..HHSSSS..", "...SSSS..."],
    "astronauta": ["..HHHHHH..", ".HHHHHHHH.", ".HHVVVVVH.", ".HHVVVkVH.", ".HHVVVVVH.", "..HHHHHH.."],
    "ninja": ["...HHHH...", "..HHHHHH..", "..HHHHHHA.", "..HHHwkH..", "..HHHHHH..", "...HHHH..."],
    "robo": ["....A.....", "..HHHHHH..", "..HhhhhH..", "..HhhhVH..", "..HhhhhH..", "...HHHH..."],
    "alien": ["..SSSSSS..", ".SSSSSSSS.", ".SSSSSkkS.", ".SSSSSkkS.", "..SSSSSS..", "...SSSS..."],
    "mago": ["......H...", ".....HH...", "....HHH...", "...HHHHH..", "..AAAAAAA.", "..HSSSSS..", "..HSSSkS..",
             "..HSSSSS..", "...SSSS..."],
    "bruxa": ["......H...", ".....HH...", "....HHH...", "...HHHHH..", ".hhhhhhhhh", "..HSSSSS..", "..HSSSkS..",
              "..HSSSSS..", "...SSSS..."],
    "coroa": ["...A.A.A..", "...AAAAA..", "..HHHHHH..", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..", "...SSSS..."],
    "capuz": ["...HHHH...", "..HHHHHH..", ".HHhSSSS..", ".HHSSSkS..", ".HHhSSSS..", "..HHHHHH.."],
    "chifres": ["w.......w.", "ww.HHHHww.", ".wHHHHHH..", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..", "...SSSS..."],
    "orelhas": ["..H....H..", "..HH..HH..", "..HHHHHH..", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..", "...SSSS..."],
    "chapeu": ["...HHHH...", "...HHHH...", ".hhhhhhhhh", "..SSSSSS..", "..SSSSkS..", "..SSSSSS..", "...SSSS..."],
    "chef": ["...wwww...", "..wwwwww..", "..wwwwww..", "..hhhhhh..", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..",
             "...SSSS..."],
    "bandana": ["...HHHH...", "..AAAAAAAA", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..", "...SSSS..."],
    "rabo": ["....HH....", "...HHHH...", "..HHHHHH..", "..HSSSSS..", "..HSSSkS..", "..HSSSSS..", "...SSSS..."],
}
_FRENTE = ["...HHHH...", "..HHHHHH..", "..HSSSSH..", "..SkSSkS..", "..SSSSSS..", "...SSSS..."]
_COSTAS = ["...HHHH...", "..HHHHHH..", "..HHHHHH..", "..HHHHHH..", "..hHHHHh..", "...SSSS..."]
CABECAS_TD = {   # (frente, costas)
    "careca": (["..........", "...SSSS...", "..SSSSSS..", "..SkSSkS..", "..SSSSSS..", "...SSSS..."],
               ["..........", "...SSSS...", "..SSSSSS..", "..SSSSSS..", "..SSSSSS..", "...SSSS..."]),
    "longo": (["...HHHH...", "..HHHHHH..", ".HHSSSSHH.", ".HSkSSkSH.", ".HSSSSSSH.", ".H.SSSS.H."],
              ["...HHHH...", "..HHHHHH..", ".HHHHHHHH.", ".HHHHHHHH.", ".HHHHHHHH.", ".HH....HH."]),
    "bone": (["...HHHH...", "..HHHHHH..", "..hhhhhh..", "..SkSSkS..", "..SSSSSS..", "...SSSS..."], _COSTAS),
    "capacete": (["...HHHH...", "..HHHHHH..", "..HhhhhH..", "..HkhhkH..", "..HSSSSH..", "...SSSS..."],
                 ["...HHHH...", "..HHHHHH..", "..HHHHHH..", "..HHHHHH..", "..HHHHHH..", "...SSSS..."]),
    "astronauta": (["..HHHHHH..", ".HHHHHHHH.", ".HVVVVVVH.", ".HVkVVkVH.", ".HVVVVVVH.", "..HHHHHH.."],
                   ["..HHHHHH..", ".HHHHHHHH.", ".HHHHHHHH.", ".HHHHHHHH.", ".HHHHHHHH.", "..HHHHHH.."]),
    "ninja": (["...HHHH...", "..HHHHHH..", "..HHHHHH..", "..HwkwkH..", "..HHHHHH..", "...HHHH..."],
              ["...HHHH...", "..HHHHHH..", "..HHHHHH..", "..AAAAAA..", "..HHHHHH..", "...HHHH..."]),
    "robo": (["....A.....", "..HHHHHH..", "..HhhhhH..", "..HVhhVH..", "..HhhhhH..", "...HHHH..."],
             ["....A.....", "..HHHHHH..", "..HHHHHH..", "..HHHHHH..", "..HHHHHH..", "...HHHH..."]),
    "alien": (["..SSSSSS..", ".SSSSSSSS.", ".SkkSSkkS.", ".SkkSSkkS.", "..SSSSSS..", "...SSSS..."],
              ["..SSSSSS..", ".SSSSSSSS.", ".SSSSSSSS.", ".SSSSSSSS.", "..SSSSSS..", "...SSSS..."]),
    "capuz": (["...HHHH...", "..HHHHHH..", ".HHSSSSHH.", ".HSkSSkSH.", ".HHSSSSHH.", "..HHHHHH.."],
              ["...HHHH...", "..HHHHHH..", ".HHHHHHHH.", ".HHHHHHHH.", ".HHHHHHHH.", "..HHHHHH.."]),
    "chapeu": (["...HHHH...", "...HHHH...", ".hhhhhhhh.", "..SkSSkS..", "..SSSSSS..", "...SSSS..."],
               ["...HHHH...", "...HHHH...", ".hhhhhhhh.", "..SSSSSS..", "..SSSSSS..", "...SSSS..."]),
    "bandana": (["...HHHH...", "..AAAAAA..", "..HSSSSH..", "..SkSSkS..", "..SSSSSS..", "...SSSS..."],
                ["...HHHH...", "..AAAAAA..", "..HHHHHH..", "..HHHHHH..", "..hHHHHh..", "...SSSS..."]),
}
_ROSTO = ["..HSSSSH..", "..SkSSkS..", "..SSSSSS..", "...SSSS..."]
_NUCA = ["..HHHHHH..", "..HHHHHH..", "..hHHHHh..", "...SSSS..."]
_PREFIXOS_TD = {   # chapeus que ficam em cima da cabeca normal
    "mago": (["....H.....", "...HHH....", "..HHHHH...", ".AAAAAAAA."], _ROSTO, _NUCA),
    "bruxa": (["....H.....", "...HHH....", "..HHHHH...", "hhhhhhhhhh"], _ROSTO, _NUCA),
    "coroa": (["...A.A.A..", "...AAAAA.."], _FRENTE, _COSTAS),
    "chifres": (["w........w", "ww......ww"], _FRENTE, _COSTAS),
    "orelhas": (["..H....H..", "..HH..HH.."], _FRENTE, _COSTAS),
    "rabo": (["....HH...."], _FRENTE, _COSTAS),
    "chef": (["...wwww...", "..wwwwww..", "..wwwwww.."],
             ["..hhhhhh..", "..SkSSkS..", "..SSSSSS..", "...SSSS..."],
             ["..hhhhhh..", "..SSSSSS..", "..SSSSSS..", "...SSSS..."]),
}
CORPOS = {
    "normal": {
        "a1": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "...PPPP...", "..PP..PP..", "..BB..BB.."],
        "a2": ["..cCCCCc..", "..cCCCCS..", "...CCCCS..", "...AAAA...", "...PPPP...", "....PP....", "....BB...."],
        "pulo": ["S.cCCCCc.S", "S.cCCCCc.S", "...CCCC...", "...AAAA...", "..PPPPPP..", ".PP....PP.", ".B......B."],
        "parado": ["..cCCCCc..", "..cCCCCc..", "...CCCC...", "...AAAA...", "...PPPP...", "...P..P...",
                   "...B..B..."],
        "f0": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "...PPPP...", "...P..P...", "...B..B..."],
        "f1": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "...PPPP...", "...P..B...", "...B......"],
        "f2": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "...PPPP...", "...B..P...", "......B..."],
    },
    "vestido": {
        "a1": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "..CCCCCC..", ".CCCCCCCC.", "..BB..BB.."],
        "a2": ["..cCCCCc..", "..cCCCCS..", "...CCCCS..", "...AAAA...", "..CCCCCC..", ".CCCCCCCC.", "...BBBB..."],
        "pulo": ["S.cCCCCc.S", "S.cCCCCc.S", "...CCCC...", "...AAAA...", "..CCCCCC..", "CCCCCCCCCC", ".B......B."],
        "parado": ["..cCCCCc..", "..cCCCCc..", "...CCCC...", "...AAAA...", "..CCCCCC..", ".CCCCCCCC.",
                   "...B..B..."],
        "f0": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "..CCCCCC..", ".CCCCCCCC.", "...B..B..."],
        "f1": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "..CCCCCC..", ".CCCCCCCC.", "...B......"],
        "f2": ["..cCCCCc..", ".ScCCCCcS.", ".S.CCCC.S.", "...AAAA...", "..CCCCCC..", ".CCCCCCCC.", "......B..."],
    },
}


def _com_capa(linhas, lado=True, letra="A"):
    out = []
    for i, l in enumerate(linhas):
        r = list(l)
        if i < 6:
            if lado:
                if r[1] == ".":
                    r[1] = letra
                if i >= 3 and r[0] == ".":
                    r[0] = letra
            else:
                if r[1] in ".S":
                    r[1] = letra
                if r[8] in ".S":
                    r[8] = letra
        out.append("".join(r))
    return out


def _costas_do_corpo(linhas, capa):
    if not capa:
        return linhas
    return [l.replace("A", capa) for l in ["..AAAAAA..", ".SAAAAAAS.", ".SAAAAAAS.", "..AAAAAA.."]] + linhas[4:]


def _pele(nome):
    return {"clara": (255, 205, 160), "morena": (200, 140, 90), "escura": (125, 82, 52), "zumbi": (130, 190, 110),
            "osso": (235, 235, 220), "metal": (170, 180, 195), "palida": (232, 222, 232), "alien": (120, 220, 120),
            "bruxa": (170, 210, 140), "gato": (250, 195, 130)}[nome]


# nome: (estilo, corpo, pele, H, h, C, c, P, B, A, V, fala do NPC)
PERSONAGENS = [
    ("Aventureiro", "curto", "normal", "clara", (120, 70, 30), (80, 45, 20), (60, 120, 220), (35, 70, 150),
     (70, 60, 50), (30, 25, 25), (160, 110, 40), None, "Bom dia! Dizem que tem um tesouro na masmorra."),
    ("Aventureira", "longo", "normal", "clara", (220, 90, 40), (150, 50, 20), (60, 170, 90), (30, 110, 60),
     (90, 70, 50), (60, 40, 30), (200, 160, 60), None, "Eu já explorei tudo por aqui. Quase tudo."),
    ("Cavaleiro", "capacete", "normal", "clara", (190, 195, 205), (110, 115, 130), (170, 175, 190), (110, 115, 130),
     (120, 125, 140), (70, 70, 80), (200, 40, 50), None, "Proteger o reino é o meu dever!"),
    ("Ninja", "ninja", "normal", "clara", (40, 40, 50), (20, 20, 28), (40, 40, 50), (25, 25, 32), (40, 40, 50),
     (20, 20, 28), (200, 40, 40), None, "...você não me viu aqui."),
    ("Mago", "mago", "normal", "clara", (60, 70, 200), (30, 35, 120), (120, 60, 180), (80, 30, 130), (80, 30, 130),
     (60, 40, 30), (250, 210, 60), None, "A magia está em todo lugar. Até nas moedas!"),
    ("Princesa", "coroa", "vestido", "clara", (250, 210, 90), (200, 150, 40), (240, 120, 180), (190, 70, 130),
     (240, 120, 180), (200, 60, 120), (255, 210, 60), None, "Você viu o meu gato? Ele fugiu pro castelo."),
    ("Pirata", "bandana", "normal", "morena", (60, 40, 30), (40, 25, 15), (235, 235, 235), (190, 190, 190),
     (110, 70, 40), (25, 20, 20), (210, 40, 40), None, "Arrr! Esse mapa leva ao tesouro... eu acho."),
    ("Astronauta", "astronauta", "normal", "clara", (240, 240, 245), (180, 180, 190), (235, 235, 240),
     (170, 170, 185), (220, 220, 230), (120, 120, 130), (255, 140, 40), (110, 210, 255),
     "Houston, temos moedas!"),
    ("Robô", "robo", "normal", "metal", (160, 170, 185), (100, 110, 125), (140, 150, 170), (90, 100, 120),
     (110, 120, 140), (60, 65, 80), (255, 200, 40), (255, 60, 60), "BIP BOP. OLÁ, HUMANO."),
    ("Zumbi", "curto", "normal", "zumbi", (60, 80, 50), (40, 55, 35), (90, 110, 140), (60, 75, 100), (80, 60, 50),
     (50, 40, 30), (110, 90, 60), None, "Uuuuh... cééérebro... brincadeira, oi!"),
    ("Esqueleto", "careca", "normal", "osso", (235, 235, 220), (180, 180, 165), (235, 235, 220), (180, 180, 165),
     (220, 220, 205), (200, 200, 185), (150, 150, 140), None, "Meus ossos doem quando chove."),
    ("Arqueira", "capuz", "normal", "clara", (50, 130, 60), (30, 85, 40), (70, 150, 70), (40, 100, 45),
     (110, 80, 50), (70, 50, 30), (170, 120, 50), None, "Nunca erro uma flecha. Quase nunca."),
    ("Viking", "chifres", "normal", "clara", (200, 130, 60), (140, 80, 30), (130, 90, 60), (90, 60, 40),
     (90, 70, 50), (70, 50, 30), (170, 170, 180), None, "Para Valhalla! Mas antes, um lanche."),
    ("Cientista", "curto", "normal", "clara", (235, 235, 240), (190, 190, 200), (245, 245, 250), (200, 200, 210),
     (70, 70, 90), (30, 25, 25), (80, 160, 255), None, "Eureca! Descobri que moedas brilham."),
    ("Bombeiro", "bone", "normal", "clara", (220, 40, 40), (150, 20, 20), (200, 60, 40), (140, 40, 30),
     (60, 60, 70), (30, 25, 25), (250, 220, 60), None, "Cuidado com a lava, ela queima!"),
    ("Policial", "bone", "normal", "morena", (30, 50, 120), (20, 30, 80), (50, 90, 180), (30, 60, 130),
     (30, 40, 80), (25, 20, 20), (240, 200, 60), None, "Tudo tranquilo por aqui, cidadão."),
    ("Chef", "chef", "normal", "clara", (80, 50, 30), (180, 180, 190), (245, 245, 245), (200, 200, 205),
     (60, 60, 70), (30, 25, 25), (220, 60, 60), None, "Hoje tem bolo de moeda! Hmm..."),
    ("Fazendeiro", "chapeu", "normal", "morena", (230, 200, 100), (180, 150, 60), (190, 60, 50), (130, 40, 35),
     (60, 90, 160), (90, 60, 40), (110, 70, 40), None, "Os slimes comeram minha plantação de novo!"),
    ("Surfista", "curto", "normal", "morena", (250, 220, 100), (200, 170, 60), (255, 150, 60), (200, 100, 30),
     (40, 140, 220), (240, 200, 150), (255, 255, 255), None, "Altas ondas hoje, brother!"),
    ("Gamer", "bone", "normal", "clara", (40, 40, 50), (20, 20, 28), (130, 70, 200), (90, 40, 150), (50, 50, 60),
     (240, 240, 240), (80, 240, 200), None, "Só mais uma partida e eu paro. Juro."),
    ("Vampiro", "curto", "normal", "palida", (30, 30, 40), (15, 15, 22), (40, 30, 50), (25, 20, 30), (30, 30, 40),
     (20, 20, 28), (170, 20, 40), None, "Eu só saio à noite. E para pegar moedas."),
    ("Rei", "coroa", "normal", "clara", (120, 80, 40), (80, 50, 25), (170, 30, 50), (110, 20, 30), (110, 20, 30),
     (30, 25, 25), (255, 210, 60), None, "Quem trouxer o tesouro ganha metade do reino!"),
    ("Samurai", "rabo", "normal", "clara", (25, 25, 32), (15, 15, 20), (40, 60, 120), (25, 40, 80), (30, 40, 70),
     (25, 20, 20), (200, 40, 40), None, "A espada só sai da bainha quando é preciso."),
    ("Bruxa", "bruxa", "vestido", "bruxa", (40, 30, 50), (20, 15, 30), (80, 40, 110), (50, 25, 70), (80, 40, 110),
     (25, 20, 25), (140, 220, 90), None, "Hihihi! Quer provar uma poção?"),
    ("Detetive", "chapeu", "normal", "clara", (110, 80, 50), (70, 50, 30), (200, 170, 120), (150, 120, 80),
     (80, 70, 60), (30, 25, 25), (60, 40, 30), None, "Elementar! O culpado é... o slime."),
    ("Gato herói", "orelhas", "normal", "gato", (240, 150, 60), (190, 100, 30), (60, 120, 220), (35, 70, 150),
     (60, 120, 220), (240, 150, 60), (255, 220, 80), None, "Miau! Quer dizer... olá, aventureiro!"),
    ("Alien", "alien", "normal", "alien", (120, 220, 120), (80, 170, 80), (150, 150, 170), (100, 100, 120),
     (120, 120, 140), (70, 70, 90), (255, 80, 200), None, "Leve-me ao seu líder. Ou à loja de moedas."),
    ("Ciborgue neon", "capacete", "normal", "metal", (30, 30, 40), (80, 255, 220), (40, 40, 55), (80, 255, 220),
     (30, 30, 40), (80, 255, 220), (255, 60, 200), None, "Sistema online. Missão: pegar todas as moedas."),
]
COM_CAPA = {"Mago": "c", "Vampiro": "A", "Rei": "C", "Bruxa": "c"}    # nome: letra da cor da capa


def _montar_quadros(spec):
    nome, estilo, corpo_n, pele, H, h, C, c, P, B, A, V, _fala = spec
    corpo = CORPOS[corpo_n]
    capa = COM_CAPA.get(nome)
    cab_lado = CABECAS_LADO.get(estilo, CABECAS_LADO["curto"])
    if estilo in _PREFIXOS_TD:
        pre, fr, co = _PREFIXOS_TD[estilo]
        frente, costas = pre + fr, pre + co
    else:
        frente, costas = CABECAS_TD.get(estilo, (_FRENTE, _COSTAS))
    corpo_lado = {k: (_com_capa(corpo[k], True, capa) if capa else corpo[k]) for k in ("a1", "a2", "pulo", "parado")}
    corpo_frente = {k: (_com_capa(corpo[k], False, capa) if capa else corpo[k]) for k in ("f0", "f1", "f2")}
    q = {
        "parado": cab_lado + corpo_lado["parado"], "a1": cab_lado + corpo_lado["a1"],
        "a2": cab_lado + corpo_lado["a2"], "pulo": cab_lado + corpo_lado["pulo"],
        "f0": frente + corpo_frente["f0"], "f1": frente + corpo_frente["f1"], "f2": frente + corpo_frente["f2"],
        "b0": costas + _costas_do_corpo(corpo["f0"], capa), "b1": costas + _costas_do_corpo(corpo["f1"], capa),
        "b2": costas + _costas_do_corpo(corpo["f2"], capa),
    }
    altura = max(len(v) for v in q.values())
    q = {k: ["." * 10] * (altura - len(v)) + [l.ljust(10, ".")[:10] for l in v] for k, v in q.items()}
    tabela = {"H": H, "h": h, "S": _pele(pele), "C": C, "c": c, "P": P, "B": B, "A": A, "V": V or (110, 210, 255),
              "k": (20, 20, 28), "w": (255, 255, 255)}
    trans = str.maketrans({k: cor_char(v) for k, v in tabela.items()})
    base = "pers_" + _slug(nome)
    nomes = {}
    for k, linhas in q.items():
        ARTES[f"{base}_{k}"] = [l.translate(trans) for l in linhas]
        nomes[k] = f"{base}_{k}"
    return nomes, altura


QUADROS_PERS = {}
for _sp in PERSONAGENS:
    QUADROS_PERS[_sp[0]] = _montar_quadros(_sp)

# quando o exemplo monta o projeto, as imagens vão para a pasta do projeto novo (não a do aberto)
_COLETAR = None


def _arq(nome_arte):
    if _COLETAR is not None:
        _COLETAR.add(nome_arte)
        return nome_arte + ".png"
    return garantir_arte(nome_arte)


def _lista(nomes):
    return ", ".join(_arq(n) for n in nomes)


def personagem_lado(nome, tipo="Player", **extra):
    q, alt = QUADROS_PERS[nome]
    d = nova_entidade(tipo, 0, 0, _slug(nome).replace("_", " ").title().replace(" ", ""), w=40, h=alt * 4,
                      imagem=_arq(q["parado"]), fps_anim=8, **extra)
    if tipo == "Player":
        d["anim_andando"] = _lista((q["a1"], q["parado"], q["a2"], q["parado"]))
        d["anim_pulando"] = _arq(q["pulo"])
    return d


def personagem_td(nome, tipo="Player", **extra):
    q, alt = QUADROS_PERS[nome]
    d = nova_entidade(tipo, 0, 0, _slug(nome).replace("_", " ").title().replace(" ", ""), w=36,
                      h=int(alt * 3.6), imagem=_arq(q["f0"]), fps_anim=8, **extra)
    # o 1o quadro de cada animação é o "parado" daquela direção
    d["anim_baixo"] = _lista((q["f0"], q["f1"], q["f0"], q["f2"]))
    d["anim_cima"] = _lista((q["b0"], q["b1"], q["b0"], q["b2"]))
    d["anim_lado"] = _lista((q["parado"], q["a1"], q["parado"], q["a2"]))
    return d


def _item_player_lado(nome):
    p = personagem_lado(nome)
    p["nome"] = "Player"
    p["_campos"] = ("imagem", "anim_andando", "anim_pulando", "fps_anim", "w", "h")
    return [(p, 0, 0)]


def _item_player_td(nome):
    p = personagem_td(nome, espada=True)
    p["nome"] = "Player"
    p["_campos"] = ("imagem", "anim_baixo", "anim_cima", "anim_lado", "fps_anim", "w", "h", "espada")
    return [(p, 0, 0)]


def _item_npc(nome):
    spec = next(s for s in PERSONAGENS if s[0] == nome)
    d = personagem_td(nome, tipo="NPC", fala=spec[-1])
    d["nome"] = _slug(nome).replace("_", " ").title().replace(" ", "")
    return [(d, 0, 0)]


def _preco_pers(i):
    if i < 6:
        return 0, None
    if i < 20:
        return 10 + (i % 6) * 5, None
    if i < 23:
        return 0, "Game Maker"
    return 0, "Dev"


for _i, _sp in enumerate(PERSONAGENS):
    _n = _sp[0]
    _q = QUADROS_PERS[_n][0]
    _preco, _plano = _preco_pers(_i)
    _novo("Personagens", f"Personagem: {_n}",
          f"Troca o visual do seu Player (modo plataforma) por {_n}: andando, parado e pulando desenhados.",
          lambda n=_n: _item_player_lado(n), _q["parado"], preco=_preco, plano=_plano)
    _novo("Top-down", f"Top-down: {_n}",
          f"Player {_n} visto de cima, com animação para baixo, para cima e de lado, e espada (Espaço ou J). "
          f"Use o botão 'Modo: Top-down' lá em cima.",
          lambda n=_n: _item_player_td(n), _q["f0"], preco=_preco, plano=_plano)
    _novo("Personagens", f"NPC: {_n}", f"Personagem que conversa (E perto dele): \"{_sp[-1]}\" "
                                        "Funciona no plataforma e no top-down.",
          lambda n=_n: _item_npc(n), _q["f0"], preco=0 if _i < 12 else 5)

# =====================================================================
# INIMIGOS TOP-DOWN (feitos com os personagens)
# =====================================================================
INIMIGOS_TD = [("Zumbi", 2, 60, 1), ("Esqueleto", 2, 90, 1), ("Vampiro", 4, 120, 2), ("Robô", 4, 80, 1),
               ("Bruxa", 3, 70, 1), ("Ninja", 3, 150, 1), ("Pirata", 3, 100, 1), ("Alien", 3, 110, 1)]


def inimigo_td(nome, vida=2, vel=80, dano=1, arqueiro=False):
    d = personagem_td(nome, tipo="Inimigo", velocidade=0, distancia=0, dano=dano, pode_ser_pisado=False,
                      grupo="Inimigos")
    d["nome"] = "Inimigo" + _slug(nome).replace("_", " ").title().replace(" ", "")
    d["comportamentos"] = [_comp("Vida", vida=vida, dano_de="TirosDoPlayer", invencivel_seg=0.3, barra="Sim")]
    if arqueiro:
        d["comportamentos"] += [_comp("Manter distância", alvo="Player", distancia=230, velocidade=vel),
                                _comp("Atirar", tipo="Flecha", a_cada_seg=1.6, velocidade=380, alvo="Player",
                                      alcance=480)]
    else:
        d["comportamentos"] += [_comp("Vagar (anda à toa)", velocidade=int(vel * 0.6)),
                                _comp("Perseguir", alvo="Player", velocidade=vel, alcance=260)]
    return d


def _flecha():
    return flecha_modelo()


for _n, _v, _vel, _dano in INIMIGOS_TD:
    _novo("Top-down", f"Inimigo top-down: {_n}",
          f"Anda à toa e corre atrás do player quando chega perto. {_v} de vida, morre na espada.",
          lambda n=_n, v=_v, ve=_vel, da=_dano: [(inimigo_td(n, v, ve, da), 0, 0)], QUADROS_PERS[_n][0]["f0"],
          preco=10 + _v * 3)
_novo("Top-down", "Inimigo top-down: Arqueiro", "Fica longe de você e atira flechas. 2 de vida.",
      lambda: [(_flecha(), 0, 0), (inimigo_td("Arqueira", 2, 110, 1, arqueiro=True), 0, 0)],
      QUADROS_PERS["Arqueira"][0]["f0"], preco=25)

# =====================================================================
# CENÁRIO TOP-DOWN
# =====================================================================
ARTES.update({
    "arbusto": ["...gggggg...", "..gggGgggg..", ".ggGggggGgg.", "gggggGgggggg", "ggGgggggGggg", "gggggggggGgg",
                ".gGgggGgggg.", "..GGGGGGGG.."],
    "vaso": ["..MMMMMM..", "...mmmm...", "..mmmmmm..", ".mmMmmmMmm", "mmmmmmmmmm", "mmmMmmmMmm", ".mmmmmmmm.",
             "..MMMMMM.."],
    "pedra": ["...SSSS...", "..SsssSS..", ".SsswsssS.", "SssssssSSS", "SsSsssssSS", ".SSSSSSSS."],
    "placa": ["MMMMMMMMMM", "MwwwwwwwwM", "MwkkwkkwwM", "MwwwwwwwwM", "MMMMMMMMMM", "....MM....", "....MM....",
              "....MM...."],
    "flores": ["..r....y..", ".rwr..yky.", "..r....y..", "..g..g.g..", ".ggg.ggg..", "..g...g..."],
    "escada": ["SSSSSSSSSS", "ssssssssss", "kkkkkkkkkk", "SSSSSSSS..", "ssssssss..", "kkkkkkkk..", "SSSSSS....",
               "ssssss....", "kkkkkk...."],
})


def peca_arte_td(arte, nome, escala=4, tipo="Peça", **extra):
    linhas = ARTES[arte]
    base = dict(w=max(len(l) for l in linhas) * escala, h=len(linhas) * escala, imagem=_arq(arte),
                cor=[255, 255, 255], gravidade=False)
    if tipo == "Peça":
        base.update(contorno=0, solido=False)
    base.update(extra)
    return nova_entidade(tipo, 0, 0, nome, **base)


def flecha_modelo(com_nome=True):
    d = nova_entidade("Peça", 0, 0, "Flecha", w=16, h=10, imagem=_arq(arte_colorida("tiro", "Pedra")), contorno=0,
                      cor=[255, 255, 255], solido=False, gravidade=False,
                      comportamentos=[_comp("Bala", velocidade=380), _comp("Dano", quanto=1, em="Player", empurrar=200,
                                                                          some_ao_acertar="Sim"),
                                      _comp("Destruir fora da tela", margem=200)])
    if com_nome:
        d["_modelo_nome"] = "Flecha"
    return d


def chao_td(material, cor, w, h, nome="Chao"):
    return nova_entidade("Peça", 0, 0, nome, w=w, h=h, material=material, cor=list(cor), solido=False,
                         gravidade=False, contorno=0, camada=-10)


def arbusto():
    return peca_arte_td("arbusto", "Arbusto", 4, solido=True,
                        comportamentos=[_comp("Quebrável (espada)", solta="Moeda", chance=40)])


def vaso():
    return peca_arte_td("vaso", "Vaso", 3, solido=True,
                        comportamentos=[_comp("Quebrável (espada)", solta="Moeda", chance=70)])


def bau_td(qtd=10):
    return peca_arte_td("bau", "Bau", 4, solido=False,
                        script=f'var aberto = falso\n\nquando tocar "Player":\n    se nao aberto:\n'
                               f'        aberto = verdadeiro\n        somar_moedas({qtd})\n'
                               f'        particulas(eu.x + eu.w / 2, eu.y, [255, 220, 60], 40)\n'
                               f'        dizer("+{qtd} moedas!", 1.5)\n')


CHAOS_TD = {"Grama": (90, 170, 90), "Pedra": (120, 120, 130), "Areia": (225, 200, 130), "Madeira": (150, 100, 60),
            "Tijolo": (160, 80, 65), "Gelo": (180, 225, 250), "Tecido": (235, 235, 245), "Metal": (110, 115, 130)}
NOMES_CHAO = {"Tecido": "Neve", "Metal": "Piso de metal", "Madeira": "Piso de madeira", "Tijolo": "Piso de tijolo"}
for _m, _c in CHAOS_TD.items():
    for _tam, _lado_chao in (("médio", 400), ("grande", 1000)):
        _novo("Top-down", f"Chão de {NOMES_CHAO.get(_m, _m)} {_tam}",
              f"Chão para o top-down ({_lado_chao}x{_lado_chao}), fica atrás de tudo e não é sólido.",
              lambda m=_m, c=_c, l=_lado_chao: [(chao_td(m, c, l, l), 0, 0)],
              icone_obj=_icone_obj("Peça", material=_m, cor=list(_c)))
for _m, _c in (("Pedra", (120, 120, 130)), ("Tijolo", (170, 75, 60)), ("Madeira", (150, 100, 60))):
    for _dir, (_w, _h) in (("deitado", (400, 40)), ("em pé", (40, 400))):
        _novo("Top-down", f"Muro de {_m} {_dir}", "Parede sólida para fechar salas e caminhos.",
              lambda m=_m, c=_c, w=_w, h=_h: [(nova_entidade("Bloco", 0, 0, "Muro", w=w, h=h, material=m,
                                                               cor=list(c)), 0, 0)],
              icone_obj=_icone_obj("Bloco", material=_m, cor=list(_c)))
_novo("Top-down", "Água rasa", "Água que deixa o player lento (comportamento Chão lento).",
      lambda: [(nova_entidade("Peça", 0, 0, "AguaRasa", w=240, h=160, material="Vidro", cor=[80, 160, 230],
                              solido=False, contorno=0, camada=-9,
                              comportamentos=[_comp("Chão lento", fator=0.5)]), 0, 0)],
      icone_obj=_icone_obj("Peça", material="Vidro", cor=[80, 160, 230]))
_novo("Top-down", "Lago fundo", "Água funda: não dá para atravessar (é sólida).",
      lambda: [(nova_entidade("Bloco", 0, 0, "Lago", w=260, h=180, material="Vidro", cor=[40, 100, 200]), 0, 0)],
      icone_obj=_icone_obj("Bloco", material="Vidro", cor=[40, 100, 200]))
_novo("Top-down", "Lama", "Lama que deixa o player bem lento.",
      lambda: [(nova_entidade("Peça", 0, 0, "Lama", w=200, h=140, material="Areia", cor=[110, 80, 50], solido=False,
                              contorno=0, camada=-9, comportamentos=[_comp("Chão lento", fator=0.35)]), 0, 0)],
      icone_obj=_icone_obj("Peça", material="Areia", cor=[110, 80, 50]))
_novo("Top-down", "Poça de lava", "Machuca quem pisar.",
      lambda: [(nova_entidade("Lava", 0, 0, "Lava", w=160, h=120, camada=-9), 0, 0)],
      icone_obj=_icone_obj("Lava"), preco=5)
_novo("Top-down", "Arbusto (quebrável)", "Arbusto sólido que quebra com a espada (às vezes solta moeda).",
      lambda: [(arbusto(), 0, 0)], "arbusto")
_novo("Top-down", "Fileira de arbustos", "6 arbustos lado a lado.",
      lambda: [(arbusto(), i * 48, 0) for i in range(6)], "arbusto", preco=5)
_novo("Top-down", "Vaso (quebrável)", "Vaso que quebra com a espada e quase sempre solta moeda.", lambda: [(vaso(), 0, 0)], "vaso")
_novo("Top-down", "Pedra (enfeite)", "Pedra sólida de enfeite.",
      lambda: [(peca_arte_td("pedra", "Pedra", 5, solido=True), 0, 0)], "pedra")
_novo("Top-down", "Árvore (top-down)", "Árvore sólida. Quem passa por trás fica escondido atrás dela.",
      lambda: [(peca_arte_td("arvore", "Arvore", 7, solido=True), 0, 0)], "arvore")
_novo("Top-down", "Flores (enfeite)", "Flores de enfeite (não sólidas).",
      lambda: [(peca_arte_td("flores", "Flores", 4, camada=-5), 0, 0)], "flores")
_novo("Top-down", "Placa", "Placa que fala quando você chega perto (mude o texto em 'fala').",
      lambda: [(nova_entidade("NPC", 0, 0, "Placa", w=40, h=32, imagem=_arq("placa"), gravidade=False,
                              fala="Bem-vindo à vila!"), 0, 0)], "placa")
_novo("Top-down", "Baú de moedas", "Baú que dá 10 moedas na primeira vez que o player encosta.",
      lambda: [(bau_td(10), 0, 0)], "bau", preco=5)
_novo("Top-down", "Escada para a próxima fase", "Escada: encostar leva para a fase 'Fase 2' (mude no comportamento).",
      lambda: [(peca_arte_td("escada", "Escada", 5, comportamentos=[_comp("Porta para fase", fase="Fase 2",
                                                                            tecla="")]), 0, 0)], "escada", preco=5)
_novo("Top-down", "Cerca", "Cerca de madeira sólida (240 de largura).",
      lambda: [(nova_entidade("Bloco", 0, 0, "Cerca", w=240, h=16, material="Madeira", cor=[170, 120, 70]), 0, 0)],
      icone_obj=_icone_obj("Bloco", material="Madeira", cor=[170, 120, 70]))


# =====================================================================
# KITS TOP-DOWN: salas de masmorra, vilas e clareiras
# =====================================================================
def _paredes_sala(x, y, w, h, mat, cor, porta=None):
    """4 paredes; porta = 'cima'/'baixo'/'esquerda'/'direita' deixa um buraco de 100."""
    out = []
    e = 40
    lados = {"cima": (x, y, w, e), "baixo": (x, y + h - e, w, e), "esquerda": (x, y, e, h),
             "direita": (x + w - e, y, e, h)}
    for nome, (px, py, pw, ph) in lados.items():
        if nome == porta:
            if pw > ph:
                meio = px + pw // 2
                out += [(px, py, meio - 50 - px, ph), (meio + 50, py, px + pw - meio - 50, ph)]
            else:
                meio = py + ph // 2
                out += [(px, py, pw, meio - 50 - py), (px, meio + 50, pw, py + ph - meio - 50)]
        else:
            out.append((px, py, pw, ph))
    return [_no(nova_entidade("Bloco", 0, 0, "Parede", w=pw, h=ph, material=mat, cor=list(cor)), px, py)
            for px, py, pw, ph in out]


def kit_masmorra(n):
    rnd = random.Random(n * 131 + 7)
    partes = [_no(chao_td("Pedra", (70, 70, 80), 900, 640), -450, -320)]
    partes += _paredes_sala(-450, -320, 900, 640, "Tijolo", (95, 80, 85), porta=rnd.choice(("direita", "cima")))
    for _ in range(rnd.randint(2, 4)):
        px, py = rnd.randrange(-330, 270, 40), rnd.randrange(-220, 180, 40)
        partes.append(_no(nova_entidade("Bloco", 0, 0, "Pilar", w=60, h=60, material="Pedra", cor=[110, 110, 120]),
                          px, py))
    for _ in range(rnd.randint(3, 6)):
        partes.append(_no(vaso(), rnd.randrange(-400, 380, 30), rnd.choice((-270, 240))))
    inimigos = ["Esqueleto", "Zumbi", "Vampiro", "Robô"]
    for i in range(rnd.randint(2, 4)):
        nome = rnd.choice(inimigos[:2 + n // 4])
        partes.append(_no(inimigo_td(nome, 2 + n // 4, 80 + n * 5), rnd.randrange(-150, 330, 40),
                          rnd.randrange(-220, 200, 40)))
    if n % 3 == 0:
        partes.insert(0, (_flecha(), 0, 0))
        partes.append(_no(inimigo_td("Arqueira", 2, 110, 1, arqueiro=True), 300, -200))
    partes.append(_no(bau_td(5 + n), 340, 200))
    for tx, ty in ((-400, -270), (380, -270)):
        partes.append(_no(preset_objeto("Tocha"), tx, ty))
    player = nova_entidade("Player", 0, 0, "Player")
    player["_campos"] = ("x", "y")
    partes.append(_no(player, -380, 0))
    return partes


def kit_vila(n):
    rnd = random.Random(n * 977 + 3)
    partes = [_no(chao_td("Grama", (90, 170, 90), 1400, 1000), -700, -500)]
    for i in range(3):
        hx, hy = -560 + i * 420 + rnd.randint(-30, 30), -380 + rnd.randint(0, 60)
        partes.append(_no(nova_entidade("Bloco", 0, 0, "Casa", w=200, h=150, material="Madeira",
                                        cor=list(rnd.choice(((160, 110, 70), (190, 150, 100), (140, 90, 60))))),
                          hx, hy))
        partes.append(_no(nova_entidade("Peça", 0, 0, "Telhado", w=230, h=50, material="Tijolo",
                                        cor=[170, 70, 55], solido=False, camada=5, contorno=0), hx - 15, hy - 30))
    partes.append(_no(nova_entidade("Bloco", 0, 0, "Lago", w=260, h=160, material="Vidro", cor=[40, 100, 200]),
                      150, 180))
    nomes = [s[0] for s in PERSONAGENS]
    for i in range(3):
        nome = nomes[(n * 3 + i) % len(nomes)]
        npc = _item_npc(nome)[0][0]
        npc["comportamentos"] = [_comp("Vagar (anda à toa)", velocidade=40)]
        partes.append(_no(npc, -500 + i * 330, -150))
    for _ in range(8):
        partes.append(_no(arbusto(), rnd.randrange(-650, 600, 48), rnd.choice((380, 420, -460))))
    for _ in range(5):
        partes.append(_no(peca_arte_td("flores", "Flores", 4, camada=-5), rnd.randrange(-600, 600, 40),
                          rnd.randrange(0, 350, 40)))
    partes.append(_no(bau_td(10), 560, 300))
    player = nova_entidade("Player", 0, 0, "Player")
    player["_campos"] = ("x", "y")
    partes.append(_no(player, -40, 100))
    return partes


def kit_clareira(n):
    rnd = random.Random(n * 313 + 11)
    partes = [_no(chao_td("Grama", (80, 155, 80), 1200, 900), -600, -450)]
    for i in range(16):
        ang = i / 16 * math.tau
        partes.append(_no(peca_arte_td("arvore", "Arvore", 7, solido=True),
                          int(math.cos(ang) * 520) - 42, int(math.sin(ang) * 380) - 42))
    for _ in range(10):
        partes.append(_no(arbusto(), rnd.randrange(-380, 340, 48), rnd.randrange(-250, 230, 48)))
    for i in range(3 + n):
        slime = peca_arte_td(arte_colorida("slime_1", rnd.choice(ELEMENTOS)), "Slime", 3, tipo="Inimigo",
                             velocidade=0, distancia=0, pode_ser_pisado=False, grupo="Inimigos")
        slime["comportamentos"] = [_comp("Vida", vida=1, dano_de="TirosDoPlayer"),
                                   _comp("Vagar (anda à toa)", velocidade=60),
                                   _comp("Perseguir", alvo="Player", velocidade=80, alcance=200)]
        partes.append(_no(slime, rnd.randrange(-300, 300, 40), rnd.randrange(-200, 200, 40)))
    player = nova_entidade("Player", 0, 0, "Player")
    player["_campos"] = ("x", "y")
    partes.append(_no(player, 0, 0))
    return partes


_CENA_TD = {"visao_de_cima": True, "olhar_a_frente": 0}
for _n in range(1, 11):
    _novo("Kits de fase", f"Sala de masmorra {_n}",
          "Sala fechada de pedra com pilares, vasos, esqueletos/zumbis, baú e tochas. Já liga o modo top-down.",
          lambda n=_n: kit_masmorra(n), "escada", plano="Dev",
          cena=dict(_CENA_TD, fundo=[20, 18, 24], escuridao=90))
for _n in range(1, 6):
    _novo("Kits de fase", f"Vila top-down {_n}",
          "Vila com casas, lago, 3 NPCs que andam e conversam, arbustos, flores e baú. Já liga o modo top-down.",
          lambda n=_n: kit_vila(n), "arvore", plano="Game Maker", cena=dict(_CENA_TD, fundo=[60, 120, 60]))
    _novo("Kits de fase", f"Clareira com slimes {_n}",
          "Clareira cercada de árvores com arbustos e slimes. Já liga o modo top-down.",
          lambda n=_n: kit_clareira(n), "slime_1", preco=30, cena=dict(_CENA_TD, fundo=[40, 90, 45]))

if "Top-down" not in CATEGORIAS_LOJA:
    CATEGORIAS_LOJA.insert(1, "Top-down")
if "Top-down" not in CATEGORIAS_VENDA:
    CATEGORIAS_VENDA.insert(len(CATEGORIAS_VENDA) - 1, "Top-down")


# =====================================================================
# EXEMPLO: RPG TOP-DOWN (vila + masmorra)
# =====================================================================
def _hud_td():
    return [nova_entidade("Texto", 16, 12, "TextoMoedas", texto="Moedas: {moedas()}", tamanho_fonte=22,
                          negrito=True, cor=[255, 230, 90]),
            nova_entidade("Texto", 16, 44, "TextoVida", texto="Vida", tamanho_fonte=16),
            nova_entidade("Barra", 60, 48, "BarraVida", valor_de="player.vida", maximo=6, w=200, h=16,
                          cor=[230, 70, 80])]


def _colocar(d, x, y):
    d["x"], d["y"] = int(x), int(y)
    return d


def exemplo_rpg_topdown():
    global _COLETAR
    _COLETAR = set()
    try:
        # ---------------- Fase 1: a vila ----------------
        c1 = cena_padrao()
        c1.update({"visao_de_cima": True, "fundo": [60, 120, 60], "olhar_a_frente": 0, "titulo": "RPG top-down",
                   "limitar_camera": False})
        f1 = [_colocar(chao_td("Grama", (90, 170, 90), 1800, 1300), -100, -100)]
        for i, (x, y, w, h) in enumerate([(-100, -100, 1800, 40), (-100, 1160, 1800, 40), (-100, -100, 40, 1300),
                                          (1660, -100, 40, 1300)]):
            f1.append(nova_entidade("Bloco", x, y, f"Cerca{i + 1}", w=w, h=h, material="Madeira",
                                    cor=[150, 105, 65]))
        for i, (x, y) in enumerate([(80, 60), (420, 40), (1200, 60)]):
            f1.append(nova_entidade("Bloco", x, y, f"Casa{i + 1}", w=210, h=150, material="Madeira",
                                    cor=[170, 120, 75]))
            f1.append(nova_entidade("Peça", x - 15, y - 30, f"Telhado{i + 1}", w=240, h=50, material="Tijolo",
                                    cor=[170, 70, 55], solido=False, camada=5, contorno=0))
        f1.append(nova_entidade("Bloco", 760, 560, "Lago", w=300, h=180, material="Vidro", cor=[40, 100, 200]))
        f1.append(nova_entidade("Peça", 720, 520, "AguaRasa", w=380, h=260, material="Vidro", cor=[90, 170, 235],
                                solido=False, contorno=0, camada=-9, comportamentos=[_comp("Chão lento", fator=0.5)]))
        velho = personagem_td("Mago", tipo="NPC",
                              fala="Olá, jovem herói!|Use as SETAS ou WASD para andar.|ESPAÇO (ou J) dá um golpe de "
                                   "espada.|Quebre os arbustos e vasos: às vezes tem moeda.|A masmorra fica na escada "
                                   "lá no canto. Cuidado com os esqueletos!")
        f1.append(_colocar(velho, 330, 260))
        velho["nome"] = "VelhoMago"
        faz = personagem_td("Fazendeiro", tipo="NPC", fala="Os slimes estão comendo minhas plantas! Me ajuda?",
                            comportamentos=[_comp("Vagar (anda à toa)", velocidade=35)])
        f1.append(_colocar(faz, 1000, 300))
        princ = personagem_td("Princesa", tipo="NPC",
                              fala="O tesouro do rei está no fundo da masmorra.|Traga ele e você ganha o jogo!")
        f1.append(_colocar(princ, 1300, 260))
        rnd = random.Random(42)
        for i in range(14):
            f1.append(_colocar(arbusto(), 60 + (i % 7) * 48, 820 + (i // 7) * 48))
        for i in range(6):
            f1.append(_colocar(vaso(), 680 + i * 40, 230))
        for i in range(8):
            f1.append(_colocar(peca_arte_td("flores", "Flores", 4, camada=-5), rnd.randrange(100, 1500, 40),
                               rnd.randrange(420, 1050, 40)))
        for i, (x, y) in enumerate([(1300, 520), (1400, 900), (500, 1000)]):
            slime = peca_arte_td(arte_colorida("slime_1", "Veneno"), f"Slime{i + 1}", 3, tipo="Inimigo",
                                 velocidade=0, distancia=0, pode_ser_pisado=False, grupo="Inimigos")
            slime["comportamentos"] = [_comp("Vida", vida=2, dano_de="TirosDoPlayer"),
                                       _comp("Vagar (anda à toa)", velocidade=60),
                                       _comp("Perseguir", alvo="Player", velocidade=85, alcance=220)]
            f1.append(_colocar(slime, x, y))
        f1.append(_colocar(bau_td(10), 1500, 1050))
        f1.append(nova_entidade("NPC", 1450, 140, "Placa", w=40, h=32, imagem=_arq("placa"), gravidade=False,
                                fala="Masmorra ↓  (encoste na escada)"))
        f1.append(_colocar(peca_arte_td("escada", "Escada", 6,
                                        comportamentos=[_comp("Porta para fase", fase="Masmorra", tecla="")]),
                           1540, 180))
        heroi = personagem_td("Aventureiro", velocidade=240, espada=True, gravidade=False)
        heroi["nome"] = "Player"
        heroi["comportamentos"] = [_comp("Vida", vida=6, dano_de="Inimigo", invencivel_seg=1)]
        f1.append(_colocar(heroi, 300, 360))
        f1 += _hud_td()

        # ---------------- Fase 2: a masmorra ----------------
        c2 = cena_padrao()
        c2.update({"visao_de_cima": True, "fundo": [18, 16, 22], "olhar_a_frente": 0, "titulo": "Masmorra",
                   "escuridao": 120})
        f2 = [_colocar(chao_td("Pedra", (70, 70, 80), 1600, 1000), 0, 0)]
        for i, (x, y, w, h) in enumerate([(0, 0, 1600, 40), (0, 960, 1600, 40), (0, 0, 40, 1000),
                                          (1560, 0, 40, 1000), (500, 40, 40, 600), (1000, 360, 40, 600)]):
            f2.append(nova_entidade("Bloco", x, y, f"Parede{i + 1}", w=w, h=h, material="Tijolo",
                                    cor=[95, 80, 85]))
        for i, (x, y) in enumerate([(80, 60), (460, 60), (560, 900), (1060, 60), (1520, 60), (80, 900)]):
            f2.append(_colocar(preset_objeto("Tocha"), x, y))
        for i in range(10):
            f2.append(_colocar(vaso(), 600 + (i % 5) * 40, 80 + (i // 5) * 40))
        for i, (x, y) in enumerate([(300, 300), (300, 700), (700, 500), (800, 800)]):
            esq = inimigo_td("Esqueleto", 2, 90)
            esq["nome"] = f"Esqueleto{i + 1}"
            f2.append(_colocar(esq, x, y))
        for i, (x, y) in enumerate([(1200, 200), (1300, 800)]):
            arq = inimigo_td("Arqueira", 2, 110, 1, arqueiro=True)
            arq["nome"] = f"Arqueiro{i + 1}"
            f2.append(_colocar(arq, x, y))
        rei = inimigo_td("Esqueleto", 12, 70, 2)
        rei["nome"] = "ReiEsqueleto"
        rei["w"], rei["h"] = rei["w"] * 2, rei["h"] * 2
        rei["eventos"] = [_ev("Quando o player chegar perto",
                              [("Mostrar título na tela", {"texto": "O REI ESQUELETO!", "seg": 2}),
                               ("Tremer câmera", {"forca": 8, "seg": 0.6})], distancia=350),
                          _ev("Ao ser destruído", [("Mostrar título na tela", {"texto": "O TESOURO É SEU!",
                                                                              "seg": 2.5}),
                                                   ("Somar moedas", {"n": 50}), ("Vencer o jogo", {})])]
        f2.append(_colocar(rei, 1300, 470))
        f2.append(_colocar(bau_td(25), 1450, 880))
        heroi2 = copy.deepcopy(heroi)
        heroi2["comportamentos"] = [_comp("Vida", vida=6, dano_de="Inimigo", invencivel_seg=1),
                                    _comp("Luz", raio=200)]
        f2.append(_colocar(heroi2, 120, 480))
        f2 += _hud_td()
        proj = {"fases": {"Vila": {"cena": c1, "objetos": f1}, "Masmorra": {"cena": c2, "objetos": f2}},
                "fase_atual": "Vila", "fase_inicial": "Vila", "modelos": {}}
        proj["modelos"]["Flecha"] = flecha_modelo(False)
        proj["_artes"] = sorted(_COLETAR)
        return proj
    finally:
        _COLETAR = None


EXEMPLOS["Exemplo: RPG top-down (vila e masmorra)"] = exemplo_rpg_topdown
