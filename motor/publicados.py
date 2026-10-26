# Minha Engine - publicados.py
# Área de JOGOS PUBLICADOS: publicar, jogar (visita = Brasas para o autor) e curtir (like = Brasas)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# JOGOS PUBLICADOS (ficam na pasta publicados/, neste computador)
# =====================================================================
# Cada jogo publicado e uma COPIA do projeto (o original continua editavel) + meta.json com
# titulo, autor, descricao, quem visitou e quem curtiu. Visita e like valem 1 vez por usuario.


def pasta_publicados():
    return os.path.join(PASTA, "publicados")


def listar_publicados():
    res = []
    try:
        nomes = os.listdir(pasta_publicados())
    except OSError:
        return res
    for n in nomes:
        pasta = os.path.join(pasta_publicados(), n)
        try:
            with open(os.path.join(pasta, "meta.json"), encoding="utf-8") as f:
                m = json.load(f)
        except (OSError, ValueError):
            continue
        if not isinstance(m, dict) or not os.path.isfile(os.path.join(pasta, "projeto.json")):
            continue
        m.setdefault("visitas", [])
        m.setdefault("likes", [])
        m["_pasta"] = pasta
        m["pasta"] = pasta
        m["miniatura"] = os.path.join(pasta, "miniatura.png")
        m["nome"] = m.get("titulo", n)
        res.append(m)
    return res


def salvar_meta(m):
    dados = {k: v for k, v in m.items() if not k.startswith("_") and k not in ("pasta", "miniatura", "nome")}
    with open(os.path.join(m["_pasta"], "meta.json"), "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=1, ensure_ascii=False)


def publicacao_de(pasta_projeto):
    """A publicacao deste projeto feita pelo usuario atual (ou None)."""
    uid = usuario_atual()["id"]
    alvo = os.path.normcase(os.path.abspath(pasta_projeto))
    for m in listar_publicados():
        if m.get("autor_id") == uid and os.path.normcase(os.path.abspath(m.get("origem", ""))) == alvo:
            return m
    return None


def publicar_projeto(pasta_projeto, titulo=None, desc=""):
    """Publica (ou atualiza) o projeto. Mantem visitas e likes se ja estava publicado."""
    arq = os.path.join(pasta_projeto, "projeto.json")
    with open(arq, encoding="utf-8") as f:
        dados = completar_projeto(json.load(f))
    if not any(d.get("tipo") == "Player" for d in dados["fases"][dados["fase_inicial"]]["objetos"]):
        raise ValueError("O jogo precisa ter um Player na fase inicial para ser publicado.")
    u = usuario_atual()
    m = publicacao_de(pasta_projeto)
    if m is None:
        pid = os.urandom(6).hex()
        destino = os.path.join(pasta_publicados(), pid)
        m = {"id": pid, "visitas": [], "likes": [], "publicado": _tempo.time(), "_pasta": destino}
    destino = m["_pasta"]
    os.makedirs(destino, exist_ok=True)
    shutil.copyfile(arq, os.path.join(destino, "projeto.json"))
    for sub in ("imagens", "sons"):
        origem = os.path.join(pasta_projeto, sub)
        if os.path.isdir(origem):
            shutil.copytree(origem, os.path.join(destino, sub), dirs_exist_ok=True)
    mini = os.path.join(pasta_projeto, "miniatura.png")
    if os.path.isfile(mini):
        shutil.copyfile(mini, os.path.join(destino, "miniatura.png"))
    m.update({"titulo": (titulo or dados.get("nome_projeto") or "Meu jogo")[:40], "desc": str(desc)[:200],
              "autor": u["nome"], "autor_id": u["id"], "origem": os.path.abspath(pasta_projeto),
              "atualizado": _tempo.time(),
              "fases": len(dados["fases"])})
    salvar_meta(m)
    return m


def despublicar(m):
    shutil.rmtree(m["_pasta"], ignore_errors=True)


def e_meu(m):
    return m.get("autor_id") == usuario_atual()["id"]


def registrar_visita(m):
    """Chamado quando alguem joga o jogo publicado. Devolve as Brasas que o autor ganhou (0 se nao conta)."""
    uid = usuario_atual()["id"]
    if e_meu(m) or uid in m["visitas"]:
        return 0
    m["visitas"].append(uid)
    salvar_meta(m)
    creditar(m["autor_id"], BRASAS_VISITA, f"Visita de {nome_usuario()} em '{m.get('titulo')}'")
    return BRASAS_VISITA


def dar_like(m):
    """Devolve (deu_certo, mensagem)."""
    uid = usuario_atual()["id"]
    if e_meu(m):
        return False, "Você não pode curtir o seu próprio jogo."
    if uid in m["likes"]:
        return False, "Você já curtiu esse jogo."
    m["likes"].append(uid)
    salvar_meta(m)
    creditar(m["autor_id"], BRASAS_LIKE, f"Like de {nome_usuario()} em '{m.get('titulo')}'")
    return True, f"Curtiu '{m.get('titulo')}'! {m.get('autor')} ganhou {fmt_brasas(BRASAS_LIKE)}."


def desenhar_coracao(t, centro, tam=7, cheio=True, cor=(235, 70, 100)):
    cx, cy = centro
    r = max(2, tam // 2)
    pontos = [(cx - tam, cy - r // 2), (cx, cy + tam), (cx + tam, cy - r // 2)]
    if cheio:
        pygame.draw.circle(t, cor, (cx - r, cy - r // 2), r)
        pygame.draw.circle(t, cor, (cx + r, cy - r // 2), r)
        pygame.draw.polygon(t, cor, pontos)
    else:
        pygame.draw.circle(t, cor, (cx - r, cy - r // 2), r, 2)
        pygame.draw.circle(t, cor, (cx + r, cy - r // 2), r, 2)
        pygame.draw.lines(t, cor, False, pontos, 2)
