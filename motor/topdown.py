# Minha Engine - topdown.py
# MODO TOP-DOWN (visão de cima, estilo Zelda/Pokémon): 8 direções, animação por direção, espada,
# tiro e dash para onde olha, objetos de baixo na frente, sombras, e comportamentos/ações/condições novos
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# PROPRIEDADES NOVAS
# =====================================================================
MODELOS["Player"].update({"anim_baixo": "", "anim_cima": "", "anim_lado": "", "espada": False,
                          "alcance_espada": 44, "tecla_espada": "j"})
for _t in ("NPC", "Inimigo"):
    MODELOS[_t].update({"anim_baixo": "", "anim_cima": "", "anim_lado": ""})
ROTULOS.update({"anim_baixo": "Anim. descendo (top-down)", "anim_cima": "Anim. subindo (top-down)",
                "anim_lado": "Anim. de lado (top-down)", "espada": "Espada", "alcance_espada": "Alcance da espada",
                "tecla_espada": "Tecla da espada", "ordenar_por_y": "Ordem por altura",
                "sombras": "Sombras"})
_cena_antiga = cena_padrao


def cena_padrao():
    c = _cena_antiga()
    c.setdefault("ordenar_por_y", True)
    c.setdefault("sombras", True)
    return c


# =====================================================================
# COMPORTAMENTOS NOVOS
# =====================================================================
COMPORTAMENTOS.update({
    "Vagar (anda à toa)": [("velocidade", "70", "e"), ("parar_as_vezes", "Sim", "sn")],
    "Manter distância": [("alvo", "Player", "s"), ("distancia", "220", "e"), ("velocidade", "120", "e")],
    "Quebrável (espada)": [("solta", "Moeda", "s"), ("chance", "50", "e")],
    "Chão lento": [("fator", "0.5", "e")],
})
DESC_COMPORTAMENTOS.update({
    "Vagar (anda à toa)": "Anda para direções aleatórias e para de vez em quando (slime, galinha, aldeão). Bom no "
                          "top-down.",
    "Manter distância": "Chega perto do alvo mas não demais: bom para inimigo que atira (arqueiro, mago).",
    "Quebrável (espada)": "Quebra com um golpe de espada do player e às vezes solta algo (arbusto, vaso, caixote).",
    "Chão lento": "Quem anda por cima fica mais lento (água rasa, lama, areia funda). Deixe o objeto não sólido.",
})
CATEGORIAS_COMPORTAMENTOS.append(("Top-down", ["Vagar (anda à toa)", "Manter distância", "Quebrável (espada)",
                                               "Chão lento", "8 direções (teclado)", "Perseguir", "Fugir de"]))
NOMES_TD = {"Vagar (anda à toa)", "Manter distância", "Chão lento"}

# =====================================================================
# QUANDO, SE e FAÇA novos
# =====================================================================
GATILHOS.update({"Ao atacar com a espada": [], "Ao levar espadada": []})
GATILHO_EVENTO.update({"Ao atacar com a espada": "espada", "Ao levar espadada": "espadada"})
EVENTOS_SCRIPT.update({"espada": False, "espadada": False})
DESC_EVENTOS.update({"espada": "Quando o player dá um golpe de espada.",
                     "espadada": "Quando este objeto é atingido pela espada do player."})
CATEGORIAS_GATILHOS.append(("Top-down", ["Ao atacar com a espada", "Ao levar espadada"]))

DIRECOES = ["baixo", "cima", "esquerda", "direita"]
CONDICOES.update({
    "Olhando para": [("direcao", "baixo", "s")],
    "Modo top-down ligado": [],
})
DESC_CONDICOES.update({"Olhando para": "Para onde o objeto está virado: baixo, cima, esquerda ou direita.",
                       "Modo top-down ligado": "Verdadeiro se a cena está em visão de cima."})
CATEGORIAS_CONDICOES.append(("Top-down", ["Olhando para", "Modo top-down ligado"]))

