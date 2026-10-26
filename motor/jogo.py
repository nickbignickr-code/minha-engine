# Minha Engine - jogo.py
# o jogo rodando quando aperta PLAY: começo e a física/update
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class Jogo(JogoFuncoes, JogoScripts, JogoTela, JogoExtras, JogoTopDown):
    def __init__(self, projeto, area, sozinho=False, fase=None):
        self.dados = completar_projeto(copy.deepcopy(projeto))
        self.area = area
        self.sozinho = sozinho
        # ---- coisas que CONTINUAM quando muda de fase ----
        self.moedas = 0
        self.inventario = []
        self.globais = Namespace("global")
        self.erros = []
        self.log = []
        self.saida = []          # tudo que aparece na janela Saida do editor
        self.saida_base = 0
        self.venceu = False
        self.perdeu = False
        self.vitoria_avisada = False
        self.pedir_reinicio = False
        self.pedir_tela = None
        self.pedir_fase = None
        self.pausado = False
        self.teclas = SemTeclas()
        self.apertadas = set()
        self.soltas = set()
        self.mouse_mundo = (-99999.0, -99999.0)
        self.mouse_tela = (-99999.0, -99999.0)
        self.mouse_seg = False
        self.eu_atual = None
        self.interp = Interpretador()
        self.cache_expr = {}
        self.cache_cod = {}
        self.tempo_total = 0.0
        self.transicao_t = 0.0
        self.congelar_t = 0.0
        self.debug = False
        self.fps_med = 60.0
        self.arrastado = None
        self.carregar_fase(fase or self.dados.get("fase_atual") or next(iter(self.dados["fases"])))

    def carregar_fase(self, nome):
        """Monta uma fase do zero. Moedas, itens e variaveis globais continuam."""
        fases = self.dados["fases"]
        if nome not in fases:
            self.erros.append(f"A fase '{nome}' não existe")
            nome = next(iter(fases))
        self.fase_nome = nome
        fase = fases[nome]
        self.cena = copy.deepcopy(fase["cena"])
        objetos = copy.deepcopy(fase["objetos"])
        self.modelos_nome = {d["nome"]: copy.deepcopy(d) for d in objetos}
        for nome_m, m in self.dados["modelos"].items():
            m = copy.deepcopy(m)
            m["modelo"] = nome_m
            self.modelos_nome[nome_m] = m
        self.objs = [ObjJogo(d) for d in objetos]
        self.player = next((o for o in self.objs if o.tipo == "Player"), None)
        self.spawn = (self.player.x, self.player.y) if self.player else (0.0, 0.0)
        self.controles = True
        self.portal_cd = 0.0
        self.tempo = 0.0
        mundo = [o for o in self.objs if not o.na_tela]
        if mundo:
            self.limites = (min(o.x for o in mundo), min(o.y for o in mundo),
                            max(o.x + o.w for o in mundo), max(o.y + o.h for o in mundo))
        else:
            self.limites = (0, 0, self.area.w, self.area.h)
        self.limite = self.limites[3] + 600
        self.cam_alvo = self.player
        self.cam = [0.0, 0.0]
        self.zoom = max(0.1, num_seguro(self.cena.get("zoom_camera", 1.0), 1.0))
        self.look = 0.0
        if self.player:
            self.cam = self.alvo_camera()
        self.tremor = 0.0
        self.tremor_t = 0.0
        self.tremor_dur = 0.5
        self.zoom = max(0.1, num_seguro(self.cena.get("zoom_camera", 1.0), 1.0))
        self.look = 0.0
        self.hud = {}
        self.novos = []
        self.agendados = []
        self.fila_global = []
        self.particulas = []
        self.tweens = []
        self.flutuantes = []
        self.dialogo = None
        self.dialogo_cd = 0.0
        self.funcoes = {f.get("nome", ""): f for f in self.cena.get("funcoes", [])}
        self.cena_dono = CenaDono(self.cena)
        self.raiz = Escopo(vars=self.criar_builtins())
        self.donos = [self.cena_dono] + self.objs
        for d in self.donos:
            self.preparar(d)
        for d in list(self.donos):
            self.disparar(d, "iniciar")
        self.juntar_novos()
        tocar_musica_da_cena(self.cena)
        self.transicao_t = 0.9   # mostra o nome da fase com a logo por um instante

    def ir_fase(self, nome):
        nome = texto(nome)
        if nome not in self.dados["fases"]:
            raise ErroBrasa(f"A fase '{nome}' não existe")
        self.pedir_fase = nome

    def proxima_fase(self):
        nomes = list(self.dados["fases"])
        i = nomes.index(self.fase_nome) if self.fase_nome in nomes else -1
        if i + 1 < len(nomes):
            self.pedir_fase = nomes[i + 1]
        else:
            self.vencer()


    # ----------------- jogo -----------------
    def alvo_camera(self):
        p = self.cam_alvo
        vis_w, vis_h = self.area.w / self.zoom, self.area.h / self.zoom
        return [p.x + p.w / 2 + self.look - vis_w / 2, p.y + p.h / 2 - vis_h / 2]

    def respawn(self):
        p = self.player
        if p:
            p.x, p.y = self.spawn
            p.vx = p.vy = 0.0
            p.apoio = None
            p.piscar_t = 1.0
            if "respawn" not in self.fila_global:
                self.fila_global.append("respawn")

    def atualizar_ui(self):
        for o in self.objs:
            if not o.vivo:
                continue
            if o.tipo in ("Texto", "Botao"):
                bruto = str(o.d.get("texto", ""))
                if "{" in bruto:
                    try:
                        o.texto_atual = self.interpolar(bruto, o.escopo)
                    except ErroBrasa as e:
                        self.erro(o, e)
                        o.texto_atual = bruto
                else:
                    o.texto_atual = None
            elif o.tipo == "Barra":
                try:
                    v = num(self.valor(o.d.get("valor_de", "0") or "0", o.escopo))
                    m = num_seguro(o.d.get("maximo", 100), 100) or 1
                    o.progresso = max(0.0, min(1.0, v / m))
                except ErroBrasa as e:
                    self.erro(o, e)
                    o.progresso = 0.0

    def passo_comportamentos(self, dt, teclas, clique):
        """Roda os comportamentos prontos de todos os objetos."""
        a = self.area
        vis_w, vis_h = a.w / self.zoom, a.h / self.zoom
        clique_mundo = None
        if clique is not None:
            clique_mundo = ((clique[0] - a.x) / self.zoom + self.cam[0], (clique[1] - a.y) / self.zoom + self.cam[1])
        for o in self.objs:
            if not o.vivo or not o.comp:
                continue
            c = o.comp
            liga = lambda nome: nome in c and nome not in o.comp_off
            if liga("Bala"):
                b = c["Bala"]
                ang = math.radians(b["angulo"])
                o.vx = math.cos(ang) * b["velocidade"]
                o.vy = math.sin(ang) * b["velocidade"]
                o.movel = True
            if liga("Senoide (vai e volta)"):
                b = c["Senoide (vai e volta)"]
                if o.sen_base is None:
                    o.sen_base = (o.x, o.y)
                desloc = math.sin(self.tempo * b["vezes_por_seg"] * math.tau) * b["distancia"]
                antes = (o.x, o.y)
                if str(b["eixo"]).lower().startswith("x"):
                    o.x = o.sen_base[0] + desloc
                else:
                    o.y = o.sen_base[1] + desloc
                    o.base_y = o.y
                o.ult_dx, o.ult_dy = o.x - antes[0], o.y - antes[1]
            if liga("Girar sempre"):
                o.d["rotacao"] = (num_seguro(o.d.get("rotacao", 0)) + c["Girar sempre"]["graus_por_seg"] * dt) % 360
            if liga("Perseguir"):
                b = c["Perseguir"]
                alvos = [z for z in self.buscar(b["alvo"]) if z is not o]
                alvo = min(alvos, key=lambda z: (z.x - o.x) ** 2 + (z.y - o.y) ** 2) if alvos else None
                if alvo is not None:
                    dx = (alvo.x + alvo.w / 2) - (o.x + o.w / 2)
                    dy = (alvo.y + alvo.h / 2) - (o.y + o.h / 2)
                    dist = math.hypot(dx, dy) or 1
                    if dist <= b["alcance"]:
                        o.vx = dx / dist * b["velocidade"]
                        if not o.d.get("gravidade") or getattr(self, "topdown", False):
                            o.vy = dy / dist * b["velocidade"]
                        o.td_vet = (dx / dist, dy / dist)
                        if dx and (o.d.get("imagem") or o.d.get("animacao")):
                            o.d["espelhar"] = dx < 0
                    elif o.tipo != "Inimigo":
                        o.vx = 0.0
                        if not o.d.get("gravidade"):
                            o.vy = 0.0
                    o.movel = True
            if liga("8 direções (teclado)") and o is not self.player:
                vel = c["8 direções (teclado)"]["velocidade"]
                hx = (1 if self.segura(teclas, "direita") else 0) - (1 if self.segura(teclas, "esquerda") else 0)
                hy = (1 if self.segura(teclas, "baixo") else 0) - (1 if self.segura(teclas, "cima") else 0)
                norma = math.hypot(hx, hy) or 1
                o.vx, o.vy = hx / norma * vel, hy / norma * vel
                o.movel = True
            if liga("Gerador"):
                b = c["Gerador"]
                o.gerados = [z for z in o.gerados if z.vivo]
                if len(o.gerados) < b["maximo"] and self.contar_timer(o, "__gerador", b["a_cada_seg"], dt):
                    try:
                        novo = self.criar(b["tipo"], 0, 0)
                        novo.x = o.x + o.w / 2 - novo.w / 2
                        novo.y = o.y + o.h / 2 - novo.h / 2
                        novo.base_y = novo.y
                        novo.inicio_x, novo.inicio_y = novo.x, novo.y
                        o.gerados.append(novo)
                    except ErroBrasa as e:
                        self.erro(o, e)
            if liga("Arrastável (mouse)") and clique_mundo is not None and self.arrastado is None:
                mx, my = clique_mundo if not o.na_tela else (clique[0] - a.x, clique[1] - a.y)
                if o.x <= mx <= o.x + o.w and o.y <= my <= o.y + o.h:
                    self.arrastado = (o, mx - o.x, my - o.y)
            if liga("Destruir fora da tela") and not o.na_tela:
                m = c["Destruir fora da tela"]["margem"]
                if (o.x + o.w < self.cam[0] - m or o.x > self.cam[0] + vis_w + m or
                        o.y + o.h < self.cam[1] - m or o.y > self.cam[1] + vis_h + m):
                    o.vivo = False
            if liga("Preso no mapa"):
                x0, y0, x1, y1 = self.limites
                o.x = max(x0, min(o.x, x1 - o.w))
                o.y = max(y0, min(o.y, y1 - o.h))
                if (o.x <= x0 and o.vx < 0) or (o.x + o.w >= x1 and o.vx > 0):
                    o.vx = 0.0      # para de empurrar contra a borda (senao a fisica passa um pouco)
                if (o.y <= y0 and o.vy < 0) or (o.y + o.h >= y1 and o.vy > 0):
                    o.vy = 0.0
            if liga("Emissor de partículas"):
                b = c["Emissor de partículas"]
                self.emitir(o, b, dt, vis_w, vis_h)
            if liga("Sumir aos poucos"):
                b = c["Sumir aos poucos"]
                o.fade_t += dt
                o.d["opacidade"] = max(0, 255 * (1 - o.fade_t / max(0.01, b["seg"])))
                if o.fade_t >= b["seg"] and b["destruir"]:
                    o.vivo = False
            self.comportamentos_extra(o, c, liga, dt)
        if self.arrastado is not None:
            o, offx, offy = self.arrastado
            if not o.vivo or not self.mouse_seg:
                self.arrastado = None
            else:
                mx, my = self.mouse_tela if o.na_tela else self.mouse_mundo
                o.x, o.y = mx - offx, my - offy
                o.vx = o.vy = 0.0
                o.base_y = o.y
                o.sen_base = None

    def emitir(self, o, b, dt, vis_w, vis_h):
        """Solta particulas no estilo escolhido (fogo, fumaca, brilho, chuva, neve)."""
        o.__dict__["emit_acc"] = o.__dict__.get("emit_acc", 0.0) + b["por_seg"] * dt
        n = int(o.emit_acc)
        if n <= 0:
            return
        o.emit_acc -= n
        estilo = str(b["estilo"]).lower()
        cor = cor_ok([b["r"], b["g"], b["b"]])
        cx, cy = o.x + o.w / 2, o.y + o.h / 2
        for _ in range(min(n, 200)):
            if estilo.startswith("chuv"):
                x = self.cam[0] + random.uniform(-40, vis_w + 40)
                pt = [x, self.cam[1] - 20, -60.0, random.uniform(700, 900), 1.6, (150, 180, 255), 2, 300.0]
            elif estilo.startswith("nev"):
                x = self.cam[0] + random.uniform(-40, vis_w + 40)
                pt = [x, self.cam[1] - 20, random.uniform(-30, 30), random.uniform(40, 90), 9.0, (245, 245, 255),
                      random.randint(2, 4), 0.0]
            elif estilo.startswith("fum"):
                pt = [cx + random.uniform(-o.w / 3, o.w / 3), o.y, random.uniform(-15, 15), random.uniform(-60, -30),
                      random.uniform(1.2, 2.0), (120, 120, 130), random.randint(5, 9), -10.0]
            elif estilo.startswith("bri"):
                pt = [cx + random.uniform(-o.w, o.w), cy + random.uniform(-o.h, o.h), 0.0, -15.0,
                      random.uniform(0.3, 0.7), cor, random.randint(2, 3), 0.0]
            else:   # fogo
                pt = [cx + random.uniform(-o.w / 3, o.w / 3), o.y + o.h * 0.6, random.uniform(-25, 25),
                      random.uniform(-160, -80), random.uniform(0.3, 0.7),
                      random.choice([cor, (255, 200, 60), (255, 90, 30)]), random.randint(3, 6), -200.0]
            self.particulas.append(pt)
        if len(self.particulas) > 1500:
            self.particulas = self.particulas[-1500:]

    def animar_zoom(self, valor, seg):
        self.zoom_tween = [self.zoom, max(0.1, float(valor)), max(0.01, float(seg)), 0.0]

    @staticmethod
    def segura(teclas, acao):
        return any(teclas[c] for c in acao_jogo(acao))

    def quer_reiniciar(self, tecla):
        return tecla in acao_jogo("reiniciar")

    def controlar_player(self, p, dt, teclas, apertadas, parado, topdown):
        """Movimento do player com aceleracao, coyote time, buffer de pulo, pulo variavel e pulo duplo."""
        if parado or not self.controles:
            if parado:
                p.vx = 0.0
                if topdown:
                    p.vy = 0.0
            return
        esq = self.segura(teclas, "esquerda")
        dir_ = self.segura(teclas, "direita")
        direcao = (1 if dir_ else 0) - (1 if esq else 0)
        vel = float(num_seguro(p.d.get("velocidade", 320), 320))
        acel = float(num_seguro(p.d.get("aceleracao", 0), 0))
        chao_mat = p.apoio.d.get("material") if (p.apoio is not None and p.chao) else None
        if chao_mat == "Gelo":       # escorrega
            acel = 450.0
        elif chao_mat == "Areia":    # deixa lento
            vel *= 0.55

        def aproximar(atual, alvo, passo):
            if acel <= 0:
                return alvo
            if atual < alvo:
                return min(alvo, atual + passo)
            return max(alvo, atual - passo)

        self.controles_extra(p, dt, teclas, apertadas, direcao)
        em_dash = getattr(p, "dash_t", 0) > 0
        if topdown:
            vert = (1 if self.segura(teclas, "baixo") else 0) - (1 if self.segura(teclas, "cima") else 0)
            norm = math.hypot(direcao, vert) or 1
            vel *= getattr(p, "lento", 1.0)        # agua rasa, lama... (comportamento Chao lento)
            p.lento = 1.0
            self.controles_topdown(p, dt, apertadas, direcao, vert)
            if not em_dash:
                p.vx = aproximar(p.vx, direcao / norm * vel, acel * dt)
                p.vy = aproximar(p.vy, vert / norm * vel, acel * dt)
            p.movel = True
        else:
            self.controles_plataforma(p, dt, apertadas)
            controle_ar = 1.0 if p.chao else 0.65
            if not em_dash:
                p.vx = aproximar(p.vx, direcao * vel, acel * controle_ar * dt)
            teclas_pulo = set(acao_jogo("pular"))
            apertou_pulo = bool(apertadas & teclas_pulo)
            forca = float(num_seguro(p.d.get("pulo", 720), 720))
            if p.chao:
                p.coyote = 0.1
                p.pulos_restantes = int(num_seguro(p.d.get("pulos_extras", 0)))
            else:
                p.coyote = max(0.0, p.coyote - dt)
            p.buffer_pulo = 0.12 if apertou_pulo else max(0.0, p.buffer_pulo - dt)
            if p.buffer_pulo > 0 and (p.chao or p.coyote > 0):
                p.vy = -forca
                p.buffer_pulo = p.coyote = 0.0
                p.chao = False
                self.disparar(p, "pulo")
            elif apertou_pulo and not p.chao and p.pulos_restantes > 0:
                p.vy = -forca * 0.9
                p.pulos_restantes -= 1
                p.buffer_pulo = 0.0
                self.disparar(p, "pulo")
                self.soltar_particulas(p.x + p.w / 2, p.y + p.h, [230, 230, 255], 8)
            segurando_pulo = any(teclas[k] for k in teclas_pulo)
            if p.d.get("pulo_variavel") and p.vy < 0 and not segurando_pulo:
                p.vy *= 0.55 if (self.soltas & teclas_pulo) else 1.0
        if direcao and (p.d.get("imagem") or p.d.get("animacao") or p.d.get("anim_andando")):
            p.d["espelhar"] = direcao < 0   # vira a imagem do player pro lado que anda

    def atualizar_efeitos(self, dt):
        for pt in self.particulas:
            pt[0] += pt[2] * dt
            pt[1] += pt[3] * dt
            pt[3] += pt[7] * dt
            pt[4] -= dt
        self.particulas = [pt for pt in self.particulas if pt[4] > 0]
        for ft in self.flutuantes:
            ft[4] += dt
            ft[1] -= 45 * dt
        self.flutuantes = [ft for ft in self.flutuantes if ft[4] < 0.9]
        for tw in self.tweens:
            obj, prop, ini, fim, dur, _ = tw
            tw[5] += dt
            k = min(1.0, tw[5] / dur)
            k = k * k * (3 - 2 * k)  # suave no comeco e no fim
            v = ini + (fim - ini) * k
            if prop in ObjJogo.PROPS:
                setattr(obj, prop, v)
                if prop == "y":
                    obj.base_y = v
            else:
                obj.d[prop] = v
        self.tweens = [tw for tw in self.tweens if tw[5] < tw[4] and tw[0].vivo]
        for o in self.objs:
            if o.piscar_t > 0:
                o.piscar_t -= dt
            if o.flash_t > 0:
                o.flash_t -= dt
            if o.squash_t > 0:
                o.squash_t -= dt
            if o.invencivel_t > 0:
                o.invencivel_t -= dt
        zt = getattr(self, "zoom_tween", None)
        if zt:
            zt[3] += dt
            k = min(1.0, zt[3] / zt[2])
            k = k * k * (3 - 2 * k)
            centro = (self.cam[0] + self.area.w / self.zoom / 2, self.cam[1] + self.area.h / self.zoom / 2)
            self.zoom = zt[0] + (zt[1] - zt[0]) * k
            self.cam[0] = centro[0] - self.area.w / self.zoom / 2
            self.cam[1] = centro[1] - self.area.h / self.zoom / 2
            if k >= 1:
                self.zoom_tween = None

    def update(self, dt, teclas, apertadas, soltas=None, mouse=None, clique=None, mouse_seg=False):
        """mouse e clique vem em coordenadas da TELA."""
        self.teclas = teclas
        self.apertadas = apertadas
        self.soltas = soltas or set()
        a = self.area
        if mouse is not None:
            self.mouse_mundo = ((mouse[0] - a.x) / self.zoom + self.cam[0], (mouse[1] - a.y) / self.zoom + self.cam[1])
            self.mouse_tela = (mouse[0] - a.x, mouse[1] - a.y)
        self.mouse_seg = bool(mouse_seg)
        if apertadas & set(acao_jogo("pausa")) and not (self.venceu or self.perdeu):
            self.alternar_pausa()
        if apertadas & set(acao_jogo("debug")):
            self.debug = not self.debug
        if dt > 0:
            self.fps_med += (1.0 / dt - self.fps_med) * 0.08
        if self.pausado:
            return
        if self.congelar_t > 0:      # hit stop: o jogo congela por um instante no impacto
            self.congelar_t = max(0.0, self.congelar_t - dt)
            return
        if self.dialogo is not None:  # com a caixa de dialogo aberta o mundo espera
            self.atualizar_dialogo(dt, apertadas, clique)
            return
        dt = self.tempo_do_jogo(dt)
        self.transicao_t = max(0.0, self.transicao_t - dt)
        self.dialogo_cd = max(0.0, self.dialogo_cd - dt)
        self.tempo += dt
        self.tempo_total += dt
        self.raiz.vars["tempo"] = self.tempo
        self.raiz.vars["dt"] = dt
        self.portal_cd = max(0.0, self.portal_cd - dt)
        topdown = bool(self.cena.get("visao_de_cima"))
        self.topdown = ObjJogo.modo_td = topdown
        g = 0.0 if topdown else float(num_seguro(self.cena.get("gravidade", 1800), 1800))
        p = self.player if (self.player and self.player.vivo) else None
        parado = self.venceu or self.perdeu
        if p:
            self.controlar_player(p, dt, teclas, apertadas, parado, topdown)

        # Comportamentos prontos
        for o in self.objs:
            if not o.vivo or o.na_tela:
                continue
            if o.tipo == "Inimigo":
                dist = num_seguro(o.d.get("distancia", 160), 160)
                vel = abs(num_seguro(o.d.get("velocidade", 100), 100))
                if o.x > o.inicio_x + dist:
                    o.vx = -vel
                elif o.x < o.inicio_x:
                    o.vx = vel
            elif o.tipo == "Moeda" and not (o.vx or o.vy):
                o.t += dt
                o.y = o.base_y + math.sin(o.t * 4) * 4
            elif o.tipo == "Plataforma Movel":
                vx = num_seguro(o.d.get("vel_x", 100))
                vy = num_seguro(o.d.get("vel_y", 0))
                dist = num_seguro(o.d.get("distancia", 200), 200)
                vel = math.hypot(vx, vy)
                o.ult_dx = o.ult_dy = 0.0
                if vel > 0 and dist > 0:
                    o.prog += o.dir_plat * vel * dt
                    if o.prog >= dist:
                        o.prog, o.dir_plat = dist, -1
                    elif o.prog <= 0:
                        o.prog, o.dir_plat = 0.0, 1
                    nx = o.inicio_x + vx / vel * o.prog
                    ny = o.inicio_y + vy / vel * o.prog
                    o.ult_dx, o.ult_dy = nx - o.x, ny - o.y
                    o.x, o.y = nx, ny
            elif o.tipo == "NPC" and p:
                o.perto = math.hypot((o.x + o.w / 2) - (p.x + p.w / 2), (o.y + o.h / 2) - (p.y + p.h / 2)) < 90
                if o.perto and apertadas & set(acao_jogo("acao")) and self.dialogo_cd <= 0:
                    try:
                        fala = self.interpolar(o.d.get("fala", ""), o.escopo)
                    except ErroBrasa as e:
                        self.erro(o, e)
                        fala = str(o.d.get("fala", ""))
                    if "|" in fala or len(fala) > 45:
                        self.abrir_dialogo(fala, o.d.get("nome", ""))
                    else:
                        o.fala, o.fala_t = fala, 3.0

        self.passo_comportamentos(dt, teclas, clique)

        # Eventos: frame, teclas, cada, cliques
        clicados = []
        if clique is not None:
            ux, uy = clique[0] - a.x, clique[1] - a.y
            wx, wy = ux / self.zoom + self.cam[0], uy / self.zoom + self.cam[1]
            for o in self.objs:
                if not (o.vivo and o.visivel):
                    continue
                cx, cy = (ux, uy) if o.na_tela else (wx, wy)
                if o.x <= cx <= o.x + o.w and o.y <= cy <= o.y + o.h:
                    clicados.append(o)
        for d in list(self.donos):
            if not d.vivo:
                continue
            ouve = self.ouvidos(d)
            if not ouve:
                continue
            if "frame" in ouve:
                self.disparar(d, "frame")
            if "tecla" in ouve and apertadas:
                self.disparar(d, "tecla")
            if "soltar" in ouve and self.soltas:
                self.disparar(d, "soltar")
            if "cada" in ouve:
                self.disparar(d, "cada", dt=dt)
            if clique is not None:
                if "clique_tela" in ouve:
                    self.disparar(d, "clique_tela")
                if "clique" in ouve and d in clicados:
                    self.disparar(d, "clique")
        self.juntar_novos()

        # Acoes agendadas (Esperar, depois, Destruir depois de)
        if self.agendados:
            prontos = [x for x in self.agendados if x[0] <= self.tempo]
            self.agendados = [x for x in self.agendados if x[0] > self.tempo]
            for _, dono, fn in prontos:
                if dono.vivo:
                    self.rodar(dono, fn)
            self.juntar_novos()

        # Fisica (grade espacial: cada objeto so testa os solidos perto dele)
        solidos = [o for o in self.objs if o.vivo and o.d.get("solido") and not o.na_tela]
        grade = GradeEspacial()
        for sol in solidos:
            grade.por(sol)
        pousaram = []
        for o in self.objs:
            if not o.vivo or o.na_tela or not (o.movel or o.vx or o.vy):
                continue
            if o.tipo == "Plataforma Movel":
                continue
            if o.apoio is not None and o.apoio.vivo:
                o.x += o.apoio.ult_dx
                o.y += o.apoio.ult_dy
            o.parede = 0
            o.bateu_teto = False
            o.teto_obj = None
            if o.d.get("gravidade") and g and not o.tem("Bala"):
                queda = 1.35 if (o is p and o.vy > 0) else 1.0   # cai mais rapido do que sobe
                escala_g = num_seguro(o.d.get("gravidade_escala", 1), 1)
                o.vy = min(o.vy + g * queda * escala_g * dt, 1200.0)
            mx = abs(o.vx * dt) + 4
            my = abs(o.vy * dt) + 4
            perto = [sol for sol in grade.perto(o.x - mx, o.y - my, o.w + 2 * mx, o.h + 2 * my)
                     if sol is not o and sol.vivo]
            bateu = False
            fundo_antes = o.y + o.h
            presos = {id(sol) for sol in perto if sobrepoe(o, sol)}   # ja estava dentro antes de andar
            o.x += o.vx * dt
            for sol in perto:
                if id(sol) in presos or not sobrepoe(o, sol) or sol.tem("Plataforma atravessável"):
                    continue
                if sol.d.get("empurravel") and o.vx != 0:
                    desloc = (o.x + o.w - sol.x) if o.vx > 0 else (o.x - (sol.x + sol.w))
                    sol.x += desloc
                    vizinhos = grade.perto(sol.x, sol.y, sol.w, sol.h)
                    if not any(z is not sol and z is not o and z.vivo and sobrepoe(sol, z) for z in vizinhos):
                        continue
                    sol.x -= desloc
                if o.vx > 0:
                    o.x = sol.x - o.w
                elif o.vx < 0:
                    o.x = sol.x + sol.w
                o.parede = 1 if o.vx > 0 else -1
                o.vx = -o.vx if (o.tipo == "Inimigo" or o.tem("Ricochetear")) else 0.0
                bateu = True
            estava_no_chao = o.chao
            vy_antes = o.vy
            o.chao = False
            o.apoio = None
            o.y += o.vy * dt
            for sol in perto:
                if not sobrepoe(o, sol):
                    continue
                if sol.tem("Plataforma atravessável") and not (o.vy > 0 and fundo_antes <= sol.y + 2):
                    continue
                bateu = True
                if id(sol) in presos and not sol.tem("Plataforma atravessável"):
                    # estava preso dentro: sai pelo lado mais perto (cima, baixo, esquerda ou direita)
                    saidas = [(o.y + o.h - sol.y, "cima"), (sol.y + sol.h - o.y, "baixo"),
                              (o.x + o.w - sol.x, "esq"), (sol.x + sol.w - o.x, "dir")]
                    _, lado = min(saidas)
                    if lado == "cima":
                        o.y = sol.y - o.h
                        o.chao, o.apoio = True, sol
                        o.vy = min(o.vy, 0.0)
                    elif lado == "baixo":
                        o.y = sol.y + sol.h
                        o.vy = max(o.vy, 0.0)
                    elif lado == "esq":
                        o.x = sol.x - o.w
                    else:
                        o.x = sol.x + sol.w
                    continue
                if o.vy > 0:
                    o.y = sol.y - o.h
                    if sol.tipo == "Trampolim":
                        o.vy = -num_seguro(sol.d.get("forca", 1100), 1100)
                        o.squash_t = 0.18
                        continue
                    o.chao = True
                    o.apoio = sol
                    if sol.d.get("material") == "Borracha" and vy_antes > 250:   # quica
                        o.vy = -vy_antes * 0.75
                        o.chao = False
                        continue
                elif o.vy < 0:
                    o.y = sol.y + sol.h
                    o.bateu_teto = True
                    o.teto_obj = sol
                if o.tem("Ricochetear") and abs(vy_antes) > 60:
                    o.vy = -vy_antes * 0.9
                    o.chao = False
                    continue
                o.vy = 0.0
            if o.tipo != "Moeda" or o.vx or o.vy:
                o.base_y = o.y
            if bateu and o.tem("Bala") and o.comp["Bala"].get("some_na_parede", True):
                o.vivo = False
                self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, o.d.get("cor", [255, 255, 255]), 6)
            if o.chao and not estava_no_chao and self.tempo > 0.05:
                pousaram.append(o)
                if o is p and vy_antes > 350 and self.cena.get("esticar_ao_pousar", True):
                    o.squash_t = 0.15
        for o in pousaram:
            self.disparar(o, "pousar")

        # Grade com todos os objetos do mundo (para os toques)
        todos = GradeEspacial()
        for o in self.objs:
            if o.vivo and not o.na_tela:
                todos.por(o)

        # Eventos de toque (tocar = comecou a encostar, parar_tocar = largou) e comportamento Vida
        for d in list(self.objs):
            if not d.quer_toque:
                continue
            agora = {}
            if d.vivo:
                for o in todos.perto(d.x, d.y, d.w, d.h):
                    if o is not d and o.vivo and encostando(d, o):
                        agora[id(o)] = o
                        if id(o) not in d.tocando:
                            self.disparar(d, "tocar", outro=o)
                if d.tem("Vida") and d.invencivel_t <= 0:
                    fonte_dano = d.comp["Vida"].get("dano_de", "")
                    for o in agora.values():
                        if d is p and o.tipo in ("Inimigo", "Espinho", "Lava"):
                            continue   # o player trata esses abaixo (pular em cima do inimigo nao doi)
                        if fonte_dano and self.combina(fonte_dano, o):
                            self.dano(d, 1)
                            if o.tem("Bala"):
                                o.vivo = False
                            break
            if d.vivo and d.tem("Dano"):
                cfg = d.comp["Dano"]
                for o in list(agora.values()):
                    if not o.vivo or not self.combina(cfg.get("em", "Player"), o):
                        continue
                    if o.invencivel_t > 0:
                        if cfg.get("some_ao_acertar"):        # tiro bateu em quem esta piscando: some do mesmo jeito
                            d.vivo = False
                            break
                        continue
                    if self.dano(o, cfg.get("quanto", 1)):
                        forca = num_seguro(cfg.get("empurrar", 350), 350)
                        if forca and o.vivo:
                            lado = -1 if o.x + o.w / 2 < d.x + d.w / 2 else 1
                            o.vx = lado * forca
                            o.vy = -forca * 0.8
                        if cfg.get("some_ao_acertar"):
                            d.vivo = False
                            self.soltar_particulas(d.x + d.w / 2, d.y + d.h / 2, d.d.get("cor", [255, 255, 255]), 8)
                            break
            for chave, o in d.tocando.items():
                if chave not in agora:
                    self.disparar(d, "parar_tocar", outro=o)
            d.tocando = agora
        self.juntar_novos()

        # Toques prontos do player
        if p and p.vivo and not parado:
            com_vida = p.tem("Vida")
            for o in todos.perto(p.x, p.y, p.w, p.h):
                if o is p or not o.vivo or o.na_tela or not sobrepoe(p, o) or "TirosDoPlayer" in o.grupos:
                    continue
                if o.tipo == "Moeda":
                    o.vivo = False
                    self.moedas += int(num_seguro(o.d.get("valor", 1), 1))
                    self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, o.d.get("cor", [255, 210, 50]), 10)
                    if "moeda" not in self.fila_global:
                        self.fila_global.append("moeda")
                elif o.tipo == "Item":
                    o.vivo = False
                    self.dar_item(o.d.get("item", "item"))
                elif o.tipo == "Inimigo":
                    if p.vy > 0 and (p.y + p.h) - o.y < 20 and o.d.get("pode_ser_pisado", True) and \
                            not self.topdown:
                        if o.tem("Vida"):
                            o.invencivel_t = 0
                            self.dano(o, num_seguro(p.d.get("dano", 1), 1))
                        else:
                            o.vivo = False
                            self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, o.d.get("cor", [230, 70, 70]), 18)
                            self.congelar_t = max(self.congelar_t, 0.04)
                        p.vy = -450.0
                        p.squash_t = 0.12
                    elif com_vida:
                        if self.dano(p, num_seguro(o.d.get("dano", 1), 1)):
                            if self.topdown:
                                self.empurrar_topdown(p, o)
                            else:
                                p.vy = -380.0
                                p.vx = -300.0 if p.x + p.w / 2 < o.x + o.w / 2 else 300.0   # empurra pra longe
                                p.x += -6 if p.vx < 0 else 6
                    else:
                        self.respawn()
                        break
                elif o.tipo in ("Espinho", "Lava"):
                    if com_vida:
                        if self.dano(p, num_seguro(o.d.get("dano", 1), 1)):
                            if self.topdown:
                                self.empurrar_topdown(p, o, 420.0)
                            else:
                                p.vy = -520.0
                    else:
                        self.respawn()
                        break
                elif o.tipo == "Bandeira":
                    destino = str(o.d.get("ir_para_fase", "") or "").strip()
                    if destino and destino in self.dados["fases"]:
                        self.pedir_fase = destino
                    else:
                        self.vencer()
                elif o.tipo == "Checkpoint" and not o.ativado:
                    o.ativado = True
                    o.d["cor"] = [60, 220, 90]
                    self.spawn = (o.x + o.w / 2 - p.w / 2, o.y + o.h - p.h)
                    o.fala, o.fala_t = "Checkpoint!", 1.5
                elif o.tipo == "Portal" and self.portal_cd <= 0:
                    destino = [z for z in self.buscar(o.d.get("destino", "")) if z is not o]
                    if destino:
                        z = destino[0]
                        p.x = z.x + z.w / 2 - p.w / 2
                        p.y = z.y + z.h - p.h
                        p.vx = p.vy = 0.0
                        self.portal_cd = 0.8
                        break
            if p.y > self.limite:
                self.respawn()

        self.eventos_extra(dt, p)

        # Eventos globais (moeda, item, respawn, vitoria)
        if self.venceu and not self.vitoria_avisada:
            self.vitoria_avisada = True
            self.fila_global.append("vitoria")
        fila, self.fila_global = self.fila_global, []
        for nome in fila:
            self.disparar_todos(nome)

        # Objetos destruidos: avisa "destruido" e tira do jogo
        for o in self.objs:
            if not o.vivo and not o.avisou_morte:
                o.avisou_morte = True
                self.disparar(o, "destruido")
                self.morte_extra(o)
        self.juntar_novos()

        self.atualizar_ui()
        for d in self.donos:
            if d.fala_t > 0:
                d.fala_t -= dt
        self.log = [(txt, tt - dt) for txt, tt in self.log if tt - dt > 0]
        self.objs = [o for o in self.objs if o.vivo]
        self.donos = [self.cena_dono] + self.objs
        if self.tremor_t > 0:
            self.tremor_t -= dt

        self.atualizar_efeitos(dt)
        if self.cam_alvo is not None and getattr(self.cam_alvo, "vivo", False):
            if self.cam_alvo is self.player and not self.cena.get("visao_de_cima"):
                frente = num_seguro(self.cena.get("olhar_a_frente", 60), 60)
                if abs(self.player.vx) > 30:
                    alvo_look = frente if self.player.vx > 0 else -frente
                    self.look += (alvo_look - self.look) * min(1.0, 2.5 * dt)
            alvo = self.alvo_camera()
            k = min(1.0, 8 * dt)
            self.cam[0] += (alvo[0] - self.cam[0]) * k
            self.cam[1] += (alvo[1] - self.cam[1]) * k
        if self.cena.get("limitar_camera"):
            x0, y0, x1, y1 = self.limites
            vis_w, vis_h = self.area.w / self.zoom, self.area.h / self.zoom
            self.cam[0] = max(x0, min(self.cam[0], x1 - vis_w)) if x1 - x0 > vis_w else x0
            self.cam[1] = max(y0, min(self.cam[1], y1 - vis_h)) if y1 - y0 > vis_h else y0
        if self.pedir_fase:
            nome, self.pedir_fase = self.pedir_fase, None
            self.carregar_fase(nome)
