# Minha Engine - editor_base.py
# fase atual, utilidades, guia Primeiros passos, Saída, seleção, desfazer, arquivos, fases, play (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class EditorBase:
    # ----------------- fase atual -----------------
    @property
    def fase(self):
        return self.projeto["fases"][self.projeto["fase_atual"]]

    @property
    def objetos(self):
        return self.fase["objetos"]

    @property
    def cena(self):
        return self.fase["cena"]

    # ----------------- utilidades -----------------
    def avisar(self, txt, tipo=None):
        self.msg = txt
        self.msg_t = 4.0
        tipo = tipo or tipo_do_aviso(txt)
        if tipo == "erro":
            self.registrar("aviso", txt)
        if hasattr(self, "toasts"):
            self.toasts = [b for b in self.toasts if b["txt"] != txt][-3:]
            self.toasts.append({"txt": txt, "tipo": tipo, "t": getattr(self, "tempo", 0.0),
                                "dur": 7.0 if tipo == "erro" else 4.5})

    def mostrar_novidades(self):
        while NOVIDADES_CARTEIRA:
            self.avisar(NOVIDADES_CARTEIRA.pop(0), "ok")

    def reabrir_passos(self):
        self.mostrar_passos = True
        self.passos_min = False
        self.aba = "cena"
        CONFIG["geral"]["primeiros_passos"] = True
        salvar_config()

    def toasts_vivos(self):
        agora = getattr(self, "tempo", 0.0)
        self.toasts = [b for b in self.toasts if agora - b["t"] < b["dur"]]
        return self.toasts

    def rects_toasts(self):
        out = []
        y = ALTURA - RODAPE - 12
        if self.saida_aberta:
            y = self.rect_saida().y - 8
        for b in reversed(self.toasts):
            linhas = quebrar_texto(b["txt"], self.fp, 330)[:3]
            h = 18 + len(linhas) * 18
            r = pygame.Rect(VIEW.right - 400, y - h, 390, h)
            out.append((b, r, linhas))
            y -= h + 8
        return out

    def desenhar_toasts(self, t, mouse):
        if not CONFIG["geral"].get("notificacoes", True) or self.jogo and self.play_cheio:
            return
        self.toasts_vivos()
        agora = self.tempo
        for b, r, linhas in self.rects_toasts():
            idade = agora - b["t"]
            entrada = min(1.0, idade / 0.18)
            saida = min(1.0, max(0.0, (b["dur"] - idade) / 0.5))
            dx = int((1 - entrada) * 40)
            r = r.move(dx, 0)
            cor = CORES_AVISO.get(b["tipo"], CORES_AVISO["info"])
            caixa = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            alpha = int(245 * saida)
            pygame.draw.rect(caixa, (12, 13, 17, alpha // 2), (2, 3, r.w - 2, r.h - 3), border_radius=10)
            pygame.draw.rect(caixa, (46, 49, 60, alpha), (0, 0, r.w - 2, r.h - 3), border_radius=10)
            pygame.draw.rect(caixa, (*cor, alpha), (0, 0, 5, r.h - 3), border_top_left_radius=10,
                             border_bottom_left_radius=10)
            t.blit(caixa, r.topleft)
            if saida > 0.3:
                desenhar_icone_aviso(t, b["tipo"], (r.x + 24, r.y + 18))
                for i, linha in enumerate(linhas):
                    t.blit(self.fp.render(linha, True, C_TEXTO), (r.x + 44, r.y + 8 + i * 18))
                if r.collidepoint(mouse):
                    t.blit(self.fpp.render("x", True, C_TEXTO2), (r.right - 16, r.y + 4))

    def clique_toast(self, pos):
        if not CONFIG["geral"].get("notificacoes", True):
            return False
        for b, r, _ in self.rects_toasts():
            if r.collidepoint(pos):
                self.toasts = [x for x in self.toasts if x is not b]
                return True
        return False

    # ----------------- primeiros passos -----------------
    def passo_feito(self, chave):
        objs = self.objetos
        if chave in self.passos_feitos:
            return True
        ok = False
        if chave == "peca":
            ok = any(d["tipo"] == "Peça" for d in objs)
        elif chave == "aparencia":
            ok = any(d["tipo"] == "Peça" and (d.get("material", "Plástico") != "Plástico" or
                                              d.get("forma", "Retângulo") != "Retângulo" or d.get("imagem") or
                                              list(d.get("cor", [])) != [163, 162, 165]) for d in objs)
        elif chave == "player":
            ok = any(d["tipo"] == "Player" for d in objs)
        elif chave == "desenho":
            ok = any(d.get("animacao") for d in objs)
        elif chave == "script":
            ok = any((d.get("script") or "").strip() or d.get("eventos") for d in objs)
        return bool(ok)

    def rect_passos(self):
        h = 44 if self.passos_min else 64 + len(PASSOS) * 34
        return pygame.Rect(VIEW.x + 10, VIEW.bottom - h - 10, 300, h)

    def desenhar_passos(self, t, mouse):
        self.hits_passos = []
        if not self.mostrar_passos or self.jogo or self.aba != "cena":
            return
        feitos = [self.passo_feito(c) for c, _, _ in PASSOS]
        n = sum(feitos)
        r = self.rect_passos()
        caixa = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        pygame.draw.rect(caixa, (30, 32, 40, 236), (0, 0, r.w, r.h), border_radius=12)
        t.blit(caixa, r.topleft)
        pygame.draw.rect(t, C_BORDA, r, 1, border_radius=12)
        titulo = "Parabéns! Você já sabe o básico" if n == len(PASSOS) else "Primeiros passos"
        if n == len(PASSOS) and ganhar_conquista("primeiros_passos"):
            self.mostrar_novidades()
        t.blit(self.fb.render(titulo, True, C_TEXTO), (r.x + 14, r.y + 10))
        barra = pygame.Rect(r.x + 14, r.y + 31, r.w - 90, 6)
        pygame.draw.rect(t, (55, 58, 70), barra, border_radius=3)
        pygame.draw.rect(t, C_VERDE, (barra.x, barra.y, int(barra.w * n / len(PASSOS)), barra.h), border_radius=3)
        t.blit(self.fpp.render(f"{n} de {len(PASSOS)}", True, C_TEXTO2), (barra.right + 8, barra.y - 5))
        bmin = pygame.Rect(r.right - 52, r.y + 8, 20, 20)
        bx = pygame.Rect(r.right - 28, r.y + 8, 20, 20)
        for b, sim in ((bmin, "+" if self.passos_min else "–"), (bx, "x")):
            pygame.draw.rect(t, clarear(C_BOTAO, 15) if b.collidepoint(mouse) else C_BOTAO, b, border_radius=5)
            img = self.fpp.render(sim, True, C_TEXTO)
            t.blit(img, (b.centerx - img.get_width() // 2, b.centery - img.get_height() // 2))
        self.hits_passos += [(bmin, ("min",)), (bx, ("fechar",))]
        if self.passos_min:
            self.hits_passos.append((r, ("min",)))
            return
        y = r.y + 50
        proximo = next((i for i, f in enumerate(feitos) if not f), None)
        for i, ((chave, rot, dica), feito) in enumerate(zip(PASSOS, feitos)):
            lr = pygame.Rect(r.x + 8, y, r.w - 16, 32)
            if lr.collidepoint(mouse) and not feito:
                pygame.draw.rect(t, (48, 52, 64), lr, border_radius=7)
            elif i == proximo:
                pygame.draw.rect(t, (40, 48, 70), lr, border_radius=7)
            c = (lr.x + 14, lr.centery)
            if feito:
                desenhar_icone_aviso(t, "ok", c, 9)
            else:
                pygame.draw.circle(t, C_DESTAQUE if i == proximo else (110, 114, 128), c, 9, 2)
            t.blit(self.fp.render(rot, True, C_TEXTO2 if feito else C_TEXTO), (lr.x + 32, lr.y + 1))
            t.blit(self.fpp.render("Feito!" if feito else dica, True, C_VERDE if feito else C_TEXTO2),
                   (lr.x + 32, lr.y + 17))
            if not feito:
                self.hits_passos.append((lr, ("passo", chave)))
            y += 34

    def clique_passos(self, pos):
        for r, a in self.hits_passos:
            if not r.collidepoint(pos):
                continue
            if a[0] == "min":
                self.passos_min = not self.passos_min
            elif a[0] == "fechar":
                self.mostrar_passos = False
                CONFIG["geral"]["primeiros_passos"] = False
                salvar_config()
                self.avisar("Guia escondido. Para ver de novo: botão Ajuda > Primeiros passos.", "info")
            elif a[0] == "passo":
                self.fazer_passo(a[1])
            return True
        return False

    def fazer_passo(self, chave):
        if chave in ("peca", "player"):
            self.ferramenta = "Peça" if chave == "peca" else "Player"
            self.avisar(f"Agora clique na cena para colocar {'a Peça' if chave == 'peca' else 'o Player'}.", "info")
        elif chave == "aparencia":
            peca = next((d for d in self.objetos if d["tipo"] == "Peça"), None)
            if peca is not None:
                self.selecionar(peca)
            self.avisar("No painel da direita mude 'cor', 'forma' ou 'material' (clique no valor).", "info")
        elif chave == "play":
            self.play()
        elif chave == "desenho":
            alvo = self.sel or next((d for d in self.objetos if d["tipo"] == "Peça"), None)
            self.abrir_desenho(alvo, "animacao" if alvo is not None else "imagem")
        elif chave == "loja":
            self.aba = "loja"
        elif chave == "script":
            self.aba = "eventos"
            self.avisar("Clique em '+ Evento' e escolha quando algo acontece. Depois adicione ações.", "info")

    # ----------------- cena vazia -----------------
    def desenhar_vazio_cena(self, t, mouse):
        self.hits_vazio = []
        if len(self.objetos) > 1 or any(d["tipo"] == "Player" for d in self.objetos) or self.jogo \
                or self.ferramenta != "Selecionar" or self.menu:
            return
        card = pygame.Rect(0, 0, 420, 196)
        card.center = (VIEW.centerx + (90 if self.mostrar_passos else 0), VIEW.centery - 20)
        caixa = pygame.Surface(card.size, pygame.SRCALPHA)
        pygame.draw.rect(caixa, (30, 32, 40, 225), (0, 0, card.w, card.h), border_radius=14)
        t.blit(caixa, card.topleft)
        desenhar_simbolo(t, card.x + 20, card.y + 20, 36)
        t.blit(self.fg.render("Sua fase ainda está vazia", True, C_TEXTO), (card.x + 68, card.y + 18))
        t.blit(self.fpp.render("Como você quer começar?", True, C_TEXTO2), (card.x + 70, card.y + 48))
        opcoes = [("Colocar uma Peça", ("ferr", "Peça"), C_DESTAQUE), ("Fase pronta (kit)", ("kit",), C_VERDE),
                  ("Abrir a Loja", ("loja",), (130, 80, 170)), ("Abrir um exemplo", ("exemplo",), (70, 76, 92))]
        for i, (rot, acao, cor) in enumerate(opcoes):
            r = pygame.Rect(card.x + 20 + (i % 2) * 194, card.y + 84 + (i // 2) * 48, 186, 38)
            desenhar_botao(t, self.fp, r, rot, mouse, cor=cor)
            self.hits_vazio.append((r, acao))

    def clique_vazio(self, pos):
        for r, a in getattr(self, "hits_vazio", []):
            if not r.collidepoint(pos):
                continue
            self.hits_vazio = []
            if a[0] == "ferr":
                self.ferramenta = a[1]
                self.avisar("Clique na cena para colocar. Esc volta para Selecionar.", "info")
            elif a[0] == "kit":
                self.loja.inserir(next(i for i in LOJA if i["nome"] == "Kit de fase"))
            elif a[0] == "loja":
                self.aba = "loja"
            elif a[0] == "exemplo":
                self.acao("novo")
            return True
        return False

    # ----------------- janela Saida -----------------
    def registrar(self, tipo, texto_, dono=None, linha=None):
        import time
        if not hasattr(self, "saida"):      # ainda abrindo o editor
            return
        self.saida.append({"tipo": tipo, "texto": str(texto_), "dono": dono, "linha": linha,
                           "hora": time.strftime("%H:%M:%S"), "fase": self.projeto.get("fase_atual")})
        if len(self.saida) > 2000:
            del self.saida[:500]
        if tipo == "erro" and not self.saida_aberta:
            self.saida_erros_novos += 1
        self.saida_scroll = 0

    def puxar_saida_do_jogo(self):
        j = self.jogo
        if j is None:
            return
        total = j.saida_base + len(j.saida)
        if self.saida_lidos_jogo > total:
            self.saida_lidos_jogo = 0
        novos = j.saida[max(0, self.saida_lidos_jogo - j.saida_base):]
        self.saida_lidos_jogo = total
        for tipo, texto_, dono, linha in novos:
            self.registrar(tipo, texto_, dono, linha)

    def rect_saida(self):
        return pygame.Rect(VIEW.x, VIEW.bottom - 190, VIEW.w, 190)

    def desenhar_saida(self, t, mouse):
        caixa = self.rect_saida()
        fundo = pygame.Surface((caixa.w, caixa.h), pygame.SRCALPHA)
        fundo.fill((16, 17, 22, 245))
        t.blit(fundo, caixa.topleft)
        pygame.draw.line(t, C_DESTAQUE, caixa.topleft, caixa.topright, 2)
        self.hits_saida = []
        t.blit(self.fb.render("SAÍDA", True, C_TEXTO), (caixa.x + 10, caixa.y + 8))
        x = caixa.x + 70
        contagem = {k: sum(1 for m in self.saida if m["tipo"] == v) for k, v in
                    (("Erros", "erro"), ("Avisos", "aviso"), ("Mensagens", "msg"))}
        for nome in ("Tudo", "Erros", "Avisos", "Mensagens"):
            rot = nome + (f" {contagem[nome]}" if nome in contagem else "")
            img = self.fpp.render(rot, True, C_TEXTO)
            r = pygame.Rect(x, caixa.y + 6, img.get_width() + 16, 20)
            ativo = self.saida_filtro == nome
            pygame.draw.rect(t, C_DESTAQUE if ativo else (48, 52, 64), r, border_radius=10)
            t.blit(img, (r.x + 8, r.y + 3))
            self.hits_saida.append((r, ("filtro", nome)))
            x = r.right + 6
        for rot, acao, dx in (("Limpar", "limpar", 120), ("x", "fechar", 30)):
            r = pygame.Rect(caixa.right - dx - (0 if acao == "fechar" else 36), caixa.y + 6, dx - 6, 20)
            pygame.draw.rect(t, (60, 44, 48) if acao == "fechar" else (48, 52, 64), r, border_radius=6)
            img = self.fpp.render(rot, True, C_TEXTO)
            t.blit(img, (r.centerx - img.get_width() // 2, r.y + 3))
            self.hits_saida.append((r, (acao,)))
        tipo_de = {"Erros": "erro", "Avisos": "aviso", "Mensagens": "msg"}.get(self.saida_filtro)
        itens = [m for m in self.saida if tipo_de is None or m["tipo"] == tipo_de]
        area = pygame.Rect(caixa.x + 4, caixa.y + 32, caixa.w - 8, caixa.h - 36)
        linhas = area.h // 19
        self.saida_scroll = max(0, min(self.saida_scroll, max(0, len(itens) - linhas)))
        fim = len(itens) - self.saida_scroll
        visiveis = itens[max(0, fim - linhas):fim]
        cores = {"erro": (255, 110, 110), "aviso": (240, 200, 90), "msg": (200, 230, 200), "info": (160, 190, 255)}
        t.set_clip(area)
        if not itens:
            t.blit(self.fp.render("Nada por aqui ainda. Erros dos scripts e o escrever() aparecem aqui.", True,
                                  C_TEXTO2), (area.x + 8, area.y + 6))
        for i, m in enumerate(visiveis):
            y = area.y + i * 19
            r = pygame.Rect(area.x, y, area.w, 18)
            clicavel = m["dono"] is not None
            if clicavel and r.collidepoint(mouse):
                pygame.draw.rect(t, (34, 38, 50), r)
            pygame.draw.circle(t, cores.get(m["tipo"], C_TEXTO), (r.x + 8, r.centery), 4)
            t.blit(self.fpp.render(m["hora"], True, C_TEXTO2), (r.x + 18, r.y + 3))
            onde = ""
            if m["dono"]:
                onde = f"   — {m['dono']}" + (f", linha {m['linha']}" if m["linha"] else "")
            t.blit(self.fp.render(m["texto"] + onde, True, cores.get(m["tipo"], C_TEXTO)), (r.x + 76, r.y + 1))
            if clicavel:
                self.hits_saida.append((r, ("ir", m)))
        t.set_clip(None)

    def clique_saida(self, pos):
        for r, a in reversed(self.hits_saida):
            if not r.collidepoint(pos):
                continue
            if a[0] == "filtro":
                self.saida_filtro = a[1]
            elif a[0] == "limpar":
                self.saida.clear()
                self.saida_erros_novos = 0
            elif a[0] == "fechar":
                self.saida_aberta = False
            elif a[0] == "ir":
                self.ir_para_erro(a[1])
            return True
        return True

    def ir_para_erro(self, m):
        """Clicou num erro: seleciona o objeto e abre o script na linha."""
        if self.jogo:
            self.parar()
        if m.get("fase") in self.projeto["fases"] and m["fase"] != self.projeto["fase_atual"]:
            self.trocar_fase(m["fase"])
        if m["dono"] == "Cena":
            self.selecionar(None)
        else:
            alvo = next((d for d in self.objetos if d["nome"] == m["dono"]), None)
            if alvo is None:
                self.avisar(f"Não achei o objeto '{m['dono']}' nesta fase.")
                return
            self.selecionar(alvo)
        script = (self.alvo_logica().get("script") or "").strip()
        if m["linha"] and script:
            self.aba = "script"
            self.cod_alvo = None
            self.carregar_codigo()
            self.cur = [max(0, min(m["linha"] - 1, len(self.cod) - 1)), 0]
            self.ancora = None
            self.cod_erro_linha = m["linha"]
            self.cod_msg = "ERRO  " + m["texto"]
            self.mostrar_cursor()
        else:
            self.aba = "eventos" if self.alvo_logica().get("eventos") else "cena"
            self.focar()

    def ajustar(self, v):
        return int(round(v / self.grade) * self.grade) if self.snap else int(round(v))

    def para_mundo(self, pos):
        return (pos[0] - VIEW.x) / self.zoom + self.cam[0], (pos[1] - VIEW.y) / self.zoom + self.cam[1]

    def coord_de(self, na_tela, pos):
        """Converte o mouse para as coordenadas do objeto (mundo ou tela/UI)."""
        if na_tela:
            return pos[0] - VIEW.x, pos[1] - VIEW.y
        return self.para_mundo(pos)

    def rect_tela(self, d):
        w = num_seguro(d.get("w", 40), 40)
        h = num_seguro(d.get("h", 40), 40)
        if d.get("na_tela"):
            return pygame.Rect(VIEW.x + round(num_seguro(d["x"])), VIEW.y + round(num_seguro(d["y"])),
                               max(1, round(w)), max(1, round(h)))
        z = self.zoom
        return pygame.Rect(round((num_seguro(d["x"]) - self.cam[0]) * z + VIEW.x),
                           round((num_seguro(d["y"]) - self.cam[1]) * z + VIEW.y),
                           max(1, round(w * z)), max(1, round(h * z)))

    def mudar_zoom(self, fator, centro=None):
        centro = centro or VIEW.center
        wx, wy = self.para_mundo(centro)
        self.zoom = max(0.2, min(4.0, self.zoom * fator))
        if abs(self.zoom - 1.0) < 0.04:
            self.zoom = 1.0
        self.cam[0] = wx - (centro[0] - VIEW.x) / self.zoom
        self.cam[1] = wy - (centro[1] - VIEW.y) / self.zoom

    def zoom_100(self):
        self.mudar_zoom(1.0 / self.zoom)

    def alca(self):
        r = self.rect_tela(self.sel)
        return pygame.Rect(r.right - 5, r.bottom - 5, 10, 10)

    def alvo_logica(self):
        return self.sel if self.sel else self.cena

    def nome_alvo(self):
        return self.sel["nome"] if self.sel else "Cena (global)"

    def ordem_desenho(self):
        camada = lambda d: num_seguro(d.get("camada", 0))
        objs = [d for d in self.objetos if not d.get("oculto_editor")]
        if self.cena.get("visao_de_cima") and self.cena.get("ordenar_por_y", True):
            mundo = sorted((d for d in objs if not d.get("na_tela")),
                           key=lambda d: (camada(d), num_seguro(d.get("y", 0)) + num_seguro(d.get("h", 0))))
        else:
            mundo = sorted((d for d in objs if not d.get("na_tela")), key=camada)
        ui = sorted((d for d in objs if d.get("na_tela")), key=camada)
        return mundo + ui

    def trocar_modo(self):
        """Botao Modo: plataforma (com gravidade) <-> top-down (visao de cima), na fase atual."""
        self.guardar()
        td = not self.cena.get("visao_de_cima")
        self.cena["visao_de_cima"] = td
        self.cena["olhar_a_frente"] = 0 if td else 60
        if td:
            for d in self.objetos:
                if d.get("tipo") == "Player" and not d.get("espada") and not d.get("tiro"):
                    d["espada"] = True
            self.avisar("Modo TOP-DOWN: setas/WASD andam nas 8 direções, Espaço ou J dá golpe de espada, "
                        "sem gravidade. Quem está mais embaixo aparece na frente. Ctrl+Z desfaz.")
        else:
            self.avisar("Modo PLATAFORMA: gravidade e pulo de volta. Ctrl+Z desfaz.")

    def nome_unico(self, base, existentes=None):
        nomes = existentes if existentes is not None else {d["nome"] for d in self.objetos}
        if base not in nomes:
            return base
        base_sem_num = base.rstrip("0123456789") or base
        i = 2
        while f"{base_sem_num}{i}" in nomes:
            i += 1
        return f"{base_sem_num}{i}"

    def alternar_tela(self):
        if alternar_tela_cheia():
            self.tela_cheia = not self.tela_cheia

    # ----------------- selecao -----------------
    def esta_selecionado(self, d):
        return any(x is d for x in self.selecao)

    def selecionar(self, d, somar=False):
        if d is None:
            if not somar:
                self.selecao = []
                self.sel = None
            return
        if somar:
            if self.esta_selecionado(d):
                self.selecao = [x for x in self.selecao if x is not d]
                self.sel = self.selecao[-1] if self.selecao else None
                return
            self.selecao.append(d)
        else:
            self.selecao = [d]
        self.sel = d
        self.insp_scroll = 0 if not somar else self.insp_scroll

    def selecionar_varios(self, lista, somar=False):
        if not somar:
            self.selecao = []
        for d in lista:
            if not self.esta_selecionado(d):
                self.selecao.append(d)
        self.sel = self.selecao[-1] if self.selecao else None

    def selecionar_tudo(self):
        self.selecionar_varios([d for d in self.objetos if not d.get("travado") and not d.get("oculto_editor")])
        self.avisar(f"{len(self.selecao)} objeto(s) selecionado(s).")

    def selecionar_tipo(self):
        if not self.sel:
            return
        tipo, modelo = self.sel["tipo"], self.sel.get("modelo")
        self.selecionar_varios([d for d in self.objetos if d["tipo"] == tipo and d.get("modelo") == modelo
                                and not d.get("oculto_editor")])
        self.avisar(f"{len(self.selecao)} objeto(s) do tipo {tipo} selecionado(s).")

    def validar_selecao(self):
        vivos = self.objetos
        self.selecao = [d for d in self.selecao if any(d is x for x in vivos)]
        if self.sel is not None and not any(self.sel is x for x in vivos):
            self.sel = self.selecao[-1] if self.selecao else None

    # ----------------- desfazer / refazer -----------------
    def guardar(self, estado=None):
        s = estado if estado is not None else json.dumps(self.projeto)
        if not self.historico or self.historico[-1] != s:
            self.historico.append(s)
            if len(self.historico) > 150:
                self.historico.pop(0)
        self.refazer_pilha.clear()
        self.sujo = True

    def restaurar(self, estado):
        nomes = [d["nome"] for d in self.selecao]
        fase = self.projeto.get("fase_atual")
        self.projeto = completar_projeto(json.loads(estado))
        if fase in self.projeto["fases"]:
            self.projeto["fase_atual"] = fase
        self.selecionar_varios([d for d in self.objetos if d["nome"] in nomes])
        self.editando = None
        self.cod_alvo = None
        self.sujo = True

    def desfazer(self):
        if not self.historico:
            self.avisar("Nada para desfazer.")
            return
        self.refazer_pilha.append(json.dumps(self.projeto))
        self.restaurar(self.historico.pop())
        self.avisar("Desfeito. (Ctrl+Y refaz)")

    def refazer(self):
        if not self.refazer_pilha:
            self.avisar("Nada para refazer.")
            return
        self.historico.append(json.dumps(self.projeto))
        self.restaurar(self.refazer_pilha.pop())
        self.avisar("Refeito.")

    # ----------------- arquivos -----------------
    def salvar(self):
        try:
            if os.path.exists(ARQUIVO):
                shutil.copyfile(ARQUIVO, os.path.join(os.path.dirname(ARQUIVO), "projeto.bak.json"))
            with open(ARQUIVO, "w", encoding="utf-8") as f:
                json.dump(self.projeto, f, indent=2, ensure_ascii=False)
            self.sujo = False
            try:
                gerar_miniatura(self.projeto, os.path.join(os.path.dirname(ARQUIVO), "miniatura.png"))
            except (pygame.error, OSError, ValueError):
                pass
            self.avisar(f"Salvo em {ARQUIVO}")
        except OSError as erro:
            self.avisar(f"Erro ao salvar: {erro}")

    def autosave(self):
        try:
            with open(ARQUIVO_AUTOSAVE, "w", encoding="utf-8") as f:
                json.dump(self.projeto, f, ensure_ascii=False)
        except OSError:
            pass

    def checar_autosave(self):
        try:
            if not os.path.exists(ARQUIVO_AUTOSAVE):
                return
            if os.path.exists(ARQUIVO) and os.path.getmtime(ARQUIVO_AUTOSAVE) <= os.path.getmtime(ARQUIVO):
                return
        except OSError:
            return

        def escolher(item):
            if item.startswith("Recuperar"):
                try:
                    with open(ARQUIVO_AUTOSAVE, encoding="utf-8") as f:
                        self.projeto = completar_projeto(json.load(f))
                    self.selecionar(None)
                    self.sujo = True
                    self.avisar("Autosave recuperado! Lembre de salvar (Ctrl+S).")
                except (OSError, ValueError) as ex:
                    self.avisar(f"Não consegui abrir o autosave: {ex}")
        self.abrir_menu((LARGURA // 2 - 110, ALTURA // 2 - 40),
                        ["Recuperar trabalho não salvo (autosave)", "Ignorar"], escolher)

    def abrir(self, silencioso=False):
        if not os.path.exists(ARQUIVO):
            self.avisar("Ainda não tem projeto.json salvo.")
            return
        try:
            with open(ARQUIVO, encoding="utf-8") as f:
                dados = completar_projeto(json.load(f))
            if not silencioso:
                self.guardar()
            self.projeto = dados
            if hasattr(self, "selecao"):
                self.selecionar(None)
            self.sujo = False
            if not silencioso:
                self.avisar("Projeto aberto.")
        except (OSError, ValueError, AttributeError, TypeError) as erro:
            self.avisar(f"Erro ao abrir: {erro}")

    def novo(self):
        def escolher(item):
            if item == "Cancelar":
                return
            self.guardar()
            if item in EXEMPLOS:
                self.projeto = completar_projeto(EXEMPLOS[item]())
                for arte in self.projeto.pop("_artes", []):     # pixel arts que o exemplo usa
                    garantir_arte(arte)
                nome_ex = item[9:] if item.startswith("Exemplo: ") else item
                self.avisar(f"{nome_ex} pronto! Aperte F5 para jogar e mexa no que quiser. (Ctrl+Z volta)")
            else:
                modelos = self.projeto.get("modelos", {})
                self.projeto = {"fases": {"Fase 1": fase_padrao()}, "fase_atual": "Fase 1",
                                "fase_inicial": "Fase 1", "modelos": modelos}
                self.avisar("Projeto novo (os modelos foram mantidos). Ctrl+Z volta.")
            self.selecionar(None)
            self.cod_alvo = None
            self.cam = [-40.0, -100.0]
            self.zoom = 1.0
        self.abrir_menu(self.botoes["novo"].bottomleft, ["Projeto vazio"] + list(EXEMPLOS) + ["Cancelar"], escolher)

    def publicar_jogo(self):
        self.salvar()
        if online_ativo():
            self.avisar("Enviando o jogo para a internet...", "info")
            em_segundo_plano(publicar_online, lambda msg, erro: (self.avisar(f"Não consegui publicar: {erro}" if erro
                                                                             else msg, "erro" if erro else "ok"),
                                                                 self.mostrar_novidades()), self.pasta_projeto)
            return
        try:
            ja = publicacao_de(self.pasta_projeto)
            m = publicar_projeto(self.pasta_projeto)
        except (OSError, ValueError, KeyError) as ex:
            self.avisar(f"Não consegui publicar: {ex}")
            return
        self.avisar(("Publicação atualizada: " if ja else "Publicado! ") + f"'{m['titulo']}' está em Início > Jogos "
                    f"publicados. Visita +{BRASAS_VISITA}, like +{BRASAS_LIKE} {MOEDA}.", "ok")

    def menu_exportar(self):
        opcoes = {
            ("Publicar para o mundo todo (visitas e likes dão Brasas)" if online_ativo() else
             "Publicar na área de Jogos (ganhe Brasas com visitas e likes)"): self.publicar_jogo,
            "Exportar o jogo (pasta pronta pra jogar)": self.exportar,
            "Atalho da Minha Engine na área de trabalho": self.atalho_engine,
            "Atalho do meu jogo na área de trabalho": self.atalho_jogo,
        }
        self.abrir_menu(self.botoes["exportar"].bottomleft, list(opcoes), lambda it: opcoes[it]())

    def atalho_engine(self):
        try:
            destino = criar_atalho("Minha Engine", os.path.abspath(__file__), PASTA)
            self.avisar(f"Atalho criado na área de trabalho: {os.path.basename(destino)}")
        except (OSError, subprocess.SubprocessError, pygame.error) as ex:
            self.avisar(f"Não consegui criar o atalho: {ex}")

    def atalho_jogo(self):
        pasta = self.exportar()
        if not pasta:
            return
        cena_ini = self.projeto["fases"][self.projeto["fase_inicial"]]["cena"]
        try:
            destino = criar_atalho(str(cena_ini.get("titulo", "Meu Jogo")), os.path.join(pasta, "jogar.py"), pasta)
            self.avisar(f"Jogo exportado e atalho criado na área de trabalho: {os.path.basename(destino)}")
        except (OSError, subprocess.SubprocessError, pygame.error) as ex:
            self.avisar(f"Exportei o jogo, mas não consegui criar o atalho: {ex}")

    def exportar(self):
        self.salvar()
        cena_ini = self.projeto["fases"][self.projeto["fase_inicial"]]["cena"]
        titulo = re.sub(r"[^\w\- ]", "", str(cena_ini.get("titulo", "Meu Jogo"))).strip() or "MeuJogo"
        destino = os.path.join(os.path.dirname(ARQUIVO), "exportado", titulo)
        try:
            os.makedirs(destino, exist_ok=True)
            if "codigo_unico" in globals():          # engine dividida em partes: junta tudo num arquivo
                with open(os.path.join(destino, "motor.py"), "w", encoding="utf-8") as f:
                    f.write(codigo_unico())
            else:
                shutil.copyfile(os.path.abspath(__file__), os.path.join(destino, "motor.py"))
            exportar = dict(self.projeto, controles=CONFIG["controles"])
            with open(os.path.join(destino, "projeto.json"), "w", encoding="utf-8") as f:
                json.dump(exportar, f, indent=2, ensure_ascii=False)
            for pasta in (PASTA_IMAGENS, PASTA_SONS, PASTA_PLUGINS):
                if os.path.isdir(pasta):
                    shutil.copytree(pasta, os.path.join(destino, os.path.basename(pasta)), dirs_exist_ok=True)
            arquivos = {
                "jogar.py": "import os\nimport sys\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n"
                            "import motor  # noqa: E402\n\nmotor.jogar_sozinho(os.path.join(motor.PASTA, "
                            "\"projeto.json\"))\n",
                "JOGAR.bat": "@echo off\ncd /d %~dp0\npython jogar.py\nif errorlevel 1 pause\n",
                "jogar.sh": "#!/bin/sh\ncd \"$(dirname \"$0\")\"\npython3 jogar.py\n",
                "LEIA-ME.txt": (
                    f"{titulo}\n{'=' * len(titulo)}\n\n"
                    "COMO JOGAR\n  Windows: dois cliques em JOGAR.bat\n  Mac/Linux: rode ./jogar.sh\n"
                    "  (precisa de Python e do pygame: pip install pygame)\n\n"
                    "CONTROLES\n  A/D ou setas = andar | Espaço/W = pular | E = falar | P = pausa | "
                    "F11 = tela cheia | ESC = sair\n\n"
                    "VIRAR UM .EXE (para mandar para quem não tem Python)\n"
                    "  1) pip install pyinstaller pygame pillow\n"
                    "  2) Nesta pasta: pyinstaller --onefile --noconsole --icon icone.png jogar.py\n"
                    "     (o --icon coloca o icone da Minha Engine no .exe; troque icone.png se quiser outro)\n"
                    "  3) Pegue o jogar.exe dentro da pasta 'dist' e coloque AQUI, junto com projeto.json,\n"
                    "     e as pastas imagens, sons e plugins. Pode mandar a pasta inteira (zipada).\n"),
            }
            for nome, conteudo in arquivos.items():
                with open(os.path.join(destino, nome), "w", encoding="utf-8") as f:
                    f.write(conteudo)
            try:
                salvar_icone(destino)
            except (pygame.error, OSError):
                pass
            abrir_pasta(destino)
            self.avisar(f"Jogo exportado em {destino}  (veja o LEIA-ME.txt)")
            self.msg_t = 8.0
            if ganhar_conquista("primeira_exportacao"):
                self.mostrar_novidades()
            return destino
        except OSError as ex:
            self.avisar(f"Erro ao exportar: {ex}")
            return None

    # ----------------- fases -----------------
    def trocar_fase(self, nome):
        if nome not in self.projeto["fases"]:
            return
        self.confirmar_edicao()
        self.projeto["fase_atual"] = nome
        self.selecionar(None)
        self.cod_alvo = None
        self.cam = [-40.0, -100.0]
        self.ev_scroll = 0
        self.avisar(f"Editando: {nome}")

    def menu_fases(self, pos):
        fases = self.projeto["fases"]
        atual, inicial = self.projeto["fase_atual"], self.projeto["fase_inicial"]
        rotulos = {}
        for nome in fases:
            rot = ("> " if nome == atual else "   ") + nome + ("  (inicial)" if nome == inicial else "")
            rotulos[rot] = nome
        extras = ["+ Nova fase", "Renomear esta fase", "Duplicar esta fase", "Apagar esta fase",
                  "Começar o jogo nesta fase"]

        def escolher(item):
            if item in rotulos:
                self.trocar_fase(rotulos[item])
            elif item == "+ Nova fase":
                self.pedir_texto("Nome da nova fase", self.nome_fase_livre("Fase"), self.criar_fase)
            elif item == "Renomear esta fase":
                self.pedir_texto("Novo nome da fase", atual, self.renomear_fase)
            elif item == "Duplicar esta fase":
                self.guardar()
                novo = self.nome_fase_livre(atual + " cópia")
                fases[novo] = copy.deepcopy(fases[atual])
                self.trocar_fase(novo)
            elif item == "Apagar esta fase":
                if len(fases) <= 1:
                    self.avisar("O projeto precisa ter pelo menos uma fase.")
                    return
                self.abrir_menu(pos, [f"Sim, apagar '{atual}'", "Cancelar"],
                                lambda it: self.apagar_fase(atual) if it.startswith("Sim") else None)
            elif item == "Começar o jogo nesta fase":
                self.projeto["fase_inicial"] = atual
                self.sujo = True
                self.avisar(f"O jogo exportado começa em '{atual}'.")
        self.abrir_menu(pos, list(rotulos) + extras, escolher)

    def nome_fase_livre(self, base):
        fases = self.projeto["fases"]
        if base not in fases:
            return base
        i = 2
        while f"{base} {i}" in fases:
            i += 1
        return f"{base} {i}"

    def criar_fase(self, nome):
        nome = nome.strip()
        if not nome:
            return
        if nome in self.projeto["fases"]:
            self.avisar("Já existe uma fase com esse nome.")
            return
        self.guardar()
        self.projeto["fases"][nome] = fase_padrao()
        self.trocar_fase(nome)

    def renomear_fase(self, novo):
        novo = novo.strip()
        antigo = self.projeto["fase_atual"]
        if not novo or novo == antigo:
            return
        if novo in self.projeto["fases"]:
            self.avisar("Já existe uma fase com esse nome.")
            return
        self.guardar()
        self.projeto["fases"] = {(novo if k == antigo else k): v for k, v in self.projeto["fases"].items()}
        self.projeto["fase_atual"] = novo
        if self.projeto["fase_inicial"] == antigo:
            self.projeto["fase_inicial"] = novo
        # atualiza quem apontava para o nome antigo
        for fase in self.projeto["fases"].values():
            for d in fase["objetos"]:
                if d.get("ir_para_fase") == antigo:
                    d["ir_para_fase"] = novo
                for ev in d.get("eventos", []):
                    for a in ev.get("acoes", []):
                        if a.get("p", {}).get("fase") == antigo:
                            a["p"]["fase"] = novo
        self.avisar(f"Fase renomeada para '{novo}'.")

    def apagar_fase(self, nome):
        self.guardar()
        self.projeto["fases"].pop(nome, None)
        primeira = next(iter(self.projeto["fases"]))
        if self.projeto["fase_inicial"] == nome:
            self.projeto["fase_inicial"] = primeira
        self.trocar_fase(primeira)

    # ----------------- caixa de texto (prompt) -----------------
    def pedir_texto(self, titulo, inicial, fn):
        self.prompt = {"titulo": titulo, "texto": str(inicial), "fn": fn}

    def confirmar_prompt(self):
        p, self.prompt = self.prompt, None
        if p:
            p["fn"](p["texto"])

    # ----------------- play -----------------
    def play(self, cheio=False):
        if self.jogo:
            self.parar()
            return
        if not any(d["tipo"] == "Player" for d in self.objetos):
            self.avisar("Coloque um Player nesta fase antes de dar Play!")
            return
        self.confirmar_edicao()
        self.arrastando = None
        self.menu = None
        self.play_cheio = cheio
        if cheio and not self.tela_cheia:
            self.alternar_tela()
            self.entrou_cheio = True
        self.jogo = Jogo(self.projeto, TELA_INTEIRA if cheio else VIEW)
        self.saida_lidos_jogo = 0
        self.registrar("info", f"Play iniciado ({self.projeto['fase_atual']})")
        self.passos_feitos.add("play")
        self.puxar_saida_do_jogo()
        if self.jogo.erros:
            self.avisar("Tem erro de script! Veja a janela Saída (F9).")

    def parar(self):
        self.puxar_saida_do_jogo()
        if self.jogo is not None:
            self.registrar("info", "Play parado")
        self.jogo = None
        self.play_cheio = False
        parar_musica()
        if self.entrou_cheio:
            if self.tela_cheia:
                self.alternar_tela()
            self.entrou_cheio = False
        self.avisar("De volta ao editor.")

    def reiniciar_jogo(self):
        self.jogo = Jogo(self.projeto, TELA_INTEIRA if self.play_cheio else VIEW)
