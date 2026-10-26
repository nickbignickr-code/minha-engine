# Minha Engine - carteira.py
# Moeda virtual (Brasas), planos Grátis / Game Maker / Dev, bônus, conquistas e recibos de venda
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# CARTEIRA: a moeda virtual da engine
# =====================================================================
# Tudo aqui e VIRTUAL e OFFLINE: as Brasas nao valem dinheiro de verdade.
# A carteira fica no arquivo carteira.json, ao lado do minha_engine.py (vale para todos os projetos).
import base64
import hashlib
import hmac
import time as _tempo

MOEDA = "Brasas"
MOEDA_1 = "Brasa"
BONUS_BOAS_VINDAS = 150
BRASAS_VISITA = 25      # cada pessoa diferente que joga o seu jogo publicado (1 vez por usuario)
BRASAS_LIKE = 50        # cada like no seu jogo publicado (1 vez por usuario)
DIAS_PLANO = 30
ORDEM_PLANOS = ["Grátis", "Game Maker", "Dev"]
PLANOS = {
    "Grátis": {"preco": 0, "bonus": 10, "vender": 1, "desconto": 0, "taxa": 30, "cor": (120, 126, 142),
               "selo": "GRÁTIS", "resumo": "Para começar",
               "beneficios": ["Todos os recursos da engine", "10 Brasas por semana", "Vender 1 item na Loja",
                              "Loja cobra 30% das suas vendas"]},
    "Game Maker": {"preco": 300, "bonus": 35, "vender": 10, "desconto": 10, "taxa": 15, "cor": (46, 168, 98),
                   "selo": "GAME MAKER", "resumo": "Para quem cria jogos",
                   "beneficios": ["35 Brasas por semana", "Vender até 10 itens na Loja", "10% de desconto na Loja",
                                  "Itens exclusivos Game Maker", "Loja cobra só 15% das vendas", "Selo GAME MAKER"]},
    "Dev": {"preco": 800, "bonus": 75, "vender": 999, "desconto": 25, "taxa": 5, "cor": (236, 168, 40),
            "selo": "DEV", "resumo": "Para quem leva a sério",
            "beneficios": ["75 Brasas por semana", "Vender itens sem limite", "25% de desconto na Loja",
                           "TODOS os itens exclusivos (GM e Dev)", "Loja cobra só 5% das vendas",
                           "Cor de destaque Dourado", "Selo DEV"]},
}
CONQUISTAS = {
    "boas_vindas": (BONUS_BOAS_VINDAS, "Presente de boas-vindas"),
    "primeiros_passos": (50, "Completou os Primeiros passos"),
    "primeira_exportacao": (30, "Exportou o primeiro jogo"),
    "primeiro_item_a_venda": (20, "Colocou o primeiro item à venda"),
}
# chave dos recibos de venda (offline: serve para os codigos nao serem digitados errado ou inventados facilmente)
_CHAVE_RECIBO = b"minha-engine-brasas-recibo-v1"
_carteira = {}
NOVIDADES_CARTEIRA = []      # mensagens de "ganhou Brasas" para o editor/Inicio mostrarem


# ---------------------------------------------------------------------
# USUARIOS: cada pessoa que usa a engine neste computador tem a sua conta (e a sua carteira)
# ---------------------------------------------------------------------
CORES_USUARIO = [(70, 140, 255), (46, 168, 98), (232, 128, 40), (222, 78, 148), (140, 92, 230), (26, 168, 190),
                 (214, 72, 72), (236, 168, 40)]
_usuario = {}


def pasta_usuarios():
    return os.path.join(PASTA, "usuarios")


def arquivo_usuario(uid):
    return os.path.join(pasta_usuarios(), re.sub(r"[^0-9a-f]", "", str(uid)) + ".json")


def arquivo_carteira():
    return arquivo_usuario(_usuario.get("id", "")) if _usuario else os.path.join(PASTA, "carteira.json")


def ler_usuario(uid):
    try:
        with open(arquivo_usuario(uid), encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) and d.get("id") else None
    except (OSError, ValueError):
        return None


def gravar_usuario(u):
    try:
        os.makedirs(pasta_usuarios(), exist_ok=True)
        with open(arquivo_usuario(u["id"]), "w", encoding="utf-8") as f:
            json.dump(u, f, indent=1, ensure_ascii=False)
    except OSError:
        pass


