# Minha Engine - editor_script.py
# aba Script (editor de código Brasa) e aba API (métodos do Editor)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class EditorScript:
    # ----------------- ABA SCRIPT (editor de codigo) -----------------
    def carregar_codigo(self):
        alvo = self.alvo_logica()
        if self.cod_alvo is not alvo:
            self.cod_alvo = alvo
            self.cod = (alvo.get("script", "") or "").split("\n")
            self.cur = [0, 0]
            self.ancora = None
            self.cod_scroll = 0
            self.cod_msg = ""
            self.cod_erro_linha = None
            self.cod_undo = []
            self.cod_redo = []
            self.cod_ultimo = None
            self.cod_sujo = False
            self.auto = None

    def salvar_codigo(self):
        if self.cod_alvo is not None:
            self.cod_alvo["script"] = "\n".join(self.cod)

    def verificar_codigo(self):
        try:
            compilar("\n".join(self.cod))
            self.cod_msg = "Sem erros! Tudo certo."
            self.cod_erro_linha = None
        except ErroBrasa as e:
            self.cod_msg = "ERRO  " + str(e)
            self.cod_erro_linha = e.linha
            self.registrar("erro", e.msg, self.alvo_logica().get("nome", "Cena") if self.sel else "Cena", e.linha)
            if e.linha:
                self.cur = [min(e.linha - 1, len(self.cod) - 1), 0]
                self.ancora = None
                self.mostrar_cursor()

    def linhas_visiveis(self):
        return max(1, (self.area_cod.h - 8) // self.lh)

    def mostrar_cursor(self):
        vis = self.linhas_visiveis()
        if self.cur[0] < self.cod_scroll:
            self.cod_scroll = self.cur[0]
        elif self.cur[0] >= self.cod_scroll + vis:
            self.cod_scroll = self.cur[0] - vis + 1

    # --- selecao de texto ---
    def tem_selecao(self):
        return self.ancora is not None and self.ancora != self.cur

    def faixa(self):
        a, b = list(self.ancora), list(self.cur)
        return (a, b) if (a[0], a[1]) <= (b[0], b[1]) else (b, a)

    def texto_selecionado(self):
        if not self.tem_selecao():
            return ""
        (l1, c1), (l2, c2) = self.faixa()
        if l1 == l2:
            return self.cod[l1][c1:c2]
        partes = [self.cod[l1][c1:]] + self.cod[l1 + 1:l2] + [self.cod[l2][:c2]]
        return "\n".join(partes)

    def apagar_selecao(self):
        (l1, c1), (l2, c2) = self.faixa()
        self.cod[l1] = self.cod[l1][:c1] + self.cod[l2][c2:]
        del self.cod[l1 + 1:l2 + 1]
        self.cur = [l1, c1]
        self.ancora = None

    def inserir_texto(self, txt):
        if self.tem_selecao():
            self.apagar_selecao()
        self.ancora = None
        l, c = self.cur
        linha = self.cod[l]
        partes = txt.split("\n")
        if len(partes) == 1:
            self.cod[l] = linha[:c] + txt + linha[c:]
            self.cur = [l, c + len(txt)]
        else:
            fim = linha[c:]
            self.cod[l] = linha[:c] + partes[0]
            novas = partes[1:]
            novas[-1] = novas[-1] + fim
            self.cod[l + 1:l + 1] = novas
            self.cur = [l + len(novas), len(partes[-1])]

    # --- desfazer do codigo ---
    def foto_codigo(self, tipo="outro"):
        """Guarda o codigo antes de mudar (para Ctrl+Z). Digitacao seguida vira um passo so."""
        if not self.cod_sujo:
            self.guardar()
            self.cod_sujo = True
        if tipo == "letra" and self.cod_ultimo == "letra":
            return
        self.cod_undo.append((list(self.cod), list(self.cur)))
        if len(self.cod_undo) > 300:
            self.cod_undo.pop(0)
        self.cod_redo.clear()
        self.cod_ultimo = tipo
        self.cod_msg = ""
        self.cod_erro_linha = None

    def desfazer_codigo(self):
        if not self.cod_undo:
            self.cod_msg = "Nada para desfazer no script."
            return
        self.cod_redo.append((list(self.cod), list(self.cur)))
        self.cod, self.cur = self.cod_undo.pop()
        self.ancora = None
        self.cod_ultimo = None
        self.salvar_codigo()

    def refazer_codigo(self):
        if not self.cod_redo:
            return
        self.cod_undo.append((list(self.cod), list(self.cur)))
        self.cod, self.cur = self.cod_redo.pop()
        self.ancora = None
        self.cod_ultimo = None
        self.salvar_codigo()

    # --- autocompletar ---
    def palavra_no_cursor(self):
        l, c = self.cur
        m = re.search(r"[A-Za-z_À-ÿ][\wÀ-ÿ]*$", self.cod[l][:c])
        return m.group(0) if m else ""

    def atualizar_auto(self):
        pref = self.palavra_no_cursor()
        if len(pref) < 2:
            self.auto = None
            return
        l, c = self.cur
        antes = self.cod[l][:c - len(pref)]
        if antes.endswith("."):
            candidatos = set(PROPS_OBJ)
        else:
            candidatos = set(NOMES_PRONTOS) | PALAVRAS | set(EVENTOS_SCRIPT) | set(PLUGIN_FUNCOES)
            candidatos |= set(RE_PALAVRA.findall("\n".join(self.cod)))
        lista = sorted((n for n in candidatos if n.lower().startswith(pref.lower()) and n != pref),
                       key=lambda n: (len(n), n))[:8]
        self.auto = {"itens": lista, "i": 0, "pref": pref} if lista else None

    def aceitar_auto(self):
        if not self.auto:
            return
        escolha = self.auto["itens"][self.auto["i"]]
        pref = self.auto["pref"]
        self.foto_codigo()
        l, c = self.cur
        self.cod[l] = self.cod[l][:c - len(pref)] + escolha + self.cod[l][c:]
        self.cur = [l, c - len(pref) + len(escolha)]
        self.auto = None
        self.salvar_codigo()

    # --- outras ferramentas ---
    def linhas_da_selecao(self):
        if self.tem_selecao():
            (l1, _), (l2, c2) = self.faixa()
            if c2 == 0 and l2 > l1:
                l2 -= 1
            return l1, l2
        return self.cur[0], self.cur[0]

    def comentar_linhas(self):
        self.foto_codigo()
        l1, l2 = self.linhas_da_selecao()
        linhas = [i for i in range(l1, l2 + 1) if self.cod[i].strip()]
        tirar = linhas and all(self.cod[i].lstrip().startswith("#") for i in linhas)
        for i in linhas:
            linha = self.cod[i]
            ind = len(linha) - len(linha.lstrip(" "))
            if tirar:
                resto = linha[ind:][1:]
                self.cod[i] = linha[:ind] + (resto[1:] if resto.startswith(" ") else resto)
            else:
                self.cod[i] = linha[:ind] + "# " + linha[ind:]
        self.cur[1] = min(self.cur[1], len(self.cod[self.cur[0]]))
        if self.ancora:
            self.ancora[1] = min(self.ancora[1], len(self.cod[self.ancora[0]]))

    def indentar(self, menos=False):
        self.foto_codigo()
        l1, l2 = self.linhas_da_selecao()
        for i in range(l1, l2 + 1):
            linha = self.cod[i]
            if menos:
                tirar = min(4, len(linha) - len(linha.lstrip(" ")))
                self.cod[i] = linha[tirar:]
                if i == self.cur[0]:
                    self.cur[1] = max(0, self.cur[1] - tirar)
                if self.ancora and i == self.ancora[0]:
                    self.ancora[1] = max(0, self.ancora[1] - tirar)
            else:
                self.cod[i] = "    " + linha
                if i == self.cur[0]:
                    self.cur[1] += 4
                if self.ancora and i == self.ancora[0]:
                    self.ancora[1] += 4

    def buscar_proximo(self):
        termo = self.busca_cod.lower()
        if not termo:
            return
        total = len(self.cod)
        l, c = self.cur
        for passo in range(total + 1):
            i = (l + passo) % total
            inicio = c if passo == 0 else 0
            pos = self.cod[i].lower().find(termo, inicio)
            if pos >= 0:
                self.ancora = [i, pos]
                self.cur = [i, pos + len(termo)]
                self.mostrar_cursor()
                self.cod_msg = f"Achei '{self.busca_cod}' na linha {i + 1}. F3 = próximo"
                return
        self.cod_msg = f"Não achei '{self.busca_cod}'."

    def pos_para_cursor(self, pos):
        l = self.cod_scroll + (pos[1] - self.area_cod.y - 4) // self.lh
        l = max(0, min(l, len(self.cod) - 1))
        c = int(round((pos[0] - (self.area_cod.x + self.gutter)) / self.cw))
        return [l, max(0, min(c, len(self.cod[l])))]

    def tecla_codigo(self, e):
        self.carregar_codigo()
        linhas = self.cod
        self.cur[0] = max(0, min(self.cur[0], len(linhas) - 1))
        self.cur[1] = max(0, min(self.cur[1], len(linhas[self.cur[0]])))
        k = e.key
        ctrl = e.mod & pygame.KMOD_CTRL
        shift = e.mod & pygame.KMOD_SHIFT

        if self.auto:
            if k == pygame.K_DOWN:
                self.auto["i"] = (self.auto["i"] + 1) % len(self.auto["itens"])
                return
            if k == pygame.K_UP:
                self.auto["i"] = (self.auto["i"] - 1) % len(self.auto["itens"])
                return
            if k in (pygame.K_TAB, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.aceitar_auto()
                return
            if k == pygame.K_ESCAPE:
                self.auto = None
                return

        if ctrl:
            if k == pygame.K_a:
                self.ancora = [0, 0]
                self.cur = [len(linhas) - 1, len(linhas[-1])]
            elif k in (pygame.K_c, pygame.K_x):
                txt = self.texto_selecionado() or (linhas[self.cur[0]] + "\n")
                self.clip_por(txt)
                if k == pygame.K_x:
                    self.foto_codigo()
                    if self.tem_selecao():
                        self.apagar_selecao()
                    else:
                        del linhas[self.cur[0]]
                        if not linhas:
                            linhas.append("")
                        self.cur = [min(self.cur[0], len(linhas) - 1), 0]
                    self.salvar_codigo()
                self.cod_msg = "Copiado."
            elif k == pygame.K_v:
                txt = self.clip_pegar()
                if txt:
                    self.foto_codigo()
                    self.inserir_texto(txt.replace("\t", "    "))
                    self.salvar_codigo()
            elif k == pygame.K_z:
                self.desfazer_codigo()
            elif k == pygame.K_y:
                self.refazer_codigo()
            elif k == pygame.K_d:
                self.foto_codigo()
                l = self.cur[0]
                linhas.insert(l + 1, linhas[l])
                self.cur = [l + 1, self.cur[1]]
                self.salvar_codigo()
            elif k == pygame.K_SLASH or e.unicode in ("/", ";", ":"):
                self.comentar_linhas()
                self.salvar_codigo()
            elif k == pygame.K_f:
                self.pedir_texto("Buscar no script", self.texto_selecionado() or self.busca_cod,
                                 lambda txt: (setattr(self, "busca_cod", txt), self.buscar_proximo()))
            self.mostrar_cursor()
            return

        if k == pygame.K_F3:
            self.buscar_proximo()
            return

        movimento = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_HOME, pygame.K_END,
                     pygame.K_PAGEUP, pygame.K_PAGEDOWN}
        if k in movimento:
            if shift:
                if self.ancora is None:
                    self.ancora = list(self.cur)
            elif self.tem_selecao() and k in (pygame.K_LEFT, pygame.K_RIGHT):
                (a, b) = self.faixa()
                self.cur = list(a if k == pygame.K_LEFT else b)
                self.ancora = None
                self.mostrar_cursor()
                return
            else:
                self.ancora = None
            l, c = self.cur
            if k == pygame.K_LEFT:
                if c > 0:
                    c -= 1
                elif l > 0:
                    l -= 1
                    c = len(linhas[l])
            elif k == pygame.K_RIGHT:
                if c < len(linhas[l]):
                    c += 1
                elif l < len(linhas) - 1:
                    l, c = l + 1, 0
            elif k == pygame.K_UP and l > 0:
                l -= 1
                c = min(c, len(linhas[l]))
            elif k == pygame.K_DOWN and l < len(linhas) - 1:
                l += 1
                c = min(c, len(linhas[l]))
            elif k == pygame.K_HOME:
                ind = len(linhas[l]) - len(linhas[l].lstrip(" "))
                c = ind if c != ind else 0
            elif k == pygame.K_END:
                c = len(linhas[l])
            elif k == pygame.K_PAGEUP:
                l = max(0, l - self.linhas_visiveis())
                c = min(c, len(linhas[l]))
            elif k == pygame.K_PAGEDOWN:
                l = min(len(linhas) - 1, l + self.linhas_visiveis())
                c = min(c, len(linhas[l]))
            self.cur = [l, c]
            self.auto = None
            self.mostrar_cursor()
            return

        mudou = False
        if k in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.foto_codigo()
            if self.tem_selecao():
                self.apagar_selecao()
            l, c = self.cur
            antes = linhas[l][:c]
            ind = len(antes) - len(antes.lstrip(" "))
            if antes.rstrip().endswith(":"):
                ind += 4
            self.inserir_texto("\n" + " " * ind)
            mudou = True
        elif k == pygame.K_BACKSPACE:
            self.foto_codigo()
            if self.tem_selecao():
                self.apagar_selecao()
            else:
                l, c = self.cur
                if c > 0:
                    antes = linhas[l][:c]
                    n = c - ((c - 1) // 4) * 4 if antes.strip() == "" and c >= 4 else 1
                    linhas[l] = linhas[l][:c - n] + linhas[l][c:]
                    self.cur = [l, c - n]
                elif l > 0:
                    c = len(linhas[l - 1])
                    linhas[l - 1] += linhas[l]
                    del linhas[l]
                    self.cur = [l - 1, c]
            mudou = True
        elif k == pygame.K_DELETE:
            self.foto_codigo()
            if self.tem_selecao():
                self.apagar_selecao()
            else:
                l, c = self.cur
                if c < len(linhas[l]):
                    linhas[l] = linhas[l][:c] + linhas[l][c + 1:]
                elif l < len(linhas) - 1:
                    linhas[l] += linhas[l + 1]
                    del linhas[l + 1]
            mudou = True
        elif k == pygame.K_TAB:
            if shift or (self.tem_selecao() and self.faixa()[0][0] != self.faixa()[1][0]):
                self.indentar(menos=bool(shift))
            else:
                self.foto_codigo()
                self.inserir_texto(" " * (4 - self.cur[1] % 4))
            mudou = True
        elif e.unicode and e.unicode.isprintable():
            self.foto_codigo("letra")
            self.inserir_texto(e.unicode)
            mudou = True
            if RE_PALAVRA.match(e.unicode) or e.unicode.isdigit():
                self.salvar_codigo()
                self.atualizar_auto()
                self.mostrar_cursor()
                return
        elif k == pygame.K_ESCAPE:
            self.ancora = None
        if mudou:
            self.salvar_codigo()
        self.auto = None
        self.mostrar_cursor()

    def clique_codigo(self, pos):
        self.carregar_codigo()
        for r, nome in self.hits_cod:
            if r.collidepoint(pos):
                if nome == "verificar":
                    self.verificar_codigo()
                elif nome == "exemplo":
                    self.foto_codigo()
                    if any(linha.strip() for linha in self.cod):
                        self.cod += [""] + EXEMPLO_SCRIPT.rstrip("\n").split("\n")
                    else:
                        self.cod = EXEMPLO_SCRIPT.rstrip("\n").split("\n")
                    self.salvar_codigo()
                    self.cod_msg = "Exemplo colocado. Leia os comentários com # e aperte Play!"
                elif nome == "ajuda":
                    self.cod_ajuda = not self.cod_ajuda
                elif nome == "buscar":
                    self.pedir_texto("Buscar no script", self.busca_cod,
                                     lambda txt: (setattr(self, "busca_cod", txt), self.buscar_proximo()))
                return
        if self.auto:
            self.auto = None
        if self.area_cod.collidepoint(pos):
            novo = self.pos_para_cursor(pos)
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if self.ancora is None:
                    self.ancora = list(self.cur)
            else:
                self.ancora = list(novo)
            self.cur = novo
            self.arrastando = ("cod_sel",)

    def pintar_linha(self, t, linha, x, y, suas=None):
        suas = suas if suas is not None else getattr(self, "funcs_usuario", set())
        pintar_codigo(t, self.fc, self.cw, linha, x, y, suas)

    def desenhar_codigo(self, t, mouse):
        self.carregar_codigo()
        if getattr(self, "_cod_funcs_de", None) != self.cod:
            self._cod_funcs_de = list(self.cod)
            self.funcs_usuario = set(re.findall(r"\bfuncao\s+([A-Za-z_À-ÿ][\wÀ-ÿ]*)", "\n".join(self.cod)))
            self.funcs_usuario |= {f.get("nome", "") for f in self.cena.get("funcoes", [])}
        pygame.draw.rect(t, cor_ok(CONFIG["script"]["cores"]["fundo"]), VIEW)
        pygame.draw.rect(t, (34, 36, 43), self.barra_cod)
        t.blit(self.f.render(f"SCRIPT de: {self.nome_alvo()}", True, C_TEXTO), (VIEW.x + 12, VIEW.y + 8))
        self.hits_cod = []
        for i, (nome, rot) in enumerate([("verificar", "Verificar"), ("buscar", "Buscar"), ("exemplo", "Exemplo"),
                                         ("ajuda", "Ajuda")]):
            r = pygame.Rect(VIEW.right - 384 + i * 94, VIEW.y + 4, 88, 26)
            ativo = nome == "ajuda" and self.cod_ajuda
            desenhar_botao(t, self.fp, r, rot, mouse, ativo=ativo, cor=C_VERDE if nome == "verificar" else None)
            self.hits_cod.append((r, nome))

        a = self.area_cod
        t.set_clip(a)
        pygame.draw.rect(t, (27, 28, 34), (a.x, a.y, self.gutter - 6, a.h))
        vis = self.linhas_visiveis()
        self.cod_scroll = max(0, min(self.cod_scroll, max(0, len(self.cod) - 1)))
        faixa = self.faixa() if self.tem_selecao() else None
        x_txt = a.x + self.gutter
        for i in range(vis + 1):
            l = self.cod_scroll + i
            if l >= len(self.cod):
                break
            y = a.y + 4 + i * self.lh
            if self.cod_erro_linha == l + 1:
                pygame.draw.rect(t, (80, 30, 30), (a.x, y - 1, a.w, self.lh))
            elif l == self.cur[0] and not faixa:
                pygame.draw.rect(t, (32, 34, 42), (x_txt - 6, y - 1, a.w, self.lh))
            if faixa and faixa[0][0] <= l <= faixa[1][0]:
                c1 = faixa[0][1] if l == faixa[0][0] else 0
                c2 = faixa[1][1] if l == faixa[1][0] else len(self.cod[l]) + 1
                pygame.draw.rect(t, (45, 75, 130), (x_txt + c1 * self.cw, y - 1, max(4, (c2 - c1) * self.cw), self.lh))
            numero = self.fc.render(str(l + 1), True, (90, 95, 110))
            t.blit(numero, (a.x + self.gutter - 12 - numero.get_width(), y))
            # guias de indentacao
            ind = len(self.cod[l]) - len(self.cod[l].lstrip(" "))
            for g in range(4, ind + 1, 4):
                gx = x_txt + (g - 4) * self.cw + 2
                pygame.draw.line(t, (45, 47, 56), (gx, y), (gx, y + self.lh - 2))
            self.pintar_linha(t, self.cod[l], x_txt, y)
        if not any(linha.strip() for linha in self.cod):
            dica = self.fp.render("Script vazio. Clique em 'Exemplo' para ver como funciona, ou na aba API.",
                                  True, C_TEXTO2)
            t.blit(dica, (x_txt, a.y + 4 + self.lh * 2))
        l, c = self.cur
        cx = x_txt + c * self.cw
        cy = a.y + 4 + (l - self.cod_scroll) * self.lh
        if int(self.tempo * 2) % 2 == 0 and self.cod_scroll <= l < self.cod_scroll + vis:
            pygame.draw.line(t, (255, 255, 255), (cx, cy), (cx, cy + self.lh - 3), 2)

        if self.auto:
            itens = self.auto["itens"]
            larg = max(self.fc.size(s)[0] for s in itens) + 20
            caixa = pygame.Rect(cx, cy + self.lh, larg, len(itens) * 20 + 6)
            if caixa.bottom > a.bottom:
                caixa.y = cy - caixa.h
            pygame.draw.rect(t, (40, 43, 54), caixa, border_radius=4)
            pygame.draw.rect(t, C_DESTAQUE, caixa, 1, border_radius=4)
            for i, s in enumerate(itens):
                r = pygame.Rect(caixa.x + 3, caixa.y + 3 + i * 20, caixa.w - 6, 20)
                if i == self.auto["i"]:
                    pygame.draw.rect(t, C_DESTAQUE, r, border_radius=3)
                t.blit(self.fc.render(s, True, C_TEXTO), (r.x + 6, r.y + 1))

        if self.cod_ajuda:
            corte = AJUDA_SCRIPT.index("@COLUNA")
            colunas = [AJUDA_SCRIPT[:corte], AJUDA_SCRIPT[corte + 1:]]
            altura = max(len(col) for col in colunas) * 17 + 14
            painel = pygame.Rect(a.right - 560, a.y + 6, 552, min(a.h - 12, altura))
            pygame.draw.rect(t, (36, 38, 48), painel, border_radius=6)
            pygame.draw.rect(t, C_DESTAQUE, painel, 1, border_radius=6)
            for ci, coluna in enumerate(colunas):
                for i, linha in enumerate(coluna):
                    titulo = linha.isupper()
                    fonte_ = self.fb if titulo else self.fp
                    cor = C_DESTAQUE if titulo else C_TEXTO
                    t.blit(fonte_.render(linha, True, cor), (painel.x + 10 + ci * 275, painel.y + 7 + i * 17))
        t.set_clip(None)

        b = self.barra_erro
        erro = self.cod_msg.startswith("ERRO")
        pygame.draw.rect(t, (90, 30, 30) if erro else (30, 33, 40), b)
        msg = self.cod_msg or (f"Linha {self.cur[0] + 1}, coluna {self.cur[1] + 1}   |   Tab aceita sugestão   |   "
                               f"Ctrl+/ comenta   |   Ctrl+F busca   |   Ctrl+Z desfaz")
        t.blit(self.fp.render(msg, True, (255, 220, 220) if erro else C_TEXTO2), (b.x + 10, b.y + 6))

    # ----------------- ABA API (documentacao) -----------------
    def inserir_no_script(self, codigo):
        alvo = self.alvo_logica()
        self.guardar()
        atual = alvo.get("script", "") or ""
        alvo["script"] = (atual.rstrip("\n") + "\n\n" if atual.strip() else "") + codigo + "\n"
        self.cod_alvo = None
        self.aba = "script"
        self.avisar(f"Colado no script de {self.nome_alvo()}.")

    def clique_api(self, pos):
        for r, a in self.hits_api:
            if r.collidepoint(pos):
                if a[0] == "cat":
                    self.api_cat = a[1]
                    self.api_scroll = 0
                elif a[0] == "usar":
                    self.inserir_no_script(a[1])
                return

    def desenhar_api(self, t, mouse):
        area = VIEW
        pygame.draw.rect(t, (24, 26, 32), area)
        self.hits_api = []
        # busca
        caixa = pygame.Rect(area.x + 12, area.y + 10, area.w - 24, 30)
        pygame.draw.rect(t, C_CAMPO, caixa, border_radius=6)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 1, border_radius=6)
        piscar = "|" if int(self.tempo * 2) % 2 == 0 else ""
        txt = self.api_busca + piscar if self.api_busca else "Digite para buscar (ex: destruir, tecla, imagem, barra)..."
        t.blit(self.f.render(txt, True, C_TEXTO if self.api_busca else C_TEXTO2), (caixa.x + 10, caixa.y + 6))
        # categorias
        x = area.x + 12
        y = area.y + 48
        for cat in API_CATS:
            img = self.fp.render(cat, True, C_TEXTO)
            r = pygame.Rect(x, y, img.get_width() + 16, 24)
            if r.right > area.right - 10:
                x = area.x + 12
                y += 28
                r = pygame.Rect(x, y, img.get_width() + 16, 24)
            ativo = cat == self.api_cat
            pygame.draw.rect(t, C_DESTAQUE if ativo else (C_BOTAO if r.collidepoint(mouse) else (38, 41, 50)), r,
                             border_radius=12)
            t.blit(img, (r.x + 8, r.y + 4))
            self.hits_api.append((r, ("cat", cat)))
            x = r.right + 6
        topo = y + 34

        busca = self.api_busca.lower().strip()
        itens = [i for i in self.api_itens
                 if (self.api_cat == "Todos" or i["cat"] == self.api_cat)
                 and (not busca or busca in i["titulo"].lower() or busca in i["desc"].lower()
                      or busca in i["exemplo"].lower())]
        lista = pygame.Rect(area.x, topo, area.w, area.bottom - topo)
        t.set_clip(lista)
        api_vis = suave((id(self), "api"), self.api_scroll)
        y = topo + 4 - api_vis
        largura_txt = area.w - 140
        for item in itens:
            linhas_desc = quebrar_texto(item["desc"], self.fp, largura_txt)
            linhas_ex = item["exemplo"].split("\n") if item["exemplo"] else []
            h = 26 + len(linhas_desc) * 17 + (len(linhas_ex) * (self.lh - 2) + 10 if linhas_ex else 0) + 8
            if y + h >= topo and y <= area.bottom:
                bloco = pygame.Rect(area.x + 8, y, area.w - 16, h)
                pygame.draw.rect(t, (34, 37, 45), bloco, border_radius=6)
                cat = self.fpp.render(item["cat"].upper(), True, C_TEXTO2)
                t.blit(cat, (bloco.right - cat.get_width() - 10, y + 7))
                t.blit(self.fc.render(item["titulo"], True, (97, 175, 239)), (bloco.x + 10, y + 5))
                yy = y + 26
                for linha in linhas_desc:
                    t.blit(self.fp.render(linha, True, C_TEXTO), (bloco.x + 10, yy))
                    yy += 17
                if linhas_ex:
                    caixa_ex = pygame.Rect(bloco.x + 10, yy + 3, largura_txt, len(linhas_ex) * (self.lh - 2) + 6)
                    pygame.draw.rect(t, (24, 25, 30), caixa_ex, border_radius=4)
                    for i, linha in enumerate(linhas_ex):
                        self.pintar_linha(t, linha, caixa_ex.x + 6, caixa_ex.y + 3 + i * (self.lh - 2))
                if item["usavel"] and item["exemplo"]:
                    br = pygame.Rect(bloco.right - 92, bloco.bottom - 32, 82, 24)
                    desenhar_botao(t, self.fp, br, "Usar", mouse, cor=C_VERDE)
                    if lista.collidepoint(br.center):
                        self.hits_api.append((br, ("usar", item["exemplo"])))
            y += h + 6
        if not itens:
            t.blit(self.f.render("Nada encontrado.", True, C_TEXTO2), (area.x + 16, topo + 10))
        self.api_total = y + api_vis - topo
        self.api_scroll = max(0, min(self.api_scroll, max(0, self.api_total - lista.h + 20)))
        t.set_clip(None)
        rod = self.fpp.render(f"{len(itens)} resultado(s)  |  'Usar' cola o exemplo no script do objeto "
                              f"selecionado ({self.nome_alvo()})", True, C_TEXTO2)
        t.blit(rod, (area.x + 12, area.bottom - 16))
