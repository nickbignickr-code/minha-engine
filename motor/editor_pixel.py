# Minha Engine - editor_pixel.py
# aba Desenho: pixel art e animação
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# EDITOR DE PIXEL ART + ANIMACAO (aba "Desenho")
# =====================================================================
PALETA_PIXEL = [
    (0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81), (171, 82, 54), (95, 87, 79), (194, 195, 199),
    (255, 241, 232), (255, 0, 77), (255, 163, 0), (255, 236, 39), (0, 228, 54), (41, 173, 255), (131, 118, 156),
    (255, 119, 168), (255, 204, 170), (255, 255, 255), (120, 120, 120), (60, 60, 60), (150, 80, 40),
    (230, 160, 100), (100, 60, 30), (40, 120, 40), (130, 200, 80), (30, 80, 160), (120, 180, 255),
    (90, 40, 140), (200, 120, 230), (180, 30, 30), (255, 90, 90), (255, 210, 120), (60, 200, 200),
]
FERRAMENTAS_PIXEL = [("lapis", "Lápis", "B"), ("borracha", "Borracha", "E"), ("balde", "Balde", "G"),
                     ("contagotas", "Conta-gotas", "I"), ("linha", "Linha", "L"), ("retangulo", "Retângulo", "R"),
                     ("circulo", "Círculo", "C")]
TAMANHOS_PIXEL = [8, 16, 24, 32, 48, 64]


def nome_arquivo_livre(base, ext=".png"):
    base = re.sub(r"[^\w\-]", "_", str(base).strip()) or "desenho"
    i, nome = 1, base + ext
    while os.path.exists(os.path.join(PASTA_IMAGENS, nome)):
        i += 1
        nome = f"{base}{i}{ext}"
    return nome


