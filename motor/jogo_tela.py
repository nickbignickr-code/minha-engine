# Minha Engine - jogo_tela.py
# o desenho do jogo na tela (objetos, luz, UI, diálogos) (métodos do Jogo)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class JogoTela:
    def desenhar_dialogo(self, tela, a):
        d = self.dialogo
        caixa = pygame.Rect(a.x + 30, a.bottom - 150, a.w - 60, 120)
        fundo = pygame.Surface((caixa.w, caixa.h), pygame.SRCALPHA)
        fundo.fill((18, 20, 28, 235))
        tela.blit(fundo, caixa.topleft)
        pygame.draw.rect(tela, (230, 230, 240), caixa, 2, border_radius=8)
        y = caixa.y + 14
        if d["nome"]:
            nome = texto_cache(d["nome"], 18, LOGO_BRASA, True)
            tela.blit(nome, (caixa.x + 18, y))
            y += 26
        visivel = d["linhas"][d["i"]][:int(d["chars"])]
        for linha in quebrar_texto(visivel, fonte(19), caixa.w - 50)[:3]:
            tela.blit(texto_cache(linha, 19, (245, 245, 250)), (caixa.x + 18, y))
            y += 25
        if int(d["chars"]) >= len(d["linhas"][d["i"]]) and int(self.tempo_total * 3) % 2 == 0:
            seta = "fim  (E)" if d["i"] + 1 >= len(d["linhas"]) else "▼  (E)"
            img = texto_cache(seta, 14, (180, 180, 195))
            tela.blit(img, (caixa.right - img.get_width() - 14, caixa.bottom - 24))

    def balao(self, tela, fonte_, msg, cx, y):
        img = fonte_.render(msg, True, (20, 20, 25))
        r = pygame.Rect(0, 0, img.get_width() + 16, img.get_height() + 8)
        r.centerx = int(cx)
        r.bottom = int(y)
        pygame.draw.rect(tela, (255, 255, 255), r, border_radius=8)
        tela.blit(img, (r.x + 8, r.y + 4))

    def rect_de(self, o, ox=0, oy=0):
        a = self.area
        if o.na_tela:
            return pygame.Rect(round(a.x + o.x), round(a.y + o.y), max(1, round(o.w)), max(1, round(o.h)))
        z = self.zoom
        return pygame.Rect(round((o.x - self.cam[0]) * z + a.x + ox), round((o.y - self.cam[1]) * z + a.y + oy),
                           max(1, round(o.w * z)), max(1, round(o.h * z)))

    def desenhar(self, tela, fonte_, fonte_grande):
        a = self.area
        pygame.draw.rect(tela, cor_ok(self.cena.get("fundo", [25, 28, 45])), a)
        tela.set_clip(a)
        fundo_img = imagem_escalada(self.cena.get("imagem_fundo", ""), a.w, a.h) if self.cena.get("imagem_fundo") else None
        if fundo_img is not None:
            par = num_seguro(self.cena.get("parallax_fundo", 0), 0)
            if par:
                desloc = int(-(self.cam[0] * par) % a.w)
                tela.blit(fundo_img, (a.x + desloc - a.w, a.y))
                tela.blit(fundo_img, (a.x + desloc, a.y))
            else:
                tela.blit(fundo_img, a.topleft)
        ox = oy = 0
        if self.tremor_t > 0 and self.tremor > 0:
            amp = self.tremor * (self.tremor_t / max(0.01, self.tremor_dur)) ** 2   # tremor que vai sumindo
            ox = random.uniform(-amp, amp)
            oy = random.uniform(-amp, amp)

        camada = lambda o: num_seguro(o.d.get("camada", 0))
        td = bool(self.cena.get("visao_de_cima"))
        if td and self.cena.get("ordenar_por_y", True):     # top-down: quem esta mais embaixo fica na frente
            mundo = sorted((o for o in self.objs if o.vivo and o.visivel and not o.na_tela),
                           key=lambda o: (camada(o), o.y + o.h))
        else:
            mundo = sorted((o for o in self.objs if o.vivo and o.visivel and not o.na_tela), key=camada)
        sombras = td and self.cena.get("sombras", True)
        ui = sorted((o for o in self.objs if o.vivo and o.visivel and o.na_tela), key=camada)
        for o in mundo:
            r = self.rect_de(o, ox, oy)
            if r.right < a.x - 50 or r.x > a.right + 50 or r.bottom < a.y - 50 or r.y > a.bottom + 50:
                continue
            if o.piscar_t > 0 and o.flash_t <= 0 and int(o.piscar_t * 12) % 2 == 0:
                continue
            if o.squash_t > 0:   # amassa e estica (squash & stretch), com a base no chao
                k = o.squash_t / 0.18
                nw, nh = round(r.w * (1 + 0.25 * k)), max(1, round(r.h * (1 - 0.22 * k)))
                r = pygame.Rect(r.centerx - nw // 2, r.bottom - nh, nw, nh)
            if sombras:
                self.desenhar_sombra(tela, o, r)
            desenhar_obj(tela, o.d, r, o.texto_atual, progresso=o.progresso, img_nome=o.imagem_atual(self.tempo))
            if o.flash_t > 0:
                branco = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                branco.fill((255, 255, 255, int(220 * min(1.0, o.flash_t / max(0.01, o.flash_dur)))))
                tela.blit(branco, r.topleft)
            if o.tipo == "NPC" and o.perto and o.fala_t <= 0:
                self.balao(tela, fonte_, "E", r.centerx, r.y - 6)
        for o in self.objs:
            if o.vivo and o.fala_t > 0 and o.fala and not o.na_tela:
                r = self.rect_de(o, ox, oy)
                self.balao(tela, fonte_, o.fala, r.centerx, r.y - 6)
        if self.cena_dono.fala_t > 0 and self.cena_dono.fala:
            self.balao(tela, fonte_, self.cena_dono.fala, a.centerx, a.y + 80)

        self.desenhar_golpes(tela, a)
        z = self.zoom
        for pt in self.particulas:
            px = round((pt[0] - self.cam[0]) * z + a.x + ox)
            py = round((pt[1] - self.cam[1]) * z + a.y + oy)
            lado = max(1, round(pt[6] * z))
            pygame.draw.rect(tela, pt[5], (px, py, lado, lado))

        # barras de vida em cima de quem tem o comportamento Vida
        for o in mundo:
            if o is self.player or not o.tem("Vida") or not o.comp["Vida"].get("barra", True):
                continue
            vida, maximo = num_seguro(o.vars.get("vida", 0)), num_seguro(o.vars.get("vida_max", 0))
            if maximo > 0 and vida < maximo:
                r = self.rect_de(o, ox, oy)
                fundo_b = pygame.Rect(r.centerx - 18, r.y - 10, 36, 5)
                pygame.draw.rect(tela, (40, 40, 45), fundo_b)
                pygame.draw.rect(tela, (90, 220, 100) if vida / maximo > 0.35 else (240, 80, 70),
                                 (fundo_b.x, fundo_b.y, max(1, int(36 * max(0.0, vida) / maximo)), 5))

        # escuridao com luzes (comportamento Luz)
        escuro = int(max(0, min(255, num_seguro(self.cena.get("escuridao", 0), 0))))
        if escuro > 0:
            noite = pygame.Surface((a.w, a.h), pygame.SRCALPHA)
            noite.fill((0, 0, 0, escuro))
            for o in self.objs:
                if o.vivo and o.tem("Luz") and not o.na_tela:
                    b = o.comp["Luz"]
                    raio = max(4, int(b["raio"] * self.zoom))
                    luz = gradiente_luz(raio, int(max(0, min(255, b["forca"]))))
                    r = self.rect_de(o, ox, oy)
                    noite.blit(luz, (r.centerx - a.x - raio, r.centery - a.y - raio),
                               special_flags=pygame.BLEND_RGBA_SUB)
            tela.blit(noite, a.topleft)

        # numeros e textos flutuantes
        for fx, fy, ftxt, fcor, ft in self.flutuantes:
            img = texto_cache(ftxt, int(20 * max(0.7, min(1.6, self.zoom))), fcor, True)
            img.set_alpha(int(255 * max(0.0, 1 - ft / 0.9)))
            px = round((fx - self.cam[0]) * z + a.x + ox) - img.get_width() // 2
            py = round((fy - self.cam[1]) * z + a.y + oy) - img.get_height()
            tela.blit(img, (px, py))
            img.set_alpha(255)

        for o in ui:
            desenhar_obj(tela, o.d, self.rect_de(o), o.texto_atual, progresso=o.progresso,
                         img_nome=o.imagem_atual(self.tempo))

        if self.cena.get("mostrar_moedas", True):
            tela.blit(fonte_.render(f"Moedas: {self.moedas}", True, (255, 210, 50)), (a.x + 12, a.y + 10))
        if self.inventario:
            inv = fonte_.render("Itens: " + ", ".join(self.inventario), True, (120, 230, 230))
            tela.blit(inv, (a.x + 140, a.y + 10))
        dica = ("ESC = sair  |  P = pausa" if self.sozinho else
                f"PLAY ({self.fase_nome})  -  P pausa  -  ESC volta ao editor")
        img = fonte_.render(dica, True, (200, 200, 210))
        tela.blit(img, (a.right - img.get_width() - 12, a.y + 10))
        for msg, x, y in self.hud.values():
            tela.blit(fonte_.render(msg, True, (255, 255, 255)), (a.x + int(x), a.y + int(y)))

        base = a.bottom - 10
        if self.erros:
            linhas = self.erros[-3:]
            h = len(linhas) * 20 + 10
            pygame.draw.rect(tela, (120, 25, 25), (a.x + 8, base - h, a.w - 16, h), border_radius=6)
            for i, msg in enumerate(linhas):
                tela.blit(fonte_.render("ERRO  " + msg, True, (255, 230, 230)), (a.x + 16, base - h + 5 + i * 20))
            base -= h + 6
        for i, (msg, _) in enumerate(reversed(self.log[-5:])):
            tela.blit(fonte_.render("> " + msg, True, (200, 230, 200)), (a.x + 12, base - 20 - i * 20))

        if self.transicao_t > 0 and len(self.dados["fases"]) > 1:
            alpha = int(255 * min(1.0, self.transicao_t / 0.5))
            cortina = pygame.Surface((a.w, a.h), pygame.SRCALPHA)
            cortina.fill((LOGO_FUNDO[0], LOGO_FUNDO[1], LOGO_FUNDO[2], alpha))
            tela.blit(cortina, a.topleft)
            tam = min(110, a.h // 4)
            desenhar_simbolo(tela, a.centerx - tam // 2, a.centery - tam - 10, tam, alpha=alpha)
            nome = fonte(34, True).render(self.fase_nome, True, (255, 255, 255))
            nome.set_alpha(alpha)
            tela.blit(nome, (a.centerx - nome.get_width() // 2, a.centery + 14))
        self.desenhar_extra(tela, a)
        if self.dialogo is not None:
            self.desenhar_dialogo(tela, a)
        if self.debug:
            for o in mundo:
                r = self.rect_de(o)
                cor = (80, 255, 120) if o.d.get("solido") else ((255, 220, 60) if o.quer_toque else (120, 170, 255))
                pygame.draw.rect(tela, cor, r, 1)
            info = [f"FPS {round(self.fps_med)}", f"Objetos {len(self.objs)}", f"Partículas {len(self.particulas)}",
                    f"Zoom {round(self.zoom, 2)}", f"Fase {self.fase_nome}"]
            if self.player:
                info.append(f"Player x {round(self.player.x)} y {round(self.player.y)} vida {self.player.vars.get('vida', '-')}")
            for k, v in list(self.globais.d.items())[:6]:
                info.append(f"global.{k} = {texto(v)}"[:40])
            caixa = pygame.Surface((300, len(info) * 18 + 10), pygame.SRCALPHA)
            caixa.fill((0, 0, 0, 170))
            tela.blit(caixa, (a.x + 10, a.y + 40))
            for i, linha in enumerate(info):
                tela.blit(texto_cache(linha, 14, (140, 255, 160)), (a.x + 18, a.y + 45 + i * 18))
        if self.pausado:
            sombra = pygame.Surface((a.w, a.h), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 140))
            tela.blit(sombra, a.topleft)
            t1 = fonte_grande.render("PAUSADO", True, (255, 255, 255))
            t2 = fonte_.render("Aperte P para continuar", True, (220, 220, 220))
            tela.blit(t1, (a.centerx - t1.get_width() // 2, a.centery - 50))
            tela.blit(t2, (a.centerx - t2.get_width() // 2, a.centery + 5))
        if self.venceu or self.perdeu:
            titulo = "VOCÊ VENCEU!" if self.venceu else "VOCÊ PERDEU!"
            cor = (255, 255, 255) if self.venceu else (255, 110, 110)
            t1 = fonte_grande.render(titulo, True, cor)
            t2 = fonte_.render("Aperte R para jogar de novo", True, (220, 220, 220))
            tela.blit(t1, (a.centerx - t1.get_width() // 2, a.centery - 50))
            tela.blit(t2, (a.centerx - t2.get_width() // 2, a.centery + 5))
        tela.set_clip(None)
