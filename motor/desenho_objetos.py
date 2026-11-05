# Minha Engine - desenho_objetos.py
# como cada objeto é desenhado (materiais, formas, texto)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Desenho dos objetos
# ---------------------------------------------------------------------
def desenhar_texto_ui(tela, d, r, txt=None, centro=False):
    tipo = d.get("tipo")
    txt = str(d.get("texto", "")) if txt is None else str(txt)
    cor = cor_ok(d.get("cor_texto", [255, 255, 255]) if tipo == "Botao" else d.get("cor", [255, 255, 255]))
    familia = FONTES_JOGO.get(d.get("fonte"), FONTES_JOGO["Arial"])
    f = fonte_familia(familia, d.get("tamanho_fonte", 20), bool(d.get("negrito")), bool(d.get("italico")))
    img = texto_cache_fonte(f, txt, cor)
    alinhar = "Centro" if centro else d.get("alinhamento", "Esquerda")
    if alinhar == "Centro":
        x = r.centerx - img.get_width() // 2
    elif alinhar == "Direita":
        x = r.right - img.get_width() - 2
    else:
        x = r.x + 2
    y = r.centery - img.get_height() // 2
    if d.get("sombra_texto"):
        tela.blit(texto_cache_fonte(f, txt, (0, 0, 0)), (x + 2, y + 2))
    tela.blit(img, (x, y))


_cache_material = {}


