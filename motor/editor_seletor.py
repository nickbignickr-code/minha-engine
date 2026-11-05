# Minha Engine - editor_seletor.py
# Janela de escolher QUANDO / SE / FAÇA / comportamentos: categorias, busca, descrição e rolagem (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

def descricao_do_item(tipo, nome):
    if tipo == "acao":
        return DESC_ACOES.get(nome, "")
    if tipo == "cond":
        return DESC_CONDICOES.get(nome, "")
    if tipo == "gatilho":
        return DESC_GATILHOS.get(nome) or DESC_EVENTOS.get(GATILHO_EVENTO.get(nome, ""), "")
    if tipo == "comp":
        return DESC_COMPORTAMENTOS.get(nome, "")
    return ""


class EditorSeletor:
    SEL_LINHA = 46

    def abrir_seletor(self, titulo, tipo, catalogo, categorias, ao_escolher, cor):
        cats = [("Tudo", list(catalogo))]
        usados = set()
        for nome, itens in categorias:
            validos = [i for i in itens if i in catalogo]
            usados.update(validos)
            if validos:
                cats.append((nome, validos))
        resto = [i for i in catalogo if i not in usados]
        if resto:
            cats.append(("Outros", resto))
        self.menu = None
        self.seletor = {"titulo": titulo, "tipo": tipo, "catalogo": catalogo, "cats": cats, "cat": "Tudo",
                        "busca": "", "scroll": 0, "fn": ao_escolher, "cor": cor, "hits": [], "sobre": None,
                        "t0": agora_ui()}

    def itens_seletor(self):
        s = self.seletor
        itens = dict(s["cats"]).get(s["cat"], [])
        b = s["busca"].strip().lower()
        if b:
            palavras = b.split()
            no_nome, na_desc = [], []
            for i in s["catalogo"]:
                nome_l = i.lower()
                if all(p in nome_l for p in palavras):
                    no_nome.append(i)
                elif all(p in nome_l or p in descricao_do_item(s["tipo"], i).lower() for p in palavras):
                    na_desc.append(i)
            # primeiro o que começa com a busca, depois o que tem no nome, depois o que só tem na descrição
            no_nome.sort(key=lambda i: (not i.lower().split(": ")[-1].startswith(b), len(i)))
            itens = no_nome + na_desc
        return itens

    def rect_seletor(self):
        w = min(900, LARGURA - 60)
        h = min(600, ALTURA - 60)
        return pygame.Rect((LARGURA - w) // 2, (ALTURA - h) // 2, w, h)

    def desenhar_seletor(self, t, mouse):
        s = self.seletor
        if not s:
            return
        s["hits"] = []
        k = entrada(s.get("t0", 0), 0.18)
        sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, int(150 * k)))
        t.blit(sombra, (0, 0))
        caixa = self.rect_seletor().move(0, int((1 - k) * 18))
        sombra_painel(t, caixa, 14)
        pygame.draw.rect(t, clarear(C_PAINEL, -6), caixa, border_radius=14)
        pygame.draw.rect(t, s["cor"], (caixa.x, caixa.y, caixa.w, 6), border_top_left_radius=14,
                         border_top_right_radius=14)
        t.blit(self.fg.render(s["titulo"], True, C_TEXTO), (caixa.x + 20, caixa.y + 16))
        fechar = pygame.Rect(caixa.right - 40, caixa.y + 14, 26, 26)
        desenhar_botao(t, self.fp, fechar, "x", mouse, cor=(90, 50, 54))
        s["hits"].append((fechar, ("fechar",)))
        # busca
        busca = pygame.Rect(caixa.x + 20, caixa.y + 54, caixa.w - 40, 32)
        pygame.draw.rect(t, C_CAMPO, busca, border_radius=8)
        pygame.draw.rect(t, s["cor"], busca, 1, border_radius=8)
        piscar = "|" if int(self.tempo * 2) % 2 == 0 else ""
        txt = s["busca"] + piscar if s["busca"] else "Digite para buscar (ex: vida, pular, tiro, mouse)..."
        t.blit(self.f.render(txt, True, C_TEXTO if s["busca"] else C_TEXTO2), (busca.x + 12, busca.y + 7))
        # categorias
        col = pygame.Rect(caixa.x + 12, busca.bottom + 12, 210, caixa.bottom - busca.bottom - 24)
        y = col.y
        for nome, itens in s["cats"]:
            r = pygame.Rect(col.x, y, col.w, 30)
            ativo = nome == s["cat"] and not s["busca"]
            if ativo:
                pygame.draw.rect(t, s["cor"], r, border_radius=7)
            elif r.collidepoint(mouse):
                pygame.draw.rect(t, (48, 52, 64), r, border_radius=7)
            rot = nome if len(nome) <= 24 else nome[:23] + "…"
            t.blit(self.fp.render(rot, True, C_TEXTO), (r.x + 10, r.y + 7))
            n = self.fpp.render(str(len(itens)), True, C_TEXTO2)
            t.blit(n, (r.right - n.get_width() - 8, r.y + 8))
            s["hits"].append((r, ("cat", nome)))
            y += 33
            if y > col.bottom - 30:
                break
        # lista
        lista = pygame.Rect(col.right + 12, col.y, caixa.right - col.right - 32, col.h)
        pygame.draw.rect(t, (28, 30, 37), lista, border_radius=10)
        itens = self.itens_seletor()
        lh = self.SEL_LINHA
        total = len(itens) * lh
        s["scroll"] = max(0, min(s["scroll"], max(0, total - lista.h + 8)))
        vis = suave(("seletor", s["titulo"], s["cat"], s["busca"]), s["scroll"])
        t.set_clip(lista)
        s["sobre"] = None
        for i, nome in enumerate(itens):
            r = pygame.Rect(lista.x + 6, lista.y + 4 + i * lh - vis, lista.w - 22, lh - 4)
            if r.bottom < lista.y or r.y > lista.bottom:
                continue
            em_cima = r.collidepoint(mouse) and lista.collidepoint(mouse)
            pygame.draw.rect(t, (52, 57, 72) if em_cima else (38, 41, 50), r, border_radius=7)
            if em_cima:
                pygame.draw.rect(t, s["cor"], (r.x, r.y + 6, 3, r.h - 12))
                s["sobre"] = nome
            t.blit(self.fb.render(nome, True, C_TEXTO), (r.x + 12, r.y + 4))
            desc = descricao_do_item(s["tipo"], nome)
            spec = s["catalogo"].get(nome, [])
            if not desc and spec:
                desc = "Opções: " + ", ".join(p[0] for p in spec)
            if desc:
                linha = quebrar_texto(desc, self.fpp, r.w - 24)[0]
                t.blit(self.fpp.render(linha, True, C_TEXTO2), (r.x + 12, r.y + 23))
            if lista.collidepoint(r.center):
                s["hits"].append((r.clip(lista), ("item", nome)))
        t.set_clip(None)
        if total > lista.h:      # barra de rolagem
            trilho = pygame.Rect(lista.right - 10, lista.y + 6, 6, lista.h - 12)
            pygame.draw.rect(t, (50, 54, 66), trilho, border_radius=3)
            alto = max(30, int(trilho.h * lista.h / total))
            topo = trilho.y + int((trilho.h - alto) * vis / max(1, total - lista.h + 8))
            pygame.draw.rect(t, s["cor"], (trilho.x, topo, trilho.w, alto), border_radius=3)
            s["hits"].append((trilho.inflate(10, 0), ("barra", trilho, total, lista.h)))
        if not itens:
            t.blit(self.f.render("Nada encontrado com essa busca.", True, C_TEXTO2), (lista.x + 16, lista.y + 16))
        rod = self.fpp.render(f"{len(itens)} opção(ões)  ·  clique para escolher  ·  rodinha rola  ·  Esc fecha",
                              True, C_TEXTO2)
        t.blit(rod, (lista.x, caixa.bottom - 18))

    def clique_seletor(self, pos):
        s = self.seletor
        caixa = self.rect_seletor()
        if not caixa.collidepoint(pos):
            self.seletor = None
            return
        for r, a in reversed(s["hits"]):
            if not r.collidepoint(pos):
                continue
            if a[0] == "fechar":
                self.seletor = None
            elif a[0] == "cat":
                s["cat"], s["busca"], s["scroll"] = a[1], "", 0
            elif a[0] == "item":
                fn, self.seletor = s["fn"], None
                fn(a[1])
            elif a[0] == "barra":
                _, trilho, total, altura = a
                k = (pos[1] - trilho.y) / max(1, trilho.h)
                s["scroll"] = int(max(0.0, min(1.0, k)) * max(0, total - altura + 8))
                self.arrastando = ("sel_barra", trilho, total, altura)
            return

    def arrastar_barra_seletor(self, pos):
        if self.seletor and self.arrastando and self.arrastando[0] == "sel_barra":
            _, trilho, total, altura = self.arrastando
            k = (pos[1] - trilho.y) / max(1, trilho.h)
            self.seletor["scroll"] = int(max(0.0, min(1.0, k)) * max(0, total - altura + 8))

    def tecla_seletor(self, e):
        s = self.seletor
        if e.key == pygame.K_ESCAPE:
            self.seletor = None
        elif e.key == pygame.K_BACKSPACE:
            s["busca"] = s["busca"][:-1]
            s["scroll"] = 0
        elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            itens = self.itens_seletor()
            if itens:
                fn, self.seletor = s["fn"], None
                fn(itens[0])
        elif e.key == pygame.K_DOWN:
            s["scroll"] += self.SEL_LINHA
        elif e.key == pygame.K_UP:
            s["scroll"] = max(0, s["scroll"] - self.SEL_LINHA)
        elif e.unicode and e.unicode.isprintable() and not (e.mod & pygame.KMOD_CTRL):
            s["busca"] += e.unicode
            s["scroll"] = 0

    def roda_seletor(self, y):
        self.seletor["scroll"] = max(0, self.seletor["scroll"] - y * self.SEL_LINHA)