def listar_usuarios():
    res = []
    try:
        nomes = sorted(os.listdir(pasta_usuarios()))
    except OSError:
        return res
    for n in nomes:
        if n.endswith(".json"):
            u = ler_usuario(n[:-5])
            if u:
                res.append(u)
    res.sort(key=lambda u: u.get("criado", 0))
    return res


def _hash_pin(pin):
    return hashlib.sha256(("minha-engine:" + str(pin)).encode()).hexdigest() if pin else ""


def criar_usuario(nome, pin=""):
    """Cria uma conta neste computador e ja entra nela. Devolve o id."""
    nome = re.sub(r"\s+", " ", str(nome)).strip()[:24] or "Criador"
    existentes = listar_usuarios()
    if any(u["nome"].lower() == nome.lower() for u in existentes):
        raise ValueError(f"Já existe um usuário chamado '{nome}'.")
    uid = os.urandom(8).hex()
    cart = carteira_padrao()
    antigo = os.path.join(PASTA, "carteira.json")       # carteira da versao 11 vira do primeiro usuario
    if not existentes and os.path.isfile(antigo):
        try:
            with open(antigo, encoding="utf-8") as f:
                velho = json.load(f)
            for k, v in velho.items():
                if k in cart and isinstance(v, type(cart[k])):
                    cart[k] = v
            os.replace(antigo, antigo + ".importado")
        except (OSError, ValueError):
            pass
    cart["id_criador"] = cart.get("id_criador") or uid
    u = {"id": uid, "nome": nome, "cor": list(CORES_USUARIO[len(existentes) % len(CORES_USUARIO)]),
         "pin": _hash_pin(pin), "criado": _tempo.time(), "carteira": cart}
    gravar_usuario(u)
    entrar(uid)
    return uid


def confere_pin(u, pin):
    return not u.get("pin") or u["pin"] == _hash_pin(pin)


def entrar(uid):
    u = ler_usuario(uid)
    if u is None:
        return False
    if online_ativo():
        sair_online()
    _usuario.clear()
    _usuario.update(u)
    CONFIG["geral"]["usuario_atual"] = uid
    salvar_config()
    _carteira.clear()
    carregar_carteira()
    return True


def usuario_atual():
    """A conta que esta usando agora (cria uma automaticamente na primeira vez)."""
    if online_ativo():
        return usuario_online()
    if not _usuario:
        uid = CONFIG["geral"].get("usuario_atual", "")
        if not (uid and entrar(uid)):
            usuarios = listar_usuarios()
            if usuarios:
                entrar(usuarios[0]["id"])
            else:
                criar_usuario(os.environ.get("USERNAME") or os.environ.get("USER") or "Criador")
    return _usuario


def nome_usuario():
    return usuario_atual().get("nome", "Criador")


def renomear_usuario(novo):
    if online_ativo():
        try:
            return renomear_online(novo)
        except ErroOnline as e:
            return str(e)
    u = usuario_atual()
    novo = str(novo).strip()[:24]
    if novo:
        u["nome"] = novo
        salvar_carteira()


def carteira_padrao():
    return {"saldo": 0, "plano": "Grátis", "plano_ate": 0, "ultimo_bonus": "", "comprados": [], "conquistas": [],
            "historico": [], "recibos_usados": [], "vendas": 0, "ganho_vendas": 0, "id_criador": "",
            "codigos_usados": []}


def carteira():
    """A carteira do usuario atual (carrega do disco na primeira vez)."""
    if online_ativo():
        if not _carteira.get("_online"):
            try:
                atualizar_carteira_online()
            except ErroOnline as e:
                _carteira.clear()
                _carteira.update(carteira_padrao())
                _carteira.update({"_online": True, "_erro": str(e)})
        return _carteira
    if not _usuario:
        usuario_atual()
    if not _carteira:
        carregar_carteira()
    return _carteira


def carregar_carteira():
    dados = _usuario.get("carteira") if _usuario else None
    if not isinstance(dados, dict):
        dados = {}
    _carteira.clear()
    _carteira.update(carteira_padrao())
    for k, v in dados.items():
        if k in _carteira and isinstance(v, type(_carteira[k])):
            _carteira[k] = v
    _carteira["saldo"] = int(num_seguro(_carteira["saldo"], 0))
    if not _carteira["id_criador"]:
        _carteira["id_criador"] = _usuario.get("id") or os.urandom(8).hex()
    if "boas_vindas" not in _carteira["conquistas"]:
        ganhar_conquista("boas_vindas")
    plano_atual()
    return _carteira


