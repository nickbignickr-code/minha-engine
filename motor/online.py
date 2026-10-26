# Minha Engine - online.py
# Ligação com o servidor (Supabase): conta online, carteira no servidor, jogos e itens da Loja para o mundo todo
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# ONLINE (Supabase). So usa a biblioteca padrao do Python: nada para instalar.
# =====================================================================
import io as _io
import queue as _fila
import threading as _threading
import urllib.error as _urlerro
import urllib.parse as _urlparse
import urllib.request as _url
import zipfile as _zip

ONLINE_URL = os.environ.get("MINHA_ENGINE_URL", "https://nbvczeegziikjugbjpwd.supabase.co").rstrip("/")
ONLINE_CHAVE = os.environ.get("MINHA_ENGINE_CHAVE", "sb_publishable_wcvxV1M_rgx1RcDSOekbWA_MexJH005")
LIMITE_JOGO_MB = 45
_sessao = {}


class ErroOnline(Exception):
    pass


ERROS_TRADUZIDOS = [
    ("could not find the function", "O servidor ainda não está pronto: falta rodar o código no SQL Editor do Supabase."),
    ("could not find the table", "O servidor ainda não está pronto: falta rodar o código no SQL Editor do Supabase."),
    ("schema cache", "O servidor ainda não está pronto: falta rodar o código no SQL Editor do Supabase."),
    ("signups not allowed", "O cadastro está desligado no Supabase (Authentication > Sign In / Providers)."),
    ("is invalid", "Esse e-mail não foi aceito. Use um e-mail de verdade (ex: seunome@gmail.com)."),
    ("invalid api key", "Chave do servidor errada."),
    ("certificate", "Erro de certificado de segurança (SSL) no Windows."),
    ("invalid login credentials", "E-mail ou senha errados."),
    ("invalid_credentials", "E-mail ou senha errados."),
    ("email not confirmed", "Falta confirmar o e-mail: abra a mensagem que chegou na sua caixa de entrada e clique no link."),
    ("user already registered", "Esse e-mail já tem conta. Use 'Entrar'."),
    ("password should be at least", "A senha precisa ter pelo menos 6 caracteres."),
    ("weak_password", "Senha fraca: use pelo menos 6 caracteres."),
    ("invalid format", "E-mail inválido."),
    ("validate email", "E-mail inválido."),
    ("rate limit", "Muitas tentativas seguidas. Espere alguns minutos e tente de novo."),
    ("over_email_send_rate_limit", "Muitos e-mails enviados. Espere alguns minutos e tente de novo."),
    ("row-level security", "Você não tem permissão para isso (ou chegou no limite do seu plano)."),
    ("permission denied", "Você não tem permissão para isso."),
    ("database error saving new user", "Não consegui criar a conta. Tente outro nome."),
    ("jwt expired", "Sua sessão expirou. Entre de novo."),
    ("refresh token", "Sua sessão expirou. Entre de novo."),
    ("payload too large", f"O jogo ficou grande demais (máximo {LIMITE_JOGO_MB} MB)."),
    ("maximum allowed size", f"O jogo ficou grande demais (máximo {LIMITE_JOGO_MB} MB)."),
]


def traduzir_erro(txt):
    baixo = str(txt).lower()
    for chave, msg in ERROS_TRADUZIDOS:
        if chave in baixo:
            return msg
    return str(txt)[:160] or "Erro no servidor."


# ----------------- sessao (fica salva em sessao_online.json) -----------------
def arquivo_sessao():
    return os.path.join(PASTA, "sessao_online.json")


def carregar_sessao():
    _sessao.clear()
    try:
        with open(arquivo_sessao(), encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict) and d.get("refresh_token") and d.get("id"):
            _sessao.update(d)
    except (OSError, ValueError):
        pass
    return bool(_sessao)


def salvar_sessao():
    try:
        if _sessao:
            with open(arquivo_sessao(), "w", encoding="utf-8") as f:
                json.dump(_sessao, f)
        elif os.path.exists(arquivo_sessao()):
            os.remove(arquivo_sessao())
    except OSError:
        pass


def online_ativo():
    return bool(_sessao.get("refresh_token"))


def guardar_sessao(d):
    user = d.get("user") or {}
    _sessao.update({"access_token": d["access_token"], "refresh_token": d["refresh_token"],
                    "expira": _tempo.time() + int(d.get("expires_in") or 3600) - 60,
                    "id": user.get("id", _sessao.get("id")), "email": user.get("email", _sessao.get("email", ""))})
    salvar_sessao()


