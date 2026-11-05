# Minha Engine - loja.py
# aba Loja (Creator Store) e pixel arts prontas
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# IMAGENS PRONTAS (pixel art gerada) + CREATOR STORE (aba "Loja")
# =====================================================================
def peca_com_imagem(nome):
    """Uma Peca com a imagem escolhida (tamanho tirado da propria imagem)."""
    img = carregar_imagem(nome)
    w = h = 64
    if img is not None and img.get_width() > 0 and img.get_height() > 0:
        iw, ih = img.get_width(), img.get_height()
        k = 4 if max(iw, ih) <= 32 else (2 if max(iw, ih) <= 64 else 1)
        w, h = iw * k, ih * k
        if max(w, h) > 128:
            f = 128 / max(w, h)
            w, h = max(8, int(w * f)), max(8, int(h * f))
    base = re.sub(r"[^\w]", "_", os.path.splitext(os.path.basename(str(nome)))[0]) or "Imagem"
    return nova_entidade("Peça", 0, 0, base[:1].upper() + base[1:], w=w, h=h, imagem=str(nome), contorno=0,
                         cor=[255, 255, 255], solido=False)


# Cada desenho: linhas de texto, cada letra vira uma cor ("." = transparente)
CORES_ARTE = {"k": (20, 20, 28), "w": (255, 255, 255), "r": (230, 40, 60), "R": (150, 20, 40), "o": (255, 150, 30),
              "y": (255, 220, 50), "Y": (200, 150, 20), "g": (60, 200, 80), "G": (30, 120, 50), "b": (60, 140, 255),
              "B": (30, 60, 160), "c": (120, 230, 255), "p": (170, 90, 230), "P": (100, 40, 150), "m": (150, 95, 50),
              "M": (95, 55, 30), "s": (190, 195, 205), "S": (110, 115, 130), "n": (255, 205, 160), "l": (255, 140, 180)}
ARTES = {
    "coracao": ["..........", ".rr....rr.", "rwrr..rrrr", "rwrrrrrrrr", "rrrrrrrrrR", ".rrrrrrrR.", "..rrrrrR..",
                "...rrrR...", "....rR....", ".........."],
    "estrela": ["......y......", ".....yy......", ".....yyy.....", "....yywyy....", "yyyyyywyyyyyY", ".yyyyyyyyyyY.",
                "..yyyyyyyyY..", "...yyyyyyY...", "...yyyYyyY...", "..yyyY.YyyY..", "..yyY...YyY..", ".yY.......YY."],
    "moeda": ["...YYYY...", "..YyyyyY..", ".YyywyyyY.", ".Yywyyy.Y.", ".YywyyyyY.", ".YyyyyyyY.", ".YyyyyyyY.",
              "..YyyyyY..", "...YYYY..."],
    "espada": ["..........ss", ".........sws", "........sws.", ".......sws..", "......sws...", ".....sws....",
               "..m.sws.....", "..mmws......", "...mm.......", "..M.mm......", ".M....m.....", "M..........."],
    "bau": ["..MMMMMMMM..", ".MmmmmmmmmM.", "MmmmmmmmmmmM", "MMMMMyyMMMMM", "MmmmmykmmmmM", "MmmmmyymmmmM",
            "MmmmmmmmmmmM", "MmmmmmmmmmmM", "MMMMMMMMMMMM"],
    "arvore": ["....gggg....", "..gggggggg..", ".ggGgggggGg.", "gggggGgggggg", "gGgggggggGgg", "gggggggGgggg",
               ".gggGgggggg.", "..ggggggGg..", ".....mM.....", ".....mM.....", ".....mM.....", "....mmMM...."],
    "chave": ["..yyy.......", ".y...y......", ".y...yyyyyyy", ".y...y..y.y.", "..yyy...y.y."],
    "pocao": ["....ss....", "....MM....", "....ww....", "...wppw...", "..wpppPw..", ".wpwppppw.", ".wpppppPw.",
              ".wPppppPw.", "..wPPPPw..", "...wwww..."],
    "cogumelo": ["...rrrrr...", ".rrwwrrrrr.", "rrrwwrrrwwr", "rrrrrrrrwwr", "rwwrrrrrrrr", ".rrrrrrrrr.",
                 "...nnnnn...", "...nknkn...", "...nnnnn...", "....nnn...."],
    "nuvem": ["....wwww......", "..wwwwwwww.ww.", ".wwwwwwwwwwwww", "wwwwwwwwwwwwww", "wwwwwwwwwwwwwc",
              ".wwccwwwwcccc.", "...cccccccc..."],
    "slime_1": ["............", "....gggg....", "..gggggggg..", ".gggwggwggg.", ".ggkwggkwgg.", "gggggggggggg",
                "gggggggggggG", ".GGGGGGGGGG."],
    "slime_2": ["............", "............", "............", "...gggggg...", ".ggwgggwggg.", "gggkwggkwggg",
                "gggggggggggG", "GGGGGGGGGGGG"],
    "heroi_1": ["...BBBB...", "..BBBBBB..", "..nnnnnn..", "..nknnkn..", "..nnnnnn..", "...bbbb...", "..bbbbbb..",
                ".n.bbbb.n.", "...bbbb...", "...B..B...", "..BB..BB.."],
    "heroi_2": ["...BBBB...", "..BBBBBB..", "..nnnnnn..", "..nknnkn..", "..nnnnnn..", "...bbbb...", "..bbbbbb..",
                "..nbbbbn..", "...bbbb...", "..B....B..", ".BB....BB."],
    "fogo_1": ["....o.....", "...oo..o..", "..oyo.oo..", "..oyyooo..", ".ooywyyoo.", ".oyywwyyo.", ".ryyyyyyr.",
               "..rryyrr.."],
    "fogo_2": [".....o....", "..o..oo...", "..oo.oyo..", "..oooyyo..", ".ooyywyoo.", ".oyywwyyo.", ".ryyyyyyr.",
               "..rryyrr.."],
}


def superficie_arte(linhas):
    h = len(linhas)
    w = max(len(l) for l in linhas)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    for y, linha in enumerate(linhas):
        for x, ch in enumerate(linha):
            if ch in CORES_ARTE:
                s.set_at((x, y), (*CORES_ARTE[ch], 255))
    return s