def salvar_carteira():
    if _carteira.get("_online") or not _usuario:
        return
    _usuario["carteira"] = _carteira
    gravar_usuario(_usuario)


def creditar(uid, valor, motivo):
    """Da Brasas para QUALQUER usuario deste computador (ex: o dono do jogo que ganhou um like)."""
    if _usuario and uid == _usuario.get("id"):
        movimentar(valor, motivo)
        return True
    u = ler_usuario(uid)
    if u is None:
        return False
    c = carteira_padrao()
    c.update(u.get("carteira") or {})
    c["saldo"] = max(0, int(num_seguro(c.get("saldo"), 0)) + int(valor))
    c["historico"] = (c.get("historico") or []) + [{"data": _tempo.strftime("%d/%m %H:%M"), "valor": int(valor),
                                                   "motivo": str(motivo)[:60]}]
    c["historico"] = c["historico"][-80:]
    u["carteira"] = c
    gravar_usuario(u)
    return True


def hoje():
    return _tempo.strftime("%Y-%m-%d")


def fmt_brasas(n):
    n = int(n)
    return f"{n:,}".replace(",", ".") + " " + (MOEDA_1 if abs(n) == 1 else MOEDA)


def movimentar(valor, motivo):
    c = carteira()
    if c.get("_online"):          # online quem mexe no saldo e o servidor
        return c["saldo"]
    c["saldo"] = max(0, int(c["saldo"]) + int(valor))
    c["historico"].append({"data": _tempo.strftime("%d/%m %H:%M"), "valor": int(valor), "motivo": str(motivo)[:60]})
    c["historico"] = c["historico"][-80:]
    salvar_carteira()
    return c["saldo"]


def plano_atual():
    c = carteira() if _carteira else _carteira
    if c.get("plano") not in PLANOS:
        c["plano"] = "Grátis"
    if c["plano"] != "Grátis" and c.get("plano_ate", 0) < _tempo.time():
        c["plano"] = "Grátis"
        c["plano_ate"] = 0
        salvar_carteira()
    if c["plano"] == "Dev":
        CORES_DESTAQUE.setdefault("Dourado", [236, 168, 40])
    else:
        CORES_DESTAQUE.pop("Dourado", None)
    return c["plano"]


def info_plano(nome=None):
    return PLANOS[nome or plano_atual()]


def nivel_plano(nome=None):
    return ORDEM_PLANOS.index(nome or plano_atual())