# ----------------- HTTP -----------------
def registrar_erro_online(metodo, caminho, detalhe):
    """Guarda o erro em online_erros.txt (sem senha) para dar para descobrir o problema."""
    try:
        with open(os.path.join(PASTA, "online_erros.txt"), "a", encoding="utf-8") as f:
            f.write(f"{_tempo.strftime('%d/%m %H:%M:%S')}  {metodo} {caminho.split('?')[0]}  ->  {str(detalhe)[:600]}\n")
    except OSError:
        pass


def _pedido(metodo, caminho, corpo=None, token=None, cabecalhos=None, timeout=25):
    cab = {"apikey": ONLINE_CHAVE}
    if token:
        cab["Authorization"] = "Bearer " + token
    dados = None
    if isinstance(corpo, (dict, list)):
        dados = json.dumps(corpo).encode("utf-8")
        cab["Content-Type"] = "application/json"
    elif isinstance(corpo, bytes):
        dados = corpo
    cab.update(cabecalhos or {})
    req = _url.Request(ONLINE_URL + caminho, data=dados, method=metodo, headers=cab)
    try:
        with _url.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except _urlerro.HTTPError as e:
        bruto = e.read()
        try:
            d = json.loads(bruto or b"{}")
            msg = d.get("msg") or d.get("message") or d.get("error_description") or d.get("error") or bruto
            codigo = d.get("error_code") or d.get("code") or ""
        except ValueError:
            msg, codigo = bruto.decode("utf-8", "replace"), ""
        registrar_erro_online(metodo, caminho, f"HTTP {e.code}: {bruto[:500].decode('utf-8', 'replace')}")
        raise ErroOnline(traduzir_erro(f"{msg} {codigo}")) from None
    except (_urlerro.URLError, TimeoutError, OSError) as e:
        motivo = getattr(e, "reason", e)
        registrar_erro_online(metodo, caminho, f"{type(e).__name__}: {motivo!r}")
        if "certificate" in str(motivo).lower() or "ssl" in str(motivo).lower():
            raise ErroOnline("Erro de certificado de segurança (SSL) ao falar com o servidor.") from None
        raise ErroOnline("Sem internet (ou o servidor está fora do ar). Tente de novo daqui a pouco.") from None


def renovar_sessao():
    if not _sessao.get("refresh_token"):
        raise ErroOnline("Entre na sua conta primeiro.")
    try:
        _, bruto = _pedido("POST", "/auth/v1/token?grant_type=refresh_token",
                           {"refresh_token": _sessao["refresh_token"]})
    except ErroOnline as e:
        if "expirou" in str(e) or "senha" in str(e):
            _sessao.clear()
            salvar_sessao()
        raise
    guardar_sessao(json.loads(bruto))


def token_valido():
    if not online_ativo():
        return None
    if not _sessao.get("access_token") or _sessao.get("expira", 0) < _tempo.time():
        renovar_sessao()
    return _sessao["access_token"]


def api(metodo, caminho, corpo=None, cabecalhos=None, bruto=False, timeout=25, com_conta=True):
    token = token_valido() if com_conta else None
    _, dados = _pedido(metodo, caminho, corpo, token, cabecalhos, timeout)
    if bruto:
        return dados
    return json.loads(dados) if dados else None


def rpc(nome, **args):
    return api("POST", f"/rest/v1/rpc/{nome}", args)


def q(valor):
    return _urlparse.quote(str(valor), safe="")


# ----------------- conta -----------------
def cadastrar_online(nome, email, senha):
    nome = re.sub(r"\s+", " ", str(nome)).strip()
    if not 2 <= len(nome) <= 24:
        raise ErroOnline("O nome precisa ter de 2 a 24 letras.")
    if not api("POST", "/rest/v1/rpc/nome_livre", {"p_nome": nome}, com_conta=False):
        raise ErroOnline(f"O nome '{nome}' já é de outra pessoa. Escolha outro.")
    _, bruto = _pedido("POST", "/auth/v1/signup", {"email": email.strip(), "password": senha, "data": {"nome": nome}})
    d = json.loads(bruto or b"{}")
    if d.get("access_token"):
        _sessao.clear()
        _sessao["nome_pendente"] = nome
        guardar_sessao(d)
        atualizar_carteira_online()
        return "Conta criada! Você ganhou 150 Brasas de boas-vindas."
    return (f"Conta criada! Mandamos um e-mail para {email.strip()}: clique no link dele e depois use 'Entrar'. "
            f"(Se não chegar, olhe o spam.)")


def entrar_online(email, senha):
    _, bruto = _pedido("POST", "/auth/v1/token?grant_type=password", {"email": email.strip(), "password": senha})
    _sessao.clear()
    guardar_sessao(json.loads(bruto))
    atualizar_carteira_online()
    return f"Oi, {_sessao.get('nome', '')}! Você está online."