def garantir_arte(nome):
    """Salva a pixel art pronta na pasta imagens do projeto (se ainda nao tiver) e devolve o nome do arquivo."""
    arquivo = nome + ".png"
    caminho = os.path.join(PASTA_IMAGENS, arquivo)
    if not os.path.exists(caminho):
        os.makedirs(PASTA_IMAGENS, exist_ok=True)
        pygame.image.save(superficie_arte(ARTES[nome]), caminho)
        limpar_cache_imagens()
    return arquivo


def _comp(nome_c, **p):
    base = params_padrao(COMPORTAMENTOS[nome_c])
    base.update({k: str(v) for k, v in p.items()})
    return {"t": nome_c, "p": base}


def _arte_peca(nome, escala=4, **extra):
    arq = garantir_arte(nome)
    linhas = ARTES[nome]
    w, h = max(len(l) for l in linhas) * escala, len(linhas) * escala
    d = nova_entidade("Peça", 0, 0, nome.split("_")[0].capitalize(), w=w, h=h, imagem=arq, contorno=0,
                      cor=[255, 255, 255], solido=False)
    d.update(extra)
    return d


def _anim(objeto, artes, fps=6):
    objeto["animacao"] = ", ".join(garantir_arte(a) for a in artes)
    objeto["fps_anim"] = fps
    objeto["imagem"] = ""
    return objeto


# --------- os itens da loja: cada um devolve uma lista de (objeto, dx, dy) ---------
def _loja_heroi():
    p = nova_entidade("Player", 0, 0, "Player", pulos_extras=1, w=40, h=44,
                      comportamentos=[_comp("Vida", vida=3, dano_de="Inimigo")])
    p["anim_andando"] = ", ".join(garantir_arte(a) for a in ("heroi_1", "heroi_2"))
    p["imagem"] = garantir_arte("heroi_1")
    p["fps_anim"] = 8
    return [(p, 0, 0)]


def _loja_slime():
    i = nova_entidade("Inimigo", 0, 0, "Slime", w=48, h=32, velocidade=70, distancia=140)
    return [(_anim(i, ("slime_1", "slime_2"), 4), 0, 0)]


def _loja_voador():
    i = nova_entidade("Inimigo", 0, 0, "Morcego", w=34, h=24, gravidade=False, cor=[120, 70, 160],
                      comportamentos=[_comp("Senoide (vai e volta)", eixo="y", distancia=50, vezes_por_seg=0.6)])
    return [(i, 0, 0)]


def _loja_perseguidor():
    i = nova_entidade("Inimigo", 0, 0, "Perseguidor", cor=[200, 40, 40], velocidade=0,
                      comportamentos=[_comp("Perseguir", alvo="Player", velocidade=130, alcance=380)])
    return [(i, 0, 0)]


def _loja_npc():
    n = nova_entidade("NPC", 0, 0, "Guia", fala="Bem-vindo!|Pegue todas as moedas.|A bandeira fica no fim da fase.")
    return [(n, 0, 0)]


def _loja_moedas_arco():
    out = []
    for i in range(7):
        ang = math.pi * i / 6
        out.append((nova_entidade("Moeda", 0, 0, "Moeda"), int(-120 * math.cos(ang)), int(-80 * math.sin(ang))))
    return out


def _loja_kit_fase():
    return [(nova_entidade("Bloco", 0, 0, "Chao", w=800, h=40), -400, 60),
            (nova_entidade("Player", 0, 0, "Player"), -360, -10),
            (nova_entidade("Moeda", 0, 0, "Moeda"), -120, 10), (nova_entidade("Moeda", 0, 0, "Moeda"), -80, 10),
            (nova_entidade("Inimigo", 0, 0, "Inimigo"), 80, 20),
            (nova_entidade("Bandeira", 0, 0, "Bandeira"), 360, -24)]


def _loja_plataforma_sobe():
    return [(nova_entidade("Plataforma Movel", 0, 0, "Elevador", vel_x=0, vel_y=80, distancia=160, material="Metal"),
             0, 0)]


def _loja_porta_chave():
    porta = nova_entidade("Peça", 0, 0, "Porta", w=40, h=100, cor=[120, 80, 40], material="Madeira",
                          script='quando tocar "Player":\n    se tem_item("chave"):\n'
                                 '        dizer("Porta aberta!", 1)\n        destruir(eu)\n'
                                 '    senao:\n        dizer("Precisa da chave", 1)\n')
    chave = _arte_peca("chave", 3)
    chave = nova_entidade("Item", 0, 0, "Chave", item="chave", w=chave["w"], h=chave["h"], imagem=chave["imagem"])
    return [(porta, 120, -60), (chave, -120, -20)]


def _loja_escada_blocos():
    return [(nova_entidade("Bloco", 0, 0, "Degrau", w=80, h=40, material="Pedra", cor=[130, 130, 140]),
             i * 80, -i * 40) for i in range(5)]


def _loja_espinhos():
    return [(nova_entidade("Espinho", 0, 0, "Espinho"), i * 40, 0) for i in range(5)]


def _loja_tocha():
    t = preset_objeto("Tocha")
    _anim(t, ("fogo_1", "fogo_2"), 8)
    return [(t, 0, 0)]


def _loja_hud():
    return [(nova_entidade("Texto", 0, 0, "TextoPontos", texto="Moedas: {moedas()}"), 20, 16),
            (nova_entidade("Barra", 0, 0, "BarraVida", valor_de="player.vida", maximo=3), 20, 56)]


def _loja_dialogo():
    return [(nova_entidade("Painel", 0, 0, "CaixaDialogo", w=560, h=110), 200, 400),
            (nova_entidade("Texto", 0, 0, "TextoDialogo", texto="Olá! Isto é uma caixa de diálogo.", w=520), 220, 420)]


def _loja_botao_jogar():
    b = nova_entidade("Botao", 0, 0, "BotaoJogar", texto="JOGAR", w=200, h=56, tamanho_fonte=28,
                      script='quando clique:\n    escrever("Clicou em JOGAR")\n')
    return [(b, 380, 240)]


