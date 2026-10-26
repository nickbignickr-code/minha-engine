# Minha Engine - midia.py
# imagens, fontes, sons e música
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Imagens e fontes
# ---------------------------------------------------------------------
_cache_img = {}
_cache_esc = {}
_fontes = {}


def carregar_imagem(nome):
    nome = str(nome or "").strip()
    if not nome:
        return None
    if nome in _cache_img:
        return _cache_img[nome]
    caminho = nome if os.path.isabs(nome) else os.path.join(PASTA_IMAGENS, nome)
    img = None
    if os.path.isfile(caminho):
        try:
            img = pygame.image.load(caminho)
            try:
                img = img.convert_alpha()
            except pygame.error:
                pass
        except (pygame.error, OSError):
            img = None
    _cache_img[nome] = img
    return img


def imagem_escalada(nome, w, h):
    chave = (nome, w, h)
    if chave in _cache_esc:
        return _cache_esc[chave]
    img = carregar_imagem(nome)
    if img is None:
        return None
    if len(_cache_esc) > 400:
        _cache_esc.clear()
    esc = pygame.transform.scale(img, (max(1, w), max(1, h)))
    _cache_esc[chave] = esc
    return esc


def limpar_cache_imagens():
    _cache_img.clear()
    _cache_esc.clear()
    _cache_obj.clear()


_cache_obj = {}
_cache_txt = {}


_cache_luz = {}


def gradiente_luz(raio, forca=255):
    """Circulo com transparencia suave: tira a escuridao no centro e vai sumindo na borda."""
    chave = (raio, forca)
    surf = _cache_luz.get(chave)
    if surf is None:
        if len(_cache_luz) > 60:
            _cache_luz.clear()
        surf = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        passo = max(1, raio // 40)
        for r in range(raio, 0, -passo):
            alpha = int(forca * (1 - r / raio) ** 0.7)
            pygame.draw.circle(surf, (0, 0, 0, alpha), (raio, raio), r)
        _cache_luz[chave] = surf
    return surf


def pintar_codigo(t, fc, cw, linha, x, y, suas=()):
    """Pinta uma linha de codigo Brasa com as cores escolhidas nas configuracoes."""
    cores = CONFIG["script"]["cores"]
    col = 0
    anterior = ""
    for m in RE_COR.finditer(linha):
        s = m.group(0)
        if m.group(1):
            cor = cores["comentarios"]
        elif m.group(2):
            cor = cores["textos"]
        elif m.group(3):
            cor = cores["numeros"]
        elif m.group(4):
            depois = linha[m.end():].lstrip()
            if s in PALAVRAS:
                cor = cores["palavras"]
            elif anterior == "quando" and s in EVENTOS_SCRIPT:
                cor = cores["eventos"]
            elif anterior == "funcao" or (s in suas and s not in NOMES_PRONTOS):
                cor = cores["suas_funcoes"]
            elif s in NOMES_PRONTOS or s in PLUGIN_FUNCOES:
                cor = cores["funcoes_prontas"]
            elif depois.startswith("("):
                cor = cores["suas_funcoes"]
            else:
                cor = cores["nomes"]
            anterior = s
        else:
            cor = cores["nomes"]
        if s.strip():
            t.blit(texto_cache_fonte(fc, s, tuple(cor)), (x + col * cw, y))
        col += len(s)


def texto_cache_fonte(f, txt, cor):
    chave = (id(f), txt, cor)
    img = _cache_txt.get(chave)
    if img is None:
        if len(_cache_txt) > 2500:
            _cache_txt.clear()
        img = f.render(txt, True, cor)
        _cache_txt[chave] = img
    return img


def texto_cache(txt, tam, cor, negrito=False):
    """Texto renderizado guardado em cache (renderizar texto todo quadro e lento)."""
    chave = (txt, int(num_seguro(tam, 20)), cor, negrito)
    img = _cache_txt.get(chave)
    if img is None:
        if len(_cache_txt) > 2500:
            _cache_txt.clear()
        img = fonte(tam, negrito).render(txt, True, cor)
        _cache_txt[chave] = img
    return img


def listar_imagens():
    try:
        return sorted(f for f in os.listdir(PASTA_IMAGENS) if f.lower().endswith(EXT_IMAGENS))
    except OSError:
        return []


def abrir_pasta(pasta):
    try:
        os.makedirs(pasta, exist_ok=True)
        if sys.platform.startswith("win"):
            os.startfile(pasta)
        elif sys.platform == "darwin":
            os.system(f'open "{pasta}"')
        else:
            os.system(f'xdg-open "{pasta}" >/dev/null 2>&1 &')
    except OSError:
        pass


# ---------------------------------------------------------------------
# Sons e musica (pasta "sons": wav, ogg, mp3)
# ---------------------------------------------------------------------
_sons = {}
_mixer = {"ok": None}


def mixer_pronto():
    if _mixer["ok"] is None:
        try:
            pygame.mixer.init()
            _mixer["ok"] = True
        except Exception:  # computador sem som, etc
            _mixer["ok"] = False
    return _mixer["ok"]


def caminho_som(nome):
    nome = str(nome or "").strip()
    return nome if os.path.isabs(nome) else os.path.join(PASTA_SONS, nome)


def tocar_som(nome, volume=1.0):
    if not nome or not mixer_pronto():
        return False
    som = _sons.get(nome)
    if som is None:
        p = caminho_som(nome)
        if not os.path.isfile(p):
            return False
        try:
            som = pygame.mixer.Sound(p)
        except Exception:
            return False
        _sons[nome] = som
    try:
        geral = CONFIG["geral"].get("volume_efeitos", 100) / 100.0
        som.set_volume(max(0.0, min(1.0, float(volume) * geral)))
        som.play()
    except Exception:
        return False
    return True


def tocar_musica(nome, volume=0.6, repetir=True):
    if not nome or not mixer_pronto():
        return False
    p = caminho_som(nome)
    if not os.path.isfile(p):
        return False
    try:
        pygame.mixer.music.load(p)
        geral = CONFIG["geral"].get("volume_musica", 60) / 60.0
        pygame.mixer.music.set_volume(max(0.0, min(1.0, float(volume) * geral)))
        pygame.mixer.music.play(-1 if repetir else 0)
    except Exception:
        return False
    return True


def parar_musica():
    if _mixer["ok"]:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass


def tocar_musica_da_cena(cena):
    musica = str(cena.get("musica", "") or "").strip()
    if musica:
        tocar_musica(musica)


def listar_sons():
    try:
        return sorted(f for f in os.listdir(PASTA_SONS) if f.lower().endswith(EXT_SONS))
    except OSError:
        return []


def fonte(tam, negrito=False):
    tam = max(6, min(200, int(num_seguro(tam, 20))))
    chave = (tam, negrito)
    if chave not in _fontes:
        _fontes[chave] = fonte_familia(familia_ui(), tam, negrito)
    return _fontes[chave]
