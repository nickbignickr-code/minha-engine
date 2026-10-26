# Minha Engine - loja_catalogo.py
# +700 itens da Loja gerados: 100 grátis, 300 por Brasas, 100 do Game Maker e 200 do Dev
# e a interface "Você prefere" (escolha de poder com botões e textos)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# PALETAS (cada uma vira 2 letras novas nas pixel arts: claro e escuro)
# =====================================================================
PALETAS = {
    "Fogo": ((255, 120, 40), (190, 50, 20)), "Gelo": ((170, 230, 255), (80, 150, 220)),
    "Veneno": ((150, 230, 60), (70, 140, 30)), "Sombra": ((120, 95, 150), (50, 38, 75)),
    "Elétrico": ((255, 240, 90), (215, 165, 20)), "Pedra": ((160, 160, 170), (95, 95, 110)),
    "Água": ((70, 170, 255), (30, 90, 190)), "Ouro": ((255, 215, 80), (185, 135, 30)),
    "Cristal": ((230, 140, 255), (150, 70, 210)), "Lava": ((255, 85, 30), (140, 22, 10)),
    "Rubi": ((240, 50, 80), (150, 20, 45)), "Safira": ((60, 110, 255), (25, 50, 160)),
    "Esmeralda": ((40, 220, 120), (15, 130, 70)), "Ametista": ((180, 90, 240), (100, 40, 160)),
    "Topázio": ((255, 190, 60), (200, 120, 20)), "Diamante": ((225, 250, 255), (140, 200, 230)),
    "Ônix": ((75, 75, 88), (28, 28, 34)), "Quartzo": ((255, 170, 210), (210, 100, 150)),
}
ELEMENTOS = ["Fogo", "Gelo", "Veneno", "Sombra", "Elétrico", "Pedra", "Água", "Ouro", "Cristal", "Lava"]
GEMAS = ["Rubi", "Safira", "Esmeralda", "Ametista", "Topázio", "Diamante", "Ônix", "Quartzo"]
_LETRAS_PALETA = {}
_CHAR_DA_COR = {}


def cor_char(rgb):
    """Uma 'letra' (caractere unicode) para a cor: assim as pixel arts podem ter quantas cores quiser."""
    rgb = tuple(int(c) for c in rgb[:3])
    ch = _CHAR_DA_COR.get(rgb)
    if ch is None:
        ch = chr(0x0100 + len(_CHAR_DA_COR))
        _CHAR_DA_COR[rgb] = ch
        CORES_ARTE[ch] = rgb
    return ch


def _letras(paleta):
    """As duas letras (claro, escuro) de uma paleta, criando as cores na primeira vez."""
    if paleta not in _LETRAS_PALETA:
        _LETRAS_PALETA[paleta] = (cor_char(PALETAS[paleta][0]), cor_char(PALETAS[paleta][1]))
    return _LETRAS_PALETA[paleta]


import unicodedata