ACOES.update({
    "Atacar com a espada": [("alcance", "44", "e")],
    "Atirar para onde olha": [("tipo", "Moeda", "s"), ("velocidade", "600", "e")],
    "Virar para a direção": [("direcao", "baixo", "s")],
    "Ligar/desligar top-down": [("ligado", "Sim", "sn")],
})
DESC_ACOES.update({
    "Atacar com a espada": "Golpe na frente do objeto: dá dano em inimigos e quebra coisas 'Quebrável (espada)'.",
    "Atirar para onde olha": "Atira na direção em que o objeto está virado (as 8 direções no top-down).",
    "Virar para a direção": "Vira o objeto para baixo, cima, esquerda ou direita.",
    "Ligar/desligar top-down": "Troca a cena entre plataforma (com gravidade) e visão de cima, na hora.",
})
CATEGORIAS_ACOES.append(("Top-down", ["Atacar com a espada", "Atirar para onde olha", "Virar para a direção",
                                      "Ligar/desligar top-down", "Dash (impulso para frente)"]))
OPCOES_PARAMS.setdefault("direcao", DIRECOES)
OPCOES_PARAMS["comportamento"].extend(n for n in COMPORTAMENTOS if n not in OPCOES_PARAMS["comportamento"])
PROPS_SUGERIDAS.extend(p for p in ("anim_baixo", "anim_cima", "anim_lado", "espada", "alcance_espada")
                       if p not in PROPS_SUGERIDAS)

_VET = {"baixo": (0.0, 1.0), "cima": (0.0, -1.0), "esquerda": (-1.0, 0.0), "direita": (1.0, 0.0)}


def olhar_de(o):
    """Vetor (x, y) para onde o objeto olha. No modo plataforma é só esquerda/direita."""
    v = getattr(o, "td_vet", None)
    if v:
        return v
    return (float(getattr(o, "olhar", 1) or 1), 0.0)


def nome_direcao(v):
    vx, vy = v
    if abs(vy) > abs(vx):
        return "baixo" if vy > 0 else "cima"
    return "direita" if vx >= 0 else "esquerda"


# ---------------------------------------------------------------------
# Animação por direção (ObjJogo)
# ---------------------------------------------------------------------
ObjJogo.modo_td = False
_imagem_antiga = ObjJogo.imagem_atual


def _imagem_atual_td(self, tempo):
    d = self.d
    if ObjJogo.modo_td and (d.get("anim_baixo") or d.get("anim_cima") or d.get("anim_lado")):
        andando = abs(self.vx) > 5 or abs(self.vy) > 5
        if andando and self.tipo != "Player":      # inimigos e NPCs viram para onde andam
            n = math.hypot(self.vx, self.vy) or 1
            self.td_vet = (self.vx / n, self.vy / n)
        lado = nome_direcao(olhar_de(self))
        anim = d.get({"baixo": "anim_baixo", "cima": "anim_cima"}.get(lado, "anim_lado")) or d.get("anim_lado") \
            or d.get("anim_baixo") or d.get("anim_cima")
        d["espelhar"] = lado == "esquerda"
        quadros = [q.strip() for q in str(anim).split(",") if q.strip()]
        if quadros:
            if not andando:
                return quadros[0]
            fps = max(0.1, num_seguro(d.get("fps_anim", 8), 8))
            return quadros[int(tempo * fps) % len(quadros)]
    if ObjJogo.modo_td and self.tipo == "Player":    # no top-down nao existe "pulando"
        anim = d.get("anim_andando") if (abs(self.vx) > 5 or abs(self.vy) > 5) else ""
        quadros = [q.strip() for q in str(anim or d.get("animacao", "") or "").split(",") if q.strip()]
        if not quadros:
            return None
        fps = max(0.1, num_seguro(d.get("fps_anim", 8), 8))
        return quadros[int(tempo * fps) % len(quadros)]
    return _imagem_antiga(self, tempo)


ObjJogo.imagem_atual = _imagem_atual_td


