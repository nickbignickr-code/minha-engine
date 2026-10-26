# Minha Engine - projetos.py
# pastas dos projetos, migração, miniaturas
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Projetos: cada um numa pasta propria (projetos/<nome>/) com suas imagens e sons
# ---------------------------------------------------------------------
def definir_projeto(pasta):
    """Aponta a engine para a pasta de um projeto."""
    global ARQUIVO, ARQUIVO_AUTOSAVE, ARQUIVO_SAVEGAME, PASTA_IMAGENS, PASTA_SONS
    ARQUIVO = os.path.join(pasta, "projeto.json")
    ARQUIVO_AUTOSAVE = os.path.join(pasta, "projeto_autosave.json")
    ARQUIVO_SAVEGAME = os.path.join(pasta, "savegame.json")
    PASTA_IMAGENS = os.path.join(pasta, "imagens")
    PASTA_SONS = os.path.join(pasta, "sons")
    for p in (pasta, PASTA_IMAGENS, PASTA_SONS):
        try:
            os.makedirs(p, exist_ok=True)
        except OSError:
            pass
    limpar_cache_imagens()
    _sons.clear()


def nome_pasta_livre(nome):
    base = re.sub(r'[\\/:*?"<>|]', "", str(nome)).strip().strip(".") or "Projeto"
    os.makedirs(PASTA_PROJETOS, exist_ok=True)
    candidato, i = base, 2
    while os.path.exists(os.path.join(PASTA_PROJETOS, candidato)):
        candidato = f"{base} {i}"
        i += 1
    return os.path.join(PASTA_PROJETOS, candidato)


def listar_projetos():
    """Lista as criacoes: [{pasta, nome, mudado, fases, objetos, miniatura}]"""
    res = []
    try:
        pastas = os.listdir(PASTA_PROJETOS)
    except OSError:
        return res
    for nome in pastas:
        pasta = os.path.join(PASTA_PROJETOS, nome)
        arq = os.path.join(pasta, "projeto.json")
        if not os.path.isfile(arq):
            continue
        info = {"pasta": pasta, "nome": nome, "mudado": os.path.getmtime(arq), "fases": 0, "objetos": 0,
                "miniatura": os.path.join(pasta, "miniatura.png")}
        try:
            with open(arq, encoding="utf-8") as f:
                dados = json.load(f)
            info["nome"] = str(dados.get("nome_projeto") or nome)
            fases = dados.get("fases") or {"Fase 1": {"objetos": dados.get("objetos", [])}}
            info["fases"] = len(fases)
            info["objetos"] = sum(len(fz.get("objetos", [])) for fz in fases.values())
        except (OSError, ValueError, AttributeError):
            info["nome"] += " (arquivo com erro)"
        res.append(info)
    return res


def criar_projeto(nome, modelo=None):
    pasta = nome_pasta_livre(nome)
    os.makedirs(pasta, exist_ok=True)
    if modelo in EXEMPLOS:
        proj = completar_projeto(EXEMPLOS[modelo]())
    else:
        proj = {"fases": {"Fase 1": fase_padrao()}, "fase_atual": "Fase 1", "fase_inicial": "Fase 1", "modelos": {}}
        proj["fases"]["Fase 1"]["objetos"].append(nova_entidade("Player", 80, 400))
        proj = completar_projeto(proj)
    proj["nome_projeto"] = str(nome).strip() or os.path.basename(pasta)
    for fase in proj["fases"].values():
        if fase["cena"].get("titulo") in ("Meu Jogo", ""):
            fase["cena"]["titulo"] = proj["nome_projeto"]
    for sub in ("imagens", "sons"):
        os.makedirs(os.path.join(pasta, sub), exist_ok=True)
    for arte in proj.pop("_artes", []):       # pixel arts prontas que o exemplo usa
        try:
            pygame.image.save(superficie_arte(ARTES[arte]), os.path.join(pasta, "imagens", arte + ".png"))
        except (KeyError, pygame.error, OSError):
            pass
    with open(os.path.join(pasta, "projeto.json"), "w", encoding="utf-8") as f:
        json.dump(proj, f, indent=2, ensure_ascii=False)
    try:
        gerar_miniatura(proj, os.path.join(pasta, "miniatura.png"))
    except (pygame.error, OSError):
        pass
    return pasta


def migrar_projeto_antigo():
    """O projeto.json antigo (ao lado da engine) vira 'Meu primeiro projeto' UMA VEZ SO.
    Depois o arquivo antigo e renomeado, para nao voltar quando voce apagar o projeto."""
    antigo = os.path.join(PASTA, "projeto.json")
    if not os.path.isfile(antigo):
        return
    if CONFIG["geral"].get("migrado") or listar_projetos():
        marcar_migrado(antigo)
        return
    pasta = nome_pasta_livre("Meu primeiro projeto")
    os.makedirs(pasta, exist_ok=True)
    shutil.copyfile(antigo, os.path.join(pasta, "projeto.json"))
    for sub in ("imagens", "sons"):
        origem = os.path.join(PASTA, sub)
        if os.path.isdir(origem):
            shutil.copytree(origem, os.path.join(pasta, sub), dirs_exist_ok=True)
    marcar_migrado(antigo)


def marcar_migrado(antigo):
    CONFIG["geral"]["migrado"] = True
    salvar_config()
    try:
        os.replace(antigo, os.path.join(PASTA, "projeto_antigo (ja importado).json"))
    except OSError:
        pass


def gerar_miniatura(projeto, caminho, tam=(320, 180)):
    """Desenha uma foto pequena da fase inicial (em volta do player) para o Início."""
    proj = completar_projeto(copy.deepcopy(projeto))
    fase = proj["fases"].get(proj.get("fase_inicial")) or next(iter(proj["fases"].values()))
    surf = criar_miniatura(fase, tam)
    pygame.image.save(surf, caminho)


def criar_miniatura(fase, tam=(320, 180)):
    surf = pygame.Surface(tam)
    surf.fill(cor_ok(fase["cena"].get("fundo", [25, 28, 45])))
    k = tam[0] / 960
    objs = [d for d in fase["objetos"] if not d.get("na_tela")]
    player = next((d for d in objs if d.get("tipo") == "Player"), None)
    if player is not None:
        cx, cy = num_seguro(player["x"]) + 16, num_seguro(player["y"]) + 24
    elif objs:
        cx, cy = num_seguro(objs[0]["x"]), num_seguro(objs[0]["y"])
    else:
        cx, cy = 480, 270
    cam_x, cam_y = cx - 300, cy - 270
    for d in sorted(objs, key=lambda d: num_seguro(d.get("camada", 0))):
        r = pygame.Rect(round((num_seguro(d["x"]) - cam_x) * k), round((num_seguro(d["y"]) - cam_y) * k),
                        max(1, round(num_seguro(d.get("w", 40), 40) * k)), max(1, round(num_seguro(d.get("h", 40), 40) * k)))
        if r.right < 0 or r.x > tam[0] or r.bottom < 0 or r.y > tam[1]:
            continue
        try:
            desenhar_obj(surf, d, r, editor=False)
        except (pygame.error, ValueError, TypeError):
            pass
    escuro = int(num_seguro(fase["cena"].get("escuridao", 0)))
    if escuro > 0:
        sombra = pygame.Surface(tam, pygame.SRCALPHA)
        sombra.fill((0, 0, 0, min(200, escuro)))
        surf.blit(sombra, (0, 0))
    return surf
