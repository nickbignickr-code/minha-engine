# Minha Engine - editor_tela.py
# desenho da tela do editor (painéis, cena, inspetor, menus) (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class EditorTela:
    # ----------------- desenho geral -----------------
    def desenhar(self):
        t = self.tela
        mouse = pygame.mouse.get_pos()
        if self.jogo and self.play_cheio:
            t.fill((0, 0, 0))
            self.jogo.desenhar(t, self.f, self.fg)
            TOQUE.desenhar_pad(t)
            pygame.display.flip()
            return
        aba_vista = "jogo" if self.jogo else self.aba
        if aba_vista != getattr(self, "aba_desenhada", aba_vista) and animacoes_ligadas():
            try:        # guarda a tela antiga para trocar de aba com um "dissolver"
                self.troca_aba = (t.subsurface(VIEW).copy(), agora_ui())
            except (pygame.error, ValueError, AttributeError):
                self.troca_aba = None
        self.aba_desenhada = aba_vista
        t.fill(C_FUNDO_UI)
        if self.jogo:
            self.jogo.desenhar(t, self.f, self.fg)
        elif self.aba == "eventos":
            self.desenhar_eventos(t, mouse)
        elif self.aba == "script":
            self.desenhar_codigo(t, mouse)
        elif self.aba == "api":
            self.desenhar_api(t, mouse)
        elif self.aba == "desenho":
            self.pixel.desenhar(t, mouse)
        elif self.aba == "loja":
            self.loja.desenhar(t, mouse)
        else:
            self.desenhar_cena(t, mouse)
        troca = getattr(self, "troca_aba", None)
        if troca:
            k = entrada(troca[1], 0.18)
            if k >= 1:
                self.troca_aba = None
            else:
                try:
                    troca[0].set_alpha(int(255 * (1 - k)))
                    t.blit(troca[0], VIEW.topleft)
                except (pygame.error, AttributeError):
                    self.troca_aba = None
        if self.jogo and agora_ui() - getattr(self, "play_t0", 0) < 0.35:
            sombra = pygame.Surface(VIEW.size, pygame.SRCALPHA)
            sombra.fill((0, 0, 0, int(255 * (1 - entrada(self.play_t0, 0.35)))))
            t.blit(sombra, VIEW.topleft)
        pygame.draw.rect(t, C_DESTAQUE if self.jogo else C_BORDA, VIEW, 2 if self.jogo else 1)
        self.desenhar_abas(t, mouse)
        self.desenhar_topo(t, mouse)
        self.desenhar_esquerda(t, mouse)
        self.desenhar_direita(t, mouse)
        self.desenhar_rodape(t, mouse)
        if self.saida_aberta:
            self.saida_erros_novos = 0
            self.desenhar_saida(t, mouse)
        if self.aba == "cena" and not self.jogo:
            self.desenhar_vazio_cena(t, mouse)
            self.desenhar_passos(t, mouse)
        self.desenhar_toasts(t, mouse)
        self.desenhar_menu(t, mouse)
        if self.jogo:
            TOQUE.desenhar_pad(t)
        self.desenhar_barra_toque(t, mouse)
        self.desenhar_seletor(t, mouse)
        self.desenhar_dica(t, mouse)
        if self.mostrar_ajuda:
            self.desenhar_ajuda(t)
        if self.prompt:
            self.desenhar_prompt(t, mouse)
        self.desenhar_tour(t, mouse)
        pygame.display.flip()

    def desenhar_dica(self, t, mouse):
        if self.prompt or self.arrastando or not CONFIG["geral"].get("dicas", True) or modo_toque():
            return
        alvo, txt = None, None
        if self.menu:
            for item, r in zip(self.menu["itens"], self.rects_menu_de(self.menu)):
                if r.collidepoint(mouse) and item in DESC_COMPORTAMENTOS:
                    alvo, txt = ("m", item), DESC_COMPORTAMENTOS[item]
            if alvo is None:
                self.hover = (None, self.tempo)
                return
        for nome, r in self.botoes.items():
            if r.collidepoint(mouse):
                alvo, txt = ("b", nome), DICAS_BOTOES.get(nome)
        if alvo is None and mouse[0] < PAINEL_ESQ:
            for r, a in self.hits_esq:
                if r.collidepoint(mouse) and a[0] == "ferr":
                    nome = a[1]
                    if nome.startswith("modelo:"):
                        txt = "Variante: clique e depois clique na cena para colocar uma cópia."
                    elif nome == "Borracha":
                        txt = "Apaga o que você clicar ou arrastar por cima (E). Ctrl+Z desfaz."
                    elif nome.startswith("preset:"):
                        txt = DESC_PRESETS.get(nome[7:], "")
                    else:
                        txt = DESC_TIPOS.get(nome, "Seleciona, move e redimensiona objetos.")
                    alvo = ("f", nome)
        if alvo is None and mouse[0] >= LARGURA - PAINEL_DIR:
            for r, chave, idx in self.hits_insp:
                if chave in ("#cativo", "#cdel") and r.collidepoint(mouse):
                    nome_c = idx.get("t", "")
                    alvo, txt = ("c", nome_c), DESC_COMPORTAMENTOS.get(nome_c)
        if alvo is None and mouse[0] >= LARGURA - PAINEL_DIR and not self.editando:
            for r, chave, idx in self.hits_insp:
                if isinstance(chave, str) and not chave.startswith("#") and chave in DESC_PROPS \
                        and r.collidepoint(mouse):
                    alvo, txt = ("p", chave), f"{ROTULOS.get(chave, chave)}: {DESC_PROPS[chave]}"
                    break
        if alvo is None and self.botao_fase.collidepoint(mouse):
            alvo, txt = ("fase",), "Trocar de fase, criar, renomear, duplicar ou apagar fases"
        if alvo != self.hover[0]:
            self.hover = (alvo, self.tempo)
            return
        if not txt or self.tempo - self.hover[1] < 0.5:
            return
        linhas = quebrar_texto(txt, self.fp, 300)
        w = max(self.fp.size(linha)[0] for linha in linhas) + 16
        h = len(linhas) * 17 + 10
        x = min(mouse[0] + 14, LARGURA - w - 4)
        y = min(mouse[1] + 18, ALTURA - h - 4)
        caixa = pygame.Rect(x, y, w, h)
        pygame.draw.rect(t, (20, 21, 26), caixa, border_radius=5)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 1, border_radius=5)
        for i, linha in enumerate(linhas):
            t.blit(self.fp.render(linha, True, C_TEXTO), (x + 8, y + 5 + i * 17))

    def desenhar_ajuda(self, t):
        caixa = pygame.Rect(LARGURA // 2 - 420, 60, 840, ALTURA - 120)
        sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        t.blit(sombra, (0, 0))
        pygame.draw.rect(t, C_PAINEL, caixa, border_radius=10)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 2, border_radius=10)
        t.blit(self.fg.render("Atalhos", True, C_TEXTO), (caixa.x + 20, caixa.y + 10))
        t.blit(self.fp.render(f"Clique em qualquer lugar ou aperte {atalho_de('ajuda')} para fechar.  "
                              "Mude os atalhos em Início > Configurações.", True, C_TEXTO2), (caixa.x + 190, caixa.y + 30))
        lista = lista_atalhos()
        metade = (len(lista) + 1) // 2
        for col, grupo in enumerate((lista[:metade], lista[metade:])):
            y = caixa.y + 70
            x = caixa.x + 24 + col * 410
            for tecla_, desc in grupo:
                if not desc:
                    t.blit(self.fb.render(tecla_, True, C_DESTAQUE), (x, y + 4))
                    y += 24
                    continue
                t.blit(self.fb.render(tecla_, True, C_TEXTO), (x, y))
                t.blit(self.fp.render(desc, True, C_TEXTO2), (x + 175, y + 1))
                y += 19

    def desenhar_prompt(self, t, mouse):
        p = self.prompt
        sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 120))
        t.blit(sombra, (0, 0))
        caixa = pygame.Rect(LARGURA // 2 - 220, ALTURA // 2 - 70, 440, 140)
        pygame.draw.rect(t, C_PAINEL, caixa, border_radius=10)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 2, border_radius=10)
        t.blit(self.f.render(p["titulo"], True, C_TEXTO), (caixa.x + 18, caixa.y + 14))
        campo = pygame.Rect(caixa.x + 18, caixa.y + 44, caixa.w - 36, 30)
        pygame.draw.rect(t, C_CAMPO, campo, border_radius=5)
        pygame.draw.rect(t, C_DESTAQUE, campo, 1, border_radius=5)
        piscar = "|" if int(self.tempo * 2) % 2 == 0 else ""
        t.blit(self.f.render(p["texto"] + piscar, True, C_TEXTO), (campo.x + 8, campo.y + 6))
        self.hits_prompt = []
        for i, (rot, acao, cor) in enumerate([("OK (Enter)", "ok", C_VERDE), ("Cancelar (Esc)", "cancelar", None)]):
            r = pygame.Rect(caixa.right - 250 + i * 122, caixa.bottom - 44, 114, 30)
            desenhar_botao(t, self.fp, r, rot, mouse, cor=cor)
            self.hits_prompt.append((r, acao))

    def desenhar_abas(self, t, mouse):
        pygame.draw.rect(t, C_FUNDO_UI, (PAINEL_ESQ, TOPO, VIEW.w, ABAS_H))
        alvo = self.alvo_logica()
        contagem = {"eventos": len(alvo.get("eventos", [])),
                    "script": sum(1 for linha in (alvo.get("script", "") or "").split("\n") if linha.strip())}
        nomes = {"cena": "Cena", "eventos": "Eventos", "script": "Script", "api": "API", "desenho": "Desenho",
                 "loja": "Loja"}
        for nome, r in self.abas.items():
            ativo = (nome == self.aba) and not self.jogo
            cor = C_PAINEL if ativo else (C_BOTAO if r.collidepoint(mouse) else (38, 40, 47))
            pygame.draw.rect(t, cor, r, border_top_left_radius=6, border_top_right_radius=6)
            if ativo:
                xi = suave(("aba_ind", "x"), r.x + 4, 20)
                wi = suave(("aba_ind", "w"), r.w - 8, 20)
                pygame.draw.rect(t, C_DESTAQUE, (xi, r.y, wi, 3), border_radius=2)
            rot = nomes[nome]
            if contagem.get(nome):
                rot += f" ({contagem[nome]})"
            img = self.fp.render(rot, True, C_TEXTO if ativo else C_TEXTO2)
            t.blit(img, (r.centerx - img.get_width() // 2, r.y + 6))
        r = self.botao_fase
        pygame.draw.rect(t, C_BOTAO if not r.collidepoint(mouse) else clarear(C_BOTAO, 20), r, border_radius=6)
        nome_fase = self.projeto["fase_atual"]
        img = self.fp.render(f"Fase: {nome_fase}  ▾", True, C_TEXTO)
        t.blit(img, (r.x + 8, r.y + 6))
        largura_chip = texto_cache(fmt_brasas(carteira()["saldo"]), 12, C_TEXTO, True).get_width() + 40
        self.rect_saldo = desenhar_saldo(t, VIEW.right - largura_chip - 6, TOPO + 3, 12, mouse)
        dica = self.fpp.render(f"Programando: {self.nome_alvo()}", True, C_TEXTO2)
        if self.rect_saldo.x - dica.get_width() - 10 > r.right + 8:
            t.blit(dica, (self.rect_saldo.x - dica.get_width() - 10, TOPO + 10))

    def desenhar_cena(self, t, mouse):
        cena = self.cena
        fundo = cena.get("fundo", [25, 28, 45])
        pygame.draw.rect(t, cor_ok(fundo), VIEW)
        t.set_clip(VIEW)
        z = self.zoom
        passo = self.grade * z
        if self.mostrar_grade and passo >= 5:
            linha = clarear(fundo, 12)
            forte = clarear(fundo, 24)
            i0 = math.floor(self.cam[0] / self.grade)
            x = VIEW.x + (i0 * self.grade - self.cam[0]) * z
            i = i0
            while x < VIEW.right:
                pygame.draw.line(t, forte if i % 5 == 0 else linha, (round(x), VIEW.y), (round(x), VIEW.bottom))
                x += passo
                i += 1
            j0 = math.floor(self.cam[1] / self.grade)
            y = VIEW.y + (j0 * self.grade - self.cam[1]) * z
            j = j0
            while y < VIEW.bottom:
                pygame.draw.line(t, forte if j % 5 == 0 else linha, (VIEW.x, round(y)), (VIEW.right, round(y)))
                y += passo
                j += 1
            ox = VIEW.x - self.cam[0] * z
            oy = VIEW.y - self.cam[1] * z
            pygame.draw.line(t, clarear(fundo, 50), (ox, VIEW.y), (ox, VIEW.bottom))
            pygame.draw.line(t, clarear(fundo, 50), (VIEW.x, oy), (VIEW.right, oy))

        ui_existe = False
        for d in self.ordem_desenho():
            r = self.rect_tela(d)
            if d.get("na_tela"):
                ui_existe = True
            elif r.right < VIEW.x or r.x > VIEW.right or r.bottom < VIEW.y or r.y > VIEW.bottom:
                continue
            if not d.get("visivel", True):
                pygame.draw.rect(t, (150, 150, 160), r, 1)
            desenhar_obj(t, d, r, editor=True)
            if d.get("eventos") or (d.get("script") or "").strip():
                pygame.draw.circle(t, (255, 200, 60), (r.right - 3, r.y + 3), 4)
            if d.get("modelo"):
                pygame.draw.circle(t, C_MODELO, (r.x + 3, r.y + 3), 4)
            if d.get("travado"):
                pygame.draw.rect(t, (200, 200, 210), (r.x + 2, r.bottom - 9, 7, 6))
                pygame.draw.rect(t, (200, 200, 210), (r.x + 3, r.bottom - 13, 5, 5), 1)

        if ui_existe or (self.sel and self.sel.get("na_tela")):
            tela_jogo = pygame.Rect(VIEW.x, VIEW.y, num_seguro(cena.get("largura_tela", 960), 960),
                                    num_seguro(cena.get("altura_tela", 540), 540))
            pygame.draw.rect(t, (120, 120, 160), tela_jogo, 1)
            t.blit(self.fpp.render("área da UI (tela do jogo)", True, (140, 140, 180)),
                   (VIEW.x + 4, tela_jogo.bottom - 14))

        for d in self.selecao:
            r = self.rect_tela(d)
            principal = d is self.sel
            pygame.draw.rect(t, C_DESTAQUE if principal else (130, 180, 255), r.inflate(6, 6), 2)
            if principal:
                t.blit(self.fp.render(d["nome"], True, (255, 255, 255)), (r.x, r.y - 20))
        if self.sel and len(self.selecao) == 1:
            pygame.draw.rect(t, (255, 255, 255), self.alca())
            pygame.draw.rect(t, C_DESTAQUE, self.alca(), 1)
            r = self.rect_tela(self.sel)
            info = f"{fmt(self.sel['x'])}, {fmt(self.sel['y'])}  ·  {fmt(self.sel['w'])}x{fmt(self.sel['h'])}"
            t.blit(self.fpp.render(info, True, (200, 200, 220)), (r.x, r.bottom + 6))

        if self.arrastando and self.arrastando[0] == "caixa":
            _, ini, fim, _ = self.arrastando
            caixa = pygame.Rect(min(ini[0], fim[0]), min(ini[1], fim[1]), abs(fim[0] - ini[0]), abs(fim[1] - ini[1]))
            if caixa.w > 1 and caixa.h > 1:
                s = pygame.Surface((caixa.w, caixa.h), pygame.SRCALPHA)
                s.fill((70, 140, 255, 45))
                t.blit(s, caixa.topleft)
            pygame.draw.rect(t, C_DESTAQUE, caixa, 1)

        if self.ferramenta == "Borracha" and VIEW.collidepoint(mouse):
            embaixo = self.objeto_em(mouse)
            if embaixo is not None:
                pygame.draw.rect(t, C_VERMELHO, self.rect_tela(embaixo).inflate(4, 4), 2)
            pygame.draw.circle(t, C_VERMELHO, mouse, 9, 2)
        gab = self.gabarito_ferramenta()
        if gab is not None and VIEW.collidepoint(mouse) and not self.menu:
            wx, wy = self.coord_de(gab.get("na_tela"), mouse)
            gab["x"] = self.ajustar(wx - num_seguro(gab["w"], 40) / 2)
            gab["y"] = self.ajustar(wy - num_seguro(gab["h"], 40) / 2)
            r = self.rect_tela(gab)
            desenhar_obj(t, dict(gab, opacidade=110), r, editor=True)
            pygame.draw.rect(t, (255, 255, 255), r, 1)
        if self.minimapa:
            self.desenhar_minimapa(t)
        nome_fase = self.fpp.render(f"{self.projeto['fase_atual']}  ·  zoom {round(self.zoom * 100)}%",
                                    True, (170, 170, 190))
        t.blit(nome_fase, (VIEW.right - nome_fase.get_width() - 8, VIEW.bottom - 16))
        t.set_clip(None)

    def desenhar_minimapa(self, t):
        mundo = [d for d in self.objetos if not d.get("na_tela") and not d.get("oculto_editor")]
        self.minimapa_rect = None
        if len(mundo) < 2:
            return
        x0 = min(num_seguro(d["x"]) for d in mundo)
        y0 = min(num_seguro(d["y"]) for d in mundo)
        x1 = max(num_seguro(d["x"]) + num_seguro(d["w"], 40) for d in mundo)
        y1 = max(num_seguro(d["y"]) + num_seguro(d["h"], 40) for d in mundo)
        larg, alt = max(1.0, x1 - x0), max(1.0, y1 - y0)
        k = min(200 / larg, 110 / alt)
        caixa = pygame.Rect(VIEW.x + 10, VIEW.bottom - int(alt * k) - 34, int(larg * k) + 12, int(alt * k) + 12)
        fundo = pygame.Surface((caixa.w, caixa.h), pygame.SRCALPHA)
        fundo.fill((10, 12, 18, 190))
        t.blit(fundo, caixa.topleft)
        pygame.draw.rect(t, C_BORDA, caixa, 1)
        ox, oy = caixa.x + 6, caixa.y + 6
        for d in mundo:
            r = pygame.Rect(ox + int((num_seguro(d["x"]) - x0) * k), oy + int((num_seguro(d["y"]) - y0) * k),
                            max(2, int(num_seguro(d["w"], 40) * k)), max(2, int(num_seguro(d["h"], 40) * k)))
            cor = (255, 255, 255) if d["tipo"] == "Player" else cor_ok(d.get("cor"))
            pygame.draw.rect(t, cor, r)
        vis = pygame.Rect(ox + int((self.cam[0] - x0) * k), oy + int((self.cam[1] - y0) * k),
                          max(2, int(VIEW.w / self.zoom * k)), max(2, int(VIEW.h / self.zoom * k)))
        pygame.draw.rect(t, (255, 220, 80), vis.clip(caixa), 1)
        t.blit(self.fpp.render("mini-mapa (M)", True, (150, 150, 170)), (caixa.x + 4, caixa.y - 14))
        self.minimapa_rect = caixa
        self.minimapa_conv = (ox, oy, x0, y0, k)

    def desenhar_topo(self, t, mouse):
        pygame.draw.rect(t, C_PAINEL, (0, 0, LARGURA, TOPO))
        pygame.draw.line(t, C_BORDA, (0, TOPO - 1), (LARGURA, TOPO - 1))
        textos = {
            "inicio": "Início",
            "play": "Parar" if self.jogo else "Play",
            "playcheio": "Play cheio", "novo": "Novo",
            "salvar": "Salvar" + (" *" if self.sujo else ""),
            "abrir": "Abrir", "desfazer": "", "refazer": "", "ajuda": "", "buscar": "Buscar",
            "grade": "", "snap": "",
            "mover": f"Mover: {self.grade} ▾", "girar": f"Girar: {round(self.passo_giro) or 1}° ▾",
            "saida": "Saída" + (f" ({self.saida_erros_novos})" if getattr(self, "saida_erros_novos", 0) else ""),
            "telacheia": "Sair tela cheia" if self.tela_cheia else f"Tela cheia ({atalho_de('tela_cheia')})",
            "exportar": "Exportar",
            "modo": "Top-down" if self.cena.get("visao_de_cima") else "Plataforma",
        }
        icones = {"inicio": "inicio", "play": "parar" if self.jogo else "play", "playcheio": "playcheio",
                  "novo": "novo", "salvar": "salvar", "desfazer": "desfazer", "refazer": "refazer",
                  "grade": "grade", "snap": "snap", "buscar": "buscar", "modo": "modo", "saida": "saida",
                  "exportar": "exportar", "ajuda": "ajuda"}
        # barra de cima com um degradê leve
        for i in range(TOPO):
            pygame.draw.line(t, clarear(C_PAINEL, int(10 * (1 - i / TOPO))), (0, i), (LARGURA, i))
        pygame.draw.line(t, C_BORDA, (0, TOPO - 1), (LARGURA, TOPO - 1))
        for nome, r in self.botoes.items():
            cor = None
            if nome == "play":
                cor = C_VERMELHO if self.jogo else C_VERDE
            elif nome == "playcheio":
                cor = (40, 130, 80)
            elif nome == "exportar":
                cor = C_MODELO
            elif nome == "inicio":
                cor = (60, 66, 90)
            elif nome == "saida":
                cor = C_VERMELHO if getattr(self, "saida_erros_novos", 0) else ((70, 90, 140) if self.saida_aberta
                                                                                  else None)
            elif nome == "salvar" and self.sujo:
                cor = (70, 90, 140)
            elif nome == "modo":
                cor = (150, 95, 40) if self.cena.get("visao_de_cima") else (60, 110, 160)
            elif nome == "ajuda":
                cor = clarear(C_DESTAQUE, -40)
            ativo = (nome == "grade" and self.mostrar_grade) or (nome == "snap" and self.snap)
            fonte_ = self.fpp if nome in ("playcheio", "telacheia") else self.fp
            desenhar_botao(t, fonte_, r, textos.get(nome, nome), mouse, ativo=ativo, cor=cor, icone=icones.get(nome))
        livre = LARGURA - 15 - (max(r.right for r in self.botoes.values()) + 12)
        nome_p = self.nome_projeto[:22]
        while nome_p and self.fb.size(nome_p)[0] > livre:
            nome_p = nome_p[:-1]
        if nome_p:
            titulo = self.fb.render(nome_p, True, C_DESTAQUE)
            t.blit(titulo, (LARGURA - titulo.get_width() - 15, 15))

    def desenhar_imagens_esq(self, t, mouse, area):
        y = area.y
        t.blit(self.fb.render("IMAGENS DO PROJETO", True, C_TEXTO2), (10, y))
        y += 20
        for i, (rot, acao, cor) in enumerate((("Importar", ("img_importar",), (70, 90, 140)),
                                              ("Desenhar", ("img_desenhar",), (130, 80, 170)),
                                              ("Atualizar", ("img_recarregar",), None))):
            r = pygame.Rect(8 + i * 62, y, 58, 24)
            desenhar_botao(t, self.fpp, r, rot, mouse, cor=cor)
            self.hits_esq.append((r, acao))
        y += 30
        imagens = listar_imagens()
        if not imagens:
            for linha in quebrar_texto("Nenhuma imagem ainda. 'Importar' abre a pasta: coloque PNG/JPG lá e clique "
                                       "em 'Atualizar'. Ou crie uma no 'Desenhar', ou pegue pixel arts prontas na "
                                       "aba Loja (categoria Imagens).", self.fp, PAINEL_ESQ - 20):
                t.blit(self.fp.render(linha, True, C_TEXTO2), (10, y))
                y += 17
            return
        lado, col = 58, 3
        linhas_vis = max(1, (area.bottom - y - 70) // (lado + 18))
        total_linhas = (len(imagens) + col - 1) // col
        self.scroll = max(0, min(self.scroll, max(0, total_linhas - linhas_vis)))
        for i, nome in enumerate(imagens[self.scroll * col:(self.scroll + linhas_vis) * col]):
            r = pygame.Rect(8 + (i % col) * (lado + 4), y + (i // col) * (lado + 18), lado, lado)
            ativo = self.ferramenta == "imagem:" + nome or self.img_escolhida == nome
            pygame.draw.rect(t, (50, 52, 62) if not r.collidepoint(mouse) else (64, 68, 82), r, border_radius=5)
            img = carregar_imagem(nome)
            if img is not None and img.get_width() and img.get_height():
                k = min((lado - 8) / img.get_width(), (lado - 8) / img.get_height())
                mini = imagem_escalada(nome, max(1, int(img.get_width() * k)), max(1, int(img.get_height() * k)))
                if mini is not None:
                    t.blit(mini, (r.centerx - mini.get_width() // 2, r.centery - mini.get_height() // 2))
            pygame.draw.rect(t, C_DESTAQUE if ativo else C_BORDA, r, 2 if ativo else 1, border_radius=5)
            rot = nome if self.fpp.size(nome)[0] <= lado else nome[:7] + "…"
            t.blit(self.fpp.render(rot, True, C_TEXTO2), (r.x, r.bottom + 2))
            self.hits_esq.append((r, ("img", nome)))
        y += linhas_vis * (lado + 18) + 4
        if self.img_escolhida:
            t.blit(self.fpp.render(f"Escolhida: {self.img_escolhida[:22]}", True, C_TEXTO), (10, y))
            y += 16
            for i, (rot, acao) in enumerate((("Pôr na seleção", ("img_aplicar",)), ("Editar", ("img_editar",)))):
                r = pygame.Rect(8 + i * 96, y, 90, 22)
                desenhar_botao(t, self.fpp, r, rot, mouse, cor=C_VERDE if i == 0 else None)
                self.hits_esq.append((r, acao))
            y += 26
        for linha in quebrar_texto("Clique numa imagem e depois na cena: cria uma Peça com ela.", self.fpp,
                                   PAINEL_ESQ - 20):
            t.blit(self.fpp.render(linha, True, C_TEXTO2), (10, y))
            y += 14

    def desenhar_esquerda(self, t, mouse):
        pygame.draw.rect(t, C_PAINEL, (0, TOPO, PAINEL_ESQ, ALTURA - TOPO - RODAPE))
        pygame.draw.line(t, C_BORDA, (PAINEL_ESQ - 1, TOPO), (PAINEL_ESQ - 1, ALTURA - RODAPE))
        nomes = {"objetos": "Objetos", "modelos": "Modelos", "imagens": "Imagens", "explorer": "Lista"}
        for nome, r in self.abas_esq.items():
            ativo = nome == self.aba_esq
            pygame.draw.rect(t, C_DESTAQUE if ativo else (C_BOTAO if r.collidepoint(mouse) else (36, 38, 46)), r,
                             border_radius=5)
            img = self.fpp.render(nomes[nome], True, C_TEXTO)
            t.blit(img, (r.centerx - img.get_width() // 2, r.y + 5))
        self.hits_esq = []
        area = pygame.Rect(0, TOPO + 36, PAINEL_ESQ - 1, ALTURA - RODAPE - TOPO - 36)
        t.set_clip(area)
        y = area.y
        if self.aba_esq == "objetos":
            r = pygame.Rect(8, y, 89, 26)
            ativo = self.ferramenta == "Selecionar"
            pygame.draw.rect(t, C_DESTAQUE if ativo else C_BOTAO, r, border_radius=5)
            pygame.draw.polygon(t, C_TEXTO, [(r.x + 8, r.y + 5), (r.x + 8, r.y + 20), (r.x + 12, r.y + 16),
                                             (r.x + 17, r.y + 18)])
            t.blit(self.fpp.render("Selecionar", True, C_TEXTO), (r.x + 24, r.y + 7))
            self.hits_esq.append((r, ("ferr", "Selecionar")))
            r = pygame.Rect(101, y, 89, 26)
            ativo = self.ferramenta == "Borracha"
            pygame.draw.rect(t, C_VERMELHO if ativo else C_BOTAO, r, border_radius=5)
            pygame.draw.rect(t, (240, 150, 160), (r.x + 7, r.y + 8, 12, 9), border_radius=2)
            t.blit(self.fpp.render("Borracha (E)", True, C_TEXTO), (r.x + 24, r.y + 7))
            self.hits_esq.append((r, ("ferr", "Borracha")))
            y += 34
            topo_lista = y
            vis_esq = suave((id(self), "esq"), self.scroll * 24)
            y -= vis_esq
            for grupo, tipos in GRUPOS_TIPOS:
                fechada = grupo in self.cats_fechadas
                cab = pygame.Rect(6, y, PAINEL_ESQ - 12, 20)
                if cab.y >= topo_lista - 4:
                    t.blit(self.fb.render(("▸ " if fechada else "▾ ") + grupo, True,
                                          C_TEXTO if cab.collidepoint(mouse) else C_TEXTO2), (10, y + 1))
                    self.hits_esq.append((cab, ("cat", grupo)))
                y += 22
                if fechada:
                    continue
                for i, tipo in enumerate(tipos):
                    col, lin = i % 2, i // 2
                    r = pygame.Rect(8 + col * 93, y + lin * 29, 89, 26)
                    if r.y < topo_lista - 4:
                        continue
                    ativo = self.ferramenta == tipo
                    pygame.draw.rect(t, C_DESTAQUE if ativo else (clarear(C_BOTAO, 17) if r.collidepoint(mouse)
                                                                  else C_BOTAO), r, border_radius=5)
                    icone = pygame.Rect(r.x + 5, r.y + 6, 14, 14)
                    if tipo.startswith("preset:"):
                        d_ic = preset_objeto(tipo[7:])
                        desenhar_icone(t, d_ic["tipo"], d_ic, icone)
                        rotulo = tipo[7:]
                    else:
                        desenhar_icone(t, tipo, dict(MODELOS[tipo], tipo=tipo), icone)
                        rotulo = NOMES_CURTOS.get(tipo, tipo)
                    t.blit(self.fpp.render(rotulo, True, C_TEXTO), (r.x + 23, r.y + 6))
                    self.hits_esq.append((r, ("ferr", tipo)))
                y += ((len(tipos) + 1) // 2) * 29 + 6
            for linha in quebrar_texto("Clique num tipo e depois na cena. Arraste para pintar vários. "
                                       "Clique no nome da categoria para fechar/abrir.", self.fpp, PAINEL_ESQ - 20):
                t.blit(self.fpp.render(linha, True, C_TEXTO2), (10, y))
                y += 14
            total = y + vis_esq - topo_lista
            limite = max(0, (total - (area.bottom - topo_lista) + 24) // 24)
            self.scroll = max(0, min(self.scroll, limite))
        elif self.aba_esq == "modelos":
            modelos = self.projeto["modelos"]
            t.blit(self.fb.render("MODELOS / VARIANTES", True, C_TEXTO2), (10, y))
            y += 22
            if not modelos:
                for linha in quebrar_texto("Nenhum ainda. Selecione um objeto na cena (com cor, tamanho, eventos, "
                                           "script e valores do jeito que quiser) e clique em 'Criar variante' no "
                                           "painel da direita (ou botão direito > Criar variante).", self.fp,
                                           PAINEL_ESQ - 20):
                    t.blit(self.fp.render(linha, True, C_TEXTO2), (10, y))
                    y += 17
            for nome, m in list(modelos.items())[self.scroll:]:
                r = pygame.Rect(8, y, PAINEL_ESQ - 16, 28)
                ativo = self.ferramenta == "modelo:" + nome
                pygame.draw.rect(t, C_DESTAQUE if ativo else (clarear(C_BOTAO, 17) if r.collidepoint(mouse)
                                                              else C_BOTAO), r, border_radius=5)
                desenhar_icone(t, m.get("tipo"), m, pygame.Rect(r.x + 6, r.y + 7, 14, 14))
                usos = sum(1 for f in self.projeto["fases"].values() for d in f["objetos"] if d.get("modelo") == nome)
                t.blit(self.fp.render(nome, True, C_TEXTO), (r.x + 26, r.y + 3))
                t.blit(self.fpp.render(f"{m.get('tipo')} · {usos} cópia(s)", True, C_TEXTO2), (r.x + 26, r.y + 16))
                xr = pygame.Rect(r.right - 20, r.y + 5, 16, 16)
                pygame.draw.rect(t, (90, 45, 45), xr, border_radius=3)
                t.blit(self.fpp.render("x", True, C_TEXTO), (xr.x + 5, xr.y + 1))
                self.hits_esq.append((xr, ("del_modelo", nome)))
                self.hits_esq.append((r, ("ferr", "modelo:" + nome)))
                y += 32
            if modelos:
                y += 6
                for linha in quebrar_texto("Clique num modelo e depois na cena para colocar uma cópia (arraste para "
                                           "pintar várias). Mudou uma cópia? Use 'Atualizar modelo' para mudar "
                                           "todas.", self.fpp, PAINEL_ESQ - 20):
                    t.blit(self.fpp.render(linha, True, C_TEXTO2), (10, y))
                    y += 14
        elif self.aba_esq == "imagens":
            self.desenhar_imagens_esq(t, mouse, area)
        else:
            filtro = self.filtro_explorer.lower()
            objs = [d for d in self.objetos if not filtro or filtro in d["nome"].lower() or filtro in d["tipo"].lower()]
            r = pygame.Rect(8, y, PAINEL_ESQ - 16, 24)
            pygame.draw.rect(t, C_CAMPO, r, border_radius=5)
            pygame.draw.rect(t, C_BORDA, r, 1, border_radius=5)
            t.blit(self.fp.render(f"Buscar: {self.filtro_explorer}" if self.filtro_explorer else "Buscar objeto...",
                                  True, C_TEXTO if self.filtro_explorer else C_TEXTO2), (r.x + 8, r.y + 4))
            self.hits_esq.append((r, ("buscar",)))
            if self.filtro_explorer:
                xr = pygame.Rect(r.right - 20, r.y + 4, 16, 16)
                pygame.draw.rect(t, (90, 45, 45), xr, border_radius=3)
                t.blit(self.fpp.render("x", True, C_TEXTO), (xr.x + 5, xr.y + 1))
                self.hits_esq.insert(0, (xr, ("limpar_busca",)))
            y += 30
            t.blit(self.fb.render(f"NESTA FASE ({len(objs)})", True, C_TEXTO2), (10, y))
            t.blit(self.fpp.render("Shift = vários · 2 cliques = ir até", True, C_TEXTO2), (10, y + 16))
            y += 34
            linhas = (area.bottom - y) // 21
            self.scroll = max(0, min(self.scroll, max(0, len(objs) - linhas)))
            for i, d in enumerate(objs[self.scroll:self.scroll + linhas]):
                r = pygame.Rect(8, y + i * 21, PAINEL_ESQ - 16, 20)
                if d is self.sel:
                    pygame.draw.rect(t, C_DESTAQUE, r, border_radius=3)
                elif self.esta_selecionado(d):
                    pygame.draw.rect(t, (60, 90, 150), r, border_radius=3)
                elif r.collidepoint(mouse):
                    pygame.draw.rect(t, C_BOTAO, r, border_radius=3)
                pygame.draw.rect(t, cor_ok(d.get("cor")), (r.x + 5, r.y + 6, 9, 9))
                marca = ""
                if d.get("na_tela"):
                    marca += " [UI]"
                if d.get("travado"):
                    marca += " [trava]"
                if d.get("oculto_editor"):
                    marca += " [oculto]"
                if d.get("eventos") or (d.get("script") or "").strip():
                    marca += " *"
                cor_txt = C_TEXTO2 if d.get("oculto_editor") else C_TEXTO
                t.blit(self.fp.render(f"{d['nome']}  ({d['tipo']}){marca}", True, cor_txt), (r.x + 20, r.y + 2))
                self.hits_esq.append((r, ("sel", d)))
        t.set_clip(None)

    def campo(self, t, r, txt, ativo, chave, idx, visivel=True):
        pygame.draw.rect(t, C_CAMPO, r, border_radius=4)
        pygame.draw.rect(t, C_DESTAQUE if ativo else C_BORDA, r, 1, border_radius=4)
        img = self.fp.render(txt, True, C_TEXTO)
        clip = t.get_clip()
        t.set_clip(r.inflate(-4, 0).clip(clip) if clip else r.inflate(-4, 0))
        t.blit(img, (r.x + 6, r.y + 4))
        t.set_clip(clip)
        if visivel:
            self.hits_insp.append((r, chave, idx))

    def esta_editando(self, alvo, chave, idx):
        return self.editando is not None and self.editando[0] is alvo and self.editando[1:] == (chave, idx)

    def desenhar_direita(self, t, mouse):
        x0 = LARGURA - PAINEL_DIR
        pygame.draw.rect(t, C_PAINEL, (x0, TOPO, PAINEL_DIR, ALTURA - TOPO - RODAPE))
        pygame.draw.line(t, C_BORDA, (x0, TOPO), (x0, ALTURA - RODAPE))
        t.blit(self.fb.render("PROPRIEDADES", True, C_TEXTO2), (x0 + 12, TOPO + 10))
        self.hits_insp = []
        area = pygame.Rect(x0 + 1, TOPO + 32, PAINEL_DIR - 1, ALTURA - RODAPE - TOPO - 32)
        t.set_clip(area)
        visivel = lambda r: area.collidepoint(r.center)
        piscar = "|" if int(self.tempo * 2) % 2 == 0 else ""
        varios = len(self.selecao) > 1

        alvo = self.alvo_logica()
        self.insp_vis = suave((id(self), "insp", id(self.sel)), self.insp_scroll)
        y = area.y + 2 - self.insp_vis
        if varios:
            titulo = f"{len(self.selecao)} objetos selecionados"
            desc = "Mudar um campo aqui muda em TODOS os selecionados. Campos marcados com ≠ são diferentes."
        elif self.sel:
            titulo = self.sel["tipo"] + (f"  (variante: {self.sel['modelo']})" if self.sel.get("modelo") else "")
            desc = DESC_TIPOS.get(self.sel["tipo"], "")
        else:
            titulo = f"Cena: {self.projeto['fase_atual']}"
            desc = "Configurações desta fase (fundo, música, gravidade, câmera) e do jogo (título, tela)."
        cor_titulo = C_MODELO if self.sel and self.sel.get("modelo") and not varios else C_TEXTO
        t.blit(self.f.render(titulo, True, cor_titulo), (x0 + 12, y))
        y += 22
        for linha in quebrar_texto(desc, self.fpp, PAINEL_DIR - 24):
            t.blit(self.fpp.render(linha, True, C_TEXTO2), (x0 + 12, y))
            y += 14
        y += 6

        # botoes de acao
        botoes = [("Eventos", "#eventos"), ("Script", "#script")]
        if varios:
            botoes = [("Copiar", "#copiar"), ("Duplicar", "#duplicar"), ("Apagar", "#apagar"),
                      ("Alinhar...", "#alinhar"), ("Camada +1", "#frente"), ("Camada -1", "#tras"),
                      ("Travar/destravar", "#travar")]
        elif self.sel:
            botoes = [("Duplicar", "#duplicar"), ("Apagar", "#apagar"),
                      ("Camada +1 (frente)", "#frente"), ("Camada -1 (trás)", "#tras")] + botoes
            botoes.append(("Criar variante", "#variante"))
            if self.sel.get("modelo"):
                botoes += [("Atualizar modelo", "#atualizar"), ("Desvincular", "#desvincular")]
        for i, (rotulo, chave) in enumerate(botoes):
            r = pygame.Rect(x0 + 12 + (i % 2) * 124, y + (i // 2) * 34, 118, 28)
            if chave == "#apagar":
                cor = C_VERMELHO
            elif chave in ("#eventos", "#script"):
                cor = C_QUANDO
            elif chave in ("#variante", "#atualizar", "#desvincular"):
                cor = C_MODELO
            else:
                cor = None
            desenhar_botao(t, self.fpp if len(rotulo) > 14 else self.fp, r, rotulo, mouse, cor=cor)
            if visivel(r):
                self.hits_insp.append((r, chave, None))
        y += ((len(botoes) + 1) // 2) * 34 + 4
        pygame.draw.line(t, C_BORDA, (x0 + 10, y), (x0 + PAINEL_DIR - 10, y))
        y += 10
        if self.sel and not varios:
            t.blit(self.fb.render("APARÊNCIA", True, C_TEXTO2), (x0 + 12, y))
            atual = "animação" if self.sel.get("animacao") else ("imagem" if self.sel.get("imagem") else "cor")
            t.blit(self.fpp.render(f"agora: {atual}", True, C_TEXTO2), (x0 + 100, y + 2))
            y += 20
            for i, (rotulo, chave, cor) in enumerate([("Cor sólida", "#ap_cor", (70, 76, 92)),
                                                       ("Imagem ▾", "#ap_img", (70, 76, 92)),
                                                       ("Desenhar", "#ap_desenhar", (130, 80, 170)),
                                                       ("Animação", "#ap_animar", (170, 100, 50))]):
                r = pygame.Rect(x0 + 12 + (i % 2) * 124, y + (i // 2) * 32, 118, 27)
                ativo = (chave == "#ap_cor" and atual == "cor") or (chave == "#ap_img" and atual == "imagem") or \
                        (chave == "#ap_animar" and atual == "animação")
                desenhar_botao(t, self.fp, r, rotulo, mouse, cor=C_DESTAQUE if ativo else cor)
                if visivel(r):
                    self.hits_insp.append((r, chave, None))
            y += 70
            pygame.draw.line(t, C_BORDA, (x0 + 10, y), (x0 + PAINEL_DIR - 10, y))
            y += 10

        if varios:
            comuns = [k for k in alvo if k not in OCULTAS and k != "nome" and all(k in d for d in self.selecao)]
        else:
            comuns = [k for k in alvo if k not in OCULTAS]
        for chave in comuns:
            valor = alvo[chave]
            diferente = varios and any(d.get(chave) != valor for d in self.selecao)
            rot = ("≠ " if diferente else "") + ROTULOS.get(chave, chave)
            t.blit(self.fp.render(rot, True, (230, 190, 110) if diferente else C_TEXTO2), (x0 + 12, y + 4))
            vx = x0 + 118
            if isinstance(valor, bool):
                r = pygame.Rect(vx, y, 60, 22)
                pygame.draw.rect(t, C_VERDE if valor else C_BOTAO, r, border_radius=11)
                img = self.fp.render("Sim" if valor else "Não", True, C_TEXTO)
                t.blit(img, (r.centerx - img.get_width() // 2, r.y + 4))
                if visivel(r):
                    self.hits_insp.append((r, chave, None))
            elif isinstance(valor, list):
                for i in range(min(3, len(valor))):
                    r = pygame.Rect(vx + i * 38, y, 34, 22)
                    ed = self.esta_editando(alvo, chave, i)
                    self.campo(t, r, self.buffer + piscar if ed else fmt(valor[i]), ed, chave, i, visivel(r))
                pygame.draw.rect(t, cor_ok(valor), (vx + 116, y + 2, 18, 18), border_radius=3)
            elif chave in OPCOES_PROPS:
                r = pygame.Rect(vx, y, 138, 22)
                pygame.draw.rect(t, (45, 48, 62), r, border_radius=4)
                pygame.draw.rect(t, C_BORDA, r, 1, border_radius=4)
                extra = f"  ({DESC_MATERIAIS[valor]})" if chave == "material" and valor in DESC_MATERIAIS else ""
                t.blit(self.fp.render(f"{valor}{extra}"[:22] + " ▾", True, C_TEXTO), (r.x + 6, r.y + 4))
                if visivel(r):
                    self.hits_insp.append((r, "#opcao", chave))
            elif chave in ("imagem", "imagem_fundo", "musica"):
                r = pygame.Rect(vx, y, 138, 22)
                pygame.draw.rect(t, (45, 40, 60), r, border_radius=4)
                pygame.draw.rect(t, C_BORDA, r, 1, border_radius=4)
                nome_arq = valor or "(nenhum)  ▾"
                if valor and chave != "musica" and carregar_imagem(valor) is None:
                    nome_arq = valor + " (não achei)"
                t.blit(self.fp.render(nome_arq, True, C_TEXTO), (r.x + 6, r.y + 4))
                if visivel(r):
                    self.hits_insp.append((r, "#som" if chave == "musica" else "#img", chave))
            else:
                r = pygame.Rect(vx, y, 138, 22)
                ed = self.esta_editando(alvo, chave, None)
                self.campo(t, r, self.buffer + piscar if ed else fmt(valor), ed, chave, None, visivel(r))
            y += 28

        if self.sel and not varios:
            y += 6
            pygame.draw.line(t, C_BORDA, (x0 + 10, y), (x0 + PAINEL_DIR - 10, y))
            y += 8
            t.blit(self.fb.render("VALORES DO OBJETO", True, C_TEXTO2), (x0 + 12, y))
            y += 18
            for linha in quebrar_texto("Use no script como eu.nome_do_valor ou no visual em 'Variável do objeto'.",
                                       self.fpp, PAINEL_DIR - 24):
                t.blit(self.fpp.render(linha, True, C_TEXTO2), (x0 + 12, y))
                y += 13
            y += 6
            valores = self.sel.setdefault("valores", {})
            for k, v in list(valores.items()):
                rk = pygame.Rect(x0 + 12, y, 104, 22)
                ed = self.esta_editando(valores, k, "#renomear")
                self.campo(t, rk, self.buffer + piscar if ed else k, ed, "#vchave", k, visivel(rk))
                rv = pygame.Rect(x0 + 120, y, 112, 22)
                ed = self.esta_editando(valores, k, "#valor")
                mostra = texto(v) if not isinstance(v, str) else v
                self.campo(t, rv, self.buffer + piscar if ed else mostra, ed, "#vvalor", k, visivel(rv))
                xr = pygame.Rect(x0 + 238, y + 2, 18, 18)
                pygame.draw.rect(t, (90, 45, 45), xr, border_radius=3)
                t.blit(self.fpp.render("x", True, C_TEXTO), (xr.x + 6, xr.y + 2))
                if visivel(xr):
                    self.hits_insp.append((xr, "#vdel", k))
                y += 26
            r = pygame.Rect(x0 + 12, y, 110, 24)
            desenhar_botao(t, self.fp, r, "+ Valor", mouse, cor=C_FUNCAO)
            if visivel(r):
                self.hits_insp.append((r, "#addvalor", None))
            y += 34

        if self.sel:
            pygame.draw.line(t, C_BORDA, (x0 + 10, y), (x0 + PAINEL_DIR - 10, y))
            y += 8
            t.blit(self.fb.render("COMPORTAMENTOS", True, C_TEXTO2), (x0 + 12, y))
            y += 18
            for linha in quebrar_texto("Movimentos e regras prontas, sem programar. Passe o mouse para ver o que "
                                       "cada um faz." if not varios else "Adiciona em todos os selecionados.",
                                       self.fpp, PAINEL_DIR - 24):
                t.blit(self.fpp.render(linha, True, C_TEXTO2), (x0 + 12, y))
                y += 13
            y += 6
            if not varios:
                for c in list(self.sel.get("comportamentos", [])):
                    nome = c.get("t", "?")
                    ligado = c.get("ativo") is not False
                    caixa = pygame.Rect(x0 + 8, y, PAINEL_DIR - 18, 26)
                    pygame.draw.rect(t, (44, 58, 60) if ligado else (48, 44, 46), caixa, border_radius=5)
                    t.blit(self.fb.render(nome, True, C_TEXTO if ligado else C_TEXTO2), (caixa.x + 8, caixa.y + 5))
                    rl = pygame.Rect(caixa.right - 72, caixa.y + 4, 46, 18)
                    pygame.draw.rect(t, C_VERDE if ligado else C_BOTAO, rl, border_radius=9)
                    img = self.fpp.render("ligado" if ligado else "off", True, C_TEXTO)
                    t.blit(img, (rl.centerx - img.get_width() // 2, rl.y + 2))
                    rx = pygame.Rect(caixa.right - 22, caixa.y + 4, 18, 18)
                    pygame.draw.rect(t, (90, 45, 45), rx, border_radius=3)
                    t.blit(self.fpp.render("x", True, C_TEXTO), (rx.x + 6, rx.y + 2))
                    if visivel(rl):
                        self.hits_insp.append((rl, "#cativo", c))
                    if visivel(rx):
                        self.hits_insp.append((rx, "#cdel", c))
                    y += 30
                    params = c.setdefault("p", {})
                    for chave_p, padrao, tipo in COMPORTAMENTOS.get(nome, []):
                        params.setdefault(chave_p, str(padrao))
                        t.blit(self.fpp.render(chave_p, True, C_TEXTO2), (x0 + 20, y + 5))
                        r = pygame.Rect(x0 + 118, y, 138, 21)
                        if tipo == "sn":
                            sim = params[chave_p] == "Sim"
                            pygame.draw.rect(t, C_VERDE if sim else C_BOTAO, (r.x, r.y, 60, r.h), border_radius=10)
                            t.blit(self.fp.render("Sim" if sim else "Não", True, C_TEXTO), (r.x + 16, r.y + 3))
                            if visivel(r):
                                self.hits_insp.append((pygame.Rect(r.x, r.y, 60, r.h), "#csn", (params, chave_p)))
                        else:
                            ed = self.esta_editando(params, chave_p, None)
                            self.campo(t, r, self.buffer + piscar if ed else params[chave_p], ed, "#cedit",
                                       (params, chave_p), visivel(r))
                        y += 25
                    y += 4
            r = pygame.Rect(x0 + 12, y, 150, 24)
            desenhar_botao(t, self.fp, r, "+ Comportamento", mouse, cor=C_FUNCAO)
            if visivel(r):
                self.hits_insp.append((r, "#addcomp", None))
            y += 34

        self.insp_total = y + self.insp_vis - area.y
        self.insp_scroll = max(0, min(self.insp_scroll, max(0, self.insp_total - area.h + 10)))
        t.set_clip(None)
        if self.insp_total > area.h:
            frac = area.h / self.insp_total
            barra_h = max(30, int(area.h * frac))
            pos = int((area.h - barra_h) * (self.insp_vis / max(1, self.insp_total - area.h)))
            pygame.draw.rect(t, C_BORDA, (LARGURA - 6, area.y + pos, 4, barra_h), border_radius=2)

    def desenhar_rodape(self, t, mouse):
        pygame.draw.rect(t, C_PAINEL, (0, ALTURA - RODAPE, LARGURA, RODAPE))
        pygame.draw.line(t, C_BORDA, (0, ALTURA - RODAPE), (LARGURA, ALTURA - RODAPE))
        if self.msg_t > 0 and not CONFIG["geral"].get("notificacoes", True):
            txt = self.msg
        else:
            nome_f = self.ferramenta[7:] + " (modelo)" if self.ferramenta.startswith("modelo:") else self.ferramenta
            txt = f"Ferramenta: {nome_f}   |   Selecionados: {len(self.selecao)}   |   " \
                  f"Objetos: {len(self.objetos)}   |   Zoom {round(self.zoom * 100)}%"
            if VIEW.collidepoint(mouse) and not self.jogo and self.aba == "cena":
                wx, wy = self.para_mundo(mouse)
                txt += f"   |   X {int(wx)}  Y {int(wy)}"
        t.blit(self.fp.render(txt, True, C_TEXTO), (10, ALTURA - RODAPE + 5))
        dica = self.fpp.render("F1 = todos os atalhos   ·   botão direito = mais opções", True, C_TEXTO2)
        t.blit(dica, (LARGURA - dica.get_width() - 10, ALTURA - RODAPE + 7))
