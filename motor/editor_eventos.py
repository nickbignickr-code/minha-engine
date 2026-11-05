# Minha Engine - editor_eventos.py
# aba Eventos (programação visual) (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class EditorEventos:
    # ----------------- ABA EVENTOS (programacao visual) -----------------
    def clique_eventos(self, pos):
        alvo = self.alvo_logica()
        for r, a in reversed(self.hits_ev):
            if not r.collidepoint(pos):
                continue
            k = a[0]
            if k == "add_evento":
                def novo_evento(g):
                    self.guardar()
                    alvo["eventos"].append({"gatilho": g, "gp": params_padrao(GATILHOS[g]),
                                            "condicoes": [], "acoes": []})
                self.abrir_seletor("QUANDO acontece...", "gatilho", GATILHOS, CATEGORIAS_GATILHOS, novo_evento,
                                   C_QUANDO)
            elif k == "gatilho":
                ev = a[1]

                def trocar(g, ev=ev):
                    self.guardar()
                    ev["gatilho"] = g
                    ev["gp"] = params_padrao(GATILHOS[g])
                self.abrir_seletor("Trocar o QUANDO", "gatilho", GATILHOS, CATEGORIAS_GATILHOS, trocar, C_QUANDO)
            elif k == "add_cond":
                lista = a[1]
                self.abrir_seletor("SE (condição)", "cond", CONDICOES, CATEGORIAS_CONDICOES,
                                   lambda c, l=lista: self.adicionar_item(l, c, CONDICOES), C_SE)
            elif k == "add_acao":
                lista = a[1]
                self.abrir_seletor("FAÇA (ação)", "acao", ACOES, CATEGORIAS_ACOES,
                                   lambda c, l=lista: self.adicionar_item(l, c, ACOES), C_FACA)
            elif k == "ev_barra":
                trilho = a[1]
                k_ = (pos[1] - trilho.y) / max(1, trilho.h)
                self.ev_scroll = int(max(0.0, min(1.0, k_)) * max(0, self.ev_total - VIEW.h + 20))
                self.arrastando = ("ev_barra", trilho)
            elif k == "del":
                self.guardar()
                if a[2] in a[1]:
                    a[1].remove(a[2])
            elif k == "edit":
                self.comecar_edicao(a[1], a[2])
            elif k == "lista":
                params, nome, opcoes = a[1], a[2], a[3]

                def escolher(item, params=params, nome=nome):
                    if item == "(escrever outro...)":
                        self.comecar_edicao(params, nome)
                        return
                    self.guardar()
                    params[nome] = item
                self.abrir_menu(pos, list(opcoes) + ["(escrever outro...)"], escolher)
            elif k == "nao":
                self.guardar()
                a[1]["nao"] = not a[1].get("nao")
            elif k == "op":
                params, nome, opcoes = a[1], a[2], a[3]
                self.guardar()
                atual = params.get(nome, opcoes[0])
                i = opcoes.index(atual) if atual in opcoes else -1
                params[nome] = opcoes[(i + 1) % len(opcoes)]
            elif k == "add_func":
                self.guardar()
                funcs = self.cena["funcoes"]
                nome = self.nome_unico("minha_funcao", {f["nome"] for f in funcs})
                funcs.append({"nome": nome, "acoes": []})
            elif k == "recolher":
                a[1]["recolhido"] = not a[1].get("recolhido")
            elif k == "ativo":
                self.guardar()
                a[1]["ativo"] = a[1].get("ativo") is False
            elif k == "copiar_ev":
                self.clip_eventos = [copy.deepcopy(a[1])]
                self.avisar("Evento copiado. Selecione outro objeto e clique em 'Colar evento'.")
            elif k == "copiar_todos":
                self.clip_eventos = copy.deepcopy(alvo["eventos"])
                self.avisar(f"{len(self.clip_eventos)} evento(s) copiado(s).")
            elif k == "dup_ev":
                self.guardar()
                lista, item = a[1], a[2]
                lista.insert(lista.index(item) + 1, copy.deepcopy(item))
            elif k == "colar_ev":
                self.guardar()
                alvo["eventos"].extend(copy.deepcopy(self.clip_eventos))
                self.avisar(f"{len(self.clip_eventos)} evento(s) colado(s) em {self.nome_alvo()}.")
            elif k == "mover_ev":
                lista, item, direcao = a[1], a[2], a[3]
                i = lista.index(item)
                j = i + direcao
                if 0 <= j < len(lista):
                    self.guardar()
                    lista[i], lista[j] = lista[j], lista[i]
            return

    def adicionar_item(self, lista, nome, catalogo):
        self.guardar()
        lista.append({"t": nome, "p": params_padrao(catalogo[nome])})

    def chip(self, t, x, y, txt, cor):
        img = self.fb.render(txt, True, (255, 255, 255))
        r = pygame.Rect(x, y, img.get_width() + 14, 22)
        pygame.draw.rect(t, cor, r, border_radius=4)
        t.blit(img, (x + 7, y + 3))
        return r

    def campo_ev(self, t, x, y, params, nome, tipo):
        valor = params.get(nome, "")
        ed = self.editando is not None and self.editando[0] is params and self.editando[1] == nome
        piscar = int(self.tempo * 2) % 2 == 0
        txt = (self.buffer + ("|" if piscar else " ")) if ed else valor
        escolha = tipo in ("cmp", "atr", "sn")
        img = self.fp.render(txt, True, (255, 230, 150) if escolha else C_TEXTO)
        r = pygame.Rect(x, y, max(28, img.get_width() + 12), 22)
        if tipo == "sn":
            fundo = C_VERDE if valor == "Sim" else C_BOTAO
        else:
            fundo = (60, 52, 25) if escolha else C_CAMPO
        pygame.draw.rect(t, fundo, r, border_radius=4)
        pygame.draw.rect(t, C_DESTAQUE if ed else C_BORDA, r, 1, border_radius=4)
        t.blit(img, (x + 6, y + 4))
        if tipo == "cmp":
            self.hits_ev.append((r, ("op", params, nome, OPS_CMP)))
        elif tipo == "atr":
            self.hits_ev.append((r, ("op", params, nome, OPS_ATR)))
        elif tipo == "sn":
            self.hits_ev.append((r, ("op", params, nome, OPS_SN)))
        elif nome in OPCOES_PARAMS:
            pygame.draw.polygon(t, C_TEXTO2, [(r.right - 9, r.y + 9), (r.right - 3, r.y + 9), (r.right - 6, r.y + 13)])
            r.w += 8
            self.hits_ev.append((r, ("lista", params, nome, OPCOES_PARAMS[nome])))
        else:
            self.hits_ev.append((r, ("edit", params, nome)))
        return r

    def linha_item(self, t, x, y, w, prefixo, cor, titulo, spec, params, hit_titulo=None, lista=None, item=None,
                   hit_prefixo=None):
        r = self.chip(t, x, y, prefixo, cor)
        if hit_prefixo:
            self.hits_ev.append((r, hit_prefixo))
        xx = r.right + 6
        img = self.fp.render(titulo, True, (255, 255, 255) if hit_titulo else C_TEXTO)
        tr = pygame.Rect(xx - 2, y, img.get_width() + 4, 22)
        if hit_titulo:
            pygame.draw.rect(t, C_BOTAO, tr, border_radius=4)
            self.hits_ev.append((tr, hit_titulo))
        t.blit(img, (xx, y + 4))
        xx += img.get_width() + 10
        for nome, _, tipo in spec:
            lbl = self.fpp.render(nome + ":", True, C_TEXTO2)
            t.blit(lbl, (xx, y + 5))
            xx += lbl.get_width() + 3
            fr = self.campo_ev(t, xx, y, params, nome, tipo)
            xx = fr.right + 8
        if lista is not None:
            xr = pygame.Rect(x + w - 20, y + 2, 18, 18)
            pygame.draw.rect(t, (90, 45, 45), xr, border_radius=3)
            t.blit(self.fpp.render("x", True, (255, 200, 200)), (xr.x + 6, xr.y + 2))
            self.hits_ev.append((xr, ("del", lista, item)))

    def botao_add(self, t, x, y, txt, hit, mouse):
        img = self.fp.render(txt, True, C_TEXTO2)
        r = pygame.Rect(x, y, img.get_width() + 16, 22)
        pygame.draw.rect(t, C_BOTAO if r.collidepoint(mouse) else (36, 39, 47), r, border_radius=4)
        pygame.draw.rect(t, C_BORDA, r, 1, border_radius=4)
        t.blit(img, (x + 8, y + 4))
        self.hits_ev.append((r, hit))
        return r

    def botao_mini(self, t, x, y, txt, hit, cor=None, largura=None):
        img = self.fpp.render(txt, True, C_TEXTO)
        r = pygame.Rect(x, y, largura or img.get_width() + 10, 18)
        pygame.draw.rect(t, cor or C_BOTAO, r, border_radius=3)
        t.blit(img, (r.centerx - img.get_width() // 2, r.y + 2))
        self.hits_ev.append((r, hit))
        return r

    def desenhar_eventos(self, t, mouse):
        alvo = self.alvo_logica()
        area = VIEW
        pygame.draw.rect(t, (24, 26, 32), area)
        t.set_clip(area)
        self.hits_ev = []
        ev_vis = suave((id(self), "ev", id(self.alvo_logica())), self.ev_scroll)
        y = area.y + 10 - ev_vis
        extra = f"   (vários selecionados: editando só '{self.sel['nome']}')" if len(self.selecao) > 1 else ""
        t.blit(self.f.render(f"EVENTOS de: {self.nome_alvo()}{extra}", True, C_TEXTO), (area.x + 12, y))
        t.blit(self.fp.render("QUANDO acontece algo  →  SE as condições forem verdade  →  FAÇA as ações.   "
                              "Nos valores dá para usar contas: eu.x + 10", True, C_TEXTO2), (area.x + 12, y + 22))
        y += 50
        eventos = alvo.setdefault("eventos", [])
        col_l = area.x + 30
        largura = area.right - 12 - col_l

        for n, ev in enumerate(eventos):
            conds = ev.setdefault("condicoes", [])
            acoes = ev.setdefault("acoes", [])
            ativo = ev.get("ativo") is not False
            recolhido = bool(ev.get("recolhido"))
            h = 34 if recolhido else (4 + len(conds) + len(acoes)) * 27 + 14
            bloco = pygame.Rect(area.x + 6, y, area.w - 12, h)
            if bloco.bottom >= area.y and bloco.y <= area.bottom:
                pygame.draw.rect(t, (38, 41, 50) if ativo else (33, 33, 36), bloco, border_radius=6)
                pygame.draw.rect(t, C_BORDA if ativo else (80, 60, 60), bloco, 1, border_radius=6)
                t.blit(self.fb.render(f"#{n + 1}", True, C_TEXTO2), (bloco.x + 6, y + 9))
                # nome do evento (comentario)
                ev.setdefault("nome", "")
                r_nome = self.campo_ev(t, col_l, y + 6, ev, "nome", "s")
                if not ev["nome"] and not (self.editando and self.editando[0] is ev):
                    t.blit(self.fpp.render("dê um nome (opcional)", True, (110, 112, 125)), (r_nome.right + 6, y + 10))
                if not ativo:
                    t.blit(self.fb.render("DESATIVADO", True, (220, 120, 120)), (r_nome.right + 150, y + 8))
                # botoes do bloco
                bx = bloco.right - 8
                for rot, hit, cor, w in reversed([
                        ("+" if recolhido else "-", ("recolher", ev), None, 20),
                        ("ligado" if ativo else "desligado", ("ativo", ev), C_VERDE if ativo else C_VERMELHO, 62),
                        ("copiar", ("copiar_ev", ev), None, 48), ("duplicar", ("dup_ev", eventos, ev), None, 56),
                        ("^", ("mover_ev", eventos, ev, -1), None, 20), ("v", ("mover_ev", eventos, ev, 1), None, 20),
                        ("x", ("del", eventos, ev), (90, 45, 45), 20)]):
                    bx -= w + 4
                    self.botao_mini(t, bx, y + 8, rot, hit, cor, w)

                if recolhido:
                    resumo = f"QUANDO {ev.get('gatilho', '?')}  ·  {len(conds)} condição(ões)  ·  {len(acoes)} ação(ões)"
                    t.blit(self.fp.render(resumo, True, C_TEXTO2), (col_l + 160, y + 10))
                else:
                    ly = y + 34
                    self.linha_item(t, col_l, ly, largura, "QUANDO", C_QUANDO, ev.get("gatilho", "?"),
                                    GATILHOS.get(ev.get("gatilho"), []), ev.setdefault("gp", {}),
                                    hit_titulo=("gatilho", ev))
                    ly += 27
                    for c in conds:
                        nao = bool(c.get("nao"))
                        self.linha_item(t, col_l + 18, ly, largura - 18, "SE NÃO" if nao else "SE",
                                        C_VERMELHO if nao else C_SE, c.get("t", "?"),
                                        CONDICOES.get(c.get("t"), []), c.setdefault("p", {}),
                                        lista=conds, item=c, hit_prefixo=("nao", c))
                        ly += 27
                    self.botao_add(t, col_l + 18, ly, "+ Condição", ("add_cond", conds), mouse)
                    if conds:
                        t.blit(self.fpp.render("(clique no SE para virar SE NÃO)", True, C_TEXTO2), (col_l + 120, ly + 5))
                    ly += 27
                    for a in acoes:
                        self.linha_item(t, col_l + 36, ly, largura - 36, "FAÇA", C_FACA,
                                        a.get("t", "?"), ACOES.get(a.get("t"), []), a.setdefault("p", {}),
                                        lista=acoes, item=a)
                        ly += 27
                    self.botao_add(t, col_l + 36, ly, "+ Ação", ("add_acao", acoes), mouse)
            y += h + 8

        r = self.botao_add(t, area.x + 12, y, "+ Novo evento", ("add_evento",), mouse)
        x = r.right + 10
        if self.clip_eventos:
            r = self.botao_add(t, x, y, f"Colar {len(self.clip_eventos)} evento(s)", ("colar_ev",), mouse)
            x = r.right + 10
        if eventos:
            self.botao_add(t, x, y, "Copiar todos os eventos", ("copiar_todos",), mouse)
        y += 44

        # Funcoes visuais (da fase)
        pygame.draw.line(t, C_BORDA, (area.x + 12, y), (area.right - 12, y))
        y += 10
        t.blit(self.f.render("FUNÇÕES (servem para todos os objetos desta fase)", True, C_TEXTO), (area.x + 12, y))
        t.blit(self.fp.render("Use a ação 'Chamar função' ou no script: nome_da_funcao()", True, C_TEXTO2),
               (area.x + 12, y + 20))
        y += 46
        funcs = self.cena.setdefault("funcoes", [])
        for f in funcs:
            acoes = f.setdefault("acoes", [])
            h = (2 + len(acoes)) * 27 + 10
            bloco = pygame.Rect(area.x + 6, y, area.w - 12, h)
            pygame.draw.rect(t, (30, 44, 46), bloco, border_radius=6)
            pygame.draw.rect(t, C_BORDA, bloco, 1, border_radius=6)
            r = self.chip(t, col_l, y + 7, "FUNÇÃO", C_FUNCAO)
            self.campo_ev(t, r.right + 8, y + 7, f, "nome", "s")
            self.botao_mini(t, bloco.right - 26, y + 6, "x", ("del", funcs, f), (90, 45, 45), 20)
            ry = y + 34
            for a in acoes:
                self.linha_item(t, col_l + 14, ry, bloco.w - 30, "FAÇA", C_FACA, a.get("t", "?"),
                                ACOES.get(a.get("t"), []), a.setdefault("p", {}), lista=acoes, item=a)
                ry += 27
            self.botao_add(t, col_l + 14, ry, "+ Ação", ("add_acao", acoes), mouse)
            y += h + 8
        self.botao_add(t, area.x + 12, y, "+ Nova função", ("add_func",), mouse)
        y += 40

        self.ev_total = y + ev_vis - area.y
        self.ev_scroll = max(0, min(self.ev_scroll, max(0, self.ev_total - area.h + 20)))
        t.set_clip(None)
        if self.ev_total > area.h:
            trilho = pygame.Rect(area.right - 9, area.y + 6, 6, area.h - 12)
            pygame.draw.rect(t, (50, 54, 66), trilho, border_radius=3)
            alto = max(30, int(trilho.h * area.h / self.ev_total))
            topo = trilho.y + int((trilho.h - alto) * ev_vis / max(1, self.ev_total - area.h + 20))
            pygame.draw.rect(t, C_DESTAQUE, (trilho.x, topo, trilho.w, alto), border_radius=3)
            self.hits_ev.append((trilho.inflate(12, 0), ("ev_barra", trilho)))