class EditorPixel:
    def __init__(self, ed):
        self.ed = ed
        self.n = 16
        self.quadros = [self.quadro_vazio()]
        self.atual = 0
        self.cor = (255, 0, 77)
        self.ferramenta = "lapis"
        self.espelho = False
        self.grade = True
        self.cebola = True
        self.fps = 8
        self.nome = "desenho"
        self.alvo = None
        self.modo = "imagem"
        self.desfazer_pilha = []
        self.refazer_pilha = []
        self.inicio_forma = None
        self.ultimo_px = None
        self.hits = []
        self.editando_nome = False
        self.mudou = False
        self.recentes = []

    # ----------------- dados -----------------
    def quadro_vazio(self, n=None):
        n = n or self.n
        q = pygame.Surface((n, n), pygame.SRCALPHA)
        q.fill((0, 0, 0, 0))
        return q

    def foto(self):
        self.desfazer_pilha.append(([q.copy() for q in self.quadros], self.atual, self.n))
        if len(self.desfazer_pilha) > 80:
            self.desfazer_pilha.pop(0)
        self.refazer_pilha.clear()
        self.mudou = True

    def desfazer(self):
        if self.desfazer_pilha:
            self.refazer_pilha.append(([q.copy() for q in self.quadros], self.atual, self.n))
            self.quadros, self.atual, self.n = self.desfazer_pilha.pop()

    def refazer(self):
        if self.refazer_pilha:
            self.desfazer_pilha.append(([q.copy() for q in self.quadros], self.atual, self.n))
            self.quadros, self.atual, self.n = self.refazer_pilha.pop()

    def novo(self, n=None):
        self.n = n or self.n
        self.quadros = [self.quadro_vazio()]
        self.atual = 0
        self.desfazer_pilha.clear()
        self.refazer_pilha.clear()
        self.nome = nome_arquivo_livre("desenho")[:-4]
        self.mudou = False

    def carregar_imagens(self, nomes):
        quadros = []
        for nome in nomes:
            caminho = os.path.join(PASTA_IMAGENS, nome)
            try:
                img = pygame.image.load(caminho)
                try:
                    img = img.convert_alpha()
                except pygame.error:
                    pass
            except (pygame.error, OSError, FileNotFoundError):
                continue
            w, h = img.get_width(), img.get_height()
            lado = min(64, max(w, h))
            lado = min(TAMANHOS_PIXEL, key=lambda t: abs(t - lado)) if lado > 0 else 16
            q = self.quadro_vazio(lado)
            if w > 0 and h > 0:
                k = min(lado / w, lado / h)
                esc = pygame.transform.scale(img, (max(1, int(w * k)), max(1, int(h * k))))
                q.blit(esc, ((lado - esc.get_width()) // 2, (lado - esc.get_height()) // 2))
            quadros.append(q)
        if quadros:
            self.n = quadros[0].get_width()
            self.quadros = [q if q.get_width() == self.n else pygame.transform.scale(q, (self.n, self.n))
                            for q in quadros]
            self.atual = 0
            self.desfazer_pilha.clear()
            self.refazer_pilha.clear()
            base = os.path.splitext(nomes[0])[0]
            self.nome = re.sub(r"_?\d+$", "", base) or base
            self.mudou = False
            return True
        return False

    def abrir_para(self, alvo, modo):
        """Abre o desenho do objeto (ou um novo) para editar como imagem ou animacao."""
        self.alvo = alvo
        self.modo = modo
        anim = [a.strip() for a in str(alvo.get("animacao", "") or "").split(",") if a.strip()] if alvo else []
        img = str(alvo.get("imagem", "") or "") if alvo else ""
        carregou = False
        if modo == "animacao" and anim:
            carregou = self.carregar_imagens(anim)
            self.fps = int(num_seguro(alvo.get("fps_anim", 8), 8))
        elif img:
            carregou = self.carregar_imagens([img])
        if not carregou:
            self.novo(16)
            if alvo:
                self.nome = nome_arquivo_livre(alvo.get("nome", "desenho"))[:-4]
        if modo == "animacao" and len(self.quadros) == 1 and not anim:
            self.ed.avisar("Animação: desenhe o 1º quadro, clique em '+ Quadro' para o próximo (ele copia o anterior).")

    def salvar(self, aplicar=True):
        os.makedirs(PASTA_IMAGENS, exist_ok=True)
        base = re.sub(r"[^\w\-]", "_", self.nome.strip()) or "desenho"
        nomes = []
        if len(self.quadros) == 1:
            nomes = [base + ".png"]
        else:
            nomes = [f"{base}_{i + 1}.png" for i in range(len(self.quadros))]
        for q, nome in zip(self.quadros, nomes):
            pygame.image.save(q, os.path.join(PASTA_IMAGENS, nome))
        limpar_cache_imagens()
        self.mudou = False
        self.ed.passos_feitos.add("desenho")
        if aplicar and self.alvo is not None:
            self.ed.guardar()
            if len(nomes) == 1 and self.modo != "animacao":
                self.alvo["imagem"] = nomes[0]
                self.alvo["animacao"] = ""
            else:
                self.alvo["animacao"] = ", ".join(nomes)
                self.alvo["fps_anim"] = self.fps
            self.ed.avisar(f"Salvo e aplicado em '{self.alvo.get('nome')}': {', '.join(nomes)}")
        else:
            self.ed.avisar(f"Desenho salvo na pasta imagens: {', '.join(nomes)}")
        return nomes

    def usar_como(self, campo):
        """Player: usar os quadros como anim_andando ou anim_pulando."""
        if self.alvo is None:
            return
        nomes = self.salvar(aplicar=False)
        self.ed.guardar()
        self.alvo[campo] = ", ".join(nomes)
        self.alvo["fps_anim"] = self.fps
        self.ed.avisar(f"'{self.alvo.get('nome')}' agora usa isso como {ROTULOS.get(campo, campo)}.")

    # ----------------- pintura -----------------
    def pintar_px(self, q, x, y, cor):
        if 0 <= x < self.n and 0 <= y < self.n:
            q.set_at((x, y), cor)
            if self.espelho:
                q.set_at((self.n - 1 - x, y), cor)

    def cor_ferramenta(self, botao):
        return (0, 0, 0, 0) if (self.ferramenta == "borracha" or botao == 3) else (*self.cor, 255)

    def linha_px(self, q, a, b, cor):
        (x0, y0), (x1, y1) = a, b
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.pintar_px(q, x0, y0, cor)
            if (x0, y0) == (x1, y1):
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def retangulo_px(self, q, a, b, cor):
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for x in range(x0, x1 + 1):
            self.pintar_px(q, x, y0, cor)
            self.pintar_px(q, x, y1, cor)
        for y in range(y0, y1 + 1):
            self.pintar_px(q, x0, y, cor)
            self.pintar_px(q, x1, y, cor)

    def circulo_px(self, q, a, b, cor):
        cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        rx, ry = max(0.5, abs(b[0] - a[0]) / 2), max(0.5, abs(b[1] - a[1]) / 2)
        passos = int(8 * max(rx, ry)) + 8
        for i in range(passos):
            ang = math.tau * i / passos
            self.pintar_px(q, int(round(cx + rx * math.cos(ang))), int(round(cy + ry * math.sin(ang))), cor)

    def balde(self, q, x, y, cor):
        alvo = tuple(q.get_at((x, y)))
        if alvo == tuple(cor):
            return
        pilha, vistos = [(x, y)], set()
        while pilha:
            px, py = pilha.pop()
            if (px, py) in vistos or not (0 <= px < self.n and 0 <= py < self.n):
                continue
            vistos.add((px, py))
            if tuple(q.get_at((px, py))) != alvo:
                continue
            q.set_at((px, py), cor)
            pilha.extend(((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)))

    # ----------------- layout -----------------
    def layout(self):
        a = VIEW
        lado = min(a.h - 150, a.w - 330)
        lado = max(self.n, (lado // self.n) * self.n)
        tela = pygame.Rect(a.x + 150 + (a.w - 330 - lado) // 2, a.y + 46, lado, lado)
        return tela, lado // self.n

    def px_em(self, pos):
        tela, k = self.layout()
        if not tela.collidepoint(pos):
            return None
        return (pos[0] - tela.x) // k, (pos[1] - tela.y) // k

    # ----------------- eventos -----------------
    def clique(self, pos, botao=1):
        for r, acao in reversed(self.hits):
            if r.collidepoint(pos):
                self.executar(acao, pos)
                return
        p = self.px_em(pos)
        if p is None:
            return
        q = self.quadros[self.atual]
        if self.ferramenta == "contagotas":
            c = q.get_at(p)
            if c[3] > 0:
                self.cor = (c[0], c[1], c[2])
            self.ferramenta = "lapis"
            return
        self.foto()
        if self.ferramenta == "balde":
            self.balde(q, p[0], p[1], self.cor_ferramenta(botao))
            return
        if self.ferramenta in ("linha", "retangulo", "circulo"):
            self.inicio_forma = (p, botao, q.copy())
        else:
            self.pintar_px(q, p[0], p[1], self.cor_ferramenta(botao))
            self.ultimo_px = p
        self.ed.arrastando = ("pix", botao)

    def arrastar(self, pos):
        p = self.px_em(pos)
        if p is None:
            return
        botao = self.ed.arrastando[1] if self.ed.arrastando else 1
        q = self.quadros[self.atual]
        if self.inicio_forma:
            inicio, botao, original = self.inicio_forma
            q.fill((0, 0, 0, 0))
            q.blit(original, (0, 0))
            cor = self.cor_ferramenta(botao)
            {"linha": self.linha_px, "retangulo": self.retangulo_px, "circulo": self.circulo_px}[self.ferramenta](
                q, inicio, p, cor)
            self.preview_fim = p
        elif self.ferramenta in ("lapis", "borracha"):
            if self.ultimo_px is not None and self.ultimo_px != p:
                self.linha_px(q, self.ultimo_px, p, self.cor_ferramenta(botao))
            self.ultimo_px = p

    def soltar(self, pos):
        self.inicio_forma = None
        self.ultimo_px = None

    def tecla(self, e):
        ctrl = e.mod & pygame.KMOD_CTRL
        if self.editando_nome:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE):
                self.editando_nome = False
            elif e.key == pygame.K_BACKSPACE:
                self.nome = self.nome[:-1]
            elif e.unicode and (e.unicode.isalnum() or e.unicode in "_-") and len(self.nome) < 30:
                self.nome += e.unicode
            return
        if ctrl and e.key == pygame.K_z:
            self.desfazer()
        elif ctrl and e.key == pygame.K_y:
            self.refazer()
        elif e.unicode and not ctrl:
            atalhos = {f[2].lower(): f[0] for f in FERRAMENTAS_PIXEL}
            u = e.unicode.lower()
            if u in atalhos:
                self.ferramenta = atalhos[u]
            elif u == "m":
                self.espelho = not self.espelho
            elif u == "[":
                self.atual = max(0, self.atual - 1)
            elif u == "]":
                self.atual = min(len(self.quadros) - 1, self.atual + 1)
        if e.key == pygame.K_DELETE:
            self.foto()
            self.quadros[self.atual].fill((0, 0, 0, 0))

    def executar(self, acao, pos):
        k = acao[0]
        if k == "ferr":
            self.ferramenta = acao[1]
        elif k == "cor":
            self.cor = acao[1]
            if self.ferramenta in ("borracha", "contagotas"):
                self.ferramenta = "lapis"
        elif k == "rgb":
            i, passo = acao[1], acao[2]
            c = list(self.cor)
            c[i] = max(0, min(255, c[i] + passo))
            self.cor = tuple(c)
        elif k == "tam":
            if self.mudou or len(self.quadros) > 1:
                self.foto()
            self.n = acao[1]
            self.quadros = [pygame.transform.scale(q, (self.n, self.n)) for q in self.quadros]
        elif k == "toggle":
            setattr(self, acao[1], not getattr(self, acao[1]))
        elif k == "quadro":
            self.atual = acao[1]
        elif k == "q_add":
            self.foto()
            self.quadros.insert(self.atual + 1, self.quadros[self.atual].copy())
            self.atual += 1
        elif k == "q_vazio":
            self.foto()
            self.quadros.insert(self.atual + 1, self.quadro_vazio())
            self.atual += 1
        elif k == "q_del":
            if len(self.quadros) > 1:
                self.foto()
                self.quadros.pop(self.atual)
                self.atual = max(0, self.atual - 1)
        elif k == "q_mover":
            j = self.atual + acao[1]
            if 0 <= j < len(self.quadros):
                self.foto()
                self.quadros[self.atual], self.quadros[j] = self.quadros[j], self.quadros[self.atual]
                self.atual = j
        elif k == "fps":
            self.fps = max(1, min(30, self.fps + acao[1]))
        elif k == "limpar":
            self.foto()
            self.quadros[self.atual].fill((0, 0, 0, 0))
        elif k == "virar":
            self.foto()
            self.quadros[self.atual] = pygame.transform.flip(self.quadros[self.atual], True, False)
        elif k == "nome":
            self.editando_nome = True
        elif k == "novo":
            self.novo()
        elif k == "salvar":
            self.salvar(aplicar=True)
        elif k == "salvar_so":
            self.salvar(aplicar=False)
        elif k == "usar_como":
            self.usar_como(acao[1])
        elif k == "abrir":
            imagens = listar_imagens()
            if not imagens:
                self.ed.avisar("A pasta imagens está vazia.")
                return
            self.ed.abrir_menu(pos, imagens, lambda nome: self.carregar_imagens([nome]))
        elif k == "desfazer":
            self.desfazer()
        elif k == "refazer":
            self.refazer()

    # ----------------- desenho -----------------
    def botao(self, t, r, txt, acao, mouse, ativo=False, cor=None):
        base = C_DESTAQUE if ativo else (cor or C_BOTAO)
        if r.collidepoint(mouse) and not ativo:
            base = clarear(base, 18)
        pygame.draw.rect(t, base, r, border_radius=6)
        img = self.ed.fp.render(txt, True, C_TEXTO)
        t.blit(img, (r.centerx - img.get_width() // 2, r.centery - img.get_height() // 2))
        self.hits.append((r, acao))

    def desenhar(self, t, mouse):
        a = VIEW
        self.hits = []
        pygame.draw.rect(t, (24, 26, 32), a)
        ed = self.ed
        titulo = "DESENHO" if self.modo == "imagem" else "ANIMAÇÃO"
        alvo_txt = f" para: {self.alvo['nome']}" if self.alvo else "  (sem objeto: só salva na pasta imagens)"
        t.blit(ed.f.render(titulo + alvo_txt, True, C_TEXTO), (a.x + 12, a.y + 10))
        # nome do arquivo
        r = pygame.Rect(a.right - 300, a.y + 8, 170, 26)
        pygame.draw.rect(t, C_CAMPO, r, border_radius=5)
        pygame.draw.rect(t, C_DESTAQUE if self.editando_nome else C_BORDA, r, 1, border_radius=5)
        piscar = "|" if self.editando_nome and int(ed.tempo * 2) % 2 == 0 else ""
        t.blit(ed.fp.render(self.nome + piscar + (".png" if len(self.quadros) == 1 else "_N.png"), True, C_TEXTO),
               (r.x + 8, r.y + 5))
        self.hits.append((r, ("nome",)))
        self.botao(t, pygame.Rect(a.right - 124, a.y + 8, 112, 26), "Abrir imagem", ("abrir",), mouse)

        # ferramentas
        y = a.y + 46
        for nome, rot, tec in FERRAMENTAS_PIXEL:
            self.botao(t, pygame.Rect(a.x + 10, y, 130, 28), f"{rot} ({tec})", ("ferr", nome), mouse,
                       ativo=self.ferramenta == nome)
            y += 32
        y += 6
        for attr, rot in (("espelho", "Espelho (M)"), ("grade", "Grade"), ("cebola", "Ver quadro anterior")):
            self.botao(t, pygame.Rect(a.x + 10, y, 130, 26), ("✓ " if getattr(self, attr) else "") + rot,
                       ("toggle", attr), mouse, ativo=getattr(self, attr))
            y += 30
        y += 6
        self.botao(t, pygame.Rect(a.x + 10, y, 63, 26), "Desfazer", ("desfazer",), mouse)
        self.botao(t, pygame.Rect(a.x + 77, y, 63, 26), "Refazer", ("refazer",), mouse)
        y += 30
        self.botao(t, pygame.Rect(a.x + 10, y, 63, 26), "Limpar", ("limpar",), mouse, cor=(90, 50, 54))
        self.botao(t, pygame.Rect(a.x + 77, y, 63, 26), "Virar ↔", ("virar",), mouse)
        y += 36
        t.blit(ed.fpp.render("Tamanho (pixels)", True, C_TEXTO2), (a.x + 12, y))
        y += 16
        for i, tam in enumerate(TAMANHOS_PIXEL):
            self.botao(t, pygame.Rect(a.x + 10 + (i % 3) * 44, y + (i // 3) * 28, 40, 24), str(tam), ("tam", tam), mouse,
                       ativo=self.n == tam)

        # tela de pintura
        tela_r, k = self.layout()
        xadrez = pygame.Surface((tela_r.w, tela_r.h))
        xadrez.fill((60, 62, 70))
        passo = max(4, k // 2) if k >= 8 else k
        for yy in range(0, tela_r.h, passo):
            for xx in range(0, tela_r.w, passo * 2):
                pygame.draw.rect(xadrez, (75, 77, 86), (xx + (passo if (yy // passo) % 2 else 0), yy, passo, passo))
        t.blit(xadrez, tela_r.topleft)
        if self.cebola and self.atual > 0:
            ant = pygame.transform.scale(self.quadros[self.atual - 1], (tela_r.w, tela_r.h))
            ant.set_alpha(70)
            t.blit(ant, tela_r.topleft)
        t.blit(pygame.transform.scale(self.quadros[self.atual], (tela_r.w, tela_r.h)), tela_r.topleft)
        if self.grade and k >= 6:
            for i in range(self.n + 1):
                cor_g = (40, 42, 50) if i % 4 else (30, 32, 38)
                pygame.draw.line(t, cor_g, (tela_r.x + i * k, tela_r.y), (tela_r.x + i * k, tela_r.bottom))
                pygame.draw.line(t, cor_g, (tela_r.x, tela_r.y + i * k), (tela_r.right, tela_r.y + i * k))
        if self.espelho:
            meio = tela_r.x + tela_r.w // 2
            pygame.draw.line(t, (255, 120, 200), (meio, tela_r.y), (meio, tela_r.bottom), 1)
        pygame.draw.rect(t, C_BORDA, tela_r, 1)
        p = self.px_em(mouse)
        if p is not None:
            pygame.draw.rect(t, (255, 255, 255), (tela_r.x + p[0] * k, tela_r.y + p[1] * k, k, k), 1)
            t.blit(ed.fpp.render(f"x {p[0]}  y {p[1]}", True, C_TEXTO2), (tela_r.x, tela_r.bottom + 4))

        # quadros (animacao)
        fy = tela_r.bottom + 22
        t.blit(ed.fb.render(f"QUADROS ({len(self.quadros)})", True, C_TEXTO2), (tela_r.x, fy))
        fx = tela_r.x + 110
        for i, q in enumerate(self.quadros[:12]):
            r = pygame.Rect(fx + i * 46, fy - 6, 40, 40)
            pygame.draw.rect(t, (50, 52, 60), r)
            t.blit(pygame.transform.scale(q, (40, 40)), r.topleft)
            pygame.draw.rect(t, C_DESTAQUE if i == self.atual else C_BORDA, r, 2 if i == self.atual else 1)
            self.hits.append((r, ("quadro", i)))
        fy += 42
        x = tela_r.x
        for rot, acao in (("+ Quadro (cópia)", ("q_add",)), ("+ Vazio", ("q_vazio",)), ("◀", ("q_mover", -1)),
                          ("▶", ("q_mover", 1)), ("Apagar quadro", ("q_del",))):
            w = ed.fp.size(rot)[0] + 18
            self.botao(t, pygame.Rect(x, fy, w, 24), rot, acao, mouse, cor=(90, 50, 54) if acao[0] == "q_del" else None)
            x += w + 6

        # paleta e cor
        px0 = a.right - 170
        y = a.y + 46
        t.blit(ed.fb.render("CORES", True, C_TEXTO2), (px0, y))
        y += 20
        for i, cor in enumerate(PALETA_PIXEL):
            r = pygame.Rect(px0 + (i % 6) * 26, y + (i // 6) * 26, 22, 22)
            pygame.draw.rect(t, cor, r, border_radius=4)
            if cor == self.cor:
                pygame.draw.rect(t, (255, 255, 255), r.inflate(4, 4), 2, border_radius=5)
            self.hits.append((r, ("cor", cor)))
        y += ((len(PALETA_PIXEL) + 5) // 6) * 26 + 8
        pygame.draw.rect(t, self.cor, (px0, y, 48, 48), border_radius=6)
        pygame.draw.rect(t, (255, 255, 255), (px0, y, 48, 48), 1, border_radius=6)
        for i, nome in enumerate("RGB"):
            yy = y + i * 17
            t.blit(ed.fpp.render(f"{nome} {self.cor[i]}", True, C_TEXTO2), (px0 + 56, yy + 2))
            self.botao(t, pygame.Rect(px0 + 112, yy, 18, 15), "-", ("rgb", i, -15), mouse)
            self.botao(t, pygame.Rect(px0 + 134, yy, 18, 15), "+", ("rgb", i, 15), mouse)
        y += 62

        # previa da animacao
        t.blit(ed.fb.render("PRÉVIA", True, C_TEXTO2), (px0, y))
        y += 18
        prev = pygame.Rect(px0, y, 96, 96)
        pygame.draw.rect(t, (50, 52, 60), prev)
        quadro = self.quadros[int(ed.tempo * self.fps) % len(self.quadros)] if len(self.quadros) > 1 else self.quadros[0]
        t.blit(pygame.transform.scale(quadro, (96, 96)), prev.topleft)
        pygame.draw.rect(t, C_BORDA, prev, 1)
        t.blit(ed.fpp.render(f"{self.fps} quadros/s", True, C_TEXTO2), (px0 + 102, y + 4))
        self.botao(t, pygame.Rect(px0 + 102, y + 22, 24, 22), "-", ("fps", -1), mouse)
        self.botao(t, pygame.Rect(px0 + 130, y + 22, 24, 22), "+", ("fps", 1), mouse)
        y += 106

        # salvar / aplicar
        if self.alvo is not None:
            rot = "Salvar e usar no objeto" if self.modo == "imagem" or len(self.quadros) == 1 else "Salvar e animar objeto"
            self.botao(t, pygame.Rect(px0, y, 160, 30), rot, ("salvar",), mouse, cor=C_VERDE)
            y += 34
            if self.alvo.get("tipo") == "Player" and len(self.quadros) > 1:
                self.botao(t, pygame.Rect(px0, y, 78, 26), "= andando", ("usar_como", "anim_andando"), mouse)
                self.botao(t, pygame.Rect(px0 + 82, y, 78, 26), "= pulando", ("usar_como", "anim_pulando"), mouse)
                y += 30
            if self.alvo.get("tipo") in ("Player", "NPC", "Inimigo") and len(self.quadros) > 1:
                for k_, (rot, campo) in enumerate((("= ↓", "anim_baixo"), ("= ↑", "anim_cima"), ("= ↔", "anim_lado"))):
                    self.botao(t, pygame.Rect(px0 + k_ * 54, y, 50, 26), rot, ("usar_como", campo), mouse)
                y += 30
        self.botao(t, pygame.Rect(px0, y, 160, 28), "Só salvar na pasta", ("salvar_so",), mouse)
        y += 32
        self.botao(t, pygame.Rect(px0, y, 160, 26), "Novo desenho", ("novo",), mouse, cor=(60, 64, 80))
        dica = "Botão direito apaga. Ctrl+Z desfaz.  [ ] troca de quadro."
        t.blit(ed.fpp.render(dica, True, C_TEXTO2), (a.x + 12, a.bottom - 18))
