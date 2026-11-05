# Minha Engine - polimento.py
# Deixa a interface mais FLUIDA e BONITA:
#  - temas de cores (Grafite, Meia-noite, Carvão, Floresta, Vinho)
#  - movimento suave (rolagem, abas, janelas que abrem) — dá para desligar em Configurações
#  - botões com brilho suave ao passar o mouse e ícones desenhados
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.
import time as _relogio_ui

# =====================================================================
# TEMAS
# =====================================================================
TEMAS_UI = {
    "Grafite": {"fundo": (30, 32, 38), "painel": (40, 43, 51), "borda": (62, 66, 78), "botao": (56, 60, 72),
                "campo": (25, 27, 33), "texto": (228, 229, 234), "texto2": (150, 153, 167)},
    "Meia-noite": {"fundo": (19, 23, 35), "painel": (27, 32, 49), "borda": (50, 58, 84), "botao": (43, 51, 77),
                   "campo": (15, 18, 29), "texto": (226, 231, 245), "texto2": (140, 150, 180)},
    "Carvão": {"fundo": (23, 23, 24), "painel": (33, 33, 35), "borda": (58, 58, 61), "botao": (52, 52, 55),
               "campo": (17, 17, 18), "texto": (232, 232, 232), "texto2": (150, 150, 152)},
    "Floresta": {"fundo": (22, 31, 27), "painel": (31, 42, 36), "borda": (55, 73, 63), "botao": (47, 63, 55),
                 "campo": (17, 24, 20), "texto": (226, 236, 230), "texto2": (140, 162, 150)},
    "Vinho": {"fundo": (33, 23, 29), "painel": (45, 31, 39), "borda": (77, 53, 65), "botao": (65, 45, 57),
              "campo": (25, 17, 22), "texto": (238, 228, 233), "texto2": (166, 145, 156)},
}
APARENCIA_PADRAO["tema"] = "Grafite"
APARENCIA_PADRAO["animacoes"] = True
_aplicar_aparencia_antiga = aplicar_aparencia


def aplicar_aparencia():
    global C_FUNDO_UI, C_PAINEL, C_BORDA, C_BOTAO, C_CAMPO, C_TEXTO, C_TEXTO2
    _aplicar_aparencia_antiga()
    tema = TEMAS_UI.get(CONFIG.get("aparencia", {}).get("tema"), TEMAS_UI["Grafite"])
    C_FUNDO_UI, C_PAINEL, C_BORDA, C_BOTAO = tema["fundo"], tema["painel"], tema["borda"], tema["botao"]
    C_CAMPO, C_TEXTO, C_TEXTO2 = tema["campo"], tema["texto"], tema["texto2"]


def animacoes_ligadas():
    return bool(CONFIG.get("aparencia", {}).get("animacoes", True))


# =====================================================================
# MOVIMENTO SUAVE
# =====================================================================
_SUAVES = {}


def suave(chave, alvo, rapidez=16.0):
    """Valor que corre suave até 'alvo' (rolagem, posição de abas...). Devolve inteiro para desenhar."""
    agora = _relogio_ui.perf_counter()
    v = _SUAVES.get(chave)
    if v is None or not animacoes_ligadas():
        _SUAVES[chave] = [float(alvo), agora]
        return int(round(alvo))
    pos, antes = v
    dt = min(0.05, max(0.0, agora - antes))
    pos += (alvo - pos) * (1.0 - math.exp(-rapidez * dt))
    if abs(alvo - pos) < 0.5:
        pos = float(alvo)
    v[0], v[1] = pos, agora
    if len(_SUAVES) > 4000:
        _SUAVES.clear()
    return int(round(pos))


def suave_rect(chave, r, rapidez=14.0):
    return pygame.Rect(suave((chave, "x"), r.x, rapidez), suave((chave, "y"), r.y, rapidez),
                       max(1, suave((chave, "w"), r.w, rapidez)), max(1, suave((chave, "h"), r.h, rapidez)))


def entrada(t0, duracao=0.16):
    """0 -> 1 com freio no fim (para coisas que aparecem)."""
    if not animacoes_ligadas():
        return 1.0
    k = max(0.0, min(1.0, (_relogio_ui.perf_counter() - t0) / duracao))
    return 1 - (1 - k) ** 3