def sair_online():
    try:
        if _sessao.get("access_token"):
            _pedido("POST", "/auth/v1/logout", {}, _sessao.get("access_token"), timeout=8)
    except ErroOnline:
        pass
    _sessao.clear()
    salvar_sessao()
    _carteira.clear()
    _usuario.clear()


def esqueci_senha(email):
    _pedido("POST", "/auth/v1/recover", {"email": email.strip()})
    return f"Se existir conta com {email.strip()}, chegou um e-mail para trocar a senha."


def usuario_online():
    return {"id": _sessao.get("id", ""), "nome": _sessao.get("nome") or (_sessao.get("email", "?").split("@")[0]),
            "email": _sessao.get("email", ""), "cor": [46, 168, 98], "online": True}


def atualizar_carteira_online():
    d = rpc("minha_carteira") or {}
    if not d:                       # conta nova (ou feita em outro lugar): cria o perfil
        rpc("garantir_perfil", p_nome=_sessao.get("nome_pendente", ""))
        d = rpc("minha_carteira") or {}
    if not d:
        raise ErroOnline("Não achei o seu perfil no servidor.")
    _sessao["nome"] = d.get("nome", "")
    _sessao.pop("nome_pendente", None)
    salvar_sessao()
    comprados = []
    for item in d.get("comprados") or []:
        comprados.append(item if str(item).startswith("loja:") else "com:" + str(item))
    _carteira.clear()
    _carteira.update(carteira_padrao())
    _carteira.update({"saldo": int(d.get("saldo") or 0), "plano": d.get("plano") or "Grátis",
                      "plano_ate": float(d.get("plano_ate") or 0), "ultimo_bonus": d.get("ultima_recompensa") or "",
                      "semana": d.get("semana") or "", "comprados": comprados,
                      "conquistas": list(d.get("conquistas") or []), "historico": list(d.get("historico") or []),
                      "id_criador": d.get("id", ""), "vendas": int(d.get("vendas") or 0), "_online": True})
    return _carteira


def renomear_online(novo):
    r = rpc("renomear", p_nome=novo) or {}
    if r.get("ok"):
        atualizar_carteira_online()
    return r.get("msg", "")


# ----------------- tarefas em segundo plano (para a tela nao travar) -----------------
_prontas = _fila.Queue()


def em_segundo_plano(fn, ao_terminar=None, *args):
    def rodar():
        try:
            res, erro = fn(*args), None
        except ErroOnline as e:
            res, erro = None, str(e)
        except Exception as e:      # noqa: BLE001 - nunca derrubar a engine por causa da internet
            res, erro = None, f"Erro: {e}"
        _prontas.put((ao_terminar, res, erro))
    _threading.Thread(target=rodar, daemon=True).start()


def processar_tarefas():
    while True:
        try:
            fn, res, erro = _prontas.get_nowait()
        except _fila.Empty:
            return
        if fn:
            try:
                fn(res, erro)
            except Exception as e:      # noqa: BLE001
                print("Minha Engine (online):", e)


# ----------------- jogos publicados online -----------------
def pasta_cache_online(*partes):
    p = os.path.join(PASTA, "cache_online", *partes)
    os.makedirs(p if not os.path.splitext(p)[1] else os.path.dirname(p), exist_ok=True)
    return p


def url_publica(caminho):
    return f"{ONLINE_URL}/storage/v1/object/public/jogos/{_urlparse.quote(caminho)}"