# =====================================================================
# O JOGO NO MODO TOP-DOWN (métodos do Jogo)
# =====================================================================
class JogoTopDown:
    topdown = False
    def controles_topdown(self, p, dt, apertadas, direcao, vert):
        """Chamado todo frame no top-down: guarda para onde o player olha e cuida da espada."""
        if direcao or vert:
            n = math.hypot(direcao, vert) or 1
            p.td_vet = (direcao / n, vert / n)
            if direcao:
                p.olhar = 1 if direcao > 0 else -1
        if getattr(p, "espada_cd", 0) > 0:
            p.espada_cd -= dt
        if p.d.get("espada"):
            tecla = str(p.d.get("tecla_espada", "j") or "j")
            ataque = set(acao_jogo("pular")) - set(acao_jogo("cima"))     # Espaco/botao A (nao a seta pra cima)
            if self.apertou(tecla) or (apertadas & ataque):
                self.golpe_espada(p, num_seguro(p.d.get("alcance_espada", 44), 44))

    def controles_plataforma(self, p, dt, apertadas):
        """No modo plataforma a espada também funciona (tecla da espada, padrão J)."""
        if getattr(p, "espada_cd", 0) > 0:
            p.espada_cd -= dt
        if p.d.get("espada") and self.apertou(str(p.d.get("tecla_espada", "j") or "j")):
            self.golpe_espada(p, num_seguro(p.d.get("alcance_espada", 44), 44))

    def golpe_espada(self, o, alcance=44):
        if getattr(o, "espada_cd", 0) > 0:
            return False
        o.espada_cd = 0.28
        vx, vy = olhar_de(o)
        if not getattr(self, "topdown", False):
            vx, vy = (1.0 if vx >= 0 else -1.0), 0.0
        cx, cy = o.x + o.w / 2, o.y + o.h / 2
        larg = max(o.w, o.h) * 1.1
        if abs(vx) >= abs(vy):
            w, h = alcance, larg
        else:
            w, h = larg, alcance
        gx = cx + vx * (o.w / 2 + alcance / 2) - w / 2
        gy = cy + vy * (o.h / 2 + alcance / 2) - h / 2
        caixa = _Caixa(gx, gy, w, h)
        if not hasattr(self, "golpes"):
            self.golpes = []
        self.golpes.append([gx, gy, w, h, 0.12, vx, vy])
        self.disparar(o, "espada")
        dano = num_seguro(o.d.get("dano", 1), 1)
        acertou = False
        for alvo in list(self.objs) + list(self.novos):
            if alvo is o or not alvo.vivo or alvo.na_tela or not sobrepoe(caixa, alvo):
                continue
            if alvo.tem("Quebrável (espada)"):
                b = alvo.comp["Quebrável (espada)"]
                alvo.vivo = False
                self.soltar_particulas(alvo.x + alvo.w / 2, alvo.y + alvo.h / 2, alvo.d.get("cor", [120, 200, 90]), 14)
                solta = str(b.get("solta", "") or "").strip()
                if solta and random.random() * 100 < num_seguro(b.get("chance", 50), 50):
                    try:
                        self.criar(solta, alvo.x + alvo.w / 2 - 10, alvo.y + alvo.h / 2 - 10)
                    except ErroBrasa as e:
                        self.erro(alvo, e)
                acertou = True
                continue
            inimigo = alvo.tipo == "Inimigo" or "Inimigos" in alvo.grupos
            if not inimigo and not (alvo.tem("Vida") and alvo.tipo not in ("NPC", "Player")):
                continue
            acertou = True
            self.disparar(alvo, "espadada")
            if alvo.tem("Vida"):
                alvo.invencivel_t = 0
                self.dano(alvo, dano)
            else:
                alvo.vivo = False
                self.soltar_particulas(alvo.x + alvo.w / 2, alvo.y + alvo.h / 2, alvo.d.get("cor", [230, 70, 70]), 16)
            alvo.vx += vx * 380
            alvo.vy += vy * 380 if getattr(self, "topdown", False) else -200
            alvo.movel = True
        if acertou:
            self.congelar_t = max(self.congelar_t, 0.04)
        return True

    def empurrar_topdown(self, p, o, forca=320.0):
        dx = (p.x + p.w / 2) - (o.x + o.w / 2)
        dy = (p.y + p.h / 2) - (o.y + o.h / 2)
        n = math.hypot(dx, dy) or 1
        p.vx, p.vy = dx / n * forca, dy / n * forca
        p.x += dx / n * 6
        p.y += dy / n * 6

    def tiro_para_onde_olha(self, o, tipo, vel):
        vx, vy = olhar_de(o)
        if not getattr(self, "topdown", False):
            vx, vy = (1.0 if vx >= 0 else -1.0), 0.0
        tiro = self.atirar(o, tipo, vx * vel, vy * vel)
        if tiro is not None:
            cx, cy = o.x + o.w / 2, o.y + o.h / 2
            tiro.x = cx - tiro.w / 2 + vx * (o.w / 2 + tiro.w / 2 + 2)
            tiro.y = cy - tiro.h / 2 + vy * (o.h / 2 + tiro.h / 2 + 2)
            tiro.base_y = tiro.y
        return tiro

    def comportamentos_td(self, o, c, liga, dt):
        if c.keys().isdisjoint(NOMES_TD):
            return
        if liga("Chão lento"):
            p = self.player
            if p is not None and p.vivo and sobrepoe(p, o):
                p.lento = min(getattr(p, "lento", 1.0), max(0.05, num_seguro(c["Chão lento"]["fator"], 0.5)))
        if liga("Vagar (anda à toa)"):
            b = c["Vagar (anda à toa)"]
            perseguindo = False
            if liga("Perseguir"):
                alvos = [z for z in self.buscar(c["Perseguir"]["alvo"]) if z is not o]
                perseguindo = any(math.hypot(z.x - o.x, z.y - o.y) <= c["Perseguir"]["alcance"] for z in alvos)
            if not perseguindo:
                o.vagar_t = getattr(o, "vagar_t", 0.0) - dt
                if o.vagar_t <= 0 or getattr(o, "parede", 0):
                    o.vagar_t = random.uniform(0.8, 2.2)
                    vel = abs(b["velocidade"])
                    if b["parar_as_vezes"] and random.random() < 0.3:
                        o.vx = o.vy = 0.0
                    else:
                        ang = random.randrange(8) * math.pi / 4
                        o.vx = math.cos(ang) * vel
                        o.vy = math.sin(ang) * vel if (getattr(self, "topdown", False) or not o.d.get("gravidade")) \
                            else o.vy
                    if o.vx and (o.d.get("imagem") or o.d.get("animacao")) and not o.d.get("anim_lado"):
                        o.d["espelhar"] = o.vx < 0
                o.movel = True
        if liga("Manter distância"):
            b = c["Manter distância"]
            alvos = [z for z in self.buscar(b["alvo"]) if z is not o]
            if alvos:
                z = min(alvos, key=lambda a: (a.x - o.x) ** 2 + (a.y - o.y) ** 2)
                dx = (z.x + z.w / 2) - (o.x + o.w / 2)
                dy = (z.y + z.h / 2) - (o.y + o.h / 2)
                dist = math.hypot(dx, dy) or 1
                alvo_d, vel = b["distancia"], abs(b["velocidade"])
                k = 1 if dist > alvo_d + 40 else (-1 if dist < alvo_d - 40 else 0)
                o.vx = dx / dist * vel * k
                if getattr(self, "topdown", False) or not o.d.get("gravidade"):
                    o.vy = dy / dist * vel * k
                o.td_vet = (dx / dist, dy / dist)
                o.olhar = 1 if dx >= 0 else -1
                o.movel = True

    def desenhar_golpes(self, tela, a):
        golpes = getattr(self, "golpes", None)
        if not golpes:
            return
        z = self.zoom
        for g in golpes:
            gx, gy, w, h, t, vx, vy = g
            g[4] -= 1 / 60
            r = pygame.Rect(round((gx - self.cam[0]) * z + a.x), round((gy - self.cam[1]) * z + a.y),
                            max(2, round(w * z)), max(2, round(h * z)))
            sup = pygame.Surface(r.size, pygame.SRCALPHA)
            alfa = int(220 * max(0.0, t / 0.12))
            pygame.draw.ellipse(sup, (255, 255, 255, alfa), sup.get_rect())
            pygame.draw.ellipse(sup, (200, 230, 255, alfa), sup.get_rect().inflate(-r.w // 3, -r.h // 3))
            tela.blit(sup, r.topleft)
        self.golpes = [g for g in golpes if g[4] > 0]

    def desenhar_sombra(self, tela, o, r):
        if o.tipo not in ("Player", "NPC", "Inimigo") and not o.d.get("sombra"):
            return
        w = max(6, int(r.w * 0.8))
        h = max(3, int(r.h * 0.16))
        cache = getattr(self, "_sombras", None)
        if cache is None:
            cache = self._sombras = {}
        sup = cache.get((w, h))
        if sup is None:
            sup = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.ellipse(sup, (0, 0, 0, 80), sup.get_rect())
            cache[(w, h)] = sup
        tela.blit(sup, (r.centerx - w // 2, r.bottom - h // 2 - 1))


class _Caixa:
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h


# ---------------------------------------------------------------------
# liga as funções novas nas antigas (ações, condições e comportamentos)
# ---------------------------------------------------------------------
_acao_extra_antiga = JogoExtras.acao_extra
_testar_extra_antigo = JogoExtras.testar_extra
_comp_extra_antigo = JogoExtras.comportamentos_extra


def _acao_extra_td(self, dono, corpo, t, p, v, sim, alvos, esc):
    if t == "Atacar com a espada":
        if corpo:
            self.golpe_espada(corpo, num(v("alcance", "44")))
        return True
    if t == "Atirar para onde olha":
        if corpo:
            self.tiro_para_onde_olha(corpo, p.get("tipo", "Moeda"), float(num(v("velocidade", "600"))))
        return True
    if t == "Virar para a direção":
        if corpo:
            vet = _VET.get(str(p.get("direcao", "baixo")).strip().lower(), (0.0, 1.0))
            corpo.td_vet = vet
            if vet[0]:
                corpo.olhar = 1 if vet[0] > 0 else -1
                corpo.d["espelhar"] = vet[0] < 0
        return True
    if t == "Ligar/desligar top-down":
        self.cena["visao_de_cima"] = sim("ligado")
        return True
    return _acao_extra_antiga(self, dono, corpo, t, p, v, sim, alvos, esc)


def _testar_extra_td(self, dono, corpo, t, p, val, op, esc):
    if t == "Olhando para":
        return bool(corpo) and nome_direcao(olhar_de(corpo)) == str(p.get("direcao", "baixo")).strip().lower()
    if t == "Modo top-down ligado":
        return bool(self.cena.get("visao_de_cima"))
    return _testar_extra_antigo(self, dono, corpo, t, p, val, op, esc)


def _comp_extra_td(self, o, c, liga, dt):
    _comp_extra_antigo(self, o, c, liga, dt)
    self.comportamentos_td(o, c, liga, dt)


JogoExtras.acao_extra = _acao_extra_td
JogoExtras.testar_extra = _testar_extra_td
JogoExtras.comportamentos_extra = _comp_extra_td


# =====================================================================
# PROJETOS NOVOS: vazio top-down
# =====================================================================
def exemplo_vazio_topdown():
    cena = cena_padrao()
    cena.update({"visao_de_cima": True, "fundo": [70, 130, 70], "olhar_a_frente": 0, "titulo": "Meu jogo top-down"})
    objs = [nova_entidade("Peça", -400, -300, "Chao", w=1600, h=1200, material="Gramado", cor=[90, 170, 90],
                          solido=False, camada=-10, contorno=0)]
    for i, (x, y, w, h) in enumerate([(-400, -300, 1600, 40), (-400, 860, 1600, 40), (-400, -300, 40, 1200),
                                      (1160, -300, 40, 1200)]):
        objs.append(nova_entidade("Bloco", x, y, f"Muro{i + 1}", w=w, h=h, material="Pedra", cor=[120, 120, 130]))
    objs.append(nova_entidade("Player", 360, 280, velocidade=240, gravidade=False, espada=True,
                              comportamentos=[{"t": "Vida", "p": dict(params_padrao(COMPORTAMENTOS["Vida"]),
                                                                       vida="5")}]))
    return {"fases": {"Fase 1": {"cena": cena, "objetos": objs}}, "fase_atual": "Fase 1", "fase_inicial": "Fase 1",
            "modelos": {}}


EXEMPLOS["Projeto vazio (top-down)"] = exemplo_vazio_topdown