def agora_ui():
    return _relogio_ui.perf_counter()


def misturar_cor(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


# =====================================================================
# ÍCONES DESENHADOS (não dependem de fonte nem de imagem)
# =====================================================================
def desenhar_icone_ui(t, nome, centro, tam=16, cor=None):
    cor = cor or C_TEXTO
    cx, cy = centro
    s = tam / 16.0

    def P(x, y):
        return (int(cx + x * s), int(cy + y * s))

    w = max(1, int(2 * s))
    if nome == "play":
        pygame.draw.polygon(t, cor, [P(-5, -7), P(-5, 7), P(7, 0)])
    elif nome == "parar":
        pygame.draw.rect(t, cor, (*P(-6, -6), int(12 * s), int(12 * s)), border_radius=max(1, int(2 * s)))
    elif nome == "playcheio":
        for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            pygame.draw.line(t, cor, P(7 * sx, 7 * sy), P(2 * sx, 7 * sy), w)
            pygame.draw.line(t, cor, P(7 * sx, 7 * sy), P(7 * sx, 2 * sy), w)
        pygame.draw.polygon(t, cor, [P(-2, -3), P(-2, 3), P(3, 0)])
    elif nome == "salvar":
        pygame.draw.rect(t, cor, (*P(-7, -7), int(14 * s), int(14 * s)), w, border_radius=max(1, int(2 * s)))
        pygame.draw.rect(t, cor, (*P(-4, -7), int(8 * s), int(5 * s)))
        pygame.draw.rect(t, cor, (*P(-4, 2), int(8 * s), int(4 * s)), w)
    elif nome in ("desfazer", "refazer"):
        d = -1 if nome == "desfazer" else 1
        pts = [P(-d * 5 + d * 10 * k / 8, 1 - 6 * math.sin(math.pi * k / 8)) for k in range(9)]
        pygame.draw.lines(t, cor, False, pts, w)
        fim = pts[-1]
        pygame.draw.polygon(t, cor, [(fim[0] + int(d * 3 * s), fim[1] - int(1 * s)),
                                     (fim[0] - int(d * 3 * s), fim[1] - int(4 * s)),
                                     (fim[0] - int(d * 1 * s), fim[1] + int(4 * s))])
    elif nome == "grade":
        for i in (-6, -2, 2, 6):
            pygame.draw.line(t, cor, P(i, -7), P(i, 7), max(1, int(1.4 * s)))
            pygame.draw.line(t, cor, P(-7, i), P(7, i), max(1, int(1.4 * s)))
    elif nome == "snap":     # ímã
        pygame.draw.arc(t, cor, (*P(-6, -7), int(12 * s), int(12 * s)), math.pi, 2 * math.pi, int(3 * s))
        pygame.draw.line(t, cor, P(-5, -1), P(-5, -7), int(3 * s))
        pygame.draw.line(t, cor, P(5, -1), P(5, -7), int(3 * s))
        pygame.draw.rect(t, (230, 90, 90), (*P(-7, -8), int(4 * s), int(3 * s)))
        pygame.draw.rect(t, (230, 90, 90), (*P(3, -8), int(4 * s), int(3 * s)))
    elif nome == "buscar":
        pygame.draw.circle(t, cor, P(-2, -2), int(5 * s), w)
        pygame.draw.line(t, cor, P(2, 2), P(7, 7), int(3 * s))
    elif nome == "ajuda":
        pygame.draw.circle(t, cor, (cx, cy), int(8 * s), w)
        img = fonte(max(9, int(12 * s)), True).render("?", True, cor)
        t.blit(img, (cx - img.get_width() // 2, cy - img.get_height() // 2))
    elif nome == "inicio":
        pygame.draw.polygon(t, cor, [P(-8, 0), P(0, -7), P(8, 0)], w)
        pygame.draw.rect(t, cor, (*P(-5, 0), int(10 * s), int(7 * s)), w)
    elif nome == "exportar":
        pygame.draw.rect(t, cor, (*P(-7, -1), int(14 * s), int(8 * s)), w, border_radius=max(1, int(2 * s)))
        pygame.draw.line(t, cor, P(0, 3), P(0, -8), w)
        pygame.draw.polygon(t, cor, [P(-4, -4), P(4, -4), P(0, -9)])
    elif nome == "modo":
        pygame.draw.polygon(t, cor, [P(0, -7), P(8, 0), P(0, 7), P(-8, 0)], w)
        pygame.draw.line(t, cor, P(-4, -3), P(4, 3), max(1, int(1.4 * s)))
    elif nome == "saida":
        pygame.draw.rect(t, cor, (*P(-8, -6), int(16 * s), int(12 * s)), w, border_radius=max(1, int(2 * s)))
        pygame.draw.lines(t, cor, False, [P(-5, -2), P(-2, 0), P(-5, 2)], w)
        pygame.draw.line(t, cor, P(0, 3), P(4, 3), w)
    elif nome == "novo":
        pygame.draw.rect(t, cor, (*P(-6, -7), int(12 * s), int(14 * s)), w, border_radius=max(1, int(2 * s)))
        pygame.draw.line(t, cor, P(0, -3), P(0, 3), w)
        pygame.draw.line(t, cor, P(-3, 0), P(3, 0), w)


# =====================================================================
# BOTÃO COM BRILHO SUAVE
# =====================================================================
_BRILHO = {}
_desenhar_botao_antigo = desenhar_botao


def desenhar_botao(tela, fonte_, rect, texto_, mouse, ativo=False, cor=None, icone=None):
    base = cor if cor else (C_DESTAQUE if ativo else C_BOTAO)
    em_cima = rect.collidepoint(mouse)
    apertado = em_cima and pygame.mouse.get_pressed()[0]
    chave = (rect.x, rect.y, rect.w, rect.h)
    agora = _relogio_ui.perf_counter()
    k, antes = _BRILHO.get(chave, (0.0, agora))
    alvo = 1.0 if em_cima and not ativo else 0.0
    if animacoes_ligadas():
        dt = min(0.05, agora - antes)
        k += (alvo - k) * (1 - math.exp(-14 * dt))
    else:
        k = alvo
    _BRILHO[chave] = (k, agora)
    if len(_BRILHO) > 3000:
        _BRILHO.clear()
    base = misturar_cor(base, clarear(base, 22), k)
    r = rect.move(0, 1) if apertado else rect
    if not apertado:
        pygame.draw.rect(tela, clarear(base, -30), rect.move(0, 2), border_radius=7)
    pygame.draw.rect(tela, base, r, border_radius=7)
    if r.h >= 18:
        pygame.draw.line(tela, clarear(base, 24 + int(10 * k)), (r.x + 6, r.y + 1), (r.right - 7, r.y + 1))
    if ativo and not cor:
        pygame.draw.rect(tela, clarear(base, 40), r, 1, border_radius=7)
    img = fonte_.render(texto_, True, C_TEXTO) if texto_ else None
    if icone:
        tam = min(16, r.h - 12)
        if img is None:
            desenhar_icone_ui(tela, icone, r.center, tam)
        else:
            larg = tam + 6 + img.get_width()
            x0 = r.centerx - larg // 2
            desenhar_icone_ui(tela, icone, (x0 + tam // 2, r.centery), tam)
            tela.blit(img, (x0 + tam + 6, r.centery - img.get_height() // 2))
    elif img is not None:
        tela.blit(img, (r.centerx - img.get_width() // 2, r.centery - img.get_height() // 2))


def sombra_painel(t, rect, raio=12, forca=90):
    """Sombra macia embaixo de janelas e cartões."""
    for i, a in ((10, forca // 5), (6, forca // 3), (3, forca // 2)):
        s = pygame.Surface((rect.w + i * 2, rect.h + i * 2), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, a), s.get_rect(), border_radius=raio + i)
        t.blit(s, (rect.x - i, rect.y - i + 4))


def escurecer_tela(t, alfa):
    s = pygame.Surface(t.get_size(), pygame.SRCALPHA)
    s.fill((0, 0, 0, max(0, min(255, int(alfa)))))
    t.blit(s, (0, 0))