def _slug(txt):
    txt = unicodedata.normalize("NFKD", str(txt)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", txt.lower()).strip("_")


# Desenhos novos: "1" = cor clara da paleta, "2" = cor escura (o resto igual às outras artes)
MOLDES = {
    "gema": ["...1111...", "..1w1112..", ".1w111122.", "1111111222", ".11111222.", "..11122...", "...112....",
             "....2....."],
    "morcego": ["1............1", "11....11....11", "111..1111..111", "1111w1k1kw1111", ".211111111112.",
                "...21111112...", ".....2..2....."],
    "fantasma": ["...1111...", "..111111..", ".11111111.", ".1kw11kw1.", ".1kk11kk1.", "1111111111", "1111111111",
                 "1111221111", "1111111111", "11.1111.11", "1...11...1"],
    "aranha": ["....2222....", "...212212...", "2..2r22r2..2", ".2.222222.2.", "..22222222..", ".2.222222.2.",
               "2...2..2...2"],
    "robo": ["....kk....", "....1.....", "..222222..", "..2c22c2..", "..222222..", "..2kkkk2..", "...2222...",
             ".21111112.", ".21w11112.", ".21111112.", "..2....2..", ".22....22."],
    "bomba": ["......y.o.", ".....k....", "....kk....", "..111111..", ".1w111112.", ".1w111112.", ".11111112.",
              ".11111122.", "..112222..", "....22...."],
    "tartaruga": ["....2222......", "...212212.....", "..21122112.nn.", ".2111111112nkn", ".22222222222nn",
                  "..nn....nn...."],
    "espinhudo": [".w...w...w..", ".12..12..12.", "111111111111", "1kw1111kw111", "1kk1111kk111", "111111111111",
                  "111122221111", ".1111111111.", "..2......2.."],
    "cubo": ["2222222222", "2111111112", "21kk11kk12", "21wk11wk12", "2111111112", "211kkkk112", "21k1111k12",
             "2111111112", "2222222222"],
    "atirador": ["...1111.....", "..111111....", ".11w1111....", ".11k111kkkkk", ".1111112kkkk", ".1111111....",
                 "..111111....", "..2....2....", ".22....22..."],
    "torre": ["....kk....", "...kkkk...", "..k1111kkk", "..k1ww1kkk", "..k1111k..", "...1111...", "..222222..",
              ".22222222.", ".21111112.", ".21111112.", "2222222222"],
    "chefe": ["....y.y.y.y.....", "....yyyyyyy.....", "..111111111111..", ".11111111111111.", "1111kk1111kk1111",
              "111kwk1111kwk111", "1111111111111111", "1112222222222111", "11w2w2w2w2w2w211", "1112222222222111",
              "1111111111111111", ".11111111111111.", "..22........22..", ".222........222."],
    "gato": ["1.......1.", "11.....11.", "111111111.", "1kw111kw1.", "1111l1111.", "111111111.", ".1111111..2",
             ".1111111.2.", ".1.1..1.1.."],
    "passaro": ["...111....", "..11k1....", ".111111yy.", "2111111...", "22111111..", ".2211111..", "...1..1...",
                "...y..y..."],
    "cachorro": ["..2.....2..", ".212...212.", ".2111111112", ".11k1111k11", ".1111kk1111", ".11111111..",
                 "..1111111.2", "..1111111.2", "..1.1..1.1."],
    "fadinha": ["w......w", "ww.11.ww", "ww1111ww", ".11w111.", ".111111.", "..1111..", "...22..."],
    "dragao": ["..2.2.......", ".11111......", "1k1111......", "111111.2...2", "..111112222.", "..11111112..",
               "..111111111.", "..1111111.11", "..1.1..1...1"],
    "tiro": ["..1111..", ".1wwww1.", "1ww11ww1", ".1wwww1.", "..1111.."],
    "frasco": ["....ss....", "....MM....", "....ww....", "...w11w...", "..w1111w..", ".w1w1111w.", ".w111112w.",
               ".w211112w.", "..w2222w..", "...wwww..."],
}
# Que letras das artes antigas viram a cor clara/escura ao recolorir
TROCAS_ARTE = {"coracao": "rR", "estrela": "yY", "moeda": "yY", "espada": "sS", "bau": "mM", "arvore": "gG",
               "chave": "y.", "pocao": "pP", "cogumelo": "rR", "nuvem": "wc", "slime_1": "gG", "slime_2": "gG",
               "heroi_1": "bB", "heroi_2": "bB"}


def arte_colorida(base, paleta):
    """Cria (uma vez) a pixel art 'base' pintada com a paleta e devolve o nome dela em ARTES."""
    nome = f"{base}_{_slug(paleta)}"
    if nome in ARTES:
        return nome
    claro, escuro = _letras(paleta)
    if base in MOLDES:
        tabela = str.maketrans({"1": claro, "2": escuro})
        linhas = MOLDES[base]
    else:
        de = TROCAS_ARTE.get(base, "")
        tabela = str.maketrans({de[0]: claro} if len(de) < 2 or de[1] == "." else {de[0]: claro, de[1]: escuro})
        linhas = ARTES[base]
    ARTES[nome] = [l.translate(tabela) for l in linhas]
    return nome


# =====================================================================
# AJUDANTES
# =====================================================================
def _peca_arte(nome_arte, nome_obj, escala=3, tipo="Peça", **extra):
    arq = garantir_arte(nome_arte)
    linhas = ARTES[nome_arte]
    w, h = max(len(l) for l in linhas) * escala, len(linhas) * escala
    base = dict(w=w, h=h, imagem=arq, cor=[255, 255, 255])
    if tipo == "Peça":
        base.update(contorno=0, solido=False)
    base.update(extra)
    return nova_entidade(tipo, 0, 0, nome_obj, **base)


def _modelo_tiro(nome, paleta, em="Player", vel=500, dano=1):
    """Um MODELO de tiro (vai para a lista de modelos do projeto, não para a cena)."""
    arte = arte_colorida("tiro", paleta)
    d = nova_entidade("Peça", 0, 0, nome, w=16, h=10, imagem=garantir_arte(arte), contorno=0, cor=[255, 255, 255],
                      solido=False, gravidade=False,
                      comportamentos=[_comp("Bala", velocidade=vel), _comp("Dano", quanto=dano, em=em, empurrar=200,
                                                                          some_ao_acertar="Sim"),
                                      _comp("Destruir fora da tela", margem=200)])
    d["_modelo_nome"] = nome
    return d


def _ev(gatilho, acoes, **gp):
    e = {"gatilho": gatilho, "gp": params_padrao(GATILHOS[gatilho]), "condicoes": [], "acoes": []}
    e["gp"].update({k: str(v) for k, v in gp.items()})
    for t, p in acoes:
        a = params_padrao(ACOES[t])
        a.update({k: str(v) for k, v in p.items()})
        e["acoes"].append({"t": t, "p": a})
    return e


def _no(d, x, y):
    """Coloca d com o canto de cima-esquerda em (x, y) (a loja usa o centro)."""
    return (d, x + num_seguro(d["w"], 40) / 2, y + num_seguro(d["h"], 40) / 2)


def _icone_obj(tipo, **p):
    return nova_entidade(tipo, 0, 0, tipo, **p)


def _novo(cat, nome, desc, fn, icone=None, preco=0, plano=None, icone_obj=None, cena=None):
    assert not any(i["nome"] == nome for i in LOJA), nome
    _item(cat, nome, desc, fn, icone, preco=preco, plano=plano)
    if icone_obj is not None:
        LOJA[-1]["icone_obj"] = icone_obj
    if cena:
        CENA_DOS_ITENS[nome] = cena


# =====================================================================
# ELEMENTOS: o que cada um muda num inimigo / chefe / player
# =====================================================================
INFO_ELEMENTO = {
    "Fogo": {"vel": 1.0, "vida": 0, "dano": 1, "particulas": "fogo", "luz": 110, "desc": "solta fogo e brilha"},
    "Gelo": {"vel": 0.7, "vida": 1, "dano": 1, "material": "Gelo", "desc": "lento, mas aguenta mais"},
    "Veneno": {"vel": 1.0, "vida": 0, "dano": 2, "desc": "tira 2 de vida"},
    "Sombra": {"vel": 1.25, "vida": 0, "dano": 1, "opacidade": 150, "desc": "quase invisível e rápido"},
    "Elétrico": {"vel": 1.5, "vida": 0, "dano": 1, "material": "Neon", "luz": 90, "desc": "muito rápido e brilha"},
    "Pedra": {"vel": 0.6, "vida": 3, "dano": 1, "desc": "lentíssimo e muito resistente"},
    "Água": {"vel": 1.0, "vida": 1, "dano": 1, "pulsar": True, "desc": "pulsa como uma bolha"},
    "Ouro": {"vel": 1.0, "vida": 1, "dano": 1, "moedas": 3, "desc": "solta 3 moedas ao morrer"},
    "Cristal": {"vel": 1.0, "vida": 2, "dano": 1, "luz": 120, "pulsar": True, "desc": "brilha e é resistente"},
    "Lava": {"vel": 0.9, "vida": 1, "dano": 2, "particulas": "fogo", "luz": 140, "desc": "queima: tira 2 de vida"},
}


def _aplicar_elemento(d, elem, base_vida=1):
    info = INFO_ELEMENTO[elem]
    comps = d.setdefault("comportamentos", [])
    vida = base_vida + info["vida"]
    if vida > 1 or base_vida > 0:
        comps.append(_comp("Vida", vida=vida, dano_de="TirosDoPlayer", invencivel_seg=0.3, barra="Sim"))
    d["dano"] = info["dano"]
    if info.get("material"):
        d["material"] = info["material"]
    if info.get("opacidade"):
        d["opacidade"] = info["opacidade"]
    if info.get("luz"):
        comps.append(_comp("Luz", raio=info["luz"]))
    if info.get("particulas"):
        r, g, b = PALETAS[elem][0]
        comps.append(_comp("Emissor de partículas", estilo=info["particulas"], por_seg=12, r=r, g=g, b=b))
    if info.get("pulsar"):
        comps.append(_comp("Pulsar", escala=0.08, vezes_por_seg=1))
    if info.get("moedas"):
        d.setdefault("eventos", []).append(_ev("Ao ser destruído", [("Criar objeto", {"tipo": "Moeda", "dx": -20,
                                                                                      "dy": -30}),
                                                                    ("Criar objeto", {"tipo": "Moeda", "dx": 0,
                                                                                      "dy": -50}),
                                                                    ("Criar objeto", {"tipo": "Moeda", "dx": 20,
                                                                                      "dy": -30})]))
    return d


# =====================================================================
# GRÁTIS (100): 40 imagens coloridas, 36 blocos, 24 gemas
# =====================================================================
NOMES_ARTES = {"coracao": "Coração", "estrela": "Estrela", "moeda": "Moeda", "espada": "Espada", "bau": "Baú",
               "arvore": "Árvore", "chave": "Chave", "pocao": "Poção", "cogumelo": "Cogumelo", "nuvem": "Nuvem"}
for _a, _rot in NOMES_ARTES.items():
    for _pal in ("Rubi", "Safira", "Esmeralda", "Ametista"):
        _nome_arte = arte_colorida(_a, _pal)
        _novo("Imagens", f"{_rot} {_pal}", f"Pixel art pronta ({_rot.lower()} na cor {_pal.lower()}). Vira uma Peça.",
              lambda n=_nome_arte, r=_rot: [(_peca_arte(n, r.replace(" ", ""), 4), 0, 0)], _nome_arte)

CORES_MATERIAIS = {"Plástico": [163, 162, 165], "Madeira": [150, 100, 60], "Tijolo": [170, 75, 60],
                   "Pedra": [130, 130, 140], "Metal": [150, 160, 175], "Grama": [90, 200, 120],
                   "Areia": [225, 200, 130], "Gelo": [170, 225, 250], "Neon": [80, 255, 220],
                   "Vidro": [180, 220, 255], "Borracha": [230, 90, 160], "Tecido": [190, 80, 80]}
for _mat, _cor in CORES_MATERIAIS.items():
    for _tam, _w in (("pequeno", 80), ("médio", 160), ("grande", 320)):
        _novo("Plataformas", f"Bloco de {_mat} {_tam}",
              f"Bloco sólido de {_mat.lower()} ({_w}x40). " + DESC_MATERIAIS.get(_mat, "").capitalize(),
              lambda m=_mat, c=_cor, w=_w: [(nova_entidade("Bloco", 0, 0, "Bloco" + _slug(m).capitalize(), w=w, h=40,
                                                           material=m, cor=list(c)), 0, 0)],
              icone_obj=_icone_obj("Bloco", material=_mat, cor=list(_cor), w=_w, h=40))

for _g in GEMAS:
    _arte_g = arte_colorida("gema", _g)
    for _vale, _esc in ((1, 2), (5, 3), (10, 4)):
        _novo("Coletáveis", f"Gema {_g} (vale {_vale})", f"Gema que dá {_vale} moeda(s) e flutua.",
              lambda a=_arte_g, v=_vale, e=_esc, g=_g: [(
                  _peca_arte(a, "Gema" + _slug(g).capitalize(), e, tipo="Moeda", valor=v,
                             comportamentos=[_comp("Senoide (vai e volta)", eixo="y", distancia=6,
                                                   vezes_por_seg=0.8)]), 0, 0)], _arte_g)

# =====================================================================
# BRASAS (300): 100 inimigos, 60 plataformas, 60 poderes, 40 efeitos, 40 scripts
# =====================================================================
BASES_INIMIGOS = {
    # nome: (arte, preço base, descrição, função que monta o objeto)
    "Slime": ("slime_1", 15, "pula de um lado para o outro"),
    "Morcego": ("morcego", 18, "voa subindo e descendo"),
    "Perseguidor": ("cubo", 20, "corre atrás do player"),
    "Atirador": ("atirador", 30, "atira no player de longe"),
    "Fantasma": ("fantasma", 25, "voa atravessando tudo e te segue"),
    "Aranha": ("aranha", 20, "anda e pula de surpresa"),
    "Robô": ("robo", 28, "patrulha e atira para frente"),
    "Bomba": ("bomba", 22, "te persegue e explode"),
    "Tartaruga": ("tartaruga", 15, "lenta, não morre se pisar"),
    "Espinhudo": ("espinhudo", 18, "cheio de espinhos: não dá para pisar"),
}


def _montar_inimigo(base, elem):
    arte, _p, _d = BASES_INIMIGOS[base]
    info = INFO_ELEMENTO[elem]
    k = info["vel"]
    nome = _slug(base).capitalize() + _slug(elem).capitalize()
    partes = []
    if base == "Slime":
        a1, a2 = arte_colorida("slime_1", elem), arte_colorida("slime_2", elem)
        d = _peca_arte(a1, nome, 4, tipo="Inimigo", velocidade=int(70 * k), distancia=140)
        _anim(d, (a1, a2), 4)
    else:
        d = _peca_arte(arte_colorida(arte, elem), nome, 3, tipo="Inimigo", velocidade=int(100 * k), distancia=160)
    c = d.setdefault("comportamentos", [])
    if base == "Morcego":
        d.update(gravidade=False)
        c.append(_comp("Senoide (vai e volta)", eixo="y", distancia=50, vezes_por_seg=0.7))
    elif base == "Perseguidor":
        d["velocidade"] = 0
        c.append(_comp("Perseguir", alvo="Player", velocidade=int(140 * k), alcance=420))
    elif base == "Atirador":
        d["velocidade"] = 0
        tiro = f"TiroInimigo{_slug(elem).capitalize()}"
        partes.append((_modelo_tiro(tiro, elem, "Player", 420, info["dano"]), 0, 0))
        c += [_comp("Olhar para", alvo="Player"),
              _comp("Atirar", tipo=tiro, a_cada_seg=round(1.8 / k, 2), velocidade=420, alvo="Player", alcance=520)]
    elif base == "Fantasma":
        d.update(gravidade=False, opacidade=170)
        c.append(_comp("Perseguir", alvo="Player", velocidade=int(80 * k), alcance=500))
    elif base == "Aranha":
        c.append(_comp("Pular sozinho", a_cada_seg=2.2, forca=600))
    elif base == "Robô":
        tiro = f"TiroRobo{_slug(elem).capitalize()}"
        partes.append((_modelo_tiro(tiro, elem, "Player", 500, info["dano"]), 0, 0))
        c += [_comp("Patrulhar", velocidade=int(90 * k), distancia=200),
              _comp("Atirar", tipo=tiro, a_cada_seg=2, velocidade=500, alvo="", alcance=0)]
    elif base == "Bomba":
        d["velocidade"] = 0
        c += [_comp("Perseguir", alvo="Player", velocidade=int(110 * k), alcance=300),
              _comp("Explodir ao morrer", raio=110, dano=info["dano"], em="Player")]
        d.setdefault("eventos", []).append(_ev("Ao tocar em", [("Destruir", {})], alvo="Player"))
    elif base == "Tartaruga":
        d.update(velocidade=int(50 * k), pode_ser_pisado=False)
    elif base == "Espinhudo":
        d["pode_ser_pisado"] = False
    _aplicar_elemento(d, elem, 2 if base in ("Robô", "Tartaruga") else 1)
    return partes + [(d, 0, 0)]


for _base, (_arte, _preco, _desc) in BASES_INIMIGOS.items():
    for _i, _el in enumerate(ELEMENTOS):
        _ic = arte_colorida(_arte, _el)
        _novo("Inimigos", f"{_base} de {_el}", f"Inimigo que {_desc}. {_el}: {INFO_ELEMENTO[_el]['desc']}.",
              lambda b=_base, e=_el: _montar_inimigo(b, e), _ic, preco=_preco + (_i % 4) * 5)

TIPOS_PLATAFORMA = {
    "normal": ("Plataforma", 5, "Plataforma sólida para pular em cima."),
    "que cai": ("Plataforma que cai", 10, "Cai pouco depois que o player pisa (e volta depois)."),
    "móvel": ("Plataforma móvel", 10, "Vai e volta de um lado para o outro."),
    "quebrável": ("Bloco quebrável", 8, "Quebra quando o player bate a cabeça e solta uma moeda."),
    "rampa": ("Rampa", 6, "Rampa para subir andando."),
}


def _montar_plataforma(tipo, mat):
    cor = list(CORES_MATERIAIS[mat])
    nome = "Plat" + _slug(mat).capitalize()
    if tipo == "móvel":
        return [(nova_entidade("Plataforma Movel", 0, 0, nome, w=140, h=24, material=mat, cor=cor, vel_x=110,
                               vel_y=0, distancia=220), 0, 0)]
    if tipo == "rampa":
        return [(nova_entidade("Peça", 0, 0, "Rampa" + _slug(mat).capitalize(), w=160, h=80, material=mat, cor=cor,
                               forma="Rampa ◢", solido=True), 0, 0)]
    d = nova_entidade("Bloco", 0, 0, nome, w=40 if tipo == "quebrável" else 160, h=40 if tipo == "quebrável" else 28,
                      material=mat, cor=cor)
    if tipo == "que cai":
        d["comportamentos"] = [_comp("Plataforma que cai", espera=0.5), _comp("Reaparecer", seg=3)]
    elif tipo == "quebrável":
        d["comportamentos"] = [_comp("Quebrar ao bater por baixo", solta="Moeda")]
    return [(d, 0, 0)]


for _tipo, (_rot, _preco, _desc) in TIPOS_PLATAFORMA.items():
    for _mat in CORES_MATERIAIS:
        _novo("Plataformas", f"{_rot} de {_mat}", _desc + f" Material: {_mat.lower()}.",
              lambda t=_tipo, m=_mat: _montar_plataforma(t, m), preco=_preco,
              icone_obj=_icone_obj("Plataforma Movel" if _tipo == "móvel" else ("Peça" if _tipo == "rampa"
                                                                                    else "Bloco"),
                                   material=_mat, cor=list(CORES_MATERIAIS[_mat]),
                                   forma="Rampa ◢" if _tipo == "rampa" else "Retângulo"))

PODERES = {
    "velocidade": ("Velocidade", "Topázio", [1.25, 1.5, 2, 3], "corre"),
    "pulo": ("Super pulo", "Esmeralda", [1.2, 1.4, 1.7, 2], "pula"),
    "gravidade_escala": ("Flutuar", "Diamante", [0.8, 0.6, 0.4, 0.25], "cai devagar"),
    "aceleracao": ("Arranque", "Rubi", [1.5, 2, 3, 4], "acelera"),
    "vel_tiro": ("Tiro veloz", "Safira", [1.5, 2, 2.5, 3], "atira mais rápido"),
}
for _prop, (_rot, _pal, _mults, _verbo) in PODERES.items():
    _arte_p = arte_colorida("frasco", _pal)
    for _j, _mult in enumerate(_mults):
        for _seg in (5, 10, 20):
            _txt = f"x{_mult}".replace(".", ",")
            _novo("Poderes", f"Poção {_rot} {_txt} ({_seg}s)",
                  f"Ao pegar, o player {_verbo} {_txt} por {_seg} segundos e depois volta ao normal.",
                  lambda p=_prop, m=_mult, s=_seg, a=_arte_p, r=_rot: [(
                      _peca_arte(a, "Pocao" + _slug(r).capitalize().replace("_", ""), 3,
                                 comportamentos=[_comp("Power-up ao tocar", propriedade=p, multiplicar=m, seg=s,
                                                       em="Player"),
                                                 _comp("Senoide (vai e volta)", eixo="y", distancia=6,
                                                       vezes_por_seg=0.8)]), 0, 0)],
                  _arte_p, preco=5 + _j * 5 + (0 if _seg == 5 else 3 if _seg == 10 else 6))

CORES_EFEITO = {"Vermelho": (255, 70, 60), "Laranja": (255, 150, 40), "Amarelo": (255, 230, 80),
                "Verde": (90, 240, 110), "Azul": (80, 150, 255), "Roxo": (180, 100, 255), "Rosa": (255, 120, 200),
                "Branco": (245, 245, 255)}
ESTILOS_EFEITO = {"fogo": ("Chamas", 40), "fumaca": ("Fumaça", 12), "brilho": ("Brilhos", 18),
                  "chuva": ("Chuva", 70), "neve": ("Neve", 25)}
for _est, (_rot, _qtd) in ESTILOS_EFEITO.items():
    for _cn, _c in CORES_EFEITO.items():
        _novo("Efeitos", f"{_rot} {_cn.lower()}", f"Emissor de partículas ({_rot.lower()}) na cor {_cn.lower()}.",
              lambda e=_est, c=_c, q=_qtd, r=_rot: [(nova_entidade(
                  "Zona", 0, 0, _slug(r).capitalize(), w=40, h=40, cor=list(c),
                  comportamentos=[_comp("Emissor de partículas", estilo=e, por_seg=q, r=c[0], g=c[1], b=c[2])]
                  + ([_comp("Luz", raio=140)] if e == "fogo" else [])), 0, 0)],
              preco=5 if _est in ("chuva", "neve") else 8, icone_obj=_icone_obj("Zona", cor=list(_c)))

SCRIPTS_LOJA_2 = {
    "Pulo triplo": 'var pulos = 0\n\nquando pousar:\n    pulos = 0\n\nquando tecla "espaco":\n'
                   '    se nao eu.no_chao e pulos < 2:\n        pulos += 1\n        eu.vy = -650\n',
    "Correr com Shift": 'quando frame:\n    se tecla("shift"):\n        eu.velocidade = 520\n    senao:\n'
                        '        eu.velocidade = 320\n',
    "Andar sozinho e virar": 'var lado = 1\n\nquando frame:\n    eu.vx = 120 * lado\n\nquando parede:\n'
                             '    lado = -lado\n',
    "Seguir o player devagar": 'quando frame:\n    se player.x > eu.x:\n        eu.vx = 90\n    senao:\n'
                               '        eu.vx = -90\n',
    "Fugir do player": 'quando frame:\n    se distancia(eu, player) < 200:\n        se player.x > eu.x:\n'
                       '            eu.vx = -200\n        senao:\n            eu.vx = 200\n',
    "Teleporte com T": 'quando tecla "t":\n    particulas(eu.x, eu.y, [150, 100, 255], 25)\n    eu.x = mouse_x()\n'
                       '    eu.y = mouse_y()\n',
    "Atirar no mouse com clique": 'quando clique_tela:\n    var tiro = lancar("Moeda", 0, 0)\n'
                                  '    mirar(tiro, achar("Player"), 0)\n',
    "Tiro triplo com G": 'quando tecla "g":\n    lancar("Moeda", 600, -150)\n    lancar("Moeda", 600, 0)\n'
                         '    lancar("Moeda", 600, 150)\n',
    "Chuva de moedas": 'quando cada 0.5:\n    criar("Moeda", eu.x + aleatorio(-300, 300), eu.y - 400)\n',
    "Gerar inimigos": 'var criados = 0\n\nquando cada 3:\n    se criados < 5:\n        criados += 1\n'
                      '        criar("Inimigo", eu.x, eu.y - 40)\n',
    "Placar de pontos": 'global.pontos = 0\n\nquando frame:\n    hud("pontos", "Pontos: " + global.pontos, 12, 12)\n',
    "Cronômetro na tela": 'var t = 0\n\nquando cada 1:\n    t += 1\n    hud("tempo", "Tempo: " + t + "s", 12, 40)\n',
    "Contagem regressiva": 'var falta = 60\n\nquando cada 1:\n    falta -= 1\n'
                           '    hud("falta", "Faltam " + falta + "s", 12, 70)\n    se falta <= 0:\n        perder()\n',
    "Vencer com 10 moedas": 'quando frame:\n    se moedas() >= 10:\n        vencer()\n',
    "Mostrar vida na tela": 'quando frame:\n    hud("vida", "Vida: " + player.vida, 12, 100)\n',
    "Piscar ao levar dano": 'quando dano:\n    piscar(eu, 1)\n    tremer(6, 0.2)\n',
    "Hit stop ao bater": 'quando tocar "Inimigo":\n    congelar(0.06)\n    tremer(8, 0.2)\n',
    "Texto ao pegar moeda": 'quando moeda:\n    texto_flutuante("+1", eu.x, eu.y - 20, [255, 230, 80])\n',
    "Combo de moedas": 'var combo = 0\nvar tempo_combo = 0\n\nquando moeda:\n    combo += 1\n'
                       '    tempo_combo = 1.5\n    se combo >= 3:\n'
                       '        texto_flutuante("COMBO x" + combo, eu.x, eu.y - 40, [255, 120, 80])\n\n'
                       'quando cada 0.5:\n    tempo_combo -= 0.5\n    se tempo_combo <= 0:\n        combo = 0\n',
    "Escuridão com lanterna": 'quando iniciar:\n    escuridao(210)\n',
    "Dia e noite": 'var noite = falso\n\nquando cada 20:\n    noite = nao noite\n    se noite:\n'
                   '        escuridao(180)\n    senao:\n        escuridao(0)\n',
    "Fundo que muda de cor": 'quando cada 2:\n    fundo(aleatorio(10, 60), aleatorio(10, 60), aleatorio(30, 90))\n',
    "Zoom ao começar": 'quando iniciar:\n    zoom(2, 0)\n    zoom(1, 1.5)\n',
    "Câmera no chefe": 'quando perto 300:\n    camera(eu)\n    tremer(5, 0.5)\n\nquando longe 500:\n'
                       '    camera(achar("Player"))\n',
    "Falar ao chegar perto": 'quando perto 150:\n    dizer("Cuidado lá na frente!", 2)\n',
    "Diálogo com E": 'quando tecla "e":\n    se distancia(eu, player) < 120 e nao dialogo_aberto():\n'
                     '        dialogo("Olá!|Pegue a chave e abra a porta.|Boa sorte!", eu.nome)\n',
    "Loja do NPC": 'quando tecla "e":\n    se distancia(eu, player) < 120:\n        se moedas() >= 5:\n'
                   '            somar_moedas(-5)\n            curar(player, 1)\n            dizer("Toma uma vida!", 2)\n'
                   '        senao:\n            dizer("Precisa de 5 moedas", 2)\n',
    "Baú que dá moedas": 'var aberto = falso\n\nquando tocar "Player":\n    se nao aberto:\n        aberto = verdadeiro\n'
                         '        somar_moedas(10)\n        particulas(eu.x, eu.y, [255, 220, 60], 40)\n'
                         '        dizer("+10 moedas!", 1.5)\n',
    "Interruptor abre porta": 'quando tocar "Player":\n    destruir(achar("Porta"))\n    dizer("Clique!", 1)\n',
    "Plataforma que some": 'quando tocar "Player":\n    depois(0.6, sumir)\n\nfuncao sumir():\n'
                           '    eu.visivel = falso\n    eu.solido = falso\n    depois(3, voltar)\n\n'
                           'funcao voltar():\n    eu.visivel = verdadeiro\n    eu.solido = verdadeiro\n',
    "Mola (pula alto)": 'quando tocar "Player":\n    player.vy = -1200\n    esticar(eu)\n',
    "Esteira": 'quando tocar "Player":\n    player.x += 4\n',
    "Vento para cima": 'quando tocar "Player":\n    player.vy = player.vy - 60\n',
    "Água (nadar)": 'quando tocar "Player":\n    player.vy = player.vy * 0.85\n    se tecla("espaco"):\n'
                    '        player.vy = -250\n',
    "Checkpoint com aviso": 'var ativo = falso\n\nquando tocar "Player":\n    se nao ativo:\n        ativo = verdadeiro\n'
                            '        salvar_jogo()\n        texto_flutuante("Salvo!", eu.x, eu.y - 30, [120, 255, 140])\n',
    "Reiniciar com R": 'quando tecla "r":\n    reiniciar()\n',
    "Pausar com Esc no texto": 'quando tecla "p":\n    hud("pausa", "PAUSADO", 560, 300)\n    pausar()\n',
    "Inimigo que dá dano e quica": 'quando tocar "Player":\n    dano(player, 1)\n    player.vy = -450\n'
                                   '    tremer(6, 0.2)\n',
    "Girar sem parar": 'quando frame:\n    eu.rotacao += 3\n',
    "Flutuar (sobe e desce)": 'var base = 0\n\nquando iniciar:\n    base = eu.y\n\nquando frame:\n'
                              '    eu.y = base + seno(tempo * 120) * 12\n',
}
assert len(SCRIPTS_LOJA_2) == 40, len(SCRIPTS_LOJA_2)
SCRIPTS_LOJA.update(SCRIPTS_LOJA_2)
for _i, _s in enumerate(SCRIPTS_LOJA_2):
    _novo("Scripts", _s, "Script em Brasa: cola no objeto selecionado (aba Script).", ("script", _s),
          preco=5 + (_i % 3) * 5)


# =====================================================================
# "VOCÊ PREFERE": painel com 3 botões de poder
# =====================================================================
def _no_player(prop, op, valor):
    return ("Mudar propriedade de outro objeto", {"objeto": "Player", "prop": prop, "op": op, "valor": valor})


OPCOES_PODER = {
    "Dois pulos": ("+1 pulo no ar", [_no_player("pulos_extras", "+=", 1)]),
    "Mais vida": ("+2 de vida máxima", [_no_player("vida_max", "+=", 2), _no_player("vida", "+=", 2)]),
    "Mais dano": ("+1 de dano", [_no_player("dano", "+=", 1)]),
    "Mais velocidade": ("+25% de velocidade", [_no_player("velocidade", "*=", 1.25)]),
    "Pulo alto": ("+20% de pulo", [_no_player("pulo", "*=", 1.2)]),
    "Dash": ("Shift dá um impulso", [_no_player("dash", "=", "verdadeiro")]),
    "Pulo na parede": ("Pula nas paredes", [_no_player("pulo_parede", "=", "verdadeiro")]),
    "Tiro": ("Aperte F para atirar", [_no_player("tiro", "=", '"TiroDoPoder"')]),
    "Tiro rápido": ("Tiros 50% mais rápidos", [_no_player("vel_tiro", "*=", 1.5)]),
    "Flutuar": ("Gravidade 30% menor", [_no_player("gravidade_escala", "=", 0.7)]),
    "Moedas": ("+20 moedas agora", [("Somar moedas", {"n": 20})]),
    "Vida cheia": ("Cura toda a vida", [("Curar objeto", {"objeto": "Player", "qtd": 99})]),
}


def _voce_prefere(titulo, opcoes, cor=(70, 140, 255), grupo="EscolhaDePoder", fundo=(24, 26, 40)):
    """Painel + título + 3 botões. Cada botão dá um poder ao Player, fecha a janela e devolve os controles."""
    partes = []
    painel = nova_entidade("Painel", 0, 0, "PainelEscolha", w=640, h=360, cor=list(fundo), opacidade=235,
                           arredondado=16, grupo=grupo,
                           eventos=[_ev("Ao iniciar", [("Controles do player", {"ativo": "Não"})])])
    partes.append((painel, 320, 150))
    partes.append((nova_entidade("Texto", 0, 0, "TituloEscolha", texto=titulo, w=600, h=50, tamanho_fonte=36,
                                 negrito=True, alinhamento="Centro", grupo=grupo), 340, 175))
    partes.append((nova_entidade("Texto", 0, 0, "SubtituloEscolha", texto="Escolha um poder (clique no botão):",
                                 w=600, h=30, tamanho_fonte=20, alinhamento="Centro", cor=[200, 205, 220],
                                 grupo=grupo), 340, 232))
    precisa_vida = precisa_tiro = False
    for i, (nome_op, num_op) in enumerate(zip(opcoes, ("1", "2", "3"))):
        desc, acoes = OPCOES_PODER[nome_op]
        precisa_vida |= nome_op in ("Mais vida", "Vida cheia")
        precisa_tiro |= nome_op in ("Tiro", "Tiro rápido")
        acoes = list(acoes) + [("Apagar botões do grupo", {"grupo": grupo}),
                               ("Controles do player", {"ativo": "Sim"}),
                               ("Mostrar título na tela", {"texto": nome_op.upper() + "!", "seg": 1.5})]
        x = 345 + i * 200
        b = nova_entidade("Botao", 0, 0, f"Opcao{num_op}", texto=f"{num_op}  {nome_op}", w=190, h=90,
                          tamanho_fonte=22, cor=list(cor), arredondado=12, grupo=grupo,
                          eventos=[_ev("Ao clicar no objeto", acoes)])
        partes.append((b, x, 290))
        partes.append((nova_entidade("Texto", 0, 0, f"DescOpcao{num_op}", texto=desc, w=190, h=26, tamanho_fonte=16,
                                     alinhamento="Centro", cor=[210, 215, 230], grupo=grupo), x, 392))
    if precisa_vida:      # o Player precisa do comportamento Vida para ter vida
        p = nova_entidade("Player", 0, 0, "Player")
        p["_campos"] = ()
        p["_garantir_comportamentos"] = [_comp("Vida", vida=3, dano_de="Inimigo")]
        partes.append((p, 0, 0))
    if precisa_tiro:
        partes.append((_modelo_tiro("TiroDoPoder", "Safira", "Inimigo", 650, 1), 0, 0))
    return partes


_novo("Interface", "Você prefere (escolha de poder)",
      "Janela com título e 3 BOTÕES: 1 Dois pulos, 2 Mais vida, 3 Mais dano. O jogo para até o jogador escolher. "
      "Tudo feito com eventos: abra cada botão para ver e mudar.",
      lambda: _voce_prefere("VOCÊ PREFERE?", ("Dois pulos", "Mais vida", "Mais dano")), "estrela", preco=50,
      icone_obj=None)

# =====================================================================
# GAME MAKER (100): 50 chefões, 30 torres, 20 interfaces
# =====================================================================
POSTOS_CHEFE = [("Guardião", 1.0, 8, 0), ("Chefão", 1.25, 14, 1), ("Rei", 1.5, 20, 1), ("Titã", 1.9, 30, 2),
                ("Lorde Supremo", 2.3, 45, 3)]


def _montar_chefe(elem, posto):
    nome_p, tam, vida, extra = next(p for p in POSTOS_CHEFE if p[0] == posto)
    info = INFO_ELEMENTO[elem]
    e = _slug(elem).capitalize()
    tiro = f"TiroChefe{e}"
    d = _peca_arte(arte_colorida("chefe", elem), "Chefe" + e, int(4 * tam), tipo="Inimigo", velocidade=0,
                   pode_ser_pisado=False, dano=info["dano"] + extra // 2)
    d["comportamentos"] = [_comp("Vida", vida=vida + info["vida"] * 2, dano_de="TirosDoPlayer", invencivel_seg=0.4,
                                 barra="Sim"),
                           _comp("Perseguir", alvo="Player", velocidade=int((60 + 15 * extra) * info["vel"]),
                                 alcance=650),
                           _comp("Atirar", tipo=tiro, a_cada_seg=round(max(0.5, 2.0 - extra * 0.4), 2),
                                 velocidade=400 + 60 * extra, alvo="Player", alcance=700),
                           _comp("Explodir ao morrer", raio=160, dano=2, em="Inimigo")]
    if extra >= 2:
        d["comportamentos"].append(_comp("Pular sozinho", a_cada_seg=3, forca=750))
    if info.get("luz"):
        d["comportamentos"].append(_comp("Luz", raio=int(info["luz"] * 1.6)))
    d["eventos"] = [_ev("Quando o player chegar perto",
                        [("Mostrar título na tela", {"texto": f"{nome_p.upper()} DE {elem.upper()}", "seg": 2}),
                         ("Tremer câmera", {"forca": 6 + extra * 3, "seg": 0.6})], distancia=420),
                    _ev("Ao ser destruído", [("Mostrar título na tela", {"texto": "VITÓRIA!", "seg": 2}),
                                             ("Somar moedas", {"n": vida})])]
    return [(_modelo_tiro(tiro, elem, "Player", 400 + 60 * extra, info["dano"]), 0, 0), (d, 0, -40)]


for _el in ELEMENTOS:
    for _posto in POSTOS_CHEFE:
        _novo("Chefões", f"{_posto[0]} de {_el}",
              f"Chefe com {_posto[2]}+ de vida e barra, persegue, atira e explode ao morrer. "
              f"Anuncia o nome quando o player chega perto. {_el}: {INFO_ELEMENTO[_el]['desc']}.",
              lambda e=_el, p=_posto[0]: _montar_chefe(e, p), arte_colorida("chefe", _el), plano="Game Maker")

RITMOS_TORRE = [("lenta", 2.2, 350), ("normal", 1.2, 450), ("rápida", 0.45, 600)]
for _el in ELEMENTOS:
    for _rit, _seg, _vel in RITMOS_TORRE:
        def _montar_torre(e=_el, s=_seg, v=_vel, r=_rit):
            tiro = f"TiroTorre{_slug(e).capitalize()}"
            d = _peca_arte(arte_colorida("torre", e), "Torre" + _slug(e).capitalize(), 4, solido=True)
            d["comportamentos"] = [_comp("Olhar para", alvo="Player"),
                                   _comp("Atirar", tipo=tiro, a_cada_seg=s, velocidade=v, alvo="Player", alcance=650),
                                   _comp("Vida", vida=4, dano_de="TirosDoPlayer", invencivel_seg=0.2, barra="Sim")]
            return [(_modelo_tiro(tiro, e, "Player", v, INFO_ELEMENTO[e]["dano"]), 0, 0), (d, 0, 0)]
        _novo("Torres", f"Torre de {_el} ({_rit})",
              f"Torre parada que mira e atira no player (cadência {_rit}). Morre com 4 tiros do player.",
              _montar_torre, arte_colorida("torre", _el), plano="Game Maker")

VARIANTES_PREFERE = [
    ("Movimento", ("Mais velocidade", "Pulo alto", "Dash"), (60, 170, 120)),
    ("Ataque", ("Mais dano", "Tiro", "Mais velocidade"), (210, 70, 60)),
    ("Defesa", ("Mais vida", "Vida cheia", "Flutuar"), (70, 120, 220)),
    ("Ninja", ("Dash", "Pulo na parede", "Dois pulos"), (90, 90, 110)),
    ("Tesouro", ("Moedas", "Mais vida", "Mais dano"), (200, 160, 40)),
    ("Céu", ("Flutuar", "Dois pulos", "Pulo alto"), (110, 180, 240)),
    ("Guerreiro", ("Mais dano", "Mais vida", "Dash"), (170, 60, 90)),
    ("Atirador", ("Tiro", "Tiro rápido", "Mais velocidade"), (60, 110, 200)),
    ("Aventura", ("Pulo na parede", "Moedas", "Tiro"), (120, 90, 200)),
    ("Sobrevivência", ("Vida cheia", "Mais vida", "Mais velocidade"), (60, 150, 90)),
]
for _tema, _ops, _cor in VARIANTES_PREFERE:
    _novo("Interface", f"Você prefere: {_tema}", "Escolha de poder com 3 botões: " + ", ".join(_ops) + ".",
          lambda t=_tema, o=_ops, c=_cor: _voce_prefere(f"VOCÊ PREFERE? ({t.upper()})", o, c,
                                                        fundo=tuple(max(10, x // 5) for x in c)),
          "estrela", plano="Game Maker")

TEMAS_HUD = [("Clássico", (80, 220, 100), (30, 30, 40)), ("Fogo", (255, 110, 40), (50, 20, 15)),
             ("Gelo", (140, 220, 255), (20, 35, 55)), ("Floresta", (90, 200, 90), (20, 40, 25)),
             ("Neon", (80, 255, 220), (15, 15, 30)), ("Ouro", (255, 210, 70), (45, 35, 15)),
             ("Sombra", (170, 120, 230), (20, 15, 30)), ("Oceano", (60, 150, 255), (10, 25, 50)),
             ("Doce", (255, 140, 200), (55, 25, 45)), ("Retrô", (240, 240, 240), (0, 0, 0))]
for _tema, _cor, _fundo in TEMAS_HUD:
    def _montar_hud(cor=_cor, fundo=_fundo, tema=_tema):
        return [(nova_entidade("Painel", 0, 0, "PainelHud", w=300, h=110, cor=list(fundo), opacidade=200,
                               arredondado=12), 10, 10),
                (nova_entidade("Texto", 0, 0, "HudMoedas", texto="Moedas: {moedas()}", cor=list(cor),
                               tamanho_fonte=22, negrito=True), 24, 20),
                (nova_entidade("Texto", 0, 0, "HudVidaTexto", texto="Vida", cor=[230, 230, 240], tamanho_fonte=16),
                 24, 54),
                (nova_entidade("Barra", 0, 0, "HudVida", valor_de="player.vida", maximo=3, cor=list(cor), w=220,
                               h=16), 74, 58),
                (nova_entidade("Texto", 0, 0, "HudTempo", texto="Tempo: {global.tempo}", cor=[200, 200, 210],
                               tamanho_fonte=16, comportamentos=[_comp("Cronômetro", variavel="tempo")]), 24, 82)]
    _novo("Interface", f"HUD {_tema}",
          f"Painel no canto com moedas, barra de vida e cronômetro, no tema {_tema.lower()}.", _montar_hud, plano="Game Maker",
          icone_obj=_icone_obj("Barra", cor=list(_cor)))

# =====================================================================
# DEV (200): 100 kits de fase, 50 mascotes, 50 upgrades do Player
# =====================================================================
TEMAS_KIT = [
    # nome, material chão, cor chão, material plataforma, cor plat, fundo, elemento dos inimigos, escuridão, perigo
    ("Floresta", "Grama", [90, 200, 120], "Madeira", [150, 100, 60], [120, 190, 230], "Veneno", 0, "Espinho"),
    ("Deserto", "Areia", [225, 200, 130], "Pedra", [190, 160, 110], [250, 210, 150], "Fogo", 0, "Espinho"),
    ("Gelo", "Gelo", [170, 225, 250], "Gelo", [200, 235, 255], [190, 220, 245], "Gelo", 0, "Espinho"),
    ("Caverna", "Pedra", [90, 90, 100], "Pedra", [120, 115, 125], [20, 18, 26], "Cristal", 160, "Espinho"),
    ("Vulcão", "Pedra", [70, 50, 50], "Metal", [110, 90, 90], [60, 20, 15], "Lava", 60, "Lava"),
    ("Castelo", "Tijolo", [150, 140, 150], "Tijolo", [170, 75, 60], [40, 40, 60], "Sombra", 90, "Espinho"),
    ("Cidade Neon", "Metal", [60, 60, 80], "Neon", [80, 255, 220], [15, 10, 35], "Elétrico", 120, "Lava"),
    ("Céu", "Tecido", [245, 245, 255], "Vidro", [180, 220, 255], [150, 200, 255], "Água", 0, "Espinho"),
    ("Pântano", "Grama", [70, 120, 60], "Madeira", [100, 80, 50], [60, 80, 60], "Veneno", 40, "Lava"),
    ("Mina de Ouro", "Pedra", [110, 95, 70], "Madeira", [150, 100, 60], [30, 25, 20], "Ouro", 140, "Espinho"),
]


def _montar_kit(tema, semente):
    nome_t, mat_c, cor_c, mat_p, cor_p, _fundo, elem, escuro, perigo = tema
    rnd = random.Random(semente * 7919 + len(nome_t))
    partes = []
    x = -640
    chao_y = 80
    buracos = 0
    while x < 640:
        w = rnd.choice((160, 200, 240, 320))
        w = min(w, 680 - x)
        partes.append(_no(nova_entidade("Bloco", 0, 0, "Chao", w=w, h=60, material=mat_c, cor=list(cor_c)), x,
                          chao_y))
        x += w
        if x < 560 and buracos < 3 and rnd.random() < 0.55:
            vao = rnd.choice((80, 100, 120))
            partes.append(_no(nova_entidade(perigo, 0, 0, perigo, w=vao, h=20 if perigo == "Espinho" else 30), x,
                              chao_y + 40))
            x += vao
            buracos += 1
    # plataformas, moedas e inimigos
    xs = sorted(rnd.sample(range(-520, 520, 70), 5))
    for i, px in enumerate(xs):
        py = chao_y - rnd.choice((90, 130, 170, 210))
        tipo = rnd.choice(("Bloco", "Bloco", "Plataforma Movel"))
        if tipo == "Bloco":
            p = nova_entidade("Bloco", 0, 0, "Plataforma", w=120, h=24, material=mat_p, cor=list(cor_p))
            if rnd.random() < 0.25:
                p["comportamentos"] = [_comp("Plataforma que cai", espera=0.6), _comp("Reaparecer", seg=3)]
        else:
            p = nova_entidade("Plataforma Movel", 0, 0, "PlatMovel", w=110, h=20, material=mat_p, cor=list(cor_p),
                              vel_x=rnd.choice((0, 80)), vel_y=0, distancia=120)
            if not p["vel_x"]:
                p["vel_y"] = 70
        partes.append(_no(p, px, py))
        for m in range(rnd.randint(1, 3)):
            partes.append(_no(nova_entidade("Moeda", 0, 0, "Moeda"), px + 15 + m * 30, py - 34))
    for i in range(rnd.randint(2, 4)):
        base = rnd.choice(("Slime", "Perseguidor", "Aranha", "Tartaruga", "Morcego"))
        ini = [d for d, _a, _b in _montar_inimigo(base, elem) if d["tipo"] == "Inimigo"][0]
        partes.append(_no(ini, rnd.randint(-380, 520), chao_y - num_seguro(ini["h"], 32) - (60 if base == "Morcego"
                                                                                          else 0)))
    partes.append(_no(nova_entidade("Checkpoint", 0, 0, "Checkpoint"), -20, chao_y - 60))
    partes.append(_no(nova_entidade("Bandeira", 0, 0, "Bandeira"), 600, chao_y - 80))
    player = nova_entidade("Player", 0, 0, "Player")
    player["_campos"] = ("x", "y")
    partes.append(_no(player, -600, chao_y - 50))
    if escuro:
        for tx in (-500, 0, 480):
            tocha = preset_objeto("Tocha")
            partes.append(_no(tocha, tx, chao_y - 40))
    return partes


for _tema in TEMAS_KIT:
    for _n in range(1, 11):
        _novo("Kits de fase", f"Fase {_tema[0]} {_n}",
              f"Fase inteira pronta ({_tema[0].lower()}): chão com buracos, plataformas, moedas, inimigos de "
              f"{_tema[6].lower()}, checkpoint e bandeira. O Player vai para o começo. Layout nº {_n}.",
              lambda t=_tema, n=_n: _montar_kit(t, n), plano="Dev",
              icone_obj=_icone_obj("Bloco", material=_tema[1], cor=list(_tema[2])),
              cena={"fundo": list(_tema[5]), "escuridao": _tema[7]})

ESPECIES_PET = {
    "Gatinho": ("gato", "segue você e puxa as moedas para perto"),
    "Passarinho": ("passaro", "voa do seu lado"),
    "Cãozinho": ("cachorro", "segue você e morde os inimigos"),
    "Fadinha": ("fadinha", "voa com você, brilha e ilumina o caminho"),
    "Dragãozinho": ("dragao", "segue você e cospe fogo nos inimigos"),
}


def _montar_pet(especie, elem):
    arte, _d = ESPECIES_PET[especie]
    nome = _slug(especie).capitalize() + _slug(elem).capitalize()
    d = _peca_arte(arte_colorida(arte, elem), nome, 3, gravidade=False)
    c = [_comp("Mascote (segue de perto)", alvo="Player", distancia=55, suavidade=5)]
    partes = []
    if especie == "Gatinho":
        c.append(_comp("Ímã", tipo="Moeda", raio=180, forca=450))
    elif especie == "Passarinho":
        c.append(_comp("Senoide (vai e volta)", eixo="y", distancia=10, vezes_por_seg=1.5))
    elif especie == "Cãozinho":
        c.append(_comp("Dano", quanto=1, em="Inimigo", empurrar=300, some_ao_acertar="Não"))
    elif especie == "Fadinha":
        r, g, b = PALETAS[elem][0]
        c += [_comp("Luz", raio=170), _comp("Emissor de partículas", estilo="brilho", por_seg=8, r=r, g=g, b=b)]
    elif especie == "Dragãozinho":
        tiro = f"FogoDoPet{_slug(elem).capitalize()}"
        partes.append((_modelo_tiro(tiro, elem, "Inimigo", 520, 1), 0, 0))
        c.append(_comp("Atirar", tipo=tiro, a_cada_seg=1.2, velocidade=520, alvo="Inimigo", alcance=380))
    d["comportamentos"] = c
    return partes + [(d, -60, 0)]


for _esp in ESPECIES_PET:
    for _el in ELEMENTOS:
        _novo("Pets", f"{_esp} de {_el}", f"Mascote que {ESPECIES_PET[_esp][1]}.",
              lambda s=_esp, e=_el: _montar_pet(s, e), arte_colorida(ESPECIES_PET[_esp][0], _el), plano="Dev")

CLASSES_PLAYER = {
    "Ninja": ("rápido, dash no Shift, pulo na parede e pulo duplo",
              {"velocidade": 420, "dash": True, "pulo_parede": True, "pulos_extras": 1}),
    "Atirador": ("atira com F e tem tiro veloz", {"vel_tiro": 800}),
    "Tanque": ("8 de vida e 2 de dano, mas é mais lento", {"velocidade": 250, "dano": 2}),
    "Saltador": ("pulo enorme, 2 pulos no ar e cai devagar", {"pulo": 980, "pulos_extras": 2,
                                                             "gravidade_escala": 0.8}),
    "Velocista": ("muito rápido, arranque forte e dash", {"velocidade": 560, "aceleracao": 5200, "dash": True}),
}


def _montar_upgrade(classe, elem):
    _desc, props = CLASSES_PLAYER[classe]
    info = INFO_ELEMENTO[elem]
    a1, a2 = arte_colorida("heroi_1", elem), arte_colorida("heroi_2", elem)
    p = nova_entidade("Player", 0, 0, "Player", w=40, h=44)
    p.update(props)
    p["imagem"] = garantir_arte(a1)
    p["anim_andando"] = ", ".join(garantir_arte(a) for a in (a1, a2))
    p["fps_anim"] = 8
    p["dano"] = p.get("dano", 1) + (1 if info["dano"] > 1 else 0)
    partes = []
    trocar = [_comp("Vida", vida=8 if classe == "Tanque" else 3 + info["vida"], dano_de="Inimigo")]
    if classe == "Atirador":
        tiro = f"TiroPlayer{_slug(elem).capitalize()}"
        p["tiro"] = tiro
        partes.append((_modelo_tiro(tiro, elem, "Inimigo", 800, p["dano"]), 0, 0))
    if info.get("luz"):
        trocar.append(_comp("Luz", raio=info["luz"] + 60))
    p["_trocar_comportamentos"] = trocar
    p["_campos"] = tuple(props) + ("imagem", "anim_andando", "fps_anim", "dano", "w", "h") + (
        ("tiro",) if classe == "Atirador" else ())
    return partes + [(p, 0, 0)]


for _cl in CLASSES_PLAYER:
    for _el in ELEMENTOS:
        _novo("Upgrades do Player", f"Player {_cl} de {_el}",
              f"Transforma o seu Player: {CLASSES_PLAYER[_cl][0]}. Visual de {_el.lower()} animado. "
              f"Não apaga os eventos nem o script dele.",
              lambda c=_cl, e=_el: _montar_upgrade(c, e), arte_colorida("heroi_1", _el), plano="Dev")

# categorias novas na loja (antes de Exclusivos)
for _c in ("Chefões", "Torres", "Plataformas", "Coletáveis", "Poderes", "Kits de fase", "Pets",
           "Upgrades do Player"):
    if _c not in CATEGORIAS_LOJA:
        CATEGORIAS_LOJA.insert(CATEGORIAS_LOJA.index("Exclusivos"), _c)
for _c in ("Grátis", "Game Maker", "Dev"):
    if _c not in CATEGORIAS_LOJA:
        CATEGORIAS_LOJA.insert(CATEGORIAS_LOJA.index("Comunidade"), _c)
for _c in ("Plataformas", "Coletáveis", "Poderes", "Chefões", "Pets"):
    if _c not in CATEGORIAS_VENDA:
        CATEGORIAS_VENDA.insert(len(CATEGORIAS_VENDA) - 1, _c)