def superficie_material(w, h, cor, material):
    """Textura desenhada pelo codigo para cada material (guardada em cache)."""
    chave = (w, h, cor, material)
    surf = _cache_material.get(chave)
    if surf is not None:
        return surf
    if len(_cache_material) > 500:
        _cache_material.clear()
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    escuro, claro = clarear(cor, -38), clarear(cor, 34)
    rnd = random.Random(w * 7919 + h * 31 + sum(cor))
    if material == "Vidro":
        surf.fill((cor[0], cor[1], cor[2], 90))
        pygame.draw.line(surf, (255, 255, 255, 150), (w // 5, h - 2), (w // 2, 2), max(2, w // 12))
    elif material == "Neon":
        surf.fill(claro)
        pygame.draw.rect(surf, (255, 255, 255), (2, 2, w - 4, h - 4), 2)
    else:
        surf.fill(cor)
    if material == "Plástico":
        pygame.draw.rect(surf, claro, (0, 0, w, max(2, h // 8)))
    elif material == "Madeira":
        for y in range(3, h, 7):
            pts = [(x, y + int(1.5 * math.sin((x + y) / 9))) for x in range(0, w + 6, 6)]
            if len(pts) > 1:
                pygame.draw.lines(surf, escuro, False, pts, 1)
    elif material == "Tijolo":
        alt = max(6, min(14, h // 3 if h > 18 else 6))
        for i, y in enumerate(range(0, h, alt)):
            pygame.draw.line(surf, clarear(cor, 55), (0, y), (w, y), 2)
            desloc = 0 if i % 2 == 0 else alt
            for x in range(desloc, w, alt * 2):
                pygame.draw.line(surf, clarear(cor, 55), (x, y), (x, y + alt), 2)
    elif material == "Pedra":
        for _ in range(max(4, w * h // 90)):
            x, y = rnd.randrange(w), rnd.randrange(h)
            pygame.draw.circle(surf, escuro if rnd.random() < 0.6 else claro, (x, y), rnd.randint(1, 3))
    elif material == "Metal":
        for y in range(h):
            k = y / max(1, h - 1)
            pygame.draw.line(surf, clarear(cor, int(40 - 70 * k)), (0, y), (w, y))
        for x, y in ((5, 5), (w - 6, 5), (5, h - 6), (w - 6, h - 6)):
            if w > 16 and h > 16:
                pygame.draw.circle(surf, clarear(cor, -60), (x, y), 2)
    elif material == "Grama":
        topo = max(4, min(14, h // 3))
        pygame.draw.rect(surf, clarear(cor, -60) if sum(cor) > 400 else (120, 84, 52), (0, topo, w, h - topo))
        pygame.draw.rect(surf, (88, 190, 80), (0, 0, w, topo))
        for x in range(0, w, 5):
            pygame.draw.line(surf, (70, 160, 64), (x, topo), (x + 2, topo + 3), 2)
    elif material == "Gramado":      # grama vista de cima (chão do top-down)
        for _ in range(max(8, w * h // 70)):
            x, y = rnd.randrange(w), rnd.randrange(h)
            c = clarear(cor, rnd.choice((-22, -14, 16, 24)))
            pygame.draw.line(surf, c, (x, y), (x + rnd.choice((-1, 0, 1)), y - rnd.randint(2, 4)), 1)
        for _ in range(max(1, w * h // 6000)):
            x, y = rnd.randrange(w), rnd.randrange(h)
            pygame.draw.circle(surf, clarear(cor, -18), (x, y), rnd.randint(3, 6))
    elif material == "Areia":
        for _ in range(max(6, w * h // 40)):
            surf.set_at((rnd.randrange(w), rnd.randrange(h)), escuro)
    elif material == "Gelo":
        surf.fill((min(255, cor[0] // 2 + 120), min(255, cor[1] // 2 + 128), 255))
        for i in range(0, w + h, 18):
            pygame.draw.line(surf, (255, 255, 255, 160), (i, 0), (i - h, h), 2)
    elif material == "Borracha":
        for x in range(0, w, 8):
            pygame.draw.line(surf, escuro, (x, 0), (x, h), 3)
    elif material == "Tecido":
        for x in range(0, w, 4):
            pygame.draw.line(surf, escuro, (x, 0), (x, h), 1)
        for y in range(0, h, 4):
            pygame.draw.line(surf, claro, (0, y), (w, y), 1)
    _cache_material[chave] = surf
    return surf


def desenhar_peca(tela, d, r, cor):
    """Desenha Peca/Bloco/Decoracao/Caixa com forma, material e contorno."""
    forma = d.get("forma", "Retângulo")
    material = d.get("material", "Plástico")
    contorno = int(num_seguro(d.get("contorno", 2), 2))
    cor_c = cor_ok(d.get("cor_contorno")) if d.get("cor_contorno") else clarear(cor, -50)
    w, h = max(1, r.w), max(1, r.h)
    if forma == "Retângulo" and w * h > 160000 and material not in ("Vidro", "Neon", "Metal", "Grama") \
            and not int(num_seguro(d.get("arredondado", 0), 0)):
        # chão grande (top-down): desenha em ladrilhos, rápido mesmo dando zoom
        lad = superficie_material(128, 128, cor, material)
        visivel = r.clip(tela.get_clip() or tela.get_rect())
        if visivel.w > 0 and visivel.h > 0:
            x0 = r.x + ((visivel.x - r.x) // 128) * 128
            y0 = r.y + ((visivel.y - r.y) // 128) * 128
            clip_antes = tela.get_clip()
            tela.set_clip(visivel)
            for yy in range(y0, visivel.bottom, 128):
                for xx in range(x0, visivel.right, 128):
                    tela.blit(lad, (xx, yy))
            tela.set_clip(clip_antes)
        if contorno > 0:
            pygame.draw.rect(tela, cor_c, r, contorno)
        return
    textura = superficie_material(w, h, cor, material)
    if material == "Neon":   # brilho em volta
        brilho = pygame.Surface((w + 16, h + 16), pygame.SRCALPHA)
        pygame.draw.rect(brilho, (cor[0], cor[1], cor[2], 70), brilho.get_rect(), border_radius=10)
        tela.blit(brilho, (r.x - 8, r.y - 8))
    if forma == "Retângulo":
        raio = int(num_seguro(d.get("arredondado", 0), 0))
        if raio:
            mascara = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(mascara, (255, 255, 255, 255), (0, 0, w, h), border_radius=raio)
            img = textura.copy()
            img.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            tela.blit(img, r.topleft)
        else:
            tela.blit(textura, r.topleft)
        if contorno > 0:
            pygame.draw.rect(tela, cor_c, r, contorno, border_radius=raio)
        return
    pontos = {"Triângulo": [(w / 2, 0), (w, h), (0, h)], "Losango": [(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2)],
              "Rampa ◢": [(w, 0), (w, h), (0, h)], "Rampa ◣": [(0, 0), (w, h), (0, h)]}.get(forma)
    mascara = pygame.Surface((w, h), pygame.SRCALPHA)
    if forma == "Círculo":
        pygame.draw.ellipse(mascara, (255, 255, 255, 255), (0, 0, w, h))
    elif pontos:
        pygame.draw.polygon(mascara, (255, 255, 255, 255), pontos)
    img = textura.copy()
    img.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    tela.blit(img, r.topleft)
    if contorno > 0:
        if forma == "Círculo":
            pygame.draw.ellipse(tela, cor_c, r, contorno)
        elif pontos:
            pygame.draw.polygon(tela, cor_c, [(r.x + x, r.y + y) for x, y in pontos], contorno)


def desenhar_forma(tela, tipo, d, r, txt=None, editor=False, progresso=None):
    cor = cor_ok(d.get("cor", [255, 255, 255]))
    raio = int(num_seguro(d.get("arredondado", 0), 0))
    if tipo == "Moeda":
        pygame.draw.ellipse(tela, cor, r)
        pygame.draw.ellipse(tela, clarear(cor, -70), r, 2)
    elif tipo in ("Espinho",):
        n = max(1, r.w // 20)
        lw = r.w / n
        for i in range(n):
            pts = [(r.x + i * lw, r.bottom), (r.x + i * lw + lw / 2, r.y), (r.x + (i + 1) * lw, r.bottom)]
            pygame.draw.polygon(tela, cor, pts)
    elif tipo == "Bandeira":
        mx = r.x + r.w // 2
        pygame.draw.rect(tela, cor, (mx - 2, r.y, 4, r.h))
        pygame.draw.polygon(tela, (240, 60, 60), [(mx + 2, r.y), (mx + 32, r.y + 12), (mx + 2, r.y + 24)])
    elif tipo == "Checkpoint":
        mx = r.x + r.w // 2
        pygame.draw.rect(tela, (200, 200, 200), (mx - 2, r.y, 4, r.h))
        pygame.draw.polygon(tela, cor, [(mx + 2, r.y), (mx + 26, r.y + 10), (mx + 2, r.y + 20)])
    elif tipo == "Lava":
        pygame.draw.rect(tela, cor, r)
        claro = clarear(cor, 60)
        for i in range(0, max(1, r.w), 16):
            pygame.draw.ellipse(tela, claro, (r.x + i, r.y - 3, 14, 8))
    elif tipo == "Portal":
        pygame.draw.ellipse(tela, cor, r, max(2, min(r.w, r.h) // 8))
        pygame.draw.ellipse(tela, clarear(cor, 70), r.inflate(-r.w // 3, -r.h // 4), 2)
    elif tipo == "Item":
        pts = [(r.centerx, r.y), (r.right, r.centery), (r.centerx, r.bottom), (r.x, r.centery)]
        pygame.draw.polygon(tela, cor, pts)
        pygame.draw.polygon(tela, clarear(cor, -70), pts, 2)
    elif tipo == "Zona":
        if editor:
            pygame.draw.rect(tela, cor, r, 1)
            pygame.draw.line(tela, cor, r.topleft, r.bottomright)
            pygame.draw.line(tela, cor, r.topright, r.bottomleft)
    elif tipo == "Trampolim":
        pygame.draw.rect(tela, clarear(cor, -80), (r.x, r.y + r.h // 2, r.w, r.h - r.h // 2))
        pygame.draw.rect(tela, cor, (r.x, r.y, r.w, max(3, r.h // 2)), border_radius=3)
    elif tipo == "Caixa":
        pygame.draw.rect(tela, cor, r)
        escuro = clarear(cor, -55)
        pygame.draw.rect(tela, escuro, r, 3)
        pygame.draw.line(tela, escuro, r.topleft, r.bottomright, 2)
        pygame.draw.line(tela, escuro, r.topright, r.bottomleft, 2)
    elif tipo == "Plataforma Movel":
        pygame.draw.rect(tela, cor, r, border_radius=4)
        escuro = clarear(cor, -60)
        cy = r.centery
        pygame.draw.polygon(tela, escuro, [(r.x + 6, cy), (r.x + 14, cy - 5), (r.x + 14, cy + 5)])
        pygame.draw.polygon(tela, escuro, [(r.right - 6, cy), (r.right - 14, cy - 5), (r.right - 14, cy + 5)])
    elif tipo == "Texto":
        if editor:
            pygame.draw.rect(tela, (90, 90, 110), r, 1)
        desenhar_texto_ui(tela, d, r, txt)
    elif tipo == "Botao":
        pygame.draw.rect(tela, cor, r, border_radius=raio)
        pygame.draw.rect(tela, clarear(cor, -50), r, 2, border_radius=raio)
        desenhar_texto_ui(tela, d, r, txt, centro=True)
    elif tipo == "Barra":
        pygame.draw.rect(tela, cor_ok(d.get("cor_fundo", [50, 50, 60])), r, border_radius=4)
        p = 0.65 if progresso is None else max(0.0, min(1.0, progresso))
        if p > 0:
            pygame.draw.rect(tela, cor, (r.x, r.y, max(1, int(r.w * p)), r.h), border_radius=4)
        pygame.draw.rect(tela, (20, 20, 25), r, 2, border_radius=4)
    elif tipo == "Painel":
        pygame.draw.rect(tela, cor, r, border_radius=raio)
        pygame.draw.rect(tela, clarear(cor, 40), r, 1, border_radius=raio)
    elif tipo == "Imagem":
        pygame.draw.rect(tela, (70, 70, 85), r)
        pygame.draw.line(tela, (120, 120, 140), r.topleft, r.bottomright)
        pygame.draw.line(tela, (120, 120, 140), r.topright, r.bottomleft)
        pygame.draw.rect(tela, (140, 140, 160), r, 1)
    elif tipo in ("Peça", "Bloco", "Decoracao", "Caixa") or (d.get("material") and tipo not in ("Player", "Inimigo",
                                                                                                "NPC")):
        desenhar_peca(tela, d, r, cor)
        if tipo == "Caixa" and d.get("forma", "Retângulo") == "Retângulo":
            escuro = clarear(cor, -55)
            pygame.draw.line(tela, escuro, r.topleft, r.bottomright, 2)
            pygame.draw.line(tela, escuro, r.topright, r.bottomleft, 2)
    else:
        pygame.draw.rect(tela, cor, r, border_radius=raio)
        pygame.draw.rect(tela, clarear(cor, -50), r, 2, border_radius=raio)
        if tipo in ("Player", "Inimigo", "NPC") and r.w >= 12 and r.h >= 12:
            olho = max(3, r.w // 8)
            yy = r.y + r.h // 3
            pygame.draw.rect(tela, (255, 255, 255), (r.x + r.w // 4 - olho // 2, yy, olho, olho))
            pygame.draw.rect(tela, (255, 255, 255), (r.x + 3 * r.w // 4 - olho // 2, yy, olho, olho))
            if tipo == "Inimigo":
                pygame.draw.line(tela, (40, 0, 0), (r.x + r.w // 4 - olho, yy - 3), (r.x + r.w // 2 - 2, yy), 2)
                pygame.draw.line(tela, (40, 0, 0), (r.x + 3 * r.w // 4 + olho, yy - 3), (r.x + r.w // 2 + 2, yy), 2)
            elif tipo == "NPC":
                pygame.draw.line(tela, (60, 30, 10), (r.x + r.w // 3, yy + olho + 6), (r.x + 2 * r.w // 3, yy + olho + 6), 2)


def desenhar_obj(tela, d, r, txt=None, editor=False, progresso=None, img_nome=None):
    """Desenha um objeto com imagem (ou quadro de animacao), opacidade, rotacao e espelhamento."""
    tipo = d.get("tipo")
    alpha = int(max(0, min(255, num_seguro(d.get("opacidade", 255), 255))))
    if editor:
        alpha = max(alpha, 70)
    elif alpha <= 0:
        return
    rot = num_seguro(d.get("rotacao", 0), 0) % 360
    esp = bool(d.get("espelhar"))
    w, h = max(1, r.w), max(1, r.h)
    if img_nome is None and editor and not d.get("imagem") and d.get("animacao"):
        img_nome = str(d["animacao"]).split(",")[0].strip()
    nome_img = img_nome or d.get("imagem", "")
    img = imagem_escalada(nome_img, w, h) if nome_img else None
    if img is None and alpha >= 255 and not rot and not esp:
        desenhar_forma(tela, tipo, d, r, txt, editor, progresso)
        return
    rot = round(rot)   # 1 grau de precisao: deixa o cache funcionar
    chave = None
    if progresso is None:
        chave = (tipo, nome_img if img is not None else "", w, h, rot, esp, alpha // 8, txt,
                 tuple(cor_ok(d.get("cor"))), d.get("texto") if tipo in ("Texto", "Botao") else None, editor,
                 d.get("material"), d.get("forma"), d.get("fonte"), d.get("negrito"), d.get("italico"),
                 d.get("contorno"), str(d.get("cor_contorno")), d.get("alinhamento"), d.get("sombra_texto"))
        pronta = _cache_obj.get(chave)
        if pronta is not None:
            rr = pronta.get_rect()
            rr.center = r.center
            tela.blit(pronta, rr)
            return
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    local = pygame.Rect(0, 0, w, h)
    if img is not None:
        surf.blit(img, (0, 0))
        if tipo in ("Texto", "Botao"):
            desenhar_texto_ui(surf, d, local, txt, centro=(tipo == "Botao"))
    else:
        desenhar_forma(surf, tipo, d, local, txt, editor, progresso)
    if esp:
        surf = pygame.transform.flip(surf, True, False)
    if rot:
        surf = pygame.transform.rotate(surf, rot)
    if alpha < 255:
        surf.set_alpha(alpha)
    if chave is not None:
        if len(_cache_obj) > 700:
            _cache_obj.clear()
        _cache_obj[chave] = surf
    rr = surf.get_rect()
    rr.center = r.center
    tela.blit(surf, rr)


def desenhar_icone(tela, tipo, d, r):
    if tipo == "Texto":
        img = fonte(13, True).render("Aa", True, (255, 255, 255))
        tela.blit(img, (r.centerx - img.get_width() // 2, r.centery - img.get_height() // 2))
    elif tipo == "Botao":
        pygame.draw.rect(tela, cor_ok(d.get("cor", [70, 140, 255])), r.inflate(0, -6), border_radius=3)
    elif tipo == "Barra":
        pygame.draw.rect(tela, (50, 50, 60), r.inflate(0, -8))
        pygame.draw.rect(tela, cor_ok(d.get("cor", [80, 220, 100])), (r.x, r.y + 4, r.w * 2 // 3, r.h - 8))
    elif tipo == "Zona":
        pygame.draw.rect(tela, cor_ok(d.get("cor")), r, 1)
    else:
        desenhar_forma(tela, tipo, d, r, editor=True)


def desenhar_botao(tela, fonte_, rect, texto_, mouse, ativo=False, cor=None):
    base = cor if cor else (C_DESTAQUE if ativo else C_BOTAO)
    em_cima = rect.collidepoint(mouse)
    apertado = em_cima and pygame.mouse.get_pressed()[0]
    if em_cima and not ativo:
        base = clarear(base, 20)
    r = rect.move(0, 1) if apertado else rect
    if not apertado:
        pygame.draw.rect(tela, clarear(base, -28), rect.move(0, 2), border_radius=6)
    pygame.draw.rect(tela, base, r, border_radius=6)
    if r.h >= 18:
        pygame.draw.line(tela, clarear(base, 22), (r.x + 5, r.y + 1), (r.right - 6, r.y + 1))
    img = fonte_.render(texto_, True, C_TEXTO)
    tela.blit(img, (r.centerx - img.get_width() // 2, r.centery - img.get_height() // 2))
