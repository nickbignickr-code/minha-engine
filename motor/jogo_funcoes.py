# Minha Engine - jogo_funcoes.py
# as funções prontas da linguagem (escrever, criar, achar...) (métodos do Jogo)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class JogoFuncoes:
    # ----------------- funcoes prontas da linguagem -----------------
    def criar_builtins(self):
        def b_escrever(*args):
            self.escrever(" ".join(texto(a) for a in args))

        def b_dizer(msg, seg=2):
            alvo = self.eu_atual or self.cena_dono
            alvo.fala = texto(msg)
            alvo.fala_t = float(num(seg))

        def b_destruir(obj=None):
            obj = obj if obj is not None else self.eu_atual
            if isinstance(obj, list):
                for o in obj:
                    b_destruir(o)
            elif isinstance(obj, str):
                for o in self.buscar(obj):
                    o.vivo = False
            elif isinstance(obj, ObjJogo):
                obj.vivo = False

        def b_achar(nome):
            lista = self.buscar(nome)
            return lista[0] if lista else None

        def b_aleatorio(a, b):
            a, b = num(a), num(b)
            if isinstance(a, int) and isinstance(b, int):
                return random.randint(min(a, b), max(a, b))
            return random.uniform(a, b)

        def b_distancia(a, b):
            if a is None or b is None:
                return 999999
            return math.hypot((a.x + a.w / 2) - (b.x + b.w / 2), (a.y + a.h / 2) - (b.y + b.h / 2))

        def b_somar_moedas(n=1):
            self.moedas += int(num(n))

        def b_lista_num(args):
            if len(args) == 1 and isinstance(args[0], list):
                args = args[0]
            return [num(a) for a in args]

        def b_adicionar(lista, v):
            lista.append(v)
            return lista

        def b_depois(seg, f):
            if not callable(f):
                raise ErroBrasa("depois(segundos, funcao) precisa de uma função")
            self.agendar(seg, self.eu_atual or self.cena_dono, f)

        def b_lancar(tipo, vx=600, vy=0):
            base = self.eu_atual if isinstance(self.eu_atual, ObjJogo) else None
            return self.lancar(tipo, base, vx, vy)

        def b_hud(id_, msg, x=12, y=40):
            self.hud[texto(id_)] = (texto(msg), num(x), num(y))

        def b_tremer(forca=8, seg=0.5):
            self.tremer(num(forca), num(seg))

        def b_camera(obj):
            if isinstance(obj, str):
                obj = b_achar(obj)
            self.cam_alvo = obj

        def b_fundo(r, g, b_):
            self.cena["fundo"] = [num(r), num(g), num(b_)]

        def b_gravidade(v):
            self.cena["gravidade"] = num(v)

        def b_controles(ativo=True):
            self.controles = verdade(ativo)

        def b_tela_cheia(ativo=True):
            self.pedir_tela = verdade(ativo)

        def b_particulas(x, y, cor=None, qtd=20):
            self.soltar_particulas(num(x), num(y), cor or [255, 210, 80], int(num(qtd)))

        def b_animar(obj, prop, valor, seg=0.5):
            if not isinstance(obj, ObjJogo):
                raise ErroBrasa("animar(objeto, \"propriedade\", valor, segundos)")
            self.animar(obj, texto(prop), num(valor), num(seg))

        def b_flash(obj=None, seg=0.12):
            obj = obj if obj is not None else self.eu_atual
            if isinstance(obj, ObjJogo):
                obj.flash_t = obj.flash_dur = float(num(seg))

        def b_esticar(obj=None):
            obj = obj if obj is not None else self.eu_atual
            if isinstance(obj, ObjJogo):
                obj.squash_t = 0.18

        def b_zoom(v, seg=0.4):
            self.animar_zoom(num(v), num(seg))

        def b_comportamento(obj, nome, ligado=True):
            if isinstance(obj, ObjJogo):
                nome = texto(nome)
                if verdade(ligado):
                    obj.comp_off.discard(nome)
                else:
                    obj.comp_off.add(nome)

        def b_piscar(obj=None, seg=1):
            obj = obj if obj is not None else self.eu_atual
            if isinstance(obj, ObjJogo):
                obj.piscar_t = float(num(seg))

        b = {
            "escrever": b_escrever, "dizer": b_dizer, "destruir": b_destruir,
            "destruir_todos": lambda nome: b_destruir(texto(nome)), "criar": self.criar,
            "achar": b_achar, "achar_todos": self.buscar,
            "tecla": self.segurando, "apertou": self.apertou, "soltou": self.soltou,
            "mouse_x": lambda: limpar(round(self.mouse_mundo[0])),
            "mouse_y": lambda: limpar(round(self.mouse_mundo[1])),
            "mouse_segurado": lambda: self.mouse_seg,
            "aleatorio": b_aleatorio, "distancia": b_distancia,
            "vencer": self.vencer, "perder": self.perder, "reiniciar": self.reiniciar,
            "voltar_inicio": self.respawn, "controles": b_controles, "tela_cheia": b_tela_cheia,
            "ir_fase": self.ir_fase, "proxima_fase": self.proxima_fase, "fase_atual": lambda: self.fase_nome,
            "tocar_som": lambda nome, vol=1: tocar_som(texto(nome), num(vol)),
            "tocar_musica": lambda nome, vol=0.6: tocar_musica(texto(nome), num(vol)),
            "parar_musica": parar_musica, "particulas": b_particulas, "animar": b_animar, "piscar": b_piscar,
            "pausar": self.alternar_pausa, "salvar_jogo": self.salvar_progresso,
            "carregar_jogo": self.carregar_progresso,
            "dano": lambda obj, qtd=1: self.dano(obj, qtd), "curar": lambda obj, qtd=1: self.curar(obj, qtd),
            "congelar": lambda seg=0.06: setattr(self, "congelar_t", float(num(seg))),
            "flash": b_flash, "esticar": b_esticar, "zoom": b_zoom,
            "linha_de_visao": lambda a, b: self.ve(a, b), "comportamento": b_comportamento,
            "no_grupo": lambda obj, g: isinstance(obj, ObjJogo) and texto(g) in obj.grupos,
            "fps": lambda: round(self.fps_med),
            "dialogo": lambda txt, nome="": self.abrir_dialogo(txt, nome),
            "dialogo_aberto": lambda: self.dialogo is not None,
            "texto_flutuante": lambda txt, x, y, cor=None: self.texto_flutuante(txt, num(x), num(y),
                                                                               cor or [255, 255, 255]),
            "escuridao": lambda v: self.cena.__setitem__("escuridao", max(0, min(255, num(v)))),
            "mirar": self.mirar,
            "moedas": lambda: self.moedas, "somar_moedas": b_somar_moedas,
            "dar_item": self.dar_item, "remover_item": self.remover_item,
            "tem_item": lambda n: texto(n) in self.inventario, "inventario": lambda: list(self.inventario),
            "depois": b_depois, "lancar": b_lancar, "hud": b_hud,
            "apagar_hud": lambda id_: self.hud.pop(texto(id_), None),
            "tremer": b_tremer, "camera": b_camera, "fundo": b_fundo, "gravidade": b_gravidade,
            "texto": texto, "numero": num, "abs": lambda v: limpar(abs(num(v))),
            "min": lambda *a: min(b_lista_num(a)), "max": lambda *a: max(b_lista_num(a)),
            "arredondar": lambda v, casas=0: limpar(round(num(v), int(num(casas)))),
            "raiz": lambda v: limpar(math.sqrt(num(v))), "tamanho": lambda v: len(v),
            "adicionar": b_adicionar,
            "maiusculo": lambda t: texto(t).upper(), "minusculo": lambda t: texto(t).lower(),
            "contem": lambda a, b: (b in a) if isinstance(a, list) else (texto(b) in texto(a)),
            "dividir": lambda t, sep=" ": texto(t).split(texto(sep)) if texto(sep) else list(texto(t)),
            "juntar": lambda lista, sep="": texto(sep).join(texto(x) for x in lista),
            "substituir": lambda t, a, b: texto(t).replace(texto(a), texto(b)),
            "remover": lambda lista, v: (lista.remove(v) if v in lista else None) or lista,
            "sortear": lambda lista: random.choice(lista) if lista else None,
            "embaralhar": lambda lista: random.sample(list(lista), len(lista)),
            "inverter": lambda v: v[::-1] if isinstance(v, (list, str)) else v,
            "ordenar": lambda lista: sorted(lista, key=lambda x: (isinstance(x, str), x)),
            "posicao": lambda lista, v: lista.index(v) if v in lista else -1,
            "lista_de": lambda a, b: list(range(int(num(a)), int(num(b)) + 1)),
            "piso": lambda v: int(math.floor(num(v))), "teto": lambda v: int(math.ceil(num(v))),
            "seno": lambda g: math.sin(math.radians(num(g))), "cosseno": lambda g: math.cos(math.radians(num(g))),
            "angulo_ate": lambda a, b: math.degrees(math.atan2((b.y + b.h / 2) - (a.y + a.h / 2),
                                                                (b.x + b.w / 2) - (a.x + a.w / 2))),
            "chamar": lambda nome: self.chamar_funcao(self.eu_atual or self.cena_dono, nome, None),
            "global": self.globais, "player": self.player, "tempo": 0, "dt": 0,
        }
        for nome, (fn, _) in PLUGIN_FUNCOES.items():
            b[nome] = plugin_seguro(nome, fn)
        for nome, f in self.funcoes.items():
            if nome.isidentifier():
                b[nome] = self.funcao_visual(f)
        return b

    def funcao_visual(self, f):
        def chamar(*_):
            dono = self.eu_atual or self.cena_dono
            self.acoes(dono, f.get("acoes", []), None)
        return chamar

    def escrever(self, msg):
        self.log.append((msg, 6.0))
        self.log = self.log[-8:]
        dono = self.eu_atual.brasa_nome() if self.eu_atual is not None else None
        self.saida.append(("msg", str(msg), dono, None))
        if len(self.saida) > 3000:
            del self.saida[:1000]
            self.saida_base += 1000

    def dar_item(self, nome):
        self.inventario.append(texto(nome))
        if "item" not in self.fila_global:
            self.fila_global.append("item")

    def remover_item(self, nome):
        nome = texto(nome)
        if nome in self.inventario:
            self.inventario.remove(nome)

    def buscar(self, nome):
        """Acha objetos vivos pelo NOME (Bloco1) ou pelo TIPO (Inimigo) ou pelo MODELO."""
        nome = texto(nome).strip()
        return [o for o in self.objs + self.novos
                if o.vivo and (o.d.get("nome") == nome or o.tipo == nome or o.d.get("modelo") == nome
                               or nome in o.grupos)]

    def criar(self, nome, x=0, y=0):
        nome = texto(nome)
        if nome in self.modelos_nome:
            d = copy.deepcopy(self.modelos_nome[nome])
        elif nome in MODELOS:
            d = nova_entidade(nome, 0, 0)
        else:
            raise ErroBrasa(f"Não existe objeto, modelo ou tipo chamado '{nome}'")
        d["x"] = num(x)
        d["y"] = num(y)
        o = ObjJogo(d)
        self.novos.append(o)
        return o

    def lancar(self, tipo, base, vx, vy):
        o = self.criar(tipo, 0, 0)
        vx, vy = num(vx), num(vy)
        if base is not None:
            cx, cy = base.x + base.w / 2, base.y + base.h / 2
            if vx > 0:
                o.x = base.x + base.w + 2
            elif vx < 0:
                o.x = base.x - o.w - 2
            else:
                o.x = cx - o.w / 2
            o.y = cy - o.h / 2
        o.base_y = o.y
        o.vx = float(vx)
        o.vy = float(vy)
        o.movel = True
        o.d["solido"] = False
        return o

    def soltar_particulas(self, x, y, cor, qtd=20):
        cor = cor_ok(cor)
        for _ in range(max(0, min(300, qtd))):
            ang = random.uniform(0, math.tau)
            vel = random.uniform(60, 280)
            self.particulas.append([x, y, math.cos(ang) * vel, math.sin(ang) * vel - 120,
                                    random.uniform(0.4, 0.9), cor, random.randint(2, 5), 600.0])
        if len(self.particulas) > 1500:
            self.particulas = self.particulas[-1500:]

    def animar(self, obj, prop, valor, seg):
        if prop in ObjJogo.PROPS:
            ini = getattr(obj, prop)
        else:
            ini = num_seguro(obj.d.get(prop, 0))
        self.tweens = [tw for tw in self.tweens if not (tw[0] is obj and tw[1] == prop)]
        self.tweens.append([obj, prop, float(ini), float(valor), max(0.01, float(seg)), 0.0])

    def abrir_dialogo(self, txt, nome=""):
        linhas = [l.strip() for l in texto(txt).split("|") if l.strip()]
        if linhas:
            self.dialogo = {"linhas": linhas, "i": 0, "chars": 0.0, "nome": texto(nome or "")}

    def atualizar_dialogo(self, dt, apertadas, clique):
        d = self.dialogo
        linha = d["linhas"][d["i"]]
        d["chars"] = min(len(linha), d["chars"] + 45 * dt)
        avancar = clique is not None or bool(apertadas & (set(acao_jogo("acao")) | set(acao_jogo("pular")) |
                                                          {pygame.K_RETURN}))
        if avancar:
            if d["chars"] < len(linha):
                d["chars"] = len(linha)        # mostra a frase inteira de uma vez
            elif d["i"] + 1 < len(d["linhas"]):
                d["i"] += 1
                d["chars"] = 0.0
            else:
                self.dialogo = None
                self.dialogo_cd = 0.35      # evita reabrir na mesma apertada de E
                self.disparar_todos("fim_dialogo")

    def mirar(self, obj, alvo, vel=400):
        if not isinstance(obj, ObjJogo) or not isinstance(alvo, ObjJogo):
            raise ErroBrasa("mirar(objeto, alvo, velocidade) precisa de dois objetos")
        ang = math.atan2((alvo.y + alvo.h / 2) - (obj.y + obj.h / 2), (alvo.x + alvo.w / 2) - (obj.x + obj.w / 2))
        vel = float(num(vel))
        obj.vx, obj.vy = math.cos(ang) * vel, math.sin(ang) * vel
        obj.movel = True
        if "Bala" in obj.comp:
            obj.comp["Bala"]["angulo"] = math.degrees(ang)
            obj.comp["Bala"]["velocidade"] = vel
        return obj

    def texto_flutuante(self, txt, x, y, cor=(255, 255, 255)):
        self.flutuantes.append([float(x), float(y), texto(txt), cor_ok(cor), 0.0])
        if len(self.flutuantes) > 60:
            self.flutuantes = self.flutuantes[-60:]

    def alternar_pausa(self, *_):
        self.pausado = not self.pausado

    def salvar_progresso(self):
        dados = {"fase": self.fase_nome, "moedas": self.moedas, "inventario": self.inventario,
                 "globais": self.globais.d}
        try:
            with open(ARQUIVO_SAVEGAME, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2, default=texto)
            return True
        except OSError as ex:
            raise ErroBrasa(f"Não consegui salvar o progresso: {ex}")

    def carregar_progresso(self):
        try:
            with open(ARQUIVO_SAVEGAME, encoding="utf-8") as f:
                dados = json.load(f)
        except (OSError, ValueError):
            return False
        self.moedas = int(num_seguro(dados.get("moedas", 0)))
        self.inventario = list(dados.get("inventario", []))
        self.globais.d.update(dados.get("globais", {}))
        if dados.get("fase") in self.dados["fases"]:
            self.pedir_fase = dados["fase"]
        return True

    def segurando(self, nome):
        cod = codigo_tecla(nome)
        return bool(cod is not None and self.teclas[cod])

    def apertou(self, nome):
        cod = codigo_tecla(nome)
        return cod is not None and cod in self.apertadas

    def soltou(self, nome):
        cod = codigo_tecla(nome)
        return cod is not None and cod in self.soltas

    def vencer(self):
        self.venceu = True

    def perder(self):
        if not self.venceu:
            if not self.perdeu:
                self.fila_global.append("derrota")
            self.perdeu = True

    def reiniciar(self):
        self.pedir_reinicio = True

    def agendar(self, seg, dono, fn):
        self.agendados.append((self.tempo + float(num(seg)), dono, fn))