def dias_restantes():
    c = carteira()
    if plano_atual() == "Grátis":
        return 0
    return max(0, int((c["plano_ate"] - _tempo.time()) // 86400) + 1)


def esta_semana():
    import datetime
    ano, semana, _ = datetime.date.today().isocalendar()
    return f"{ano}-S{semana:02d}"


def pode_pegar_bonus():
    c = carteira()
    if c.get("_online"):
        return bool(c.get("semana")) and c["ultimo_bonus"] != c["semana"]
    return c["ultimo_bonus"] != esta_semana()


def pegar_bonus():
    if not pode_pegar_bonus():
        return 0
    if carteira().get("_online"):
        try:
            v = rpc("pegar_recompensa") or 0
            atualizar_carteira_online()
            return v
        except ErroOnline:
            return 0
    valor = info_plano()["bonus"]
    carteira()["ultimo_bonus"] = esta_semana()
    movimentar(valor, f"Recompensa semanal ({plano_atual()})")
    return valor


def ganhar_conquista(chave):
    c = carteira() if (_carteira or online_ativo()) else _carteira
    if chave in c["conquistas"] or chave not in CONQUISTAS:
        return 0
    if c.get("_online"):
        try:
            v = rpc("conquista", p_chave=chave) or 0
            atualizar_carteira_online()
        except ErroOnline:
            return 0
        if v:
            NOVIDADES_CARTEIRA.append(f"+{fmt_brasas(v)}: {CONQUISTAS[chave][1]}!")
        return v
    valor, motivo = CONQUISTAS[chave]
    c["conquistas"].append(chave)
    movimentar(valor, motivo)
    NOVIDADES_CARTEIRA.append(f"+{fmt_brasas(valor)}: {motivo}!")
    return valor


def assinar(plano):
    """Assina (ou renova) um plano pagando com Brasas. Devolve (deu_certo, mensagem)."""
    if plano not in PLANOS or plano == "Grátis":
        return False, "Esse plano não existe."
    c = carteira()
    if c.get("_online"):
        try:
            r = rpc("assinar", p_plano=plano) or {}
            atualizar_carteira_online()
            return bool(r.get("ok")), r.get("msg", "")
        except ErroOnline as e:
            return False, str(e)
    preco = PLANOS[plano]["preco"]
    atual = plano_atual()
    if nivel_plano(plano) < nivel_plano(atual):
        return False, f"Você já tem o plano {atual}, que é melhor. Espere ele acabar para trocar."
    if c["saldo"] < preco:
        return False, (f"Faltam {fmt_brasas(preco - c['saldo'])} para o plano {plano}. Publique jogos: cada "
                       f"visita dá {BRASAS_VISITA} e cada like dá {BRASAS_LIKE}!")
    agora = _tempo.time()
    base = c["plano_ate"] if (atual == plano and c["plano_ate"] > agora) else agora
    c["plano"] = plano
    c["plano_ate"] = base + DIAS_PLANO * 86400
    movimentar(-preco, f"Plano {plano} ({DIAS_PLANO} dias)")
    if plano == "Dev":
        CORES_DESTAQUE.setdefault("Dourado", [236, 168, 40])
    return True, f"Pronto! Agora você é {plano} por 1 mês ({dias_restantes()} dias)."


def preco_final(preco):
    return int(round(preco * (100 - info_plano()["desconto"]) / 100))


def ja_comprou(item_id):
    return item_id in carteira()["comprados"]


def comprar(item_id, preco, nome):
    c = carteira()
    valor = preco_final(preco)
    if ja_comprou(item_id):
        return True, "Você já tem esse item."
    if c.get("_online"):
        try:
            if item_id.startswith("com:"):
                r = rpc("comprar_item", p_item=item_id[4:]) or {}
            else:
                r = rpc("comprar_da_loja", p_item=item_id, p_preco=int(preco)) or {}
            atualizar_carteira_online()
        except ErroOnline as e:
            return False, str(e)
        return bool(r.get("ok")), (f"'{nome}': " + r.get("msg", "") if r.get("ok") else r.get("msg", ""))
    if c["saldo"] < valor:
        return False, f"Faltam {fmt_brasas(valor - c['saldo'])} para comprar '{nome}'."
    c["comprados"].append(item_id)
    movimentar(-valor, f"Comprou '{nome}'")
    return True, f"Comprou '{nome}' por {fmt_brasas(valor)}!"


# ----------------- recibos de venda (vender para outras pessoas, offline) -----------------
def _b32(dados):
    return base64.b32encode(dados).decode().rstrip("=")


def _de_b32(txt):
    txt = re.sub(r"[^A-Z2-7]", "", txt.upper())
    return base64.b32decode(txt + "=" * (-len(txt) % 8))


def gerar_recibo(item_id, preco):
    """Quem COMPRA um item da comunidade recebe este codigo e manda para quem vendeu."""
    corpo = bytes.fromhex(item_id[:8]) + int(preco).to_bytes(2, "big") + os.urandom(3)
    assinatura = hmac.new(_CHAVE_RECIBO, corpo, hashlib.sha256).digest()[:5]
    txt = _b32(corpo + assinatura)
    return "ME-" + "-".join(txt[i:i + 4] for i in range(0, len(txt), 4))


def ler_recibo(codigo):
    """Devolve (id8, preco) se o codigo for valido, senao None."""
    try:
        bruto = _de_b32(str(codigo).upper().replace("ME-", "", 1))
    except (ValueError, TypeError):
        return None
    if len(bruto) != 14:
        return None
    corpo, assinatura = bruto[:9], bruto[9:]
    if not hmac.compare_digest(hmac.new(_CHAVE_RECIBO, corpo, hashlib.sha256).digest()[:5], assinatura):
        return None
    return corpo[:4].hex(), int.from_bytes(corpo[4:6], "big")


def resgatar_recibo(codigo, meus_itens):
    """Quem VENDEU digita o codigo do comprador e ganha as Brasas (menos a taxa da Loja)."""
    if carteira().get("_online"):
        return False, "Online as vendas caem sozinhas na sua carteira: não precisa de recibo."
    lido = ler_recibo(codigo)
    if lido is None:
        return False, "Código inválido. Confira se digitou certinho (ME-XXXX-...)."
    limpo = re.sub(r"[^A-Z2-7]", "", str(codigo).upper().replace("ME-", "", 1))
    c = carteira()
    if limpo in c["recibos_usados"]:
        return False, "Esse código já foi usado."
    id8, preco = lido
    item = next((i for i in meus_itens if i.get("id", "")[:8] == id8), None)
    if item is None:
        return False, "Esse recibo é de um item que não é seu."
    taxa = info_plano()["taxa"]
    ganho = max(0, preco - preco * taxa // 100)
    c["recibos_usados"].append(limpo)
    c["vendas"] = int(c.get("vendas", 0)) + 1
    c["ganho_vendas"] = int(c.get("ganho_vendas", 0)) + ganho
    movimentar(ganho, f"Venda de '{item.get('nome', '?')}' (taxa {taxa}%)")
    return True, f"Venda recebida! +{fmt_brasas(ganho)} (a Loja ficou com {taxa}%)."


# ----------------- desenho -----------------
def desenhar_moeda(t, centro, raio=9):
    """Uma brasa: moeda laranja com o miolo amarelo."""
    cx, cy = int(centro[0]), int(centro[1])
    pygame.draw.circle(t, (150, 60, 20), (cx, cy + 1), raio)
    pygame.draw.circle(t, (255, 138, 61), (cx, cy), raio)
    pygame.draw.circle(t, (255, 196, 90), (cx, cy), max(2, raio * 6 // 10))
    pygame.draw.polygon(t, (255, 120, 40), [(cx, cy - raio * 5 // 10), (cx + raio * 3 // 10, cy + raio * 3 // 10),
                                            (cx - raio * 3 // 10, cy + raio * 3 // 10)])


def desenhar_avatar(t, u, centro, raio):
    cor = tuple(u.get("cor") or CORES_USUARIO[0])
    pygame.draw.circle(t, cor, centro, raio)
    letra = texto_cache((u.get("nome") or "?")[0].upper(), max(10, int(raio * 1.1)), (255, 255, 255), True)
    t.blit(letra, (centro[0] - letra.get_width() // 2, centro[1] - letra.get_height() // 2))


def desenhar_selo(t, x, y, plano=None, tam=11):
    plano = plano or plano_atual()
    info = PLANOS[plano]
    img = texto_cache(info["selo"], tam, (255, 255, 255), True)
    r = pygame.Rect(x, y, img.get_width() + 14, img.get_height() + 6)
    pygame.draw.rect(t, info["cor"], r, border_radius=r.h // 2)
    t.blit(img, (r.x + 7, r.y + 3))
    return r


def desenhar_saldo(t, x, y, tam=14, mouse=None):
    """Chip com a moeda e o saldo. Devolve o retangulo (para clicar)."""
    img = texto_cache(fmt_brasas(carteira()["saldo"]), tam, C_TEXTO, True)
    r = pygame.Rect(x, y, img.get_width() + 40, max(26, img.get_height() + 10))
    cor = (44, 40, 36) if not (mouse and r.collidepoint(mouse)) else (60, 54, 46)
    pygame.draw.rect(t, cor, r, border_radius=r.h // 2)
    pygame.draw.rect(t, (120, 80, 40), r, 1, border_radius=r.h // 2)
    desenhar_moeda(t, (r.x + 15, r.centery), 8)
    t.blit(img, (r.x + 29, r.centery - img.get_height() // 2))
    return r


def desenhar_planos(t, area, mouse):
    """Pagina de planos e carteira (usada no Inicio e na Loja). Devolve a lista de (retangulo, acao)."""
    hits = []
    c = carteira()
    atual = plano_atual()
    y = area.y
    t.blit(texto_cache("Planos e Brasas", 28, C_TEXTO, True), (area.x, y))
    r = desenhar_saldo(t, area.x + texto_cache("Planos e Brasas", 28, C_TEXTO, True).get_width() + 20, y + 4, 15)
    sr = desenhar_selo(t, r.right + 10, y + 8, atual)
    if atual != "Grátis":
        t.blit(texto_cache(f"faltam {dias_restantes()} dia(s)", 12, C_TEXTO2), (sr.right + 8, y + 10))
    y += 46
    t.blit(texto_cache(f"As {MOEDA} são a moeda da Minha Engine (não é dinheiro de verdade). Ganhe com a recompensa "
                       f"semanal, +{BRASAS_VISITA} por visita e +{BRASAS_LIKE} por like nos seus jogos publicados.",
                       13, C_TEXTO2), (area.x + 2, y))
    y += 30
    # cartoes dos planos
    gap = 14
    cw = max(200, min(300, (area.w - 2 * gap) // 3))
    ch = 300
    for i, nome in enumerate(ORDEM_PLANOS):
        info = PLANOS[nome]
        card = pygame.Rect(area.x + i * (cw + gap), y, cw, ch)
        e_atual = nome == atual
        pygame.draw.rect(t, (16, 17, 21), card.move(0, 4), border_radius=14)
        pygame.draw.rect(t, (40, 43, 52), card, border_radius=14)
        pygame.draw.rect(t, info["cor"], card, 3 if e_atual else 1, border_radius=14)
        pygame.draw.rect(t, info["cor"], (card.x, card.y, card.w, 8), border_top_left_radius=14,
                         border_top_right_radius=14)
        t.blit(texto_cache(nome, 22, C_TEXTO, True), (card.x + 16, card.y + 20))
        t.blit(texto_cache(info["resumo"], 12, C_TEXTO2), (card.x + 17, card.y + 50))
        if info["preco"]:
            desenhar_moeda(t, (card.x + 26, card.y + 84), 10)
            t.blit(texto_cache(str(info["preco"]), 24, C_TEXTO, True), (card.x + 42, card.y + 70))
            t.blit(texto_cache("/ mês", 12, C_TEXTO2),
                   (card.x + 48 + texto_cache(str(info["preco"]), 24, C_TEXTO, True).get_width(), card.y + 80))
        else:
            t.blit(texto_cache("Grátis para sempre", 18, C_TEXTO, True), (card.x + 16, card.y + 72))
        yy = card.y + 112
        for b in info["beneficios"]:
            pygame.draw.lines(t, info["cor"], False, [(card.x + 18, yy + 8), (card.x + 22, yy + 12), (card.x + 29, yy + 3)],
                              2)
            for j, linha in enumerate(quebrar_texto(b, fonte_ui(13), cw - 52)[:2]):
                t.blit(texto_cache(linha, 13, C_TEXTO), (card.x + 36, yy + j * 16))
            yy += 22 if len(quebrar_texto(b, fonte_ui(13), cw - 52)) < 2 else 38
        br = pygame.Rect(card.x + 14, card.bottom - 48, cw - 28, 36)
        if e_atual:
            rot = "Seu plano" if nome == "Grátis" else "Renovar +1 mês"
            cor = (60, 64, 78) if nome == "Grátis" else info["cor"]
        elif nivel_plano(nome) < nivel_plano(atual):
            rot, cor = "Incluído no seu plano", (60, 64, 78)
        else:
            rot, cor = f"Assinar {nome}", info["cor"]
        desenhar_botao(t, fonte_ui(14, True), br, rot, mouse, cor=cor)
        if nome != "Grátis" and nivel_plano(nome) >= nivel_plano(atual):
            hits.append((br, ("assinar", nome)))
    y += ch + 22
    # carteira
    t.blit(texto_cache("Carteira", 20, C_TEXTO, True), (area.x, y))
    bb = pygame.Rect(area.x + 120, y - 2, 290, 32)
    if pode_pegar_bonus():
        desenhar_botao(t, fonte_ui(14, True), bb, f"Pegar recompensa da semana (+{info_plano()['bonus']})", mouse,
                       cor=(200, 110, 40))
        hits.append((bb, ("bonus",)))
    else:
        t.blit(texto_cache("Recompensa desta semana já pega. Volte semana que vem!", 13, C_TEXTO2), (bb.x, bb.y + 8))
    t.blit(texto_cache(f"Vendas recebidas: {c.get('vendas', 0)}  ·  ganhou {fmt_brasas(c.get('ganho_vendas', 0))}",
                       13, C_TEXTO2), (bb.right + 20, y + 6))
    y += 40
    for h in reversed(c["historico"][-max(1, (area.bottom - y) // 20):]):
        cor = (110, 220, 140) if h["valor"] >= 0 else (240, 120, 120)
        t.blit(texto_cache(h["data"], 12, C_TEXTO2), (area.x + 4, y))
        t.blit(texto_cache(("+" if h["valor"] >= 0 else "") + str(h["valor"]), 13, cor, True), (area.x + 90, y))
        t.blit(texto_cache(h["motivo"], 13, C_TEXTO), (area.x + 150, y))
        y += 20
    return hits


# ----------------- codigo secreto -----------------
# Clique no cantinho de baixo, a direita, da tela Inicio e digite a senha.
# Para trocar a senha, rode no Python: import hashlib; print(hashlib.sha256(b"minha-engine:SUA_SENHA").hexdigest())
# e cole o resultado aqui.
SENHA_SECRETA = "f679180cc524c5e78522a1bbafac46b1f51ea464e2815d9364b3517a67dae1ef"
BRASAS_SECRETAS = 99999999


# Codigos promocionais (qualquer pessoa pode usar 1 vez). So o "hash" fica aqui, ninguem le o codigo.
# hash -> (brasas, plano, dias)
CODIGOS_PROMO = {
    "e28f60ad5830198d04257a697cf64fac9deace377424ae978ad12b8580050b68": (100, None, 0),
    "2b11d1dfd752a644744044a25c5a09f21a06d4efb9348c24362d2663b8f679cd": (150, None, 0),
    "b3a24736ad1eb45c7982098cb7b5121f5eb4b9a30a5dbefdfab905669f5330e8": (50, None, 0),
    "59aa344a422da22c85c531f60899c54902158ccf4a91a64a395ab2d603fff242": (75, None, 0),
    "03cce75ae15fd00ce3f49033f1ddab0ba8073c4a2d36f549a47db267052fff97": (0, "Game Maker", 7),
    "c98fc36c4e6087f18f2ef529c44012298ccdb83df76404ea382d7e02f889534e": (0, "Dev", 3),
}


def usar_codigo_secreto(senha):
    """O cantinho secreto do Inicio: aceita o codigo do dono e os codigos promocionais."""
    if carteira().get("_online"):
        try:
            r = rpc("usar_codigo", p_codigo=str(senha).strip()) or {}
            atualizar_carteira_online()
            return bool(r.get("ok")), r.get("msg", "")
        except ErroOnline as e:
            return False, str(e)
    if hashlib.sha256(("minha-engine:" + str(senha).strip()).encode()).hexdigest() == SENHA_SECRETA:
        movimentar(BRASAS_SECRETAS, "Código secreto")
        return True, f"Código secreto! +{fmt_brasas(BRASAS_SECRETAS)}"
    h = hashlib.sha256(("minha-engine-codigo:" + re.sub(r"\s", "", str(senha)).upper()).encode()).hexdigest()
    if h not in CODIGOS_PROMO:
        return False, "Código inválido."
    c = carteira()
    usados = c.setdefault("codigos_usados", [])
    if h in usados:
        return False, "Você já usou esse código."
    usados.append(h)
    brasas, plano, dias = CODIGOS_PROMO[h]
    partes = []
    if brasas:
        movimentar(brasas, "Código promocional")
        partes.append(f"+{fmt_brasas(brasas)}")
    if plano and nivel_plano(plano) >= nivel_plano():
        agora = _tempo.time()
        base = c["plano_ate"] if (plano_atual() == plano and c["plano_ate"] > agora) else agora
        c["plano"], c["plano_ate"] = plano, base + dias * 86400
        partes.append(f"{plano} por {dias} dias")
    salvar_carteira()
    return True, "Código aceito! " + " e ".join(partes)


def acao_carteira(acao):
    """Executa uma acao da pagina de planos. Devolve a mensagem para mostrar."""
    if acao[0] == "bonus":
        v = pegar_bonus()
        return (f"+{fmt_brasas(v)} de recompensa semanal! Volte semana que vem." if v
                else "Você já pegou a recompensa desta semana.")
    if acao[0] == "assinar":
        return assinar(acao[1])[1]
    return ""
