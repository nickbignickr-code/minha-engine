# Minha Engine - editor_entrada.py
# teclado e mouse do editor (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class EditorEntrada:
    # ----------------- eventos do pygame -----------------
    def evento(self, e):
        if e.type == pygame.QUIT:
            if self.sujo:
                self.autosave()
            self.rodando = False
        elif e.type == pygame.KEYDOWN:
            self.tecla(e)
        elif e.type == TOQUE_GESTO:
            self.gesto_toque(e)
        elif e.type == APP_PAUSOU:          # celular: saiu do app -> salva o que não foi salvo
            if self.sujo:
                self.autosave()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if self.clique_barra_toque(e.pos):
                    return
                self.clique(e.pos)
            elif e.button == 3 and self.aba == "desenho" and not self.jogo and not self.prompt and not self.menu \
                    and VIEW.collidepoint(e.pos):
                self.pixel.clique(e.pos, 3)
            elif e.button in (2, 3) and not self.jogo and not self.prompt:
                self.menu = None
                if self.aba == "cena" and VIEW.collidepoint(e.pos):
                    self.arrastando = ("pan", e.pos[0], e.pos[1], self.cam[0], self.cam[1])
                    self.dir_inicio = e.pos if e.button == 3 else None
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 3 and self.dir_inicio is not None and not self.jogo:
                ini = self.dir_inicio
                self.dir_inicio = None
                if abs(e.pos[0] - ini[0]) + abs(e.pos[1] - ini[1]) < 5:
                    self.arrastando = None
                    self.menu_contexto(e.pos)
                    return
            if e.button in (1, 2, 3) and self.arrastando:
                self.soltar_mouse(e.pos)
        elif e.type == pygame.MOUSEMOTION:
            self.mover_mouse(e.pos)
        elif e.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if self.saida_aberta and self.rect_saida().collidepoint((mx, my)):
                self.saida_scroll = max(0, self.saida_scroll + e.y * 2)
                return
            if self.seletor:
                self.roda_seletor(e.y)
                return
            if self.jogo or self.menu or self.prompt:
                return
            if mx < PAINEL_ESQ:
                self.scroll = max(0, self.scroll - e.y)
            elif mx >= LARGURA - PAINEL_DIR:
                self.insp_scroll = max(0, self.insp_scroll - e.y * 40)
            elif VIEW.collidepoint((mx, my)):
                if self.aba == "cena":
                    self.mudar_zoom(1.15 ** e.y, (mx, my))
                elif self.aba == "eventos":
                    self.ev_scroll = max(0, self.ev_scroll - e.y * 40)
                elif self.aba == "script":
                    self.cod_scroll = max(0, min(self.cod_scroll - e.y * 3, len(self.cod) - 1))
                elif self.aba == "api":
                    self.api_scroll = max(0, self.api_scroll - e.y * 50)
                elif self.aba == "loja":
                    self.loja.scroll = max(0, self.loja.scroll - e.y * 50)

    def soltar_mouse(self, pos):
        modo = self.arrastando[0]
        if modo in ("mover", "redim", "pintar", "apagar") and self.antes is not None:
            if json.dumps(self.projeto) != self.antes:
                self.guardar(self.antes)
        elif modo == "caixa":
            _, ini, fim, somar = self.arrastando
            caixa = pygame.Rect(min(ini[0], fim[0]), min(ini[1], fim[1]), abs(fim[0] - ini[0]), abs(fim[1] - ini[1]))
            if caixa.w > 3 or caixa.h > 3:
                dentro = [d for d in self.ordem_desenho() if not d.get("travado") and
                          self.intersecta(caixa, self.rect_tela(d))]
                self.selecionar_varios(dentro, somar)
                if dentro:
                    self.avisar(f"{len(self.selecao)} objeto(s) selecionado(s).")
        elif modo == "cod_sel" and self.ancora == self.cur:
            self.ancora = None
        elif modo == "pix":
            self.pixel.soltar(pos)
        self.arrastando = None
        self.antes = None

    @staticmethod
    def intersecta(a, b):
        return a.x < b.right and a.right > b.x and a.y < b.bottom and a.bottom > b.y

    def tecla(self, e):
        ctrl = e.mod & pygame.KMOD_CTRL
        shift = e.mod & pygame.KMOD_SHIFT
        if self.prompt:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.confirmar_prompt()
            elif e.key == pygame.K_ESCAPE:
                self.prompt = None
            elif e.key == pygame.K_BACKSPACE:
                self.prompt["texto"] = self.prompt["texto"][:-1]
            elif ctrl and e.key == pygame.K_v:
                self.prompt["texto"] += self.clip_pegar().split("\n")[0]
            elif e.unicode and e.unicode.isprintable():
                self.prompt["texto"] += e.unicode
            return
        if self.seletor:
            self.tecla_seletor(e)
            return
        if evento_e(e, "tela_cheia"):
            self.alternar_tela()
            return
        if evento_e(e, "ajuda") and not self.editando:
            self.mostrar_ajuda = not self.mostrar_ajuda
            return
        if self.editando:
            self.tecla_edicao(e)
            return
        if self.jogo:
            if e.key == pygame.K_ESCAPE or evento_e(e, "play") or evento_e(e, "play_cheio"):
                self.parar()
            elif self.jogo.quer_reiniciar(e.key) and (self.jogo.venceu or self.jogo.perdeu):
                self.reiniciar_jogo()
            return
        if self.menu and e.key == pygame.K_ESCAPE:
            self.menu = None
            return
        if self.mostrar_ajuda and e.key == pygame.K_ESCAPE:
            self.mostrar_ajuda = False
            return
        if evento_e(e, "saida"):
            self.saida_aberta = not self.saida_aberta
            return
        for acao, fn in (("salvar", self.salvar), ("abrir", self.abrir), ("inicio", self.ir_inicio),
                         ("play", self.play), ("play_cheio", lambda: self.play(cheio=True))):
            if evento_e(e, acao):
                fn()
                return
        if self.aba == "script":
            self.tecla_codigo(e)
            return
        if self.aba == "desenho":
            self.pixel.tecla(e)
            return
        if self.aba == "loja":
            if e.key == pygame.K_BACKSPACE:
                self.loja.busca = self.loja.busca[:-1]
            elif e.key == pygame.K_ESCAPE:
                self.loja.busca = ""
            elif e.unicode and e.unicode.isprintable() and not ctrl:
                self.loja.busca += e.unicode
            self.loja.scroll = 0
            return
        if evento_e(e, "refazer"):
            self.refazer()
            return
        if evento_e(e, "desfazer"):
            self.desfazer()
            return
        if self.aba == "api":
            if e.key == pygame.K_BACKSPACE:
                self.api_busca = self.api_busca[:-1]
            elif e.key == pygame.K_ESCAPE:
                self.api_busca = ""
            elif e.unicode and e.unicode.isprintable() and not ctrl:
                self.api_busca += e.unicode
            self.api_scroll = 0
            return
        if e.key == pygame.K_ESCAPE:
            if self.ferramenta != "Selecionar":
                self.ferramenta = "Selecionar"
            else:
                self.selecionar(None)
            return
        if self.aba != "cena":
            return

        def borracha():
            self.ferramenta = "Selecionar" if self.ferramenta == "Borracha" else "Borracha"
            self.avisar("Borracha: clique ou arraste por cima para apagar. Esc volta." if self.ferramenta == "Borracha"
                        else "Modo Selecionar.")

        def snap():
            self.snap = not self.snap
            self.avisar("Snap na grade: " + ("ligado" if self.snap else "desligado"))

        acoes_cena = (("girar_menos", lambda: self.girar_selecao(-1)), ("girar", lambda: self.girar_selecao(1)),
                      ("copiar", self.copiar), ("recortar", self.recortar), ("colar", self.colar),
                      ("duplicar", self.duplicar), ("selecionar_tudo", self.selecionar_tudo),
                      ("zoom_100", self.zoom_100), ("apagar", self.apagar), ("snap", snap), ("focar", self.focar),
                      ("travar", self.alternar_trava), ("minimapa", lambda: setattr(self, "minimapa", not self.minimapa)),
                      ("borracha", borracha), ("esconder", self.esconder_no_editor),
                      ("zoom_mais", lambda: self.mudar_zoom(1.2)), ("zoom_menos", lambda: self.mudar_zoom(1 / 1.2)))
        for acao, fn in acoes_cena:
            if evento_e(e, acao):
                fn()
                return
        if self.selecao and e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN) and not ctrl:
            passo = 1 if (shift or not self.snap) else self.grade
            dx = {pygame.K_LEFT: -passo, pygame.K_RIGHT: passo}.get(e.key, 0)
            dy = {pygame.K_UP: -passo, pygame.K_DOWN: passo}.get(e.key, 0)
            self.mover_selecao(dx, dy)

    def clique(self, pos):
        if self.jogo and self.play_cheio:
            self.clique_jogo = pos
            return
        if self.prompt:
            for r, acao in self.hits_prompt:
                if r.collidepoint(pos):
                    if acao == "ok":
                        self.confirmar_prompt()
                    else:
                        self.prompt = None
                    return
            return
        if self.seletor:
            self.clique_seletor(pos)
            return
        if self.menu:
            m = self.menu
            self.menu = None
            for item, r in zip(m["itens"], self.rects_menu_de(m)):
                if r.collidepoint(pos):
                    m["fn"](item)
            return
        if self.mostrar_ajuda:
            self.mostrar_ajuda = False
            return
        self.confirmar_edicao()
        for nome, r in self.botoes.items():
            if r.collidepoint(pos):
                self.acao(nome)
                return
        if self.clique_toast(pos):
            return
        if self.aba == "cena" and not self.jogo and (self.clique_passos(pos) or self.clique_vazio(pos)):
            return
        if self.saida_aberta and self.rect_saida().collidepoint(pos):
            self.clique_saida(pos)
            return
        if self.jogo:
            if VIEW.collidepoint(pos):
                self.clique_jogo = pos
            return
        if getattr(self, "rect_saldo", None) is not None and self.rect_saldo.collidepoint(pos):
            self.aba = "loja"
            self.loja.vista = "planos"
            return
        if self.botao_fase.collidepoint(pos):
            self.menu_fases(self.botao_fase.bottomleft)
            return
        for nome, r in self.abas.items():
            if r.collidepoint(pos):
                self.aba = nome
                self.ferramenta = "Selecionar"
                return
        for nome, r in self.abas_esq.items():
            if r.collidepoint(pos):
                self.aba_esq = nome
                self.scroll = 0
                return

        if pos[0] < PAINEL_ESQ:
            self.clique_esquerda(pos)
        elif pos[0] >= LARGURA - PAINEL_DIR:
            self.clique_inspetor(pos)
        elif VIEW.collidepoint(pos):
            if self.aba == "cena":
                self.clique_cena(pos)
            elif self.aba == "eventos":
                self.clique_eventos(pos)
            elif self.aba == "script":
                self.clique_codigo(pos)
            elif self.aba == "desenho":
                self.pixel.clique(pos, 1)
            elif self.aba == "loja":
                self.loja.clique(pos)
            else:
                self.clique_api(pos)

    def duplo_clique(self, alvo):
        agora = self.tempo
        anterior_t, anterior = self.ultimo_clique
        self.ultimo_clique = (agora, alvo)
        return anterior is alvo and agora - anterior_t < 0.4

    def clique_esquerda(self, pos):
        shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
        for r, a in self.hits_esq:
            if not r.collidepoint(pos):
                continue
            if a[0] == "ferr":
                self.ferramenta = a[1]
                self.aba = "cena"
            elif a[0] == "sel":
                d = a[1]
                if self.duplo_clique(d):
                    self.selecionar(d)
                    self.aba = "cena"
                    self.focar()
                else:
                    self.selecionar(d, somar=bool(shift))
                self.ferramenta = "Selecionar"
            elif a[0] == "cat":
                if a[1] in self.cats_fechadas:
                    self.cats_fechadas.discard(a[1])
                else:
                    self.cats_fechadas.add(a[1])
            elif a[0] == "del_modelo":
                self.abrir_menu(pos, [f"Sim, apagar o modelo '{a[1]}'", "Cancelar"],
                                lambda it, nome=a[1]: self.apagar_modelo(nome) if it.startswith("Sim") else None)
            elif a[0] == "buscar":
                self.pedir_texto("Filtrar o Explorer (nome ou tipo)", self.filtro_explorer,
                                 lambda txt: setattr(self, "filtro_explorer", txt.strip()))
            elif a[0] == "limpar_busca":
                self.filtro_explorer = ""
            elif a[0] == "img":
                self.img_escolhida = a[1]
                if self.duplo_clique(("img", a[1])) and self.selecao:
                    self.aplicar_imagem(a[1])
                else:
                    self.ferramenta = "imagem:" + a[1]
                    self.aba = "cena"
            elif a[0] == "img_importar":
                abrir_pasta(PASTA_IMAGENS)
                self.avisar("Coloque arquivos PNG/JPG na pasta e clique em 'Atualizar'.")
            elif a[0] == "img_recarregar":
                limpar_cache_imagens()
                self.avisar(f"{len(listar_imagens())} imagem(ns) na pasta.")
            elif a[0] == "img_desenhar":
                self.abrir_desenho(self.sel, "imagem")
                if self.sel is None:
                    self.pixel.novo(16)
            elif a[0] == "img_aplicar" and self.img_escolhida:
                self.aplicar_imagem(self.img_escolhida)
            elif a[0] == "img_editar" and self.img_escolhida:
                self.abrir_desenho(None, "imagem")
                self.pixel.carregar_imagens([self.img_escolhida])
            return

    def menu_arquivos(self, pos, alvo, chave, tipo="imagem"):
        if tipo == "imagem":
            arquivos, pasta, ext = listar_imagens(), PASTA_IMAGENS, "PNG/JPG"
        else:
            arquivos, pasta, ext = listar_sons(), PASTA_SONS, "WAV/OGG/MP3"
        itens = ["(nenhum)"] + arquivos + [f"» Abrir pasta {os.path.basename(pasta)}", "» Recarregar"]

        def escolher(item):
            if item.startswith("» Abrir"):
                abrir_pasta(pasta)
                self.avisar(f"Coloque arquivos {ext} na pasta e clique em 'Recarregar'.")
            elif item == "» Recarregar":
                limpar_cache_imagens()
                self.avisar(f"{len(arquivos)} arquivo(s) na pasta {os.path.basename(pasta)}.")
            else:
                self.guardar()
                alvo[chave] = "" if item == "(nenhum)" else item
                self.propagar(alvo, chave)
                limpar_cache_imagens()
        if not arquivos:
            self.avisar(f"A pasta '{os.path.basename(pasta)}' está vazia. Coloque arquivos {ext} nela.")
        self.abrir_menu(pos, itens, escolher)

    def clique_inspetor(self, pos):
        alvo = self.alvo_logica()
        for r, chave, idx in self.hits_insp:
            if not r.collidepoint(pos):
                continue
            acoes = {"#duplicar": self.duplicar, "#apagar": self.apagar, "#frente": lambda: self.camada(True),
                     "#tras": lambda: self.camada(False), "#eventos": lambda: setattr(self, "aba", "eventos"),
                     "#script": lambda: setattr(self, "aba", "script"), "#variante": self.criar_variante,
                     "#atualizar": self.atualizar_modelo, "#desvincular": self.desvincular,
                     "#copiar": self.copiar, "#travar": self.alternar_trava,
                     "#alinhar": lambda: self.abrir_menu(pos, ["Alinhar à esquerda", "Alinhar ao topo",
                                                               "Alinhar embaixo", "Centralizar (vertical)",
                                                               "Mesmo tamanho", "Distribuir na horizontal"],
                                                         self.escolher_alinhar)}
            if chave in acoes:
                acoes[chave]()
            elif chave == "#img":
                self.menu_arquivos(pos, alvo, idx, "imagem")
            elif chave == "#opcao":
                def escolher(item, prop=idx, alvo=alvo):
                    self.guardar()
                    alvo[prop] = item
                    self.propagar(alvo, prop)
                opcoes = OPCOES_PROPS[idx]
                rotulos = [f"{o}  ({DESC_MATERIAIS[o]})" if idx == "material" and o in DESC_MATERIAIS else o
                           for o in opcoes]
                self.abrir_menu(pos, rotulos, lambda it: escolher(it.split("  (")[0]))
            elif chave == "#ap_cor":
                self.guardar()
                self.sel["imagem"] = ""
                self.sel["animacao"] = ""
                self.avisar("Aparência: cor sólida. Mude a cor e o material nas propriedades.")
            elif chave == "#ap_img":
                self.menu_arquivos(pos, self.sel, "imagem", "imagem")
            elif chave == "#ap_desenhar":
                self.abrir_desenho(self.sel, "imagem")
            elif chave == "#ap_animar":
                self.abrir_desenho(self.sel, "animacao")
            elif chave == "#som":
                self.menu_arquivos(pos, alvo, idx, "som")
            elif chave == "#addvalor":
                self.guardar()
                valores = self.sel.setdefault("valores", {})
                nome, i = "valor1", 1
                while nome in valores:
                    i += 1
                    nome = f"valor{i}"
                valores[nome] = 0
                self.comecar_edicao(valores, nome, "#renomear")
            elif chave == "#vchave":
                self.comecar_edicao(self.sel["valores"], idx, "#renomear")
            elif chave == "#vvalor":
                self.comecar_edicao(self.sel["valores"], idx, "#valor")
            elif chave == "#vdel":
                self.guardar()
                self.sel["valores"].pop(idx, None)
            elif chave == "#addcomp":
                alvo_comp = self.selecao if len(self.selecao) > 1 else [self.sel]

                def adicionar(nome, objs=alvo_comp):
                    self.guardar()
                    for d in objs:
                        lista = d.setdefault("comportamentos", [])
                        if any(c.get("t") == nome for c in lista):
                            continue
                        lista.append({"t": nome, "p": params_padrao(COMPORTAMENTOS[nome])})
                    self.avisar(f"Comportamento '{nome}' adicionado. {DESC_COMPORTAMENTOS.get(nome, '')}")
                self.abrir_seletor("Escolha um comportamento", "comp", COMPORTAMENTOS, CATEGORIAS_COMPORTAMENTOS,
                                   adicionar, (40, 150, 140))
            elif chave == "#cdel":
                self.guardar()
                lista = self.sel.get("comportamentos", [])
                if idx in lista:
                    lista.remove(idx)
            elif chave == "#cativo":
                self.guardar()
                idx["ativo"] = idx.get("ativo") is False
            elif chave == "#cedit":
                self.comecar_edicao(idx[0], idx[1])
            elif chave == "#csn":
                self.guardar()
                idx[0][idx[1]] = "Não" if idx[0].get(idx[1], "Sim") == "Sim" else "Sim"
            elif isinstance(alvo.get(chave), bool):
                self.guardar()
                alvo[chave] = not alvo[chave]
                self.propagar(alvo, chave)
            else:
                self.comecar_edicao(alvo, chave, idx)
            return

    def escolher_alinhar(self, item):
        modos = {"Alinhar à esquerda": "esquerda", "Alinhar ao topo": "topo", "Alinhar embaixo": "base",
                 "Centralizar (vertical)": "centro", "Mesmo tamanho": "tamanho",
                 "Distribuir na horizontal": "distribuir"}
        self.alinhar(modos[item])

    def apagar_em(self, pos):
        d = self.objeto_em(pos)
        if d is not None:
            self.fase["objetos"] = [x for x in self.objetos if x is not d]
            self.validar_selecao()
            return True
        return False

    def clique_cena(self, pos):
        shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
        if self.minimapa and self.minimapa_rect is not None and self.minimapa_rect.collidepoint(pos):
            ox, oy, x0, y0, k = self.minimapa_conv     # clicou no mini-mapa: leva a camera pra la
            self.cam[0] = x0 + (pos[0] - ox) / k - VIEW.w / self.zoom / 2
            self.cam[1] = y0 + (pos[1] - oy) / k - VIEW.h / self.zoom / 2
            self.arrastando = ("minimapa",)
            return
        if self.ferramenta == "Borracha":
            self.antes = json.dumps(self.projeto)
            self.apagar_em(pos)
            self.arrastando = ("apagar",)
            return
        if self.ferramenta != "Selecionar":
            self.antes = json.dumps(self.projeto)
            novo = self.colocar(pos)
            self.arrastando = ("pintar",) if novo is not None and novo["tipo"] != "Player" else None
            if novo is None and self.antes is not None and json.dumps(self.projeto) != self.antes:
                self.guardar(self.antes)
            return

        if self.sel and len(self.selecao) == 1 and self.alca().collidepoint(pos):
            self.antes = json.dumps(self.projeto)
            self.arrastando = ("redim",)
            return

        d = self.objeto_em(pos)
        if d is not None:
            if shift:
                self.selecionar(d, somar=True)
                return
            if not self.esta_selecionado(d):
                self.selecionar(d)
            else:
                self.sel = d
            wx, wy = self.coord_de(d.get("na_tela"), pos)
            self.antes = json.dumps(self.projeto)
            origens = [(x, num_seguro(x["x"]), num_seguro(x["y"])) for x in self.selecao]
            self.arrastando = ("mover", wx - num_seguro(d["x"]), wy - num_seguro(d["y"]), origens)
            return
        if not shift:
            self.selecionar(None)
        self.arrastando = ("caixa", pos, pos, bool(shift))

    def mover_mouse(self, pos):
        if not self.arrastando:
            return
        modo = self.arrastando[0]
        if modo == "sel_barra":
            self.arrastar_barra_seletor(pos)
            return
        if modo == "ev_barra":
            trilho = self.arrastando[1]
            k = (pos[1] - trilho.y) / max(1, trilho.h)
            self.ev_scroll = int(max(0.0, min(1.0, k)) * max(0, self.ev_total - VIEW.h + 20))
            return
        if modo == "pix":
            self.pixel.arrastar(pos)
        elif modo == "pan":
            _, sx, sy, cx, cy = self.arrastando
            self.cam[0] = cx - (pos[0] - sx) / self.zoom
            self.cam[1] = cy - (pos[1] - sy) / self.zoom
        elif modo == "caixa":
            _, ini, _, somar = self.arrastando
            self.arrastando = ("caixa", ini, pos, somar)
        elif modo == "pintar":
            if VIEW.collidepoint(pos):
                self.colocar(pos, pintando=True)
        elif modo == "apagar":
            if VIEW.collidepoint(pos):
                self.apagar_em(pos)
        elif modo == "minimapa" and self.minimapa_conv:
            ox, oy, x0, y0, k = self.minimapa_conv
            self.cam[0] = x0 + (pos[0] - ox) / k - VIEW.w / self.zoom / 2
            self.cam[1] = y0 + (pos[1] - oy) / k - VIEW.h / self.zoom / 2
        elif modo == "cod_sel":
            self.cur = self.pos_para_cursor(pos)
            self.mostrar_cursor()
        elif self.sel is None:
            return
        elif modo == "mover":
            _, offx, offy, origens = self.arrastando
            wx, wy = self.coord_de(self.sel.get("na_tela"), pos)
            base = next((o for o in origens if o[0] is self.sel), None)
            if base is None:
                return
            nx = self.ajustar(wx - offx)
            ny = self.ajustar(wy - offy)
            dx, dy = nx - base[1], ny - base[2]
            for d, x0, y0 in origens:
                d["x"] = x0 + dx
                d["y"] = y0 + dy
        elif modo == "redim":
            wx, wy = self.coord_de(self.sel.get("na_tela"), pos)
            minimo = self.grade if self.snap else 4
            self.sel["w"] = max(minimo, self.ajustar(wx - num_seguro(self.sel["x"])))
            self.sel["h"] = max(minimo, self.ajustar(wy - num_seguro(self.sel["y"])))
