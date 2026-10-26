# Minha Engine - editor_objetos.py
# editar objetos, variantes, campos de texto, copiar/colar (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class EditorObjetos:
    # ----------------- editar objetos -----------------
    def copiar(self):
        if not self.selecao:
            self.avisar("Nada selecionado para copiar.")
            return
        self.clipboard = copy.deepcopy(self.selecao)
        self.avisar(f"{len(self.clipboard)} objeto(s) copiado(s). Ctrl+V cola onde o mouse estiver.")

    def recortar(self):
        if self.selecao:
            self.copiar()
            self.apagar()

    def colar(self, pos=None):
        if not self.clipboard:
            self.avisar("Nada copiado ainda (Ctrl+C).")
            return
        self.guardar()
        itens = copy.deepcopy(self.clipboard)
        tem_player = any(d["tipo"] == "Player" for d in self.objetos)
        itens = [d for d in itens if not (d["tipo"] == "Player" and tem_player)]
        if not itens:
            self.avisar("Só pode ter 1 Player por fase.")
            return
        mouse = pygame.mouse.get_pos()
        if pos is None and VIEW.collidepoint(mouse) and self.aba == "cena":
            pos = mouse
        mundo = [d for d in itens if not d.get("na_tela")]
        if pos is not None and mundo:
            wx, wy = self.para_mundo(pos)
            dx = self.ajustar(wx) - min(num_seguro(d["x"]) for d in mundo)
            dy = self.ajustar(wy) - min(num_seguro(d["y"]) for d in mundo)
        else:
            dx = dy = self.grade * 2
        nomes = {d["nome"] for d in self.objetos}
        for d in itens:
            if d.get("na_tela"):
                d["x"] = num_seguro(d["x"]) + self.grade
                d["y"] = num_seguro(d["y"]) + self.grade
            else:
                d["x"] = num_seguro(d["x"]) + dx
                d["y"] = num_seguro(d["y"]) + dy
            d["nome"] = self.nome_unico(d["nome"], nomes)
            d.pop("travado", None)
            nomes.add(d["nome"])
            self.objetos.append(d)
        self.selecionar_varios(itens)
        self.avisar(f"{len(itens)} objeto(s) colado(s).")

    def duplicar(self):
        if not self.selecao:
            return
        guardado = self.clipboard
        self.clipboard = copy.deepcopy(self.selecao)
        self._colar_deslocado()
        self.clipboard = guardado

    def _colar_deslocado(self):
        self.guardar()
        tem_player = any(d["tipo"] == "Player" for d in self.objetos)
        nomes = {d["nome"] for d in self.objetos}
        novos = []
        for d in copy.deepcopy(self.clipboard):
            if d["tipo"] == "Player" and tem_player:
                continue
            d["x"] = num_seguro(d["x"]) + self.grade * 2
            d["y"] = num_seguro(d["y"]) + self.grade
            d["nome"] = self.nome_unico(d["nome"], nomes)
            d.pop("travado", None)
            nomes.add(d["nome"])
            self.objetos.append(d)
            novos.append(d)
        if novos:
            self.selecionar_varios(novos)
        else:
            self.avisar("Só pode ter 1 Player por fase.")

    def apagar(self):
        if not self.selecao:
            return
        self.guardar()
        ids = {id(d) for d in self.selecao}
        self.fase["objetos"] = [d for d in self.objetos if id(d) not in ids]
        n = len(ids)
        self.selecionar(None)
        self.avisar(f"{n} objeto(s) apagado(s). Ctrl+Z volta.")

    def camada(self, frente):
        if not self.selecao:
            return
        self.guardar()
        for d in self.selecao:
            d["camada"] = int(num_seguro(d.get("camada", 0)) + (1 if frente else -1))

    def girar_selecao(self, sentido):
        if not self.selecao:
            return
        self.guardar()
        passo = (self.passo_giro or 1) * sentido
        for d in self.selecao:
            d["rotacao"] = round((num_seguro(d.get("rotacao", 0)) + passo) % 360, 2)
        self.avisar(f"Girado para {fmt(self.sel['rotacao'])}°  ({atalho_de('girar')} / {atalho_de('girar_menos')})")

    def mover_selecao(self, dx, dy):
        if not self.selecao:
            return
        self.guardar()
        for d in self.selecao:
            d["x"] = num_seguro(d["x"]) + dx
            d["y"] = num_seguro(d["y"]) + dy

    def alternar_trava(self):
        if not self.selecao:
            return
        self.guardar()
        travar = not all(d.get("travado") for d in self.selecao)
        for d in self.selecao:
            if travar:
                d["travado"] = True
            else:
                d.pop("travado", None)
        self.avisar("Travado(s): não dá pra clicar na cena (use o Explorer)." if travar else "Destravado(s).")
        if travar:
            self.selecionar(None)

    def esconder_no_editor(self):
        if not self.selecao:
            return
        self.guardar()
        for d in self.selecao:
            d["oculto_editor"] = True
        self.avisar(f"{len(self.selecao)} escondido(s) só no editor (no jogo aparecem). Botão direito > Mostrar.")
        self.selecionar(None)

    def mostrar_escondidos(self):
        self.guardar()
        for d in self.objetos:
            d.pop("oculto_editor", None)

    def alinhar(self, modo):
        itens = [d for d in self.selecao if not d.get("na_tela")] or list(self.selecao)
        if len(itens) < 2:
            return
        self.guardar()
        ref = self.sel if self.sel in itens else itens[0]
        X = lambda d: num_seguro(d["x"])
        Y = lambda d: num_seguro(d["y"])
        W = lambda d: num_seguro(d["w"], 40)
        H = lambda d: num_seguro(d["h"], 40)
        if modo == "esquerda":
            m = min(X(d) for d in itens)
            for d in itens:
                d["x"] = m
        elif modo == "topo":
            m = min(Y(d) for d in itens)
            for d in itens:
                d["y"] = m
        elif modo == "base":
            m = max(Y(d) + H(d) for d in itens)
            for d in itens:
                d["y"] = m - H(d)
        elif modo == "centro":
            c = X(ref) + W(ref) / 2
            for d in itens:
                d["x"] = round(c - W(d) / 2)
        elif modo == "tamanho":
            for d in itens:
                d["w"], d["h"] = ref["w"], ref["h"]
        elif modo == "distribuir":
            ordem = sorted(itens, key=X)
            ini, fim = X(ordem[0]), X(ordem[-1])
            passo = (fim - ini) / (len(ordem) - 1)
            for i, d in enumerate(ordem):
                d["x"] = round(ini + passo * i)

    def focar(self):
        itens = [d for d in self.selecao if not d.get("na_tela")]
        if not itens:
            itens = [d for d in self.objetos if d["tipo"] == "Player"] or [d for d in self.objetos if not d.get("na_tela")]
        if not itens:
            self.cam = [-40.0, -100.0]
            return
        x0 = min(num_seguro(d["x"]) for d in itens)
        y0 = min(num_seguro(d["y"]) for d in itens)
        x1 = max(num_seguro(d["x"]) + num_seguro(d["w"], 40) for d in itens)
        y1 = max(num_seguro(d["y"]) + num_seguro(d["h"], 40) for d in itens)
        self.cam[0] = (x0 + x1) / 2 - VIEW.w / 2 / self.zoom
        self.cam[1] = (y0 + y1) / 2 - VIEW.h / 2 / self.zoom

    def acao(self, nome):
        if nome == "inicio":
            self.ir_inicio()
        elif nome == "play":
            self.play()
        elif nome == "playcheio":
            self.play(cheio=True)
        elif nome == "telacheia":
            self.alternar_tela()
        elif nome == "ajuda":
            opcoes = {f"Atalhos do teclado ({atalho_de('ajuda')})": lambda: setattr(self, "mostrar_ajuda", True),
                      "Primeiros passos (guia)": self.reabrir_passos,
                      "Tudo da engine (aba API)": lambda: setattr(self, "aba", "api"),
                      "Coisas prontas (aba Loja)": lambda: setattr(self, "aba", "loja"),
                      "Dica: " + dica_do_dia()[:60] + ("…" if len(dica_do_dia()) > 60 else ""): lambda: None}
            self.abrir_menu(self.botoes["ajuda"].bottomleft, list(opcoes), lambda it: opcoes[it]())
        elif self.jogo:
            return
        elif nome == "novo":
            self.novo()
        elif nome == "salvar":
            self.salvar()
        elif nome == "abrir":
            self.abrir()
        elif nome == "desfazer":
            self.desfazer()
        elif nome == "refazer":
            self.refazer()
        elif nome == "grade":
            self.mostrar_grade = not self.mostrar_grade
        elif nome == "modo":
            self.trocar_modo()
        elif nome == "mover":
            def escolher(item):
                self.grade = int(item.split()[0])
                self.snap = True
                self.avisar(f"Agora os objetos andam de {self.grade} em {self.grade} studs.")
            self.abrir_menu(self.botoes["mover"].bottomleft, [f"{v} studs" for v in self.STUDS], escolher)
        elif nome == "girar":
            def escolher_giro(item):
                self.passo_giro = 0 if item.startswith("Livre") else float(item.rstrip("°"))
                self.avisar(f"Girar com {atalho_de('girar')}: {item}")
            self.abrir_menu(self.botoes["girar"].bottomleft, ["Livre (1°)"] + [f"{v}°" for v in (5, 15, 30, 45, 90)],
                            escolher_giro)
        elif nome == "saida":
            self.saida_aberta = not self.saida_aberta
        elif nome == "snap":
            self.snap = not self.snap
        elif nome == "exportar":
            self.menu_exportar()

    def menu_contexto(self, pos):
        if self.ferramenta != "Selecionar":
            self.ferramenta = "Selecionar"
            self.avisar("Modo Selecionar.")
            return
        embaixo = self.objeto_em(pos)
        if embaixo is not None and not self.esta_selecionado(embaixo):
            self.selecionar(embaixo)
        acoes = {}

        def add(rot, fn):
            acoes[rot] = fn

        if self.selecao:
            add("Copiar   (Ctrl+C)", self.copiar)
            add("Recortar   (Ctrl+X)", self.recortar)
        if self.clipboard:
            add("Colar aqui   (Ctrl+V)", lambda: self.colar(pos))
        if self.selecao:
            add("Duplicar   (Ctrl+D)", self.duplicar)
            add("Apagar   (Delete)", self.apagar)
            add("Trazer pra frente", lambda: self.camada(True))
            add("Mandar pra trás", lambda: self.camada(False))
            add("Destravar" if all(d.get("travado") for d in self.selecao) else "Travar   (L)", self.alternar_trava)
            add("Esconder no editor   (H)", self.esconder_no_editor)
            add("Selecionar todos deste tipo", self.selecionar_tipo)
            if len(self.selecao) >= 2:
                add("Alinhar à esquerda", lambda: self.alinhar("esquerda"))
                add("Alinhar ao topo", lambda: self.alinhar("topo"))
                add("Alinhar embaixo", lambda: self.alinhar("base"))
                add("Centralizar (vertical)", lambda: self.alinhar("centro"))
                add("Mesmo tamanho", lambda: self.alinhar("tamanho"))
                add("Distribuir na horizontal", lambda: self.alinhar("distribuir"))
            elif self.sel and self.sel["tipo"] != "Player":
                add("Criar variante", self.criar_variante)
            add("Editar eventos", lambda: setattr(self, "aba", "eventos"))
            add("Editar script", lambda: setattr(self, "aba", "script"))
            add("Focar câmera   (F)", self.focar)
        add("Selecionar tudo   (Ctrl+A)", self.selecionar_tudo)
        if any(d.get("oculto_editor") for d in self.objetos):
            add("Mostrar escondidos", self.mostrar_escondidos)
        add("Zoom 100%   (Ctrl+0)", self.zoom_100)
        self.abrir_menu(pos, list(acoes), lambda it: acoes[it]())

    def objeto_em(self, pos):
        for d in reversed(self.ordem_desenho()):
            if not d.get("travado") and self.rect_tela(d).collidepoint(pos):
                return d
        return None

    # ----------------- variantes (modelos) -----------------
    def criar_variante(self):
        if not self.sel:
            return
        if self.sel["tipo"] == "Player":
            self.avisar("O Player não pode virar variante.")
            return
        self.guardar()
        modelos = self.projeto["modelos"]
        nome = self.nome_unico(self.sel["nome"], set(modelos))
        m = copy.deepcopy(self.sel)
        for k in ("modelo", "travado", "oculto_editor"):
            m.pop(k, None)
        m["nome"] = nome
        modelos[nome] = m
        self.sel["modelo"] = nome
        self.aba_esq = "modelos"
        self.avisar(f"Variante '{nome}' criada! Ela está na aba Modelos, pronta pra usar em qualquer fase.")

    def atualizar_modelo(self):
        nome = self.sel.get("modelo") if self.sel else None
        modelos = self.projeto["modelos"]
        if not nome or nome not in modelos:
            self.avisar("Esse objeto não está ligado a um modelo.")
            return
        self.guardar()
        novo = copy.deepcopy(self.sel)
        for k in ("modelo", "travado", "oculto_editor"):
            novo.pop(k, None)
        novo["nome"] = nome
        modelos[nome] = novo
        n = 0
        for fase in self.projeto["fases"].values():
            for d in fase["objetos"]:
                if d is not self.sel and d.get("modelo") == nome:
                    manter = {k: d[k] for k in ("nome", "x", "y", "modelo", "travado", "oculto_editor") if k in d}
                    d.clear()
                    d.update(copy.deepcopy(novo))
                    d.update(manter)
                    n += 1
        self.avisar(f"Modelo '{nome}' atualizado. {n} cópia(s) mudaram junto (em todas as fases).")

    def desvincular(self):
        if self.sel and self.sel.get("modelo"):
            self.guardar()
            self.sel.pop("modelo", None)
            self.avisar("Objeto desligado do modelo.")

    def apagar_modelo(self, nome):
        self.guardar()
        self.projeto["modelos"].pop(nome, None)
        for fase in self.projeto["fases"].values():
            for d in fase["objetos"]:
                if d.get("modelo") == nome:
                    d.pop("modelo", None)
        if self.ferramenta == "modelo:" + nome:
            self.ferramenta = "Selecionar"

    def abrir_desenho(self, alvo=None, modo="imagem"):
        """Abre a aba Desenho para desenhar a imagem (ou os quadros da animacao) do objeto."""
        if self.pixel.mudou and self.pixel.alvo is not alvo:
            self.pixel.salvar(aplicar=False)
        self.confirmar_edicao()
        self.pixel.abrir_para(alvo, modo)
        self.aba = "desenho"
        self.ferramenta = "Selecionar"

    def aplicar_imagem(self, nome, alvos=None):
        alvos = alvos or self.selecao
        if not alvos:
            self.avisar("Selecione um objeto na cena (ou clique na imagem e depois na cena para criar uma Peça).")
            return
        self.guardar()
        for d in alvos:
            d["imagem"] = nome
            d["animacao"] = ""
        self.avisar(f"Imagem '{nome}' aplicada em {len(alvos)} objeto(s).")

    def gabarito_ferramenta(self):
        """O objeto que a ferramenta atual vai criar (para o fantasma e para colocar)."""
        if self.ferramenta.startswith("modelo:"):
            m = self.projeto["modelos"].get(self.ferramenta[7:])
            if m is None:
                return None
            m = copy.deepcopy(m)
            m["modelo"] = self.ferramenta[7:]
            return m
        if self.ferramenta.startswith("preset:"):
            return preset_objeto(self.ferramenta[7:])
        if self.ferramenta.startswith("imagem:"):
            return peca_com_imagem(self.ferramenta[7:])
        if self.ferramenta in MODELOS:
            return nova_entidade(self.ferramenta, 0, 0)
        return None

    def colocar(self, pos, pintando=False):
        """Coloca um objeto da ferramenta atual no ponto do mouse."""
        modelo = self.gabarito_ferramenta()
        if modelo is None:
            return None
        wx, wy = self.coord_de(bool(modelo.get("na_tela")), pos)
        x = self.ajustar(wx - num_seguro(modelo["w"], 40) / 2)
        y = self.ajustar(wy - num_seguro(modelo["h"], 40) / 2)
        if pintando:
            for d in self.objetos:
                if num_seguro(d["x"]) == x and num_seguro(d["y"]) == y and d["tipo"] == modelo["tipo"] \
                        and d.get("modelo") == modelo.get("modelo"):
                    return None
        if modelo["tipo"] == "Player":
            existente = next((d for d in self.objetos if d["tipo"] == "Player"), None)
            if existente:
                existente["x"], existente["y"] = x, y
                self.selecionar(existente)
                self.avisar("Só pode ter 1 Player por fase, então movi ele pra cá.")
                return None
        modelo["x"], modelo["y"] = x, y
        modelo["nome"] = self.nome_unico(modelo.get("nome") or modelo["tipo"])
        self.objetos.append(modelo)
        self.selecionar(modelo)
        return modelo

    # ----------------- edicao de campos de texto -----------------
    def valor_atual(self, alvo, chave, idx):
        if idx == "#renomear":
            return chave
        if idx in (None, "#valor"):
            return alvo[chave]
        return alvo[chave][idx]

    def comecar_edicao(self, alvo, chave, idx=None):
        self.editando = (alvo, chave, idx)
        self.buffer = fmt(self.valor_atual(alvo, chave, idx))

    def propagar(self, alvo, chave, idx=None):
        """Com varios selecionados, a mudanca no principal vai para todos."""
        if alvo is not self.sel or len(self.selecao) < 2 or chave in ("nome",):
            return
        for d in self.selecao:
            if d is alvo or chave not in d:
                continue
            if idx is None:
                d[chave] = copy.deepcopy(alvo[chave])
            elif isinstance(d[chave], list) and idx < len(d[chave]):
                d[chave][idx] = alvo[chave][idx]

    def confirmar_edicao(self):
        if not self.editando:
            return
        alvo, chave, idx = self.editando
        self.editando = None
        txt = self.buffer.strip()
        if idx == "#renomear":
            novo = re.sub(r"\W", "_", txt)
            if not novo or novo == chave or chave not in alvo:
                return
            if novo in alvo:
                self.avisar(f"Já existe um valor chamado '{novo}'.")
                return
            self.guardar()
            itens = list(alvo.items())
            alvo.clear()
            for k, v in itens:
                alvo[novo if k == chave else k] = v
            return
        if idx == "#valor":
            if chave not in alvo:
                return
            v = interpretar_valor(self.buffer)
            if v != alvo[chave] or type(v) is not type(alvo[chave]):
                self.guardar()
                alvo[chave] = v
            return
        if chave not in alvo:
            return
        antigo = self.valor_atual(alvo, chave, idx)
        try:
            if isinstance(antigo, (int, float)) and not isinstance(antigo, bool):
                v = float(txt.replace(",", "."))
                if isinstance(antigo, int) and v.is_integer():
                    v = int(v)
                if idx is not None:
                    v = max(0, min(255, int(v)))
                if chave in ("w", "h"):
                    v = max(4, v)
                if chave == "opacidade":
                    v = max(0, min(255, v))
            else:
                v = self.buffer if txt else antigo
        except ValueError:
            self.avisar("Valor inválido. Digite um número.")
            return
        if chave == "nome" and alvo is self.sel and v != antigo:
            v = self.nome_unico(v, {d["nome"] for d in self.objetos if d is not alvo})
        if v != antigo:
            self.guardar()
            if idx is not None:
                alvo[chave][idx] = v
            else:
                alvo[chave] = v
            self.propagar(alvo, chave, idx)

    def tecla_edicao(self, e):
        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB):
            self.confirmar_edicao()
        elif e.key == pygame.K_ESCAPE:
            self.editando = None
        elif e.key == pygame.K_BACKSPACE:
            self.buffer = self.buffer[:-1]
        elif e.mod & pygame.KMOD_CTRL and e.key == pygame.K_v:
            self.buffer += self.clip_pegar().split("\n")[0]
        elif e.mod & pygame.KMOD_CTRL and e.key == pygame.K_c:
            self.clip_por(self.buffer)
        elif e.unicode and e.unicode.isprintable() and len(self.buffer) < 300:
            self.buffer += e.unicode

    # ----------------- area de transferencia (copiar texto) -----------------
    def clip_por(self, txt):
        self.clip_txt = txt
        try:
            if hasattr(pygame, "scrap"):
                if not pygame.scrap.get_init():
                    pygame.scrap.init()
                pygame.scrap.put_text(txt)
        except Exception:  # nem todo sistema tem area de transferencia no pygame
            pass

    def clip_pegar(self):
        try:
            if hasattr(pygame, "scrap"):
                if not pygame.scrap.get_init():
                    pygame.scrap.init()
                t = pygame.scrap.get_text()
                if t:
                    return t.replace("\r\n", "\n").replace("\x00", "")
        except Exception:
            pass
        return self.clip_txt

    def abrir_menu(self, pos, itens, ao_escolher):
        por_col = min(len(itens), self.MENU_POR_COLUNA)
        colunas = (len(itens) + por_col - 1) // por_col
        w = colunas * self.MENU_LARG + 8
        h = por_col * 24 + 8
        x = max(5, min(pos[0], LARGURA - w - 5))
        y = max(5, min(pos[1], ALTURA - h - 5))
        self.menu = {"x": x, "y": y, "w": w, "h": h, "itens": itens, "fn": ao_escolher, "por_col": por_col}

    def rects_menu_de(self, m):
        pc = m["por_col"]
        return [pygame.Rect(m["x"] + 4 + (i // pc) * self.MENU_LARG, m["y"] + 4 + (i % pc) * 24,
                            self.MENU_LARG - 4, 23) for i in range(len(m["itens"]))]

    def desenhar_menu(self, t, mouse):
        if not self.menu:
            return
        m = self.menu
        fundo = pygame.Rect(m["x"], m["y"], m["w"], m["h"])
        pygame.draw.rect(t, (20, 21, 26), fundo.move(3, 3), border_radius=6)
        pygame.draw.rect(t, C_PAINEL, fundo, border_radius=6)
        pygame.draw.rect(t, C_DESTAQUE, fundo, 1, border_radius=6)
        for item, r in zip(m["itens"], self.rects_menu_de(m)):
            if r.collidepoint(mouse):
                pygame.draw.rect(t, C_DESTAQUE, r, border_radius=4)
            t.blit(self.fp.render(item, True, C_TEXTO), (r.x + 8, r.y + 4))