SCRIPTS_LOJA = {
    "Pulo duplo com som": 'quando tecla "espaco":\n    se eu.vy > 0:\n        eu.vy = -650\n',
    "Contador de tempo": 'var segundos = 0\n\nquando cada 1:\n    segundos += 1\n    global.tempo = segundos\n',
    "Piscar (aviso)": 'quando cada 0.5:\n    eu.visivel = nao eu.visivel\n',
    "Seguir o mouse": 'quando frame:\n    eu.x = mouse_x() - eu.w / 2\n    eu.y = mouse_y() - eu.h / 2\n',
    "Atirar com F": 'quando tecla "f":\n    lancar("Moeda", 600, 0)\n',
    "Dano ao tocar inimigo": 'quando tocar "Inimigo":\n    dizer("Ai!", 1)\n    eu.vy = -500\n',
}


def _loja_script(nome):
    return SCRIPTS_LOJA[nome]


LOJA = []
_CACHE_ICONES = {}

# Precos em Brasas (o que nao esta aqui e gratis)
PRECOS_LOJA = {"Herói animado": 40, "Slime": 15, "Morcego voador": 15, "Perseguidor": 10, "Porta com chave": 20,
               "Elevador": 10, "Escada de blocos": 5, "Tocha animada": 20, "Caixa de diálogo": 10, "Botão JOGAR": 5,
               "Espada": 5, "Baú": 5, "Árvore": 5, "Chave": 5, "Poção": 5, "Cogumelo": 5, "Nuvem": 5,
               "Atirar com F": 10, "Seguir o mouse": 5}


def _item(cat, nome, desc, fn, icone=None, preco=None, plano=None):
    LOJA.append({"id": "loja:" + nome, "cat": cat, "nome": nome, "desc": desc, "fn": fn, "icone": icone,
                 "preco": PRECOS_LOJA.get(nome, 0) if preco is None else preco, "plano": plano})


def _loja_chefao():
    b = nova_entidade("Inimigo", 0, 0, "Chefao", w=96, h=96, cor=[140, 20, 40], velocidade=0,
                      comportamentos=[_comp("Perseguir", alvo="Player", velocidade=90, alcance=600)],
                      script='quando iniciar:\n    dizer("Você não vai passar!", 2)\n')
    return [(_anim(b, ("slime_1", "slime_2"), 3), 0, -30)]


def _loja_moeda_dourada():
    m = nova_entidade("Moeda", 0, 0, "MoedaDourada", w=28, h=28, valor=5,
                      comportamentos=[_comp("Senoide (vai e volta)", eixo="y", distancia=8, vezes_por_seg=1),
                                      _comp("Luz", raio=90)])
    m["imagem"] = garantir_arte("moeda")
    return [(m, 0, 0)]


def _loja_caverna():
    out = [(nova_entidade("Bloco", 0, 0, "ChaoCaverna", w=900, h=40, material="Pedra", cor=[90, 90, 100]), -450, 80)]
    for i, (x, w) in enumerate(((-300, 120), (-60, 100), (200, 140))):
        out.append((nova_entidade("Bloco", 0, 0, "Rocha", w=w, h=30, material="Pedra", cor=[110, 105, 115]), x,
                    -40 - i * 50))
    for x in (-380, 0, 380):
        t = preset_objeto("Tocha")
        _anim(t, ("fogo_1", "fogo_2"), 8)
        out.append((t, x, 40))
    out.append((nova_entidade("Moeda", 0, 0, "Moeda"), -20, -100))
    out.append((nova_entidade("Bandeira", 0, 0, "Saida"), 420, 0))
    return out


_item("Personagens", "Herói animado", "Player com pulo duplo, 3 vidas e animação de andar desenhada.", _loja_heroi,
      "heroi_1")
_item("Personagens", "NPC Guia", "Personagem que conversa (E perto dele).", _loja_npc)
_item("Inimigos", "Slime", "Inimigo que pula de um lado pro outro com animação.", _loja_slime, "slime_1")
_item("Inimigos", "Morcego voador", "Inimigo sem gravidade que sobe e desce.", _loja_voador)
_item("Inimigos", "Perseguidor", "Vai atrás do player quando ele chega perto.", _loja_perseguidor)
_item("Inimigos", "Fileira de espinhos", "5 espinhos lado a lado.", _loja_espinhos)
_item("Inimigos", "Chefão", "Inimigo gigante que persegue o player de longe e fala ao começar.", _loja_chefao,
      "slime_1", preco=0, plano="Game Maker")
_item("Mecânicas", "Kit de fase", "Chão, player, moedas, inimigo e bandeira: uma fase pronta para mexer.",
      _loja_kit_fase)
_item("Mecânicas", "Porta com chave", "A porta só abre se o player pegou a chave.", _loja_porta_chave, "chave")
_item("Mecânicas", "Elevador", "Plataforma de metal que sobe e desce.", _loja_plataforma_sobe)
_item("Mecânicas", "Escada de blocos", "5 degraus de pedra.", _loja_escada_blocos)
_item("Mecânicas", "Moedas em arco", "7 moedas em arco para guiar o pulo.", _loja_moedas_arco, "moeda")
_item("Mecânicas", "Caverna pronta", "Chão e rochas de pedra, 3 tochas animadas, moeda e saída. Deixa a cena escura.",
      _loja_caverna, "fogo_1", preco=0, plano="Dev")
_item("Efeitos", "Tocha animada", "Tocha com fogo desenhado, luz e partículas.", _loja_tocha, "fogo_1")
_item("Efeitos", "Moeda dourada", "Moeda que flutua, brilha e vale 5.", _loja_moeda_dourada, "moeda", preco=0,
      plano="Dev")
for _p in ("Chuva", "Neve", "Fogueira", "Brilhos", "Luz"):
    _item("Efeitos", _p, DESC_PRESETS.get(_p, "Efeito pronto."), lambda p=_p: [(preset_objeto(p), 0, 0)])