def _epoca(txt):
    import datetime
    try:
        return datetime.datetime.fromisoformat(str(txt).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def listar_publicados_online():
    linhas = api("GET", "/rest/v1/jogos?select=id,titulo,descricao,arquivo,miniatura,visitas,likes,publicado,"
                        "atualizado,autor,perfis!jogos_autor_fkey(nome)&order=atualizado.desc&limit=300") or []
    curti, visitei = set(), set()
    if online_ativo():
        curti = {x["jogo"] for x in api("GET", "/rest/v1/likes?select=jogo&limit=1000") or []}
        visitei = {x["jogo"] for x in api("GET", "/rest/v1/visitas?select=jogo&limit=1000") or []}
    meu = _sessao.get("id")
    pasta_mini = pasta_cache_online("miniaturas")
    res = []
    for j in linhas:
        res.append({"id": j["id"], "titulo": j["titulo"], "nome": j["titulo"], "desc": j.get("descricao", ""),
                    "autor": (j.get("perfis") or {}).get("nome", "?"), "autor_id": j["autor"],
                    "n_visitas": int(j.get("visitas") or 0), "n_likes": int(j.get("likes") or 0),
                    "atualizado": _epoca(j.get("atualizado")), "arquivo": j["arquivo"],
                    "miniatura_url": j.get("miniatura") or "", "online": True, "eu_curti": j["id"] in curti,
                    "eu_visitei": j["id"] in visitei, "meu": j["autor"] == meu,
                    "pasta": os.path.join(PASTA, "cache_online", "jogos", j["id"]),
                    "miniatura": os.path.join(pasta_mini, j["id"] + ".png")})
    return res


def baixar_miniatura(m):
    if not m.get("miniatura_url") or os.path.isfile(m["miniatura"]):
        return m["miniatura"]
    dados = api("GET", f"/storage/v1/object/public/jogos/{_urlparse.quote(m['miniatura_url'])}", bruto=True,
                com_conta=False, timeout=15)
    with open(m["miniatura"], "wb") as f:
        f.write(dados)
    return m["miniatura"]


def _zipar_projeto(pasta):
    buf = _io.BytesIO()
    with _zip.ZipFile(buf, "w", _zip.ZIP_DEFLATED) as z:
        z.write(os.path.join(pasta, "projeto.json"), "projeto.json")
        for sub in ("imagens", "sons"):
            raiz = os.path.join(pasta, sub)
            for atual, _, arquivos in os.walk(raiz):
                for a in arquivos:
                    caminho = os.path.join(atual, a)
                    z.write(caminho, os.path.relpath(caminho, pasta).replace(os.sep, "/"))
    dados = buf.getvalue()
    if len(dados) > LIMITE_JOGO_MB * 1024 * 1024:
        raise ErroOnline(f"O jogo tem {len(dados) // (1024 * 1024)} MB. O máximo é {LIMITE_JOGO_MB} MB "
                         f"(tire sons ou imagens grandes).")
    return dados


def publicacao_online_de(pasta_projeto):
    try:
        with open(os.path.join(pasta_projeto, "publicado_online.json"), encoding="utf-8") as f:
            d = json.load(f)
        return d if d.get("conta") == _sessao.get("id") else None
    except (OSError, ValueError):
        return None


def publicar_online(pasta_projeto, titulo=None, desc=""):
    """Envia o jogo para o servidor (ou atualiza). Devolve a mensagem."""
    if not online_ativo():
        raise ErroOnline("Entre na sua conta online primeiro (Início > clique no seu nome).")
    with open(os.path.join(pasta_projeto, "projeto.json"), encoding="utf-8") as f:
        dados = completar_projeto(json.load(f))
    if not any(d.get("tipo") == "Player" for d in dados["fases"][dados["fase_inicial"]]["objetos"]):
        raise ErroOnline("O jogo precisa ter um Player na fase inicial para ser publicado.")
    titulo = (titulo or dados.get("nome_projeto") or "Meu jogo")[:40]
    uid = _sessao["id"]
    pub = publicacao_online_de(pasta_projeto)
    existe = None
    if pub:
        existe = api("GET", f"/rest/v1/jogos?select=id,arquivo,miniatura&id=eq.{q(pub['id'])}") or None
        existe = existe[0] if existe else None
    nome_base = existe["arquivo"].rsplit("/", 1)[-1].rsplit(".", 1)[0] if existe else os.urandom(8).hex()
    arquivo = f"{uid}/{nome_base}.zip"
    api("POST", f"/storage/v1/object/jogos/{_urlparse.quote(arquivo)}", _zipar_projeto(pasta_projeto),
        {"Content-Type": "application/zip", "x-upsert": "true"}, timeout=180)
    mini = ""
    caminho_mini = os.path.join(pasta_projeto, "miniatura.png")
    if os.path.isfile(caminho_mini):
        mini = f"{uid}/{nome_base}.png"
        with open(caminho_mini, "rb") as f:
            api("POST", f"/storage/v1/object/jogos/{_urlparse.quote(mini)}", f.read(),
                {"Content-Type": "image/png", "x-upsert": "true"}, timeout=60)
    import datetime
    agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    linha = {"titulo": titulo, "descricao": str(desc)[:200], "arquivo": arquivo, "miniatura": mini}
    if existe:
        api("PATCH", f"/rest/v1/jogos?id=eq.{q(existe['id'])}", dict(linha, atualizado=agora),
            {"Prefer": "return=minimal"})
        jid, novo = existe["id"], False
    else:
        criado = api("POST", "/rest/v1/jogos", linha, {"Prefer": "return=representation"})
        jid, novo = criado[0]["id"], True
    with open(os.path.join(pasta_projeto, "publicado_online.json"), "w", encoding="utf-8") as f:
        json.dump({"id": jid, "conta": uid}, f)
    if novo:
        v = rpc("conquista", p_chave="primeiro_jogo_publicado") or 0
        if v:
            NOVIDADES_CARTEIRA.append(f"+{fmt_brasas(v)}: Publicou o primeiro jogo!")
    return (f"'{titulo}' está online para o mundo todo! " if novo else f"'{titulo}' foi atualizado online. ") + \
        f"Cada visita dá +{BRASAS_VISITA} e cada like +{BRASAS_LIKE} {MOEDA}."


def baixar_jogo_online(m):
    """Baixa (se mudou) e devolve a pasta pronta para jogar."""
    pasta = m["pasta"]
    marca = os.path.join(pasta, ".versao")
    versao = f"{m['arquivo']}|{m.get('atualizado')}"
    try:
        with open(marca, encoding="utf-8") as f:
            if f.read() == versao and os.path.isfile(os.path.join(pasta, "projeto.json")):
                return pasta
    except OSError:
        pass
    dados = api("GET", f"/storage/v1/object/public/jogos/{_urlparse.quote(m['arquivo'])}", bruto=True,
                com_conta=False, timeout=180)
    shutil.rmtree(pasta, ignore_errors=True)
    os.makedirs(pasta, exist_ok=True)
    raiz = os.path.abspath(pasta)
    with _zip.ZipFile(_io.BytesIO(dados)) as z:
        for info in z.infolist():
            destino = os.path.abspath(os.path.join(pasta, info.filename))
            if not destino.startswith(raiz + os.sep) or info.is_dir():
                continue            # protege contra zip malicioso (../../)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with z.open(info) as src, open(destino, "wb") as dst:
                shutil.copyfileobj(src, dst)
    with open(marca, "w", encoding="utf-8") as f:
        f.write(versao)
    return pasta


def visitar_online(m):
    if not online_ativo():
        return 0
    v = rpc("registrar_visita", p_jogo=m["id"]) or 0
    if v:
        m["n_visitas"] += 1
        m["eu_visitei"] = True
    return v


def curtir_online(m):
    r = rpc("curtir", p_jogo=m["id"]) or {}
    if r.get("ok"):
        m["n_likes"] += 1
        m["eu_curti"] = True
    return r.get("msg", "")


def denunciar_online(m, motivo):
    return rpc("denunciar", p_jogo=m["id"], p_motivo=motivo) or ""


def despublicar_online(m):
    api("DELETE", f"/rest/v1/jogos?id=eq.{q(m['id'])}", cabecalhos={"Prefer": "return=minimal"})
    for caminho in (m.get("arquivo"), m.get("miniatura_url")):
        if caminho:
            try:
                api("DELETE", f"/storage/v1/object/jogos/{_urlparse.quote(caminho)}")
            except ErroOnline:
                pass


# ----------------- itens da Loja (comunidade) online -----------------
def listar_itens_online():
    linhas = api("GET", "/rest/v1/itens_venda?select=id,autor,nome,descricao,categoria,preco,vendas,pacote,"
                        "perfis!itens_venda_autor_fkey(nome)&order=criado.desc&limit=300") or []
    meu = _sessao.get("id")
    res = []
    for i in linhas:
        pac = i.get("pacote") or {}
        res.append({"formato": "minha-engine-item", "id": i["id"], "nome": i["nome"], "desc": i.get("descricao", ""),
                    "cat": i.get("categoria", "Outros"), "preco": int(i.get("preco") or 0),
                    "autor": (i.get("perfis") or {}).get("nome", "?"), "autor_id": i["autor"],
                    "objetos": pac.get("objetos") or [], "imagens": pac.get("imagens") or {},
                    "vendas": int(i.get("vendas") or 0), "_meu": i["autor"] == meu, "_online": True})
    return [p for p in res if p["objetos"]]


def vender_online(pacote):
    api("POST", "/rest/v1/itens_venda", {"nome": pacote["nome"], "descricao": pacote["desc"],
                                         "categoria": pacote["cat"], "preco": pacote["preco"],
                                         "pacote": {"objetos": pacote["objetos"], "imagens": pacote["imagens"]}},
        {"Prefer": "return=minimal"})


def mudar_preco_online(item_id, preco):
    api("PATCH", f"/rest/v1/itens_venda?id=eq.{q(item_id)}", {"preco": int(preco)}, {"Prefer": "return=minimal"})


def tirar_item_online(item_id):
    api("DELETE", f"/rest/v1/itens_venda?id=eq.{q(item_id)}", cabecalhos={"Prefer": "return=minimal"})
