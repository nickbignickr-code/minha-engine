# Minha Engine - jogo_scripts.py
# scripts, eventos visuais e comportamentos (métodos do Jogo)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class JogoScripts:
    # ----------------- scripts e eventos -----------------
    def erro(self, dono, e):
        msg = f"{dono.brasa_nome()}: {e}"
        if msg not in self.erros:
            self.erros.append(msg)
            linha = getattr(e, "linha", None)
            texto_e = getattr(e, "msg", str(e))
            self.saida.append(("erro", texto_e, dono.brasa_nome(), linha))

    def preparar(self, dono):
        dono.escopo = Escopo(self.raiz, {"eu": None if dono.eh_cena else dono, "__quando__": dono.handlers})
        codigo = dono.d.get("script", "") or ""
        if codigo.strip():
            try:
                prog = compilar(codigo)
            except ErroBrasa as e:
                self.erro(dono, e)
                prog = None
            if prog:
                self.rodar(dono, lambda: self.interp.executar(prog, dono.escopo))
        tem_toque = any(h[0] in ("tocar", "parar_tocar") for h in dono.handlers) or any(
            ev.get("gatilho") in ("Ao tocar em", "Ao parar de tocar em") for ev in dono.d.get("eventos", []))
        dono.quer_toque = tem_toque and not dono.eh_cena and not dono.na_tela
        if not dono.eh_cena:
            self.preparar_comportamentos(dono)

    def preparar_comportamentos(self, o):
        o.comp = {}
        for c in o.d.get("comportamentos", []):
            nome = c.get("t")
            spec = COMPORTAMENTOS.get(nome)
            if spec is None or c.get("ativo") is False:
                continue
            vals = {}
            for chave, padrao, tipo in spec:
                bruto = c.get("p", {}).get(chave, padrao)
                if tipo == "e":
                    try:
                        vals[chave] = num(self.valor(bruto, o.escopo))
                    except ErroBrasa as e:
                        self.erro(o, ErroBrasa(f"comportamento {nome}: {e.msg}"))
                        vals[chave] = num_seguro(padrao)
                elif tipo == "sn":
                    vals[chave] = bruto == "Sim"
                else:
                    vals[chave] = str(bruto)
            o.comp[nome] = vals
        if "Vida" in o.comp:     # o comportamento Vida manda na vida inicial e na vida maxima
            o.vars["vida"] = limpar(o.comp["Vida"]["vida"])
            o.vars["vida_max"] = limpar(o.comp["Vida"]["vida"])
        if "Bala" in o.comp or "Perseguir" in o.comp or "8 direções (teclado)" in o.comp:
            o.movel = True
        if "Bala" in o.comp:
            o.d["solido"] = False
            if o.vx or o.vy:   # criado com lancar(): a bala segue a direcao em que foi lancada
                o.comp["Bala"]["angulo"] = math.degrees(math.atan2(o.vy, o.vx))
                o.comp["Bala"]["velocidade"] = math.hypot(o.vx, o.vy)
        if o.comp and any(k in o.comp for k in ("Vida", "Bala", "Dano")):
            o.quer_toque = o.quer_toque or "Vida" in o.comp or "Dano" in o.comp

    def dano(self, o, qtd=1):
        """Tira vida do objeto. Retorna True se levou dano."""
        if not isinstance(o, ObjJogo) or not o.vivo or o.invencivel_t > 0:
            return False
        vida = num_seguro(o.vars.get("vida", 1), 1) - num_seguro(qtd, 1)
        o.vars["vida"] = limpar(vida)
        self.texto_flutuante(f"-{texto(limpar(num_seguro(qtd, 1)))}", o.x + o.w / 2, o.y - 6, (255, 90, 90))
        inv = o.comp.get("Vida", {}).get("invencivel_seg", 1.0) if o.tem("Vida") else 0.6
        o.invencivel_t = inv
        o.piscar_t = inv
        o.flash_t = o.flash_dur = 0.12
        self.congelar_t = max(self.congelar_t, 0.05)
        self.tremer(4, 0.2)
        self.disparar(o, "dano")
        if vida <= 0:
            self.disparar(o, "sem_vida")
            self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, o.d.get("cor", [255, 80, 80]), 24)
            if o is self.player:
                o.vars["vida"] = o.vars.get("vida_max", 3)
                self.respawn()
            else:
                o.vivo = False
        return True

    def curar(self, o, qtd=1):
        if isinstance(o, ObjJogo):
            maximo = num_seguro(o.vars.get("vida_max", 0), 0)
            antes = num_seguro(o.vars.get("vida", 0), 0)
            vida = antes + num_seguro(qtd, 1)
            o.vars["vida"] = limpar(min(vida, maximo) if maximo > 0 else vida)
            if num_seguro(o.vars["vida"], 0) > antes:
                self.disparar(o, "curado")

    def tremer(self, forca, seg):
        if forca >= self.tremor * (self.tremor_t / max(0.01, self.tremor_dur)):
            self.tremor = float(forca)
            self.tremor_t = self.tremor_dur = max(0.01, float(seg))

    def ve(self, a, b, alcance=1e9):
        if a is None or b is None:
            return False
        ax, ay = a.x + a.w / 2, a.y + a.h / 2
        bx, by = b.x + b.w / 2, b.y + b.h / 2
        if math.hypot(bx - ax, by - ay) > alcance:
            return False
        solidos = [o for o in self.objs if o.vivo and o.d.get("solido") and not o.na_tela
                   and min(ax, bx) - 1 <= o.x + o.w and o.x <= max(ax, bx) + 1
                   and min(ay, by) - 1 <= o.y + o.h and o.y <= max(ay, by) + 1]
        return linha_livre(ax, ay, bx, by, solidos, ignorar=(a, b))

    def rodar(self, dono, fn):
        anterior = self.eu_atual
        self.eu_atual = dono
        self.interp.passos = 0
        try:
            fn()
        except ErroBrasa as e:
            self.erro(dono, e)
        except (Retorno, Parar, Continuar):
            pass
        except RecursionError:
            self.erro(dono, ErroBrasa("Função chamando ela mesma vezes demais"))
        finally:
            self.eu_atual = anterior

    def contar_timer(self, dono, chave, seg, dt):
        seg = num(seg)
        if seg <= 0:
            return 0
        t = dono.timers.get(chave, 0.0) + dt
        n = 0
        while t >= seg and n < 10:
            t -= seg
            n += 1
        dono.timers[chave] = t
        return n

    @staticmethod
    def combina(alvo, outro):
        alvo = texto(alvo).strip()
        return outro is not None and (alvo == outro.tipo or alvo == outro.d.get("nome")
                                      or alvo == outro.d.get("modelo") or alvo in getattr(outro, "grupos", ()))

    def passa_filtro(self, evento, arg, outro):
        if evento == "tecla":
            return self.apertou(arg)
        if evento == "soltar":
            return self.soltou(arg)
        if evento in ("tocar", "parar_tocar"):
            return self.combina(arg, outro)
        return True

    @staticmethod
    def ouvidos(dono):
        """Eventos que o objeto escuta (calculado uma vez; refeito se o script registrar outro 'quando')."""
        if dono.ouve is None or dono.n_handlers != len(dono.handlers):
            dono.n_handlers = len(dono.handlers)
            dono.ouve = {h[0] for h in dono.handlers} | {
                GATILHO_EVENTO.get(ev.get("gatilho")) for ev in dono.d.get("eventos", []) if ev.get("ativo") is not False}
        return dono.ouve

    def disparar(self, dono, evento, outro=None, dt=0.0):
        if evento not in self.ouvidos(dono):
            return
        for i, (ev, arg, corpo, esc) in enumerate(list(dono.handlers)):
            if ev != evento or not self.passa_filtro(evento, arg, outro):
                continue
            vezes = 1
            if evento == "cada":
                try:
                    vezes = self.contar_timer(dono, ("s", i), arg, dt)
                except ErroBrasa as e:
                    self.erro(dono, e)
                    continue
            for _ in range(vezes):
                local = Escopo(esc, {"outro": outro})
                self.rodar(dono, lambda c=corpo, l=local: self.interp.executar(c, l))

        for i, ev in enumerate(dono.d.get("eventos", [])):
            if GATILHO_EVENTO.get(ev.get("gatilho")) != evento or ev.get("ativo") is False:
                continue
            gp = ev.get("gp", {})
            arg = gp.get("tecla", gp.get("alvo", ""))
            if not self.passa_filtro(evento, arg, outro):
                continue
            vezes = 1
            if evento == "cada":
                try:
                    seg = self.valor(gp.get("seg", "1"), dono.escopo)
                    vezes = self.contar_timer(dono, ("v", i), seg, dt)
                except ErroBrasa as e:
                    self.erro(dono, e)
                    continue
            for _ in range(vezes):
                self.rodar_visual(dono, ev, outro)

    def disparar_todos(self, evento):
        for d in list(self.donos):
            self.disparar(d, evento)

    def valor(self, txt, esc):
        s = str(txt).strip()
        no = self.cache_expr.get(s)
        try:
            if no is None:
                no = compilar_expr(s)
                self.cache_expr[s] = no
            return self.interp.avaliar(no, esc or self.raiz)
        except ErroBrasa as e:
            raise ErroBrasa(f"no valor '{s}': {e.msg}")
        except ZeroDivisionError:
            raise ErroBrasa(f"no valor '{s}': divisão por zero")
        except (TypeError, ValueError, IndexError, KeyError, AttributeError) as ex:
            raise ErroBrasa(f"no valor '{s}': {ex}")

    def interpolar(self, s, esc):
        return re.sub(r"\{([^{}]+)\}", lambda m: texto(self.valor(m.group(1), esc)), str(s))

    def rodar_visual(self, dono, ev, outro):
        def fn():
            local = Escopo(dono.escopo or self.raiz, {"outro": outro})
            for c in ev.get("condicoes", []):
                if not self.condicao(dono, c, local):
                    return
            self.acoes(dono, ev.get("acoes", []), local)
        self.rodar(dono, fn)

    def condicao(self, dono, c, esc):
        r = bool(self.testar(dono, c, esc))
        return (not r) if c.get("nao") else r

    def mouse_em_cima(self, o):
        mx, my = self.mouse_tela if o.na_tela else self.mouse_mundo
        return o.x <= mx <= o.x + o.w and o.y <= my <= o.y + o.h

    def testar(self, dono, c, esc):
        t = c.get("t")
        p = c.get("p", {})
        corpo = dono if isinstance(dono, ObjJogo) else None
        val = lambda nome, padrao="0": self.valor(p.get(nome, padrao), esc)
        op = p.get("op", "==")
        if t == "Tecla segurada":
            return self.segurando(p.get("tecla", ""))
        if t == "Botão do mouse segurado":
            return self.mouse_seg
        if t == "Mouse em cima do objeto":
            return bool(corpo and self.mouse_em_cima(corpo))
        if t == "Está no chão":
            return bool(corpo and corpo.chao)
        if t == "Tocando em":
            return bool(corpo and any(o is not corpo and encostando(corpo, o) for o in self.buscar(p.get("alvo", ""))))
        if t == "Objeto existe":
            return len(self.buscar(p.get("objeto", ""))) > 0
        if t == "Quantidade de objetos":
            return comparar(len(self.buscar(p.get("objeto", ""))), op, val("valor"))
        if t == "Distância até objeto":
            alvos = [o for o in self.buscar(p.get("objeto", "")) if o is not corpo]
            if not corpo or not alvos:
                return False
            menor = min(math.hypot((corpo.x + corpo.w / 2) - (o.x + o.w / 2), (corpo.y + corpo.h / 2) - (o.y + o.h / 2))
                        for o in alvos)
            return comparar(menor, op, val("valor"))
        if t == "Posição X":
            return bool(corpo) and comparar(corpo.x, op, val("valor"))
        if t == "Posição Y":
            return bool(corpo) and comparar(corpo.y, op, val("valor"))
        if t == "Está visível":
            return bool(corpo and corpo.visivel)
        if t == "Tem item":
            return p.get("item", "") in self.inventario
        if t == "Fase atual é":
            return p.get("fase", "") == self.fase_nome
        if t == "Existe progresso salvo":
            return os.path.isfile(ARQUIVO_SAVEGAME)
        if t == "Vida do objeto":
            return bool(corpo) and comparar(corpo.vars.get("vida", 0), op, val("valor"))
        if t == "Vê o objeto (linha de visão)":
            alvos = [o for o in self.buscar(p.get("objeto", "")) if o is not corpo]
            alcance = num(val("alcance", "500"))
            return bool(corpo) and any(self.ve(corpo, o, alcance) for o in alvos)
        if t == "Está no grupo":
            return bool(corpo) and p.get("grupo", "") in corpo.grupos
        if t == "Tem comportamento ligado":
            return bool(corpo) and corpo.tem(p.get("comportamento", ""))
        if t == "Diálogo aberto":
            return self.dialogo is not None
        if t == "Variável do objeto":
            return comparar(dono.vars.get(p.get("var", ""), 0), op, val("valor"))
        if t == "Variável de outro objeto":
            alvos = self.buscar(p.get("objeto", ""))
            return bool(alvos) and comparar(alvos[0].vars.get(p.get("var", ""), 0), op, val("valor"))
        if t == "Variável global":
            return comparar(self.globais.d.get(p.get("var", ""), 0), op, val("valor"))
        if t == "Moedas":
            return comparar(self.moedas, op, val("valor"))
        if t == "Tempo de jogo (seg)":
            return comparar(self.tempo, op, val("valor"))
        if t == "Comparar valores":
            return comparar(val("a"), op, val("b"))
        if t == "Chance (%)":
            return random.random() * 100 < num(val("chance", "50"))
        if t == "Expressão":
            return verdade(val("expr", "verdadeiro"))
        r = self.testar_extra(dono, corpo, t, p, val, op, esc)
        return True if r is None else r

    def acoes(self, dono, lista, esc):
        esc = esc or dono.escopo or self.raiz
        corpo = dono if isinstance(dono, ObjJogo) else None
        for i, a in enumerate(lista):
            t = a.get("t")
            p = a.get("p", {})
            v = lambda nome, padrao="0": self.valor(p.get(nome, padrao), esc)
            sim = lambda nome: p.get(nome, "Sim") == "Sim"
            alvos = lambda: self.buscar(p.get("objeto", ""))

            if t == "Esperar (segundos)":
                resto = lista[i + 1:]
                if resto:
                    self.agendar(v("seg", "1"), dono, lambda r=resto, e=esc: self.acoes(dono, r, e))
                return

            # ----- este objeto -----
            if t == "Mover" and corpo:
                corpo.x += num(v("dx"))
                corpo.y += num(v("dy"))
                corpo.base_y = corpo.y
            elif t == "Ir para" and corpo:
                corpo.x = float(num(v("x")))
                corpo.y = float(num(v("y")))
                corpo.base_y = corpo.y
            elif t == "Ir até objeto" and corpo:
                lista_alvos = [o for o in alvos() if o is not corpo]
                if lista_alvos:
                    o = lista_alvos[0]
                    corpo.x = o.x + o.w / 2 - corpo.w / 2
                    corpo.y = o.y + o.h - corpo.h
                    corpo.base_y = corpo.y
                    corpo.vx = corpo.vy = 0.0
            elif t == "Velocidade X" and corpo:
                corpo.vx = float(num(v("v")))
                corpo.movel = True
            elif t == "Velocidade Y (pulo)" and corpo:
                corpo.vy = float(num(v("v")))
                corpo.movel = True
            elif t == "Pular (se no chão)" and corpo:
                if corpo.chao:
                    corpo.vy = -float(num(v("forca", "700")))
                    corpo.movel = True
            elif t == "Empurrar" and corpo:
                corpo.vx += float(num(v("fx")))
                corpo.vy += float(num(v("fy")))
                corpo.movel = True
            elif t == "Parar movimento" and corpo:
                corpo.vx = corpo.vy = 0.0
            elif t == "Seguir objeto" and corpo:
                lista_alvos = [o for o in alvos() if o is not corpo]
                if lista_alvos:
                    o = lista_alvos[0]
                    dx = (o.x + o.w / 2) - (corpo.x + corpo.w / 2)
                    dy = (o.y + o.h / 2) - (corpo.y + corpo.h / 2)
                    dist = math.hypot(dx, dy) or 1
                    vel = float(num(v("velocidade", "120")))
                    corpo.vx = dx / dist * vel
                    if not corpo.d.get("gravidade"):
                        corpo.vy = dy / dist * vel
                    corpo.movel = True
            elif t == "Mudar tamanho" and corpo:
                corpo.w = max(1.0, float(num(v("w", "40"))))
                corpo.h = max(1.0, float(num(v("h", "40"))))
            elif t == "Mudar cor":
                dono.d["cor"] = [num(v("r")), num(v("g")), num(v("b"))]
            elif t == "Mudar imagem":
                dono.d["imagem"] = p.get("imagem", "")
            elif t == "Mudar texto":
                dono.d["texto"] = p.get("texto", "")
            elif t == "Mudar opacidade":
                dono.d["opacidade"] = num(v("valor", "255"))
            elif t == "Girar":
                dono.d["rotacao"] = num_seguro(dono.d.get("rotacao", 0)) + num(v("graus", "15"))
            elif t == "Espelhar":
                dono.d["espelhar"] = sim("espelhar")
            elif t == "Mudar animação":
                dono.d["animacao"] = p.get("animacao", "")
            elif t == "Mover suavemente para" and corpo:
                seg = num(v("seg", "1"))
                self.animar(corpo, "x", num(v("x")), seg)
                self.animar(corpo, "y", num(v("y")), seg)
            elif t == "Animar propriedade" and corpo:
                self.animar(corpo, p.get("prop", "opacidade"), num(v("valor")), num(v("seg", "1")))
            elif t == "Piscar" and corpo:
                corpo.piscar_t = float(num(v("seg", "1")))
            elif t == "Partículas":
                px = corpo.x + corpo.w / 2 if corpo else self.cam[0] + self.area.w / self.zoom / 2
                py = corpo.y + corpo.h / 2 if corpo else self.cam[1] + self.area.h / self.zoom / 2
                self.soltar_particulas(px, py, [num(v("r", "255")), num(v("g", "210")), num(v("b", "80"))],
                                       int(num(v("qtd", "20"))))
            elif t == "Esconder" and corpo:
                corpo.visivel = False
            elif t == "Mostrar" and corpo:
                corpo.visivel = True
            elif t == "Ligar/desligar sólido" and corpo:
                corpo.d["solido"] = sim("solido")
            elif t == "Ligar/desligar gravidade" and corpo:
                corpo.d["gravidade"] = sim("gravidade")
                corpo.movel = True
            elif t == "Destruir" and corpo:
                corpo.vivo = False
            elif t == "Destruir depois de" and corpo:
                self.agendar(v("seg", "3"), dono, lambda c=corpo: setattr(c, "vivo", False))
            elif t == "Destruir quem tocou":
                outro = esc.get("outro") if esc.achar("outro") else None
                if isinstance(outro, ObjJogo):
                    outro.vivo = False

            # ----- outros objetos -----
            elif t == "Destruir objeto":
                for o in alvos():
                    o.vivo = False
            elif t == "Mover objeto":
                dx, dy = num(v("dx")), num(v("dy"))
                for o in alvos():
                    o.x += dx
                    o.y += dy
                    o.base_y = o.y
            elif t == "Teleportar objeto":
                x, y = float(num(v("x"))), float(num(v("y")))
                for o in alvos():
                    o.x, o.y = x, y
                    o.base_y = y
            elif t == "Velocidade do objeto":
                vx, vy = float(num(v("vx"))), float(num(v("vy")))
                for o in alvos():
                    o.vx, o.vy = vx, vy
                    o.movel = True
            elif t == "Mudar cor do objeto":
                cor = [num(v("r")), num(v("g")), num(v("b"))]
                for o in alvos():
                    o.d["cor"] = list(cor)
            elif t == "Mudar texto do objeto":
                for o in alvos():
                    o.d["texto"] = p.get("texto", "")
            elif t == "Mudar imagem do objeto":
                for o in alvos():
                    o.d["imagem"] = p.get("imagem", "")
            elif t == "Esconder objeto":
                for o in alvos():
                    o.visivel = False
            elif t == "Mostrar objeto":
                for o in alvos():
                    o.visivel = True
            elif t == "Sólido no objeto":
                for o in alvos():
                    o.d["solido"] = sim("solido")
            elif t == "Variável de outro objeto":
                nome = p.get("var", "")
                valor = v("valor")
                for o in alvos():
                    o.vars[nome] = aplicar_op(p.get("op", "="), o.vars.get(nome, 0), valor)

            # ----- criar -----
            elif t == "Criar objeto":
                bx = corpo.x if corpo else 0
                by = corpo.y if corpo else 0
                self.criar(p.get("tipo", "Moeda"), bx + num(v("dx")), by + num(v("dy")))
            elif t == "Criar objeto em":
                self.criar(p.get("tipo", "Moeda"), v("x"), v("y"))
            elif t == "Lançar objeto (tiro)":
                self.lancar(p.get("tipo", "Moeda"), corpo, v("vx"), v("vy"))

            # ----- variaveis, itens e logica -----
            elif t == "Variável do objeto":
                nome = p.get("var", "")
                dono.vars[nome] = aplicar_op(p.get("op", "="), dono.vars.get(nome, 0), v("valor"))
            elif t == "Variável global":
                nome = p.get("var", "")
                self.globais.d[nome] = aplicar_op(p.get("op", "="), self.globais.d.get(nome, 0), v("valor"))
            elif t == "Dar item":
                self.dar_item(p.get("item", ""))
            elif t == "Remover item":
                self.remover_item(p.get("item", ""))
            elif t == "Chamar função":
                self.chamar_funcao(dono, p.get("nome", ""), esc)
            elif t == "Executar código":
                cod = p.get("codigo", "")
                prog = self.cache_cod.get(cod)
                if prog is None:
                    prog = compilar(cod)
                    self.cache_cod[cod] = prog
                self.interp.executar(prog, esc)

            # ----- textos -----
            elif t == "Mostrar texto":
                dono.fala = self.interpolar(p.get("texto", ""), esc)
                dono.fala_t = float(num(v("seg", "2")))
            elif t == "Texto na tela":
                self.hud[p.get("id", "")] = (self.interpolar(p.get("texto", ""), esc), num(v("x", "12")),
                                             num(v("y", "40")))
            elif t == "Apagar texto da tela":
                self.hud.pop(p.get("id", ""), None)
            elif t == "Escrever no console":
                self.escrever(self.interpolar(p.get("texto", ""), esc))

            # ----- jogo e camera -----
            elif t == "Somar moedas":
                self.moedas += int(num(v("n", "1")))
            elif t == "Ir para fase":
                self.ir_fase(p.get("fase", ""))
            elif t == "Próxima fase":
                self.proxima_fase()
            elif t == "Tocar som":
                tocar_som(p.get("som", ""), num(v("volume", "1")))
            elif t == "Tocar música":
                tocar_musica(p.get("musica", ""))
            elif t == "Parar música":
                parar_musica()
            elif t == "Pausar jogo":
                self.alternar_pausa()
            elif t == "Salvar progresso":
                self.salvar_progresso()
            elif t == "Carregar progresso":
                self.carregar_progresso()
            elif t == "Voltar ao início":
                self.respawn()
            elif t == "Vencer o jogo":
                self.vencer()
            elif t == "Perder o jogo":
                self.perder()
            elif t == "Reiniciar fase":
                self.reiniciar()
            elif t == "Controles do player":
                self.controles = sim("ativo")
            elif t == "Mudar gravidade da cena":
                self.cena["gravidade"] = num(v("valor", "1800"))
            elif t == "Mudar cor do fundo":
                self.cena["fundo"] = [num(v("r")), num(v("g")), num(v("b"))]
            elif t == "Tremer câmera":
                self.tremer(num(v("forca", "8")), num(v("seg", "0.5")))
            elif t == "Câmera seguir objeto":
                lista_alvos = alvos()
                self.cam_alvo = lista_alvos[0] if lista_alvos else None
            elif t == "Zoom da câmera":
                self.animar_zoom(num(v("zoom", "1")), num(v("seg", "0.5")))
            elif t == "Congelar tela (impacto)":
                self.congelar_t = float(num(v("seg", "0.06")))
            elif t == "Flash branco" and corpo:
                corpo.flash_t = corpo.flash_dur = float(num(v("seg", "0.12")))
            elif t == "Esticar (squash)" and corpo:
                corpo.squash_t = 0.18
            elif t == "Dar dano":
                qtd = v("qtd", "1")
                for o in alvos():
                    self.dano(o, qtd)
            elif t == "Curar" and corpo:
                self.curar(corpo, v("qtd", "1"))
            elif t == "Mudar vida" and corpo:
                corpo.vars["vida"] = v("vida", "3")
            elif t == "Ligar comportamento" and corpo:
                corpo.comp_off.discard(p.get("comportamento", ""))
            elif t == "Desligar comportamento" and corpo:
                corpo.comp_off.add(p.get("comportamento", ""))
            elif t == "Mudar ângulo da bala" and corpo and "Bala" in corpo.comp:
                corpo.comp["Bala"]["angulo"] = num(v("angulo", "0"))
            elif t == "Mostrar diálogo":
                self.abrir_dialogo(self.interpolar(p.get("texto", ""), esc), p.get("nome", ""))
            elif t == "Texto flutuante":
                fx = corpo.x + corpo.w / 2 if corpo else self.cam[0] + self.area.w / self.zoom / 2
                fy = corpo.y - 6 if corpo else self.cam[1] + self.area.h / self.zoom / 2
                self.texto_flutuante(self.interpolar(p.get("texto", ""), esc), fx, fy,
                                     [num(v("r", "255")), num(v("g", "255")), num(v("b", "255"))])
            elif t == "Mudar escuridão":
                self.cena["escuridao"] = max(0, min(255, num(v("valor", "200"))))
            else:
                self.acao_extra(dono, corpo, t, p, v, sim, alvos, esc)

    def chamar_funcao(self, dono, nome, esc):
        esc = esc or dono.escopo or self.raiz
        nome = texto(nome)
        lugar = esc.achar(nome)
        if lugar is not None and isinstance(lugar.vars[nome], FuncaoBrasa):
            return lugar.vars[nome]()
        f = self.funcoes.get(nome)
        if f is not None:
            self.acoes(dono, f.get("acoes", []), esc)
            return None
        for o in self.donos:      # funcao escrita no script de OUTRO objeto (ex: botao criado por acao)
            vars_ = getattr(getattr(o, "escopo", None), "vars", None)
            if vars_ and isinstance(vars_.get(nome), FuncaoBrasa):
                return vars_[nome]()
        raise ErroBrasa(f"A função '{nome}' não existe")

    def juntar_novos(self):
        voltas = 0
        while self.novos and voltas < 20:
            voltas += 1
            lista, self.novos = self.novos, []
            for o in lista:
                self.objs.append(o)
                self.donos.append(o)
                self.preparar(o)
                self.disparar(o, "iniciar")