_item("Interface", "HUD de moedas e vida", "Texto de moedas e barra de vida no canto da tela.", _loja_hud)
_item("Interface", "Caixa de diálogo", "Painel com texto para conversas.", _loja_dialogo)
_item("Interface", "Botão JOGAR", "Botão grande já com script de clique.", _loja_botao_jogar)
for _a in ("coracao", "estrela", "moeda", "espada", "bau", "arvore", "chave", "pocao", "cogumelo", "nuvem"):
    _item("Imagens", _a.capitalize().replace("Coracao", "Coração").replace("Bau", "Baú").replace("Pocao", "Poção")
          .replace("Arvore", "Árvore"), "Pixel art pronta: vira uma Peça com a imagem (salva na pasta imagens).",
          lambda a=_a: [(_arte_peca(a), 0, 0)], _a)
for _s in SCRIPTS_LOJA:
    _item("Scripts", _s, "Cola este script no objeto selecionado.", ("script", _s))
CENA_DOS_ITENS = {"Caverna pronta": {"escuridao": 170}}
CATEGORIAS_LOJA = ["Tudo", "Personagens", "Inimigos", "Mecânicas", "Efeitos", "Interface", "Imagens", "Scripts",
                   "Exclusivos", "Comunidade", "Meus itens"]
CATEGORIAS_VENDA = ["Personagens", "Inimigos", "Mecânicas", "Efeitos", "Interface", "Imagens", "Outros"]


# ---------------------------------------------------------------------
# Itens da COMUNIDADE: pacotes .mepack (o que voce vende e o que os outros vendem)
# ---------------------------------------------------------------------
def pasta_comunidade():
    return os.path.join(PASTA, "loja_comunidade")


def meu_id_criador():
    c = carteira()
    if not c.get("id_criador"):
        c["id_criador"] = os.urandom(8).hex()
        salvar_carteira()
    return c["id_criador"]


def listar_pacotes():
    pacotes = []
    pasta = pasta_comunidade()
    try:
        nomes = sorted(os.listdir(pasta))
    except OSError:
        return []
    for nome in nomes:
        if not nome.lower().endswith(".mepack"):
            continue
        try:
            with open(os.path.join(pasta, nome), encoding="utf-8") as f:
                p = json.load(f)
        except (OSError, ValueError):
            continue
        if not isinstance(p, dict) or p.get("formato") != "minha-engine-item" or not p.get("objetos"):
            continue
        p["_arquivo"] = os.path.join(pasta, nome)
        p["_meu"] = p.get("autor_id") == meu_id_criador()
        pacotes.append(p)
    return pacotes


def imagens_dos_objetos(objs):
    nomes = set()
    for d in objs:
        for k in ("imagem", "animacao", "anim_andando", "anim_pulando"):
            for n in str(d.get(k, "") or "").split(","):
                if n.strip():
                    nomes.add(n.strip())
    return sorted(nomes)


def criar_pacote(objs, nome, desc, preco, cat, autor):
    """Guarda objetos (com as imagens) num arquivo .mepack na pasta loja_comunidade."""
    objs = [copy.deepcopy(d) for d in objs]
    x0 = min(num_seguro(d["x"]) for d in objs)
    x1 = max(num_seguro(d["x"]) + num_seguro(d.get("w", 40)) for d in objs)
    y0 = min(num_seguro(d["y"]) for d in objs)
    y1 = max(num_seguro(d["y"]) + num_seguro(d.get("h", 40)) for d in objs)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lista = []
    for d in objs:
        dx = num_seguro(d["x"]) + num_seguro(d.get("w", 40)) / 2 - cx
        dy = num_seguro(d["y"]) + num_seguro(d.get("h", 40)) / 2 - cy
        d.pop("modelo", None)
        lista.append({"obj": d, "dx": int(dx), "dy": int(dy)})
    imagens = {}
    for n in imagens_dos_objetos(objs):
        caminho = os.path.join(PASTA_IMAGENS, n)
        if os.path.isfile(caminho):
            with open(caminho, "rb") as f:
                imagens[n] = base64.b64encode(f.read()).decode()
    pid = os.urandom(8).hex()
    pacote = {"formato": "minha-engine-item", "versao": 1, "id": pid, "nome": nome[:40], "desc": desc[:160],
              "cat": cat, "preco": max(0, min(9999, int(preco))), "autor": autor[:30], "autor_id": meu_id_criador(),
              "criado": _tempo.strftime("%d/%m/%Y"), "objetos": lista, "imagens": imagens}
    if online_ativo():
        vender_online(pacote)
        return "online"
    os.makedirs(pasta_comunidade(), exist_ok=True)
    base = re.sub(r"[^\w\-]", "_", nome.strip())[:30] or "item"
    caminho = os.path.join(pasta_comunidade(), f"{base}_{pid[:6]}.mepack")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(pacote, f, ensure_ascii=False)
    return caminho


def salvar_pacote(p):
    dados = {k: v for k, v in p.items() if not k.startswith("_")}
    with open(p["_arquivo"], "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)


def item_do_pacote(p):
    def fazer(p=p):
        os.makedirs(PASTA_IMAGENS, exist_ok=True)
        for nome, dados in (p.get("imagens") or {}).items():
            nome = os.path.basename(nome)
            caminho = os.path.join(PASTA_IMAGENS, nome)
            if not os.path.exists(caminho):
                with open(caminho, "wb") as f:
                    f.write(base64.b64decode(dados))
        limpar_cache_imagens()
        out = []
        for o in p["objetos"]:
            d = copy.deepcopy(o["obj"])
            if d.get("tipo") not in MODELOS:
                continue
            completar_entidade(d)
            out.append((d, int(num_seguro(o.get("dx"))), int(num_seguro(o.get("dy")))))
        return out
    return {"id": "com:" + str(p.get("id", "")), "cat": "Comunidade", "nome": str(p.get("nome", "Item")),
            "desc": str(p.get("desc", "")) + f"  (por {p.get('autor', '?')})", "fn": fazer, "icone": None,
            "preco": int(num_seguro(p.get("preco"), 0)), "plano": None, "pacote": p, "cat_venda": p.get("cat")}


class Loja:
    def __init__(self, ed):
        self.ed = ed
        self.cat = "Tudo"
        self.busca = ""
        self.scroll = 0
        self.hits = []
        self.total = 0
        self.vista = "itens"
        self.pacotes = None

    def recarregar(self):
        self.erro_online = ""
        if online_ativo():
            try:
                self.pacotes = listar_itens_online()
            except ErroOnline as e:
                self.pacotes = []
                self.erro_online = str(e)
            return
        self.pacotes = listar_pacotes()

    def itens_comunidade(self):
        if self.pacotes is None:
            self.recarregar()
        return [item_do_pacote(p) for p in self.pacotes]

    def itens(self):
        b = self.busca.lower()
        com = self.itens_comunidade()
        if self.cat == "Comunidade":
            base = com
        elif self.cat == "Meus itens":
            base = [i for i in com if i["pacote"].get("_meu")]
        elif self.cat == "Exclusivos":
            base = [i for i in LOJA if i["plano"]]
        elif self.cat == "Grátis":
            base = [i for i in LOJA if not i["plano"] and not i["preco"]]
        elif self.cat in ("Game Maker", "Dev"):
            base = [i for i in LOJA if i["plano"] == self.cat]
        elif self.cat == "Tudo":
            base = LOJA + com
        else:
            base = [i for i in LOJA if i["cat"] == self.cat] + [i for i in com if i.get("cat_venda") == self.cat]
        return [i for i in base if not b or b in i["nome"].lower() or b in i["desc"].lower()]

    def estado(self, item):
        """'inserir', 'comprar' ou 'plano' (precisa de um plano melhor)."""
        if item.get("pacote") and item["pacote"].get("_meu"):
            return "inserir"
        if item.get("plano") and nivel_plano() < nivel_plano(item["plano"]):
            return "plano"
        if item.get("preco", 0) > 0 and not ja_comprou(item["id"]):
            return "comprar"
        return "inserir"

    def comprar(self, item):
        ok, msg = comprar(item["id"], item["preco"], item["nome"])
        self.ed.avisar(msg)
        if ok and item.get("pacote") and not online_ativo():
            codigo = gerar_recibo(item["pacote"].get("id", "0" * 16), preco_final(item["preco"]))
            self.ed.clip_por(codigo)
            self.ed.pedir_texto(f"Comprado! Mande este RECIBO para {item['pacote'].get('autor', 'quem vendeu')} "
                                f"(já foi copiado):", codigo, lambda _txt: None)
        return ok

    def inserir(self, item):
        ed = self.ed
        est = self.estado(item)
        if est == "plano":
            self.vista = "planos"
            ed.avisar(f"'{item['nome']}' é exclusivo do plano {item['plano']}.", "aviso")
            return
        if est == "comprar" and not self.comprar(item):
            return
        if isinstance(item["fn"], tuple):
            alvo = ed.sel
            if alvo is None:
                ed.avisar("Selecione um objeto na cena para receber o script.")
                return
            ed.guardar()
            codigo = _loja_script(item["fn"][1])
            atual = alvo.get("script", "") or ""
            alvo["script"] = (atual.rstrip("\n") + "\n\n" if atual.strip() else "") + codigo
            ed.avisar(f"Script '{item['nome']}' colado em '{alvo['nome']}' (aba Script).")
            return
        try:
            partes = item["fn"]()
        except (OSError, ValueError, pygame.error) as erro:
            ed.avisar(f"Não deu para inserir: {erro}")
            return
        if not partes:
            ed.avisar("Esse item está vazio.")
            return
        ed.guardar()
        for k, v in CENA_DOS_ITENS.get(item["nome"], {}).items():
            ed.cena[k] = v
        cx = ed.cam[0] + VIEW.w / ed.zoom / 2
        cy = ed.cam[1] + VIEW.h / ed.zoom / 2
        novos = []
        modelos_novos = []
        for d, dx, dy in partes:
            nome_modelo = d.pop("_modelo_nome", None)
            if nome_modelo:                       # o item traz um modelo (ex: o tiro que um inimigo usa)
                ed.projeto["modelos"][nome_modelo] = d
                modelos_novos.append(nome_modelo)
                continue
            campos = d.pop("_campos", None)
            garantir = d.pop("_garantir_comportamentos", [])     # so coloca se o objeto ainda nao tiver
            trocar = d.pop("_trocar_comportamentos", [])         # coloca ou troca o que ja tinha
            if d.get("na_tela"):
                d["x"], d["y"] = int(dx), int(dy)
            else:
                d["x"] = int(ed.ajustar(cx + dx - num_seguro(d["w"], 40) / 2))
                d["y"] = int(ed.ajustar(cy + dy - num_seguro(d["h"], 40) / 2))
            alvo = d
            if d["tipo"] == "Player":
                existente = next((o for o in ed.objetos if o["tipo"] == "Player"), None)
                if existente is not None:
                    for k in (("anim_andando", "imagem", "fps_anim", "pulos_extras", "comportamentos", "w", "h")
                              if campos is None else campos):
                        if k in d:
                            existente[k] = copy.deepcopy(d[k])
                    alvo = existente
            lista = alvo.setdefault("comportamentos", [])
            for c in garantir:
                if not any(x.get("t") == c["t"] for x in lista):
                    lista.append(copy.deepcopy(c))
            for c in trocar:
                lista[:] = [x for x in lista if x.get("t") != c["t"]] + [copy.deepcopy(c)]
            if alvo is not d:
                novos.append(alvo)
                continue
            d["nome"] = ed.nome_unico(d.get("nome") or d["tipo"])
            ed.objetos.append(d)
            novos.append(d)
        ed.selecionar_varios(novos, False) if len(novos) > 1 else ed.selecionar(novos[0] if novos else None)
        ed.aba = "cena"
        ed.passos_feitos.add("loja")
        extra = f" Modelos novos: {', '.join(modelos_novos)}." if modelos_novos else ""
        ed.avisar(f"'{item['nome']}' inserido no meio da tela ({len(novos)} objeto(s)).{extra} Ctrl+Z desfaz.")

    # ----------------- vender -----------------
    def meus_pacotes(self):
        if self.pacotes is None:
            self.recarregar()
        return [p for p in self.pacotes if p.get("_meu")]

    def comecar_venda(self, pos):
        ed = self.ed
        limite = info_plano()["vender"]
        if len(self.meus_pacotes()) >= limite:
            self.vista = "planos"
            ed.avisar(f"O plano {plano_atual()} deixa vender até {limite} item(ns). Assine um plano para vender mais.",
                      "aviso")
            return
        opcoes = {}
        if ed.selecao:
            opcoes[f"Os objetos selecionados ({len(ed.selecao)})"] = list(ed.selecao)
        for nome, m in ed.projeto["modelos"].items():
            opcoes[f"A variante '{nome}'"] = [dict(copy.deepcopy(m), x=0, y=0, nome=nome)]
        if not opcoes:
            ed.avisar("Selecione na cena o que você quer vender (ou crie uma variante) e clique em Vender de novo.",
                      "aviso")
            ed.aba = "cena"
            return
        ed.abrir_menu(pos, list(opcoes) + ["Cancelar"],
                      lambda it: self.perguntar_nome(opcoes[it]) if it in opcoes else None)

    def perguntar_nome(self, objs):
        sugestao = objs[0].get("nome", "Meu item") if len(objs) == 1 else "Meu pacote"
        self.ed.pedir_texto("Nome do item na Loja", sugestao,
                            lambda nome: self.perguntar_preco(objs, nome.strip() or sugestao))

    def perguntar_preco(self, objs, nome):
        def ok(txt):
            preco = int(num_seguro(re.sub(r"[^\d]", "", txt) or 0, 0))
            self.ed.pedir_texto(f"Descrição de '{nome}' (o que ele faz?)", "",
                                lambda desc: self.perguntar_categoria(objs, nome, preco, desc.strip()))
        self.ed.pedir_texto(f"Preço de '{nome}' em {MOEDA} (0 = grátis)", "10", ok)

    def perguntar_categoria(self, objs, nome, preco, desc):
        pos = (VIEW.centerx - 100, VIEW.centery - 120)
        self.ed.abrir_menu(pos, CATEGORIAS_VENDA, lambda cat: self.publicar(objs, nome, preco, desc, cat))

    def publicar(self, objs, nome, preco, desc, cat):
        ed = self.ed
        autor = nome_usuario()
        try:
            onde = criar_pacote(objs, nome, desc or "Feito na Minha Engine.", preco, cat, autor)
        except ErroOnline as erro:
            ed.avisar(f"Não deu para colocar à venda: {erro}")
            return
        except (OSError, ValueError) as erro:
            ed.avisar(f"Não deu para colocar à venda: {erro}")
            return
        self.recarregar()
        self.cat = "Meus itens"
        self.vista = "itens"
        ganho = ganhar_conquista("primeiro_item_a_venda")
        extra = f" Ganhou +{ganho} {MOEDA} pela primeira venda!" if ganho else ""
        if onde == "online":
            ed.avisar(f"'{nome}' está à venda por {fmt_brasas(preco)} para o mundo todo! Quando alguém comprar, "
                      f"as Brasas caem sozinhas na sua carteira.{extra}", "ok")
            return
        ed.avisar(f"'{nome}' está à venda por {fmt_brasas(preco)}. Clique em 'Enviar' para mandar para "
                  f"outras pessoas.{extra}", "ok")

    def remover(self, p):
        if p.get("_online"):
            try:
                tirar_item_online(p["id"])
            except ErroOnline as erro:
                self.ed.avisar(f"Não consegui tirar da Loja: {erro}")
                return
            self.recarregar()
            self.ed.avisar(f"'{p.get('nome')}' saiu da Loja.", "info")
            return
        try:
            os.remove(p["_arquivo"])
        except OSError as erro:
            self.ed.avisar(f"Não consegui remover: {erro}")
            return
        self.recarregar()
        self.ed.avisar(f"'{p.get('nome')}' saiu da Loja.", "info")

    def mudar_preco(self, p):
        def ok(txt):
            p["preco"] = max(0, min(9999, int(num_seguro(re.sub(r"[^\d]", "", txt) or 0, 0))))
            try:
                mudar_preco_online(p["id"], p["preco"]) if p.get("_online") else salvar_pacote(p)
            except ErroOnline as erro:
                self.ed.avisar(f"Não consegui mudar o preço: {erro}")
                return
            self.recarregar()
            self.ed.avisar(f"Novo preço de '{p.get('nome')}': {fmt_brasas(p['preco'])}.", "ok")
        self.ed.pedir_texto(f"Novo preço de '{p.get('nome')}' em {MOEDA}", str(p.get("preco", 0)), ok)

    def enviar(self, p):
        if p.get("_online"):
            self.ed.avisar("Seu item já aparece para todo mundo em Loja > Comunidade.", "info")
            return
        abrir_pasta(pasta_comunidade())
        self.ed.avisar(f"Mande o arquivo {os.path.basename(p['_arquivo'])} para quem vai comprar. A pessoa coloca "
                       f"ele na pasta loja_comunidade dela e clica em Atualizar.", "info")

    def resgatar(self):
        def ok(txt):
            self.ed.avisar(resgatar_recibo(txt, self.meus_pacotes())[1])
        self.ed.pedir_texto("Código do recibo que o comprador te mandou (ME-XXXX-...)", "", ok)

    # ----------------- cliques -----------------
    def clique(self, pos):
        for r, acao in reversed(self.hits):
            if r.collidepoint(pos):
                k = acao[0]
                if k == "cat":
                    self.cat = acao[1]
                    self.scroll = 0
                elif k == "inserir":
                    self.inserir(acao[1])
                elif k == "buscar":
                    self.ed.pedir_texto("Buscar na loja", self.busca, lambda txt: setattr(self, "busca", txt.strip()))
                elif k == "limpar":
                    self.busca = ""
                elif k == "vista":
                    self.vista = acao[1]
                elif k in ("bonus", "assinar"):
                    self.ed.avisar(acao_carteira(acao))
                elif k == "vender":
                    self.comecar_venda(pos)
                elif k == "resgatar":
                    self.resgatar()
                elif k == "atualizar":
                    self.recarregar()
                    if online_ativo():
                        self.ed.avisar(self.erro_online or f"{len(self.pacotes)} item(ns) da comunidade online.", "info")
                    else:
                        os.makedirs(pasta_comunidade(), exist_ok=True)
                        self.ed.avisar(f"{len(self.pacotes)} item(ns) da comunidade. Coloque arquivos .mepack na "
                                       f"pasta loja_comunidade para aparecerem aqui.", "info")
                elif k == "pasta":
                    abrir_pasta(pasta_comunidade())
                elif k == "remover":
                    p = acao[1]
                    self.ed.abrir_menu(pos, [f"Sim, tirar '{p.get('nome')}' da Loja", "Cancelar"],
                                       lambda it, p=p: self.remover(p) if it.startswith("Sim") else None)
                elif k == "preco":
                    self.mudar_preco(acao[1])
                elif k == "enviar":
                    self.enviar(acao[1])
                return

    # ----------------- desenho -----------------
    def desenhar(self, t, mouse):
        ed = self.ed
        a = VIEW
        self.hits = []
        pygame.draw.rect(t, (24, 26, 32), a)
        if self.vista == "planos":
            voltar = pygame.Rect(a.right - 170, a.y + 14, 154, 30)
            desenhar_botao(t, ed.fp, voltar, "← Voltar para a Loja", mouse)
            self.hits.append((voltar, ("vista", "itens")))
            self.hits += desenhar_planos(t, pygame.Rect(a.x + 20, a.y + 14, a.w - 40, a.h - 24), mouse)
            return
        t.blit(ed.fg.render("Creator Store", True, C_TEXTO), (a.x + 16, a.y + 10))
        x = a.x + 20 + ed.fg.size("Creator Store")[0]
        sr = desenhar_saldo(t, x, a.y + 12, 13, mouse)
        self.hits.append((sr, ("vista", "planos")))
        pr = desenhar_selo(t, sr.right + 8, a.y + 16)
        self.hits.append((pr, ("vista", "planos")))
        x = pr.right + 12
        botoes = []
        if pode_pegar_bonus():
            botoes.append((f"Semanal +{info_plano()['bonus']}", ("bonus",), (200, 110, 40)))
        botoes += [("Planos", ("vista", "planos"), (70, 76, 92)), ("Vender", ("vender",), C_VERDE)]
        if not online_ativo():
            botoes.append(("Resgatar venda", ("resgatar",), (70, 90, 140)))
        for rot, acao, cor in botoes:
            w = ed.fp.size(rot)[0] + 20
            r = pygame.Rect(x, a.y + 12, w, 28)
            if r.right > a.right - 200:
                break
            desenhar_botao(t, ed.fp, r, rot, mouse, cor=cor)
            self.hits.append((r, acao))
            x += w + 6
        sub = (f"ONLINE como {nome_usuario()}: o que você vende aparece para o mundo todo." if online_ativo() else
               f"Compre com {MOEDA}, venda suas criações e assine Game Maker ou Dev. Entre na conta online "
               f"(Início) para vender para o mundo todo.")
        if getattr(self, "erro_online", ""):
            sub = "Sem conexão: " + self.erro_online
        t.blit(ed.fpp.render(sub, True, C_TEXTO2), (a.x + 18, a.y + 46))
        r = pygame.Rect(a.right - 190, a.y + 12, 176, 28)
        pygame.draw.rect(t, C_CAMPO, r, border_radius=6)
        pygame.draw.rect(t, C_BORDA, r, 1, border_radius=6)
        t.blit(ed.fp.render(f"Buscar: {self.busca}" if self.busca else "Buscar...", True,
                            C_TEXTO if self.busca else C_TEXTO2), (r.x + 10, r.y + 6))
        self.hits.append((r, ("buscar",)))
        if self.busca:
            xr = pygame.Rect(r.right - 24, r.y + 6, 16, 16)
            pygame.draw.rect(t, (90, 45, 45), xr, border_radius=3)
            t.blit(ed.fpp.render("x", True, C_TEXTO), (xr.x + 5, xr.y + 1))
            self.hits.append((xr, ("limpar",)))
        x, y = a.x + 14, a.y + 66
        for cat in CATEGORIAS_LOJA:
            w = ed.fp.size(cat)[0] + 22
            if x + w > a.right - 10:
                x, y = a.x + 14, y + 32
            cr = pygame.Rect(x, y, w, 26)
            ativo = cat == self.cat
            pygame.draw.rect(t, C_DESTAQUE if ativo else (clarear(C_BOTAO, 15) if cr.collidepoint(mouse) else C_BOTAO),
                             cr, border_radius=13)
            img = ed.fp.render(cat, True, C_TEXTO)
            t.blit(img, (cr.centerx - img.get_width() // 2, cr.centery - img.get_height() // 2))
            self.hits.append((cr, ("cat", cat)))
            x += w + 6
        if self.cat in ("Comunidade", "Meus itens"):
            y += 34
            for i, (rot, acao) in enumerate((("Atualizar", ("atualizar",)), ("Abrir pasta loja_comunidade", ("pasta",)))):
                w = ed.fp.size(rot)[0] + 20
                r = pygame.Rect(a.x + 14 + i * 110, y, w, 24)
                desenhar_botao(t, ed.fp, r, rot, mouse)
                self.hits.append((r, acao))
            dica = (f"Seus itens à venda: {len(self.meus_pacotes())} de "
                    f"{'sem limite' if info_plano()['vender'] > 100 else info_plano()['vender']}")
            t.blit(ed.fpp.render(dica, True, C_TEXTO2), (a.x + 330, y + 5))
        lista = pygame.Rect(a.x + 8, y + 38, a.w - 16, a.bottom - y - 46)
        t.set_clip(lista)
        colunas = max(1, lista.w // 250)
        cw = (lista.w - (colunas - 1) * 10) // colunas
        itens = self.itens()
        linhas = (len(itens) + colunas - 1) // colunas
        self.total = linhas * 128
        self.scroll = max(0, min(self.scroll, max(0, self.total - lista.h)))
        vis = suave((id(self), "loja", self.cat), self.scroll)
        for i, item in enumerate(itens):
            cx = lista.x + (i % colunas) * (cw + 10)
            cy = lista.y + (i // colunas) * 128 - vis
            if cy > lista.bottom or cy + 118 < lista.y:
                continue
            self.desenhar_card(t, mouse, item, pygame.Rect(cx, cy, cw, 118), lista)
        if not itens:
            vazio = {"Comunidade": "Nenhum item da comunidade ainda. Peça para alguém te mandar um arquivo .mepack "
                                   "e coloque na pasta loja_comunidade (botão acima).",
                     "Meus itens": "Você ainda não vende nada. Selecione objetos na cena e clique em 'Vender'."}
            for j, linha in enumerate(quebrar_texto(vazio.get(self.cat, "Nada encontrado."), ed.f, lista.w - 20)):
                t.blit(ed.f.render(linha, True, C_TEXTO2), (lista.x + 10, lista.y + 10 + j * 20))
        t.set_clip(None)

    def desenhar_card(self, t, mouse, item, card, lista):
        ed = self.ed
        p = item.get("pacote")
        meu = bool(p and p.get("_meu"))
        borda = PLANOS[item["plano"]]["cor"] if item.get("plano") else (C_DESTAQUE if meu else C_BORDA)
        pygame.draw.rect(t, (40, 43, 52) if not card.collidepoint(mouse) else (48, 52, 64), card, border_radius=8)
        pygame.draw.rect(t, borda, card, 2 if (item.get("plano") or meu) else 1, border_radius=8)
        ic = pygame.Rect(card.x + 10, card.y + 10, 56, 56)
        pygame.draw.rect(t, (30, 32, 40), ic, border_radius=6)
        mini = None
        if item["icone"] in ARTES:
            s = _CACHE_ICONES.get(item["icone"])
            if s is None:
                mini = superficie_arte(ARTES[item["icone"]])
                k = min(48 / max(1, mini.get_width()), 48 / max(1, mini.get_height()))
                s = pygame.transform.scale(mini, (max(1, int(mini.get_width() * k)), max(1, int(mini.get_height() * k))))
                _CACHE_ICONES[item["icone"]] = s
            t.blit(s, (ic.centerx - s.get_width() // 2, ic.centery - s.get_height() // 2))
            mini = None
        elif p:
            nomes = imagens_dos_objetos([o["obj"] for o in p["objetos"]])
            if nomes and nomes[0] in (p.get("imagens") or {}):
                mini = carregar_imagem(nomes[0]) if os.path.exists(os.path.join(PASTA_IMAGENS, nomes[0])) else None
        if item["icone"] in ARTES:
            pass
        elif mini is not None and mini.get_width() and mini.get_height():
            k = min(48 / mini.get_width(), 48 / mini.get_height())
            s = pygame.transform.scale(mini, (max(1, int(mini.get_width() * k)), max(1, int(mini.get_height() * k))))
            t.blit(s, (ic.centerx - s.get_width() // 2, ic.centery - s.get_height() // 2))
        elif p:
            o = p["objetos"][0]["obj"]
            desenhar_icone(t, o.get("tipo"), o, ic.inflate(-16, -16))
        elif item.get("icone_obj"):
            o = item["icone_obj"]
            desenhar_icone(t, o.get("tipo"), o, ic.inflate(-14, -14))
        else:
            letra = ed.fg.render(item["cat"][0], True, C_DESTAQUE)
            t.blit(letra, (ic.centerx - letra.get_width() // 2, ic.centery - letra.get_height() // 2))
        t.blit(ed.fb.render(item["nome"][:26], True, C_TEXTO), (card.x + 76, card.y + 10))
        sub = item.get("cat_venda") or item["cat"]
        x_sub = card.x + 76
        if meu:
            sub = "Seu item à venda"
        t.blit(ed.fpp.render(sub, True, C_DESTAQUE), (x_sub, card.y + 28))
        if item.get("plano"):
            desenhar_selo(t, x_sub + ed.fpp.size(sub)[0] + 8, card.y + 26, item["plano"], 9)
        for j, linha in enumerate(quebrar_texto(item["desc"], ed.fpp, card.w - 86)[:3]):
            t.blit(ed.fpp.render(linha, True, C_TEXTO2), (card.x + 76, card.y + 44 + j * 14))
        # preco
        est = self.estado(item)
        preco = item.get("preco", 0)
        px, py = card.x + 12, card.bottom - 26
        if preco > 0 and not meu:
            if ja_comprou(item["id"]):
                t.blit(ed.fpp.render("Já é seu", True, (110, 220, 140)), (px, py + 2))
            else:
                desenhar_moeda(t, (px + 7, py + 9), 7)
                final = preco_final(preco)
                t.blit(ed.fb.render(str(final), True, C_TEXTO), (px + 18, py + 1))
                if final != preco:
                    t.blit(ed.fpp.render(f"(era {preco})", True, C_TEXTO2), (px + 26 + ed.fb.size(str(final))[0], py + 3))
        elif meu:
            desenhar_moeda(t, (px + 7, py + 9), 7)
            r = pygame.Rect(px + 16, py, ed.fb.size(str(preco))[0] + 8, 20)
            t.blit(ed.fb.render(str(preco), True, C_TEXTO), (r.x + 2, r.y + 1))
            self.hits.append((r, ("preco", p)))
        else:
            t.blit(ed.fpp.render("Grátis", True, (110, 220, 140)), (px, py + 2))
        br = pygame.Rect(card.right - 92, card.bottom - 32, 82, 24)
        if est == "plano":
            desenhar_botao(t, ed.fpp, br, "Ver planos", mouse, cor=PLANOS[item["plano"]]["cor"])
        elif est == "comprar":
            desenhar_botao(t, ed.fp, br, "Comprar", mouse, cor=(200, 110, 40))
        else:
            desenhar_botao(t, ed.fp, br, "Inserir", mouse, cor=C_VERDE)
        if lista.collidepoint(br.center):
            self.hits.append((br, ("inserir", item)))
        if meu:
            for k_, (rot, acao) in enumerate((("Enviar", ("enviar", p)), ("x", ("remover", p)))):
                w = 52 if rot == "Enviar" else 22
                r = pygame.Rect(br.x - 6 - (58 if k_ == 0 else 86), br.y, w, 24)
                desenhar_botao(t, ed.fpp, r, rot, mouse, cor=(90, 45, 45) if rot == "x" else (70, 90, 140))
                if lista.collidepoint(r.center):
                    self.hits.append((r, acao))
