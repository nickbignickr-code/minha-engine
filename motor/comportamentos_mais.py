# Minha Engine - comportamentos_mais.py
# +250 COMPORTAMENTOS prontos (arraste no objeto e pronto, sem programar):
#  - ~130 feitos à mão: movimento, visual, câmera, player, inimigos, física, combate, itens, mecanismos,
#    interface, som e tempo
#  - ~120 REAÇÕES "quando acontece X -> faz Y" (ex: "Ao tocar no player → dar moedas")
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

REG_COMP = {}            # nome -> função(jogo, objeto, params, dt, estado)
CAT_COMP_MAIS = {}       # categoria -> nomes


def novo_comp(nome, cat, desc, params=()):
    """Registra um comportamento novo (usado como decorador)."""
    def deco(fn):
        assert nome not in COMPORTAMENTOS or nome in REG_COMP, nome
        COMPORTAMENTOS[nome] = list(params)
        DESC_COMPORTAMENTOS[nome] = desc
        CAT_COMP_MAIS.setdefault(cat, []).append(nome)
        REG_COMP[nome] = fn
        return fn
    return deco


def _cm_pl(jogo):
    p = jogo.player
    return p if p is not None and p.vivo else None


def _cm_c(o):
    return o.x + o.w / 2, o.y + o.h / 2


def _cm_distancia(a, b):
    ax, ay = _cm_c(a)
    bx, by = _cm_c(b)
    return math.hypot(ax - bx, ay - by)


def _cm_base(o, st):
    if "base" not in st:
        st["base"] = (o.x, o.y)
    return st["base"]


def _cm_mover_para(o, x, y, st, jogo):
    """Move o objeto para (x, y) e guarda o quanto andou (para carregar quem está em cima)."""
    o.ult_dx, o.ult_dy = x - o.x, y - o.y
    o.x, o.y = x, y
    o.base_y = o.y


def _cm_particula(jogo, x, y, cor, vx=0.0, vy=0.0, vida=0.5, tam=4, grav=0.0):
    jogo.particulas.append([x, y, vx, vy, vida, cor_ok(cor), tam, grav])


def _cm_escala(o, st, k):
    """Muda o tamanho mantendo o centro."""
    if "tam0" not in st:
        st["tam0"] = (o.w, o.h)
    w0, h0 = st["tam0"]
    cx, cy = _cm_c(o)
    o.w, o.h = max(2.0, w0 * k), max(2.0, h0 * k)
    o.x, o.y = cx - o.w / 2, cy - o.h / 2


def _cm_hsv(h):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, 0.75, 1.0)
    return [int(r * 255), int(g * 255), int(b * 255)]


def _cm_acima_de(p, o, folga=6):
    return p.apoio is o or (abs((p.y + p.h) - o.y) <= folga and p.x + p.w > o.x and p.x < o.x + o.w and p.vy >= 0)


def _cm_pode(st, chave, seg, agora):
    """Espera entre repetições."""
    if agora - st.get(chave, -1e9) >= seg:
        st[chave] = agora
        return True
    return False


# =====================================================================
# MOVIMENTO
# =====================================================================
@novo_comp("Círculo", "Movimento", "Anda em círculo em volta de onde começou.",
           [("raio", "80", "e"), ("voltas_por_seg", "0.3", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    a = j.tempo * b["voltas_por_seg"] * math.tau
    _cm_mover_para(o, bx + math.cos(a) * b["raio"], by + math.sin(a) * b["raio"], st, j)


@novo_comp("Oito (infinito)", "Movimento", "Desenha um 8 no ar (ótimo para morcegos e fadas).",
           [("largura", "120", "e"), ("altura", "50", "e"), ("vezes_por_seg", "0.25", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    a = j.tempo * b["vezes_por_seg"] * math.tau
    _cm_mover_para(o, bx + math.sin(a) * b["largura"], by + math.sin(2 * a) * b["altura"] / 2, st, j)


@novo_comp("Zigue-zague", "Movimento", "Anda para o lado subindo e descendo em zigue-zague.",
           [("velocidade", "120", "e"), ("altura", "40", "e"), ("vezes_por_seg", "1", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    st["dist"] = st.get("dist", 0.0) + b["velocidade"] * dt
    fase = (j.tempo * b["vezes_por_seg"]) % 1.0
    tri = 4 * abs(fase - 0.5) - 1
    _cm_mover_para(o, bx + st["dist"], by + tri * b["altura"], st, j)


@novo_comp("Espiral", "Movimento", "Gira em volta abrindo cada vez mais (e volta ao começo).",
           [("raio_max", "150", "e"), ("voltas_por_seg", "0.5", "e"), ("seg_para_abrir", "4", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    k = (j.tempo % max(0.1, b["seg_para_abrir"])) / max(0.1, b["seg_para_abrir"])
    a = j.tempo * b["voltas_por_seg"] * math.tau
    _cm_mover_para(o, bx + math.cos(a) * b["raio_max"] * k, by + math.sin(a) * b["raio_max"] * k, st, j)


@novo_comp("Pêndulo", "Movimento", "Balança como um pêndulo pendurado acima de onde começou.",
           [("comprimento", "120", "e"), ("angulo", "50", "e"), ("vezes_por_seg", "0.5", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    ang = math.radians(b["angulo"]) * math.sin(j.tempo * b["vezes_por_seg"] * math.tau)
    px, py = bx, by - b["comprimento"]
    _cm_mover_para(o, px + math.sin(ang) * b["comprimento"], py + math.cos(ang) * b["comprimento"], st, j)
    o.d["rotacao"] = -math.degrees(ang)


@novo_comp("Quicar no lugar", "Movimento", "Fica pulando no lugar como uma bola.",
           [("altura", "60", "e"), ("vezes_por_seg", "1.2", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    _cm_mover_para(o, bx, by - abs(math.sin(j.tempo * b["vezes_por_seg"] * math.pi)) * b["altura"], st, j)


@novo_comp("Flutuar suave", "Movimento", "Flutua devagar para cima, para baixo e um pouco para os lados.",
           [("altura", "10", "e"), ("vezes_por_seg", "0.4", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    a = j.tempo * b["vezes_por_seg"] * math.tau + st.setdefault("fase", random.random() * 6)
    _cm_mover_para(o, bx + math.sin(a * 0.5) * b["altura"] * 0.5, by + math.sin(a) * b["altura"], st, j)


@novo_comp("Tremer sempre", "Movimento", "Fica tremendo (bom para coisas prestes a cair ou com raiva).",
           [("forca", "2", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    f = b["forca"]
    o.x, o.y = bx + random.uniform(-f, f), by + random.uniform(-f, f)


@novo_comp("Ir e voltar até um ponto", "Movimento", "Vai até (dx, dy) e volta, sem parar.",
           [("dx", "200", "e"), ("dy", "0", "e"), ("seg_ida", "2", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    k = (j.tempo / max(0.1, b["seg_ida"])) % 2.0
    k = k if k <= 1 else 2 - k
    k = k * k * (3 - 2 * k)
    _cm_mover_para(o, bx + b["dx"] * k, by + b["dy"] * k, st, j)


@novo_comp("Andar em quadrado", "Movimento", "Dá voltas num quadrado (direita, baixo, esquerda, cima).",
           [("lado", "150", "e"), ("velocidade", "100", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    L = max(1.0, b["lado"])
    st["d"] = (st.get("d", 0.0) + b["velocidade"] * dt) % (4 * L)
    d = st["d"]
    pts = [(d, 0), (L, d - L), (L - (d - 2 * L), L), (0, L - (d - 3 * L))][int(d // L)]
    _cm_mover_para(o, bx + pts[0], by + pts[1], st, j)


@novo_comp("Quicar nas bordas da tela", "Movimento", "Anda na diagonal e quica nas bordas da tela (logo de DVD).",
           [("velocidade", "150", "e")])
def _(j, o, b, dt, st):
    if "v" not in st:
        st["v"] = [b["velocidade"], b["velocidade"] * 0.7]
    vw, vh = j.area.w / j.zoom, j.area.h / j.zoom
    o.x += st["v"][0] * dt
    o.y += st["v"][1] * dt
    if o.x < j.cam[0] or o.x + o.w > j.cam[0] + vw:
        st["v"][0] *= -1
        o.x = max(j.cam[0], min(o.x, j.cam[0] + vw - o.w))
    if o.y < j.cam[1] or o.y + o.h > j.cam[1] + vh:
        st["v"][1] *= -1
        o.y = max(j.cam[1], min(o.y, j.cam[1] + vh - o.h))


@novo_comp("Teleportar aleatório", "Movimento", "De tempos em tempos some e aparece perto (fantasma, mago).",
           [("a_cada_seg", "3", "e"), ("raio", "150", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    if _cm_pode(st, "t", b["a_cada_seg"], j.tempo) and j.tempo > 0.1:
        j.soltar_particulas(*_cm_c(o), [180, 120, 255], 14)
        o.x = bx + random.uniform(-b["raio"], b["raio"])
        o.y = by + random.uniform(-b["raio"], b["raio"]) * 0.5
        j.soltar_particulas(*_cm_c(o), [180, 120, 255], 14)


@novo_comp("Cair quando o player passa embaixo", "Movimento", "Fica parado no alto e despenca quando o player "
           "passa embaixo, depois sobe de volta (tipo Thwomp).", [("velocidade_queda", "900", "e"),
                                                                  ("velocidade_volta", "120", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    p = _cm_pl(j)
    modo = st.setdefault("modo", "esperando")
    if modo == "esperando":
        o.y = by
        if p and p.y > o.y and abs(_cm_c(p)[0] - _cm_c(o)[0]) < o.w * 0.8:
            st["modo"] = "caindo"
    elif modo == "caindo":
        o.y += b["velocidade_queda"] * dt
        bateu = any(s is not o and s.vivo and s.d.get("solido") and sobrepoe(o, s) for s in j.objs)
        if bateu or o.y - by > 1200:
            j.tremer(8, 0.3)
            st["modo"], st["t"] = "parado", j.tempo
            o.y -= b["velocidade_queda"] * dt
    elif modo == "parado":
        if j.tempo - st["t"] > 0.8:
            st["modo"] = "voltando"
    else:
        o.y -= b["velocidade_volta"] * dt
        if o.y <= by:
            o.y, st["modo"] = by, "esperando"
    o.base_y = o.y


@novo_comp("Elevador (para nas pontas)", "Movimento", "Sobe e desce, esperando um pouco em cima e embaixo.",
           [("altura", "200", "e"), ("velocidade", "90", "e"), ("espera", "1", "e")])
def _(j, o, b, dt, st):
    bx, by = _cm_base(o, st)
    alvo = by - b["altura"] if st.get("subindo", True) else by
    if st.get("esperar", 0) > 0:
        st["esperar"] -= dt
        o.ult_dy = 0
        return
    passo = b["velocidade"] * dt
    ny = o.y - passo if alvo < o.y else o.y + passo
    if abs(alvo - o.y) <= passo:
        ny = alvo
        st["subindo"] = not st.get("subindo", True)
        st["esperar"] = b["espera"]
    _cm_mover_para(o, o.x, ny, st, j)


@novo_comp("Fugir do mouse", "Movimento", "Corre para longe do mouse quando ele chega perto.",
           [("alcance", "150", "e"), ("velocidade", "250", "e")])
def _(j, o, b, dt, st):
    mx, my = j.mouse_mundo
    cx, cy = _cm_c(o)
    d = math.hypot(cx - mx, cy - my)
    if 0 < d < b["alcance"]:
        o.x += (cx - mx) / d * b["velocidade"] * dt
        o.y += (cy - my) / d * b["velocidade"] * dt


@novo_comp("Acelerar aos poucos", "Movimento", "Começa devagar e vai ficando mais rápido para o lado que olha.",
           [("aceleracao", "200", "e"), ("maxima", "500", "e")])
def _(j, o, b, dt, st):
    lado = -1 if o.d.get("espelhar") else 1
    o.vx = max(-b["maxima"], min(b["maxima"], o.vx + lado * b["aceleracao"] * dt))
    o.movel = True


@novo_comp("Atrito (vai parando)", "Movimento", "Vai perdendo velocidade sozinho (bom para coisas empurradas).",
           [("forca", "3", "e")])
def _(j, o, b, dt, st):
    k = math.exp(-b["forca"] * dt)
    o.vx *= k
    if not o.d.get("gravidade"):
        o.vy *= k


@novo_comp("Gravidade própria", "Movimento", "Cai com uma força só dele (use negativo para cair para cima!).",
           [("forca", "-600", "e")])
def _(j, o, b, dt, st):
    o.d["gravidade"] = False
    o.vy += b["forca"] * dt
    o.movel = True


@novo_comp("Seguir o líder", "Movimento", "Segue o mesmo caminho que outro objeto fez (fila de cobra, vagões).",
           [("lider", "Player", "s"), ("atraso_seg", "0.3", "e")])
def _(j, o, b, dt, st):
    alvos = j.buscar(b["lider"])
    if not alvos:
        return
    lid = alvos[0]
    hist = st.setdefault("h", [])
    hist.append((j.tempo, lid.x + lid.w / 2 - o.w / 2, lid.y + lid.h - o.h))
    while hist and j.tempo - hist[0][0] > b["atraso_seg"]:
        _t, x, y = hist.pop(0)
        o.x, o.y = x, y
    o.d["espelhar"] = lid.d.get("espelhar", False)


@novo_comp("Espelhar o player", "Movimento", "Anda igual ao player, mas ao contrário (puzzle de espelho).",
           [("eixo_x", "0", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p:
        bx, by = _cm_base(o, st)
        if "p0" not in st:
            st["p0"] = (p.x, p.y)
        o.x = bx - (p.x - st["p0"][0])
        o.y = by + (p.y - st["p0"][1])


@novo_comp("Rolar (gira andando)", "Movimento", "Gira conforme anda, como uma roda ou bola.", [])
def _(j, o, b, dt, st):
    raio = max(4.0, o.w / 2)
    o.d["rotacao"] = (num_seguro(o.d.get("rotacao", 0)) - math.degrees(o.vx * dt / raio)) % 360


# =====================================================================
# VISUAL
# =====================================================================
@novo_comp("Piscar sempre", "Visual", "Fica piscando (aparece e some).", [("vezes_por_seg", "3", "e")])
def _(j, o, b, dt, st):
    o.visivel = int(j.tempo * b["vezes_por_seg"] * 2) % 2 == 0


@novo_comp("Arco-íris", "Visual", "Troca de cor passando por todas as cores.", [("velocidade", "0.3", "e")])
def _(j, o, b, dt, st):
    o.d["cor"] = _cm_hsv(j.tempo * b["velocidade"])


@novo_comp("Pulsar entre duas cores", "Visual", "Vai e volta entre a cor do objeto e outra cor.",
           [("r", "255", "e"), ("g", "255", "e"), ("b", "255", "e"), ("vezes_por_seg", "1", "e")])
def _(j, o, b, dt, st):
    c0 = st.setdefault("cor0", list(cor_ok(o.d.get("cor", [255, 255, 255]))))
    k = 0.5 + 0.5 * math.sin(j.tempo * b["vezes_por_seg"] * math.tau)
    o.d["cor"] = [int(c0[i] + (v - c0[i]) * k) for i, v in enumerate((b["r"], b["g"], b["b"]))]


@novo_comp("Aparecer devagar", "Visual", "Começa invisível e vai aparecendo.", [("seg", "1", "e")])
def _(j, o, b, dt, st):
    st["t"] = st.get("t", 0.0) + dt
    o.d["opacidade"] = int(255 * min(1.0, st["t"] / max(0.05, b["seg"])))


@novo_comp("Sumir devagar e destruir", "Visual", "Vai ficando transparente e some de vez (fumaça, fantasma).",
           [("seg", "2", "e")])
def _(j, o, b, dt, st):
    st["t"] = st.get("t", 0.0) + dt
    k = st["t"] / max(0.05, b["seg"])
    o.d["opacidade"] = int(255 * max(0.0, 1 - k))
    if k >= 1:
        o.vivo = False


@novo_comp("Balançar", "Visual", "Fica balançando de um lado para o outro (placa, planta, sino).",
           [("graus", "10", "e"), ("vezes_por_seg", "0.8", "e")])
def _(j, o, b, dt, st):
    o.d["rotacao"] = math.sin(j.tempo * b["vezes_por_seg"] * math.tau) * b["graus"]


@novo_comp("Rastro", "Visual", "Deixa um rastro de luz por onde passa.",
           [("r", "120", "e"), ("g", "200", "e"), ("b", "255", "e"), ("por_seg", "40", "e")])
def _(j, o, b, dt, st):
    if abs(o.ult_dx) + abs(o.ult_dy) + abs(o.vx) + abs(o.vy) < 1:
        return
    st["acc"] = st.get("acc", 0.0) + b["por_seg"] * dt
    while st["acc"] >= 1:
        st["acc"] -= 1
        _cm_particula(j, o.x + random.uniform(0, o.w), o.y + random.uniform(0, o.h), [b["r"], b["g"], b["b"]],
                   vida=0.45, tam=int(max(2, min(o.w, o.h) / 4)))


@novo_comp("Poeira ao andar", "Visual", "Solta poeirinha dos pés quando anda no chão.", [])
def _(j, o, b, dt, st):
    if o.chao and abs(o.vx) > 60 and _cm_pode(st, "t", 0.08, j.tempo):
        _cm_particula(j, o.x + o.w / 2, o.y + o.h - 2, [190, 180, 160], -o.vx * 0.2, -40, 0.4, 3, 300)


@novo_comp("Virar para onde anda", "Visual", "Vira a imagem para o lado em que está andando.", [])
def _(j, o, b, dt, st):
    vx = o.vx if abs(o.vx) > 1 else o.ult_dx / max(dt, 1e-4)
    if abs(vx) > 5:
        o.d["espelhar"] = vx < 0


@novo_comp("Inclinar ao andar", "Visual", "Inclina um pouco para frente quando anda rápido.", [("graus", "8", "e")])
def _(j, o, b, dt, st):
    alvo = -max(-1.0, min(1.0, o.vx / 400)) * b["graus"]
    atual = num_seguro(o.d.get("rotacao", 0))
    if atual > 180:
        atual -= 360
    o.d["rotacao"] = atual + (alvo - atual) * min(1.0, dt * 10)


@novo_comp("Esticar ao pular", "Visual", "Estica quando sobe e achata quando cai (estilo desenho animado).",
           [("forca", "0.25", "e")])
def _(j, o, b, dt, st):
    k = max(-1.0, min(1.0, -o.vy / 900)) * b["forca"]
    if "tam0" not in st:
        st["tam0"] = (o.w, o.h)
    w0, h0 = st["tam0"]
    pe = o.y + o.h
    o.h = h0 * (1 + k)
    o.y = pe - o.h
    cx = o.x + o.w / 2
    o.w = w0 * (1 - k * 0.6)
    o.x = cx - o.w / 2


@novo_comp("Girar ao pular", "Visual", "Dá uma cambalhota no ar.", [("voltas_por_seg", "2", "e")])
def _(j, o, b, dt, st):
    if not o.chao:
        o.d["rotacao"] = (num_seguro(o.d.get("rotacao", 0)) - 360 * b["voltas_por_seg"] * dt) % 360
    else:
        o.d["rotacao"] = 0


@novo_comp("Transparente perto do player", "Visual", "Fica meio transparente quando o player está atrás "
           "(árvores e telhados no top-down).", [("opacidade", "110", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    alvo = b["opacidade"] if (p and sobrepoe(o, p)) else 255
    atual = num_seguro(o.d.get("opacidade", 255), 255)
    o.d["opacidade"] = int(atual + (alvo - atual) * min(1.0, dt * 10))


@novo_comp("Tremer com pouca vida", "Visual", "Treme e pisca vermelho quando a vida está baixa.",
           [("vida_baixa", "1", "e")])
def _(j, o, b, dt, st):
    if num_seguro(o.vars.get("vida", 99), 99) <= b["vida_baixa"]:
        o.x += random.uniform(-1.5, 1.5)
        if int(j.tempo * 6) % 2 == 0:
            o.flash_t = o.flash_dur = 0.05


@novo_comp("Trocar de imagem sozinho", "Visual", "Troca entre imagens (separe por vírgula) a cada tanto tempo.",
           [("imagens", "", "s"), ("a_cada_seg", "1", "e")])
def _(j, o, b, dt, st):
    lista = [i.strip() for i in b["imagens"].split(",") if i.strip()]
    if lista:
        o.d["imagem"] = lista[int(j.tempo / max(0.05, b["a_cada_seg"])) % len(lista)]


@novo_comp("Brilho que pisca", "Visual", "Uma luz que fica mais forte e mais fraca (vela, tocha, cristal).",
           [("raio", "160", "e"), ("vezes_por_seg", "2", "e")])
def _(j, o, b, dt, st):
    k = 0.8 + 0.2 * math.sin(j.tempo * b["vezes_por_seg"] * math.tau) + random.uniform(-0.05, 0.05)
    if "Luz" not in o.comp:
        o.comp["Luz"] = {"raio": b["raio"], "forca": 255}
    o.comp["Luz"]["raio"] = b["raio"] * k


@novo_comp("Crescer e encolher", "Visual", "Fica maior e menor, sem parar.",
           [("quanto", "0.2", "e"), ("vezes_por_seg", "0.7", "e")])
def _(j, o, b, dt, st):
    _cm_escala(o, st, 1 + b["quanto"] * math.sin(j.tempo * b["vezes_por_seg"] * math.tau))


@novo_comp("Nome em cima", "Visual", "Mostra o nome do objeto (ou um texto) flutuando em cima dele.",
           [("texto", "", "s")])
def _(j, o, b, dt, st):
    st["txt"] = b["texto"] or o.d.get("nome", "")
    o.rotulo_em_cima = st["txt"]


# =====================================================================
# CÂMERA E TELA
# =====================================================================
@novo_comp("Tremer a tela perto", "Câmera e tela", "Treme a câmera quando o player chega perto (chefe, cachoeira).",
           [("alcance", "300", "e"), ("forca", "3", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and _cm_distancia(o, p) < b["alcance"]:
        j.tremer(b["forca"] * (1 - _cm_distancia(o, p) / b["alcance"]) + 0.5, 0.1)


@novo_comp("Zoom quando chegar perto", "Câmera e tela", "A câmera aproxima (ou afasta) quando o player chega perto.",
           [("alcance", "250", "e"), ("zoom", "1.5", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None:
        return
    perto = _cm_distancia(o, p) < b["alcance"]
    if perto != st.get("perto", False):
        st["perto"] = perto
        if "z0" not in st:
            st["z0"] = j.zoom
        j.animar_zoom(b["zoom"] if perto else st["z0"], 0.5)


@novo_comp("Câmera lenta perto", "Câmera e tela", "Tudo fica em câmera lenta quando o player chega perto.",
           [("alcance", "200", "e"), ("velocidade", "0.4", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and _cm_distancia(o, p) < b["alcance"]:
        j.escala_tempo = max(0.05, b["velocidade"])
        j.escala_ate = j.tempo + 0.05


@novo_comp("Escurecer perto", "Câmera e tela", "A tela escurece quando o player entra na área (caverna).",
           [("alcance", "250", "e"), ("escuridao", "200", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None:
        return
    if "e0" not in st:
        st["e0"] = num_seguro(j.cena.get("escuridao", 0), 0)
    alvo = b["escuridao"] if _cm_distancia(o, p) < b["alcance"] else st["e0"]
    atual = num_seguro(j.cena.get("escuridao", 0), 0)
    j.cena["escuridao"] = atual + (alvo - atual) * min(1.0, dt * 3)


@novo_comp("Seta apontando (fora da tela)", "Câmera e tela", "Quando o objeto está fora da tela, aparece uma seta "
           "na borda apontando para ele (objetivo, saída).", [("r", "255", "e"), ("g", "220", "e"), ("b", "80", "e")])
def _(j, o, b, dt, st):
    o.seta_cor = (int(b["r"]), int(b["g"]), int(b["b"]))
    SETAS_FORA.add(id(o))


@novo_comp("Câmera segue este objeto", "Câmera e tela", "A câmera segue este objeto em vez do player.", [])
def _(j, o, b, dt, st):
    if j.cam_alvo is not o:
        j.cam_alvo = o


SETAS_FORA = set()

# =====================================================================
# PLAYER
# =====================================================================


@novo_comp("Planar (segurar pulo)", "Player", "Segurando o pulo no ar, cai bem devagar.",
           [("queda_max", "120", "e")])
def _(j, o, b, dt, st):
    if not o.chao and o.vy > b["queda_max"] and Jogo.segura(j.teclas, "pular"):
        o.vy = b["queda_max"]
        if _cm_pode(st, "p", 0.1, j.tempo):
            _cm_particula(j, o.x + o.w / 2, o.y, [230, 230, 255], 0, -30, 0.4, 3)


@novo_comp("Jetpack", "Player", "Segurar o pulo no ar faz voar (gasta combustível, recarrega no chão).",
           [("forca", "1500", "e"), ("combustivel_seg", "1.5", "e")])
def _(j, o, b, dt, st):
    st.setdefault("comb", b["combustivel_seg"])
    if o.chao:
        st["comb"] = min(b["combustivel_seg"], st["comb"] + dt * 2)
    elif Jogo.segura(j.teclas, "pular") and st["comb"] > 0 and o.vy > -400:
        st["comb"] -= dt
        o.vy -= b["forca"] * dt
        _cm_particula(j, o.x + o.w / 2 + random.uniform(-4, 4), o.y + o.h, [255, 170, 60], random.uniform(-30, 30),
                   200, 0.3, 4)
    o.combustivel = st["comb"] / max(0.01, b["combustivel_seg"])


@novo_comp("Correr com Shift", "Player", "Segurando Shift, corre mais rápido.", [("multiplicar", "1.7", "e")])
def _(j, o, b, dt, st):
    if "v0" not in st:
        st["v0"] = num_seguro(o.d.get("velocidade", 320), 320)
    corre = j.teclas[pygame.K_LSHIFT] or j.teclas[pygame.K_RSHIFT]
    o.d["velocidade"] = st["v0"] * (b["multiplicar"] if corre else 1)
    if corre and o.chao and abs(o.vx) > 100 and _cm_pode(st, "p", 0.06, j.tempo):
        _cm_particula(j, o.x + o.w / 2, o.y + o.h, [200, 200, 200], -o.vx * 0.2, -30, 0.3, 3, 200)


@novo_comp("Agachar", "Player", "Segurando para baixo, fica mais baixinho (passa por buracos).",
           [("altura", "0.55", "e")])
def _(j, o, b, dt, st):
    if "h0" not in st:
        st["h0"] = o.h
    baixo = Jogo.segura(j.teclas, "baixo") and o.chao
    alvo = st["h0"] * (b["altura"] if baixo else 1)
    if abs(o.h - alvo) > 0.5:
        pe = o.y + o.h
        o.h = alvo
        o.y = pe - o.h


@novo_comp("Escalar paredes", "Player", "Encostado na parede, segura para cima para subir.",
           [("velocidade", "200", "e")])
def _(j, o, b, dt, st):
    if getattr(o, "parede", 0) and Jogo.segura(j.teclas, "cima"):
        o.vy = -b["velocidade"]


@novo_comp("Pulo carregado", "Player", "Quanto mais tempo segura o pulo no chão, mais alto pula (solte para pular).",
           [("forca_max", "1400", "e"), ("seg_para_encher", "0.8", "e")])
def _(j, o, b, dt, st):
    if o.chao and Jogo.segura(j.teclas, "baixo"):
        st["carga"] = min(1.0, st.get("carga", 0.0) + dt / max(0.05, b["seg_para_encher"]))
        o.vx *= 0.5
        if _cm_pode(st, "p", 0.05, j.tempo):
            _cm_particula(j, o.x + random.uniform(0, o.w), o.y + o.h, [255, 230, 120], 0, -60 * st["carga"], 0.3, 3)
    elif st.get("carga", 0) > 0:
        if o.chao:
            o.vy = -b["forca_max"] * (0.35 + 0.65 * st["carga"])
        st["carga"] = 0.0


@novo_comp("Pisar em qualquer inimigo", "Player", "Pular em cima de QUALQUER objeto com Vida dá dano nele.",
           [("dano", "1", "e")])
def _(j, o, b, dt, st):
    if o.vy <= 0:
        return
    for z in j.objs:
        if z is not o and z.vivo and z.tem("Vida") and sobrepoe(o, z) and (o.y + o.h) - z.y < 18:
            z.invencivel_t = 0
            j.dano(z, b["dano"])
            o.vy = -500


@novo_comp("Invencível no começo", "Player", "Fica invencível (piscando) nos primeiros segundos.", [("seg", "3", "e")])
def _(j, o, b, dt, st):
    if not st.get("feito"):
        st["feito"] = True
        o.invencivel_t = o.piscar_t = b["seg"]


@novo_comp("Atirar para o mouse", "Player", "Clique atira na direção do mouse.",
           [("tipo", "Moeda", "s"), ("velocidade", "700", "e"), ("espera", "0.25", "e")])
def _(j, o, b, dt, st):
    if j.clique_mundo_frame is not None and _cm_pode(st, "t", b["espera"], j.tempo):
        mx, my = j.clique_mundo_frame
        cx, cy = _cm_c(o)
        d = math.hypot(mx - cx, my - cy) or 1
        j.atirar(o, b["tipo"], (mx - cx) / d * b["velocidade"], (my - cy) / d * b["velocidade"])


@novo_comp("Deixar rastro de fogo", "Player", "Correndo, deixa chamas que machucam inimigos.",
           [("a_cada_seg", "0.15", "e")])
def _(j, o, b, dt, st):
    if abs(o.vx) > 120 and o.chao and _cm_pode(st, "t", b["a_cada_seg"], j.tempo):
        f = ObjJogo(nova_entidade("Zona", int(o.x + o.w / 2 - 8), int(o.y + o.h - 16), "FogoRastro", w=16, h=16,
                                  cor=[255, 120, 40], comportamentos=[
                                      {"t": "Emissor de partículas", "p": dict(params_padrao(COMPORTAMENTOS[
                                          "Emissor de partículas"]), estilo="fogo", por_seg="20")},
                                      {"t": "Dano", "p": dict(params_padrao(COMPORTAMENTOS["Dano"]), em="Inimigo")},
                                      {"t": "Destruir depois de", "p": {"seg": "1.2"}}]))
        j.novos.append(f)


@novo_comp("Nadar (dentro da água)", "Player", "Dentro de objetos do grupo Agua: cai devagar e pula sem parar.",
           [("grupo_agua", "Agua", "s")])
def _(j, o, b, dt, st):
    dentro = any(z.vivo and b["grupo_agua"] in z.grupos and sobrepoe(o, z) for z in j.objs if z is not o)
    if dentro:
        o.vy = min(o.vy, 140)
        if j.apertadas & set(acao_jogo("pular")):
            o.vy = -380
            _cm_particula(j, o.x + o.w / 2, o.y, [180, 220, 255], 0, -60, 0.4, 3)


@novo_comp("Subir escadas", "Player", "Dentro de objetos do grupo Escada, cima/baixo sobem e descem.",
           [("grupo_escada", "Escada", "s"), ("velocidade", "200", "e")])
def _(j, o, b, dt, st):
    dentro = any(z.vivo and b["grupo_escada"] in z.grupos and sobrepoe(o, z) for z in j.objs if z is not o)
    if dentro:
        cima, baixo = Jogo.segura(j.teclas, "cima"), Jogo.segura(j.teclas, "baixo")
        if cima or baixo or st.get("subindo"):
            st["subindo"] = True
            o.vy = -b["velocidade"] if cima else (b["velocidade"] if baixo else 0.0)
            o.y -= num_seguro(j.cena.get("gravidade", 1800), 1800) * dt * dt
    else:
        st["subindo"] = False


# =====================================================================
# INIMIGOS E IA
# =====================================================================
@novo_comp("Patrulhar sem cair", "Inimigos e IA", "Anda de um lado para o outro e vira na beirada da plataforma.",
           [("velocidade", "90", "e")])
def _(j, o, b, dt, st):
    lado = st.setdefault("lado", 1)
    if getattr(o, "parede", 0):
        lado = st["lado"] = -o.parede
    if o.chao:
        frente_x = o.x + o.w + 4 if lado > 0 else o.x - 4
        pe = o.y + o.h + 6
        tem_chao = any(s is not o and s.vivo and s.d.get("solido") and s.x <= frente_x <= s.x + s.w and
                       s.y <= pe <= s.y + s.h + 8 for s in j.objs)
        if not tem_chao:
            lado = st["lado"] = -lado
    o.vx = lado * b["velocidade"]
    o.d["espelhar"] = lado < 0
    o.movel = True


@novo_comp("Pular quando o player chega perto", "Inimigos e IA", "Dá um pulo quando o player chega perto.",
           [("alcance", "180", "e"), ("forca", "650", "e"), ("espera", "1.5", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and o.chao and _cm_distancia(o, p) < b["alcance"] and _cm_pode(st, "t", b["espera"], j.tempo):
        o.vy = -b["forca"]


@novo_comp("Investida", "Inimigos e IA", "Quando vê o player, para, treme e corre muito rápido na direção dele.",
           [("alcance", "350", "e"), ("velocidade", "600", "e"), ("descanso", "1.5", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    modo = st.setdefault("modo", "olhando")
    if modo == "olhando":
        if p and _cm_distancia(o, p) < b["alcance"] and j.tempo - st.get("fim", -9) > b["descanso"]:
            st["modo"], st["t"], st["lado"] = "preparando", j.tempo, 1 if _cm_c(p)[0] > _cm_c(o)[0] else -1
    elif modo == "preparando":
        o.vx = 0
        o.x += random.uniform(-1.5, 1.5)
        if j.tempo - st["t"] > 0.5:
            st["modo"], st["t"] = "correndo", j.tempo
    else:
        o.vx = st["lado"] * b["velocidade"]
        o.d["espelhar"] = st["lado"] < 0
        if _cm_pode(st, "p", 0.05, j.tempo):
            _cm_particula(j, o.x + o.w / 2, o.y + o.h, [200, 200, 200], -o.vx * 0.1, -20, 0.3, 3)
        if j.tempo - st["t"] > 0.9 or getattr(o, "parede", 0):
            st["modo"], st["fim"] = "olhando", j.tempo
            o.vx = 0
    o.movel = True


@novo_comp("Atirar em leque", "Inimigos e IA", "Atira vários tiros de uma vez, abertos como um leque.",
           [("tipo", "Moeda", "s"), ("tiros", "3", "e"), ("abertura", "40", "e"), ("velocidade", "350", "e"),
            ("a_cada_seg", "2", "e"), ("alcance", "500", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if not p or _cm_distancia(o, p) > b["alcance"] or not _cm_pode(st, "t", b["a_cada_seg"], j.tempo):
        return
    cx, cy = _cm_c(o)
    px, py = _cm_c(p)
    base = math.atan2(py - cy, px - cx)
    n = max(1, int(b["tiros"]))
    for i in range(n):
        a = base + math.radians(b["abertura"]) * ((i / (n - 1) - 0.5) if n > 1 else 0)
        j.atirar(o, b["tipo"], math.cos(a) * b["velocidade"], math.sin(a) * b["velocidade"])


@novo_comp("Atirar em círculo", "Inimigos e IA", "Solta tiros para todos os lados ao mesmo tempo.",
           [("tipo", "Moeda", "s"), ("tiros", "8", "e"), ("velocidade", "300", "e"), ("a_cada_seg", "2.5", "e"),
            ("girar", "15", "e")])
def _(j, o, b, dt, st):
    if not _cm_pode(st, "t", b["a_cada_seg"], j.tempo) or j.tempo < 0.2:
        return
    st["giro"] = st.get("giro", 0.0) + math.radians(b["girar"])
    n = max(1, int(b["tiros"]))
    for i in range(n):
        a = st["giro"] + math.tau * i / n
        j.atirar(o, b["tipo"], math.cos(a) * b["velocidade"], math.sin(a) * b["velocidade"])


@novo_comp("Fugir com pouca vida", "Inimigos e IA", "Quando a vida fica baixa, foge do player.",
           [("vida_baixa", "1", "e"), ("velocidade", "220", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and num_seguro(o.vars.get("vida", 99), 99) <= b["vida_baixa"]:
        lado = 1 if _cm_c(o)[0] > _cm_c(p)[0] else -1
        o.vx = lado * b["velocidade"]
        o.d["espelhar"] = lado < 0
        o.movel = True


@novo_comp("Dormir até ver o player", "Inimigos e IA", "Fica parado (dormindo) até o player chegar perto; aí "
           "liga os outros comportamentos.", [("alcance", "300", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if not st.get("acordou"):
        outros = [n for n in o.comp if n != "Dormir até ver o player"]
        o.comp_off.update(outros)
        o.vx = 0
        if _cm_pode(st, "z", 1.2, j.tempo):
            j.texto_flutuante("z", o.x + o.w, o.y - 4, (200, 200, 255))
        if p and _cm_distancia(o, p) < b["alcance"]:
            st["acordou"] = True
            o.comp_off.difference_update(outros)
            j.texto_flutuante("!", o.x + o.w / 2, o.y - 10, (255, 220, 60))
            if o.tipo == "Inimigo":
                o.vx = abs(num_seguro(o.d.get("velocidade", 100), 100))


@novo_comp("Toupeira (esconde e aparece)", "Inimigos e IA", "Fica escondido e de vez em quando aparece por um tempo.",
           [("seg_escondido", "2", "e"), ("seg_aparecendo", "1.5", "e")])
def _(j, o, b, dt, st):
    ciclo = b["seg_escondido"] + b["seg_aparecendo"]
    fase = (j.tempo + st.setdefault("des", random.random() * ciclo)) % ciclo
    fora = fase >= b["seg_escondido"]
    o.visivel = fora
    o.d["solido"] = fora and st.setdefault("solido0", bool(o.d.get("solido")))
    o.intocavel = not fora


@novo_comp("Gerar inimigos", "Inimigos e IA", "Cria um objeto (inimigo) a cada tanto tempo, até um máximo.",
           [("tipo", "Inimigo", "s"), ("a_cada_seg", "3", "e"), ("maximo", "5", "e")])
def _(j, o, b, dt, st):
    vivos = [z for z in st.get("criados", []) if z.vivo]
    st["criados"] = vivos
    if len(vivos) < b["maximo"] and _cm_pode(st, "t", b["a_cada_seg"], j.tempo) and j.tempo > 0.5:
        try:
            novo = j.criar(b["tipo"], o.x + o.w / 2 - 16, o.y)
            if novo is not None:
                vivos.append(novo)
            j.soltar_particulas(*_cm_c(o), [200, 120, 255], 12)
        except ErroBrasa as e:
            j.erro(o, e)


@novo_comp("Kamikaze", "Inimigos e IA", "Corre até o player e explode quando chega perto.",
           [("velocidade", "200", "e"), ("alcance", "400", "e"), ("raio", "100", "e"), ("dano", "2", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None or _cm_distancia(o, p) > b["alcance"]:
        return
    lado = 1 if _cm_c(p)[0] > _cm_c(o)[0] else -1
    o.vx = lado * b["velocidade"]
    if not o.d.get("gravidade"):
        dy = _cm_c(p)[1] - _cm_c(o)[1]
        o.vy = math.copysign(min(abs(dy) * 3, b["velocidade"]), dy)
    o.movel = True
    if int(j.tempo * 8) % 2 == 0:
        o.flash_t = o.flash_dur = 0.05
    if _cm_distancia(o, p) < max(o.w, o.h) * 0.8 + 10:
        j.explodir(o, b["raio"], b["dano"], "Player")
        o.vivo = False


@novo_comp("Chefe que fica bravo", "Inimigos e IA", "Com metade da vida, fica vermelho e mais rápido.",
           [("multiplicar", "1.6", "e")])
def _(j, o, b, dt, st):
    vmax = num_seguro(o.vars.get("vida_max", 0), 0)
    if not st.get("bravo") and vmax > 0 and num_seguro(o.vars.get("vida", vmax), vmax) <= vmax / 2:
        st["bravo"] = True
        j.mudar_prop(o, "velocidade", "*=", b["multiplicar"])
        o.vx *= b["multiplicar"]
        o.d["cor"] = [230, 70, 60]
        j.tremer(8, 0.5)
        j.texto_flutuante("FÚRIA!", o.x + o.w / 2, o.y - 14, (255, 80, 60))
        for n, c in o.comp.items():
            if "a_cada_seg" in c:
                c["a_cada_seg"] = max(0.2, c["a_cada_seg"] / b["multiplicar"])


@novo_comp("Invisível longe do player", "Inimigos e IA", "Só aparece quando o player chega perto (fantasma).",
           [("alcance", "200", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    alvo = 255 if (p and _cm_distancia(o, p) < b["alcance"]) else 0
    atual = num_seguro(o.d.get("opacidade", 255), 255)
    o.d["opacidade"] = int(atual + (alvo - atual) * min(1.0, dt * 5))


@novo_comp("Morcego (voa atrás do player)", "Inimigos e IA", "Voa atrás do player em ondas, sem gravidade.",
           [("velocidade", "130", "e"), ("alcance", "450", "e")])
def _(j, o, b, dt, st):
    o.d["gravidade"] = False
    p = _cm_pl(j)
    if p and _cm_distancia(o, p) < b["alcance"]:
        dx, dy = _cm_c(p)[0] - _cm_c(o)[0], _cm_c(p)[1] - _cm_c(o)[1]
        d = math.hypot(dx, dy) or 1
        o.vx = dx / d * b["velocidade"]
        o.vy = dy / d * b["velocidade"] + math.sin(j.tempo * 6) * 90
        o.d["espelhar"] = dx < 0
    else:
        o.vx *= 0.95
        o.vy = math.sin(j.tempo * 3) * 40
    o.movel = True


# =====================================================================
# FÍSICA
# =====================================================================
@novo_comp("Esteira", "Física", "Carrega quem estiver em cima para um lado.", [("velocidade", "150", "e")])
def _(j, o, b, dt, st):
    for z in j.objs:
        if z is not o and z.vivo and z.movel and _cm_acima_de(z, o):
            z.x += b["velocidade"] * dt


@novo_comp("Mola (pula ao pisar)", "Física", "Quem pisa em cima é jogado para o alto.", [("forca", "1100", "e")])
def _(j, o, b, dt, st):
    for z in j.objs:
        if z is not o and z.vivo and z.movel and _cm_acima_de(z, o, 8) and z.vy >= 0:
            z.vy = -b["forca"]
            z.chao = False
            _cm_escala(o, st, 0.85)
            st["volta"] = j.tempo + 0.12
    if st.get("volta") and j.tempo > st["volta"]:
        _cm_escala(o, st, 1.0)
        st["volta"] = None


@novo_comp("Zona de vento", "Física", "Empurra quem estiver dentro (use negativo para o outro lado).",
           [("forca_x", "0", "e"), ("forca_y", "-1500", "e")])
def _(j, o, b, dt, st):
    for z in j.objs:
        if z is not o and z.vivo and z.movel and sobrepoe(o, z):
            z.vx += b["forca_x"] * dt
            z.vy += b["forca_y"] * dt
    if _cm_pode(st, "p", 0.08, j.tempo):
        _cm_particula(j, o.x + random.uniform(0, o.w), o.y + random.uniform(0, o.h), [220, 230, 255],
                   b["forca_x"] * 0.2, b["forca_y"] * 0.2, 0.5, 2)


@novo_comp("Areia movediça", "Física", "Quem entra afunda devagar e anda lento.", [("afundar", "40", "e")])
def _(j, o, b, dt, st):
    for z in j.objs:
        if z is not o and z.vivo and z.movel and sobrepoe(o, z):
            z.vx *= 0.85
            z.vy = min(z.vy, b["afundar"])


@novo_comp("Buraco negro (atrai)", "Física", "Puxa tudo que se move para o centro.",
           [("alcance", "300", "e"), ("forca", "900", "e")])
def _(j, o, b, dt, st):
    cx, cy = _cm_c(o)
    for z in j.objs:
        if z is o or not z.vivo or not z.movel:
            continue
        zx, zy = _cm_c(z)
        d = math.hypot(cx - zx, cy - zy)
        if 1 < d < b["alcance"]:
            k = b["forca"] * (1 - d / b["alcance"]) * dt
            z.vx += (cx - zx) / d * k
            z.vy += (cy - zy) / d * k
    o.d["rotacao"] = (num_seguro(o.d.get("rotacao", 0)) + 120 * dt) % 360


@novo_comp("Repelir (empurra para longe)", "Física", "Empurra para longe tudo que se move perto.",
           [("alcance", "150", "e"), ("forca", "1200", "e")])
def _(j, o, b, dt, st):
    cx, cy = _cm_c(o)
    for z in j.objs:
        if z is o or not z.vivo or not z.movel:
            continue
        zx, zy = _cm_c(z)
        d = math.hypot(cx - zx, cy - zy)
        if 1 < d < b["alcance"]:
            k = b["forca"] * (1 - d / b["alcance"]) * dt
            z.vx += (zx - cx) / d * k
            z.vy += (zy - cy) / d * k


@novo_comp("Quicar ao cair", "Física", "Quica no chão como uma bola de borracha.", [("elasticidade", "0.7", "e")])
def _(j, o, b, dt, st):
    if o.chao and st.get("vy_ant", 0) > 150:
        o.vy = -st["vy_ant"] * b["elasticidade"]
        o.chao = False
    st["vy_ant"] = o.vy


@novo_comp("Pesado (cai rápido)", "Física", "Cai bem mais rápido que o normal.", [("multiplicar", "2.2", "e")])
def _(j, o, b, dt, st):
    if not o.chao and o.d.get("gravidade"):
        o.vy += num_seguro(j.cena.get("gravidade", 1800), 1800) * (b["multiplicar"] - 1) * dt


@novo_comp("Leve (cai devagar)", "Física", "Cai devagar como uma pena.", [("queda_max", "90", "e")])
def _(j, o, b, dt, st):
    o.vy = min(o.vy, b["queda_max"])
    if not o.chao:
        o.x += math.sin(j.tempo * 3 + id(o) % 7) * 20 * dt


@novo_comp("Plataforma de mão única", "Física", "Dá para pular por baixo e ficar em cima (só é sólida por cima).", [])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    o.d["solido"] = bool(p and p.y + p.h <= o.y + 8 and p.vy >= -1)


@novo_comp("Pegar e carregar (E)", "Física", "O player pega com E, carrega em cima da cabeça e solta/joga com E.",
           [("forca_jogar", "500", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None:
        return
    apertou = bool(j.apertadas & set(acao_jogo("acao")))
    if st.get("carregando"):
        o.x, o.y = p.x + p.w / 2 - o.w / 2, p.y - o.h - 2
        o.vx = o.vy = 0
        if apertou:
            st["carregando"] = False
            lado = -1 if p.d.get("espelhar") else 1
            o.vx, o.vy = lado * b["forca_jogar"], -300
            o.d["solido"] = st.get("solido0", True)
            o.movel = True
            st["pegou_t"] = j.tempo
    elif apertou and sobrepoe(o, p) or (apertou and _cm_distancia(o, p) < max(o.w, p.w) + 20
                                         and j.tempo - st.get("pegou_t", -9) > 0.3):
        st["carregando"] = True
        st["solido0"] = bool(o.d.get("solido"))
        o.d["solido"] = False


@novo_comp("Quebrar ao cair de alto", "Física", "Se cair de muito alto, quebra em pedaços.", [("altura", "250", "e")])
def _(j, o, b, dt, st):
    if not o.chao:
        st.setdefault("y0", o.y)
    else:
        if o.y - st.get("y0", o.y) > b["altura"]:
            j.soltar_particulas(*_cm_c(o), o.d.get("cor", [180, 140, 100]), 24)
            o.vivo = False
        st.pop("y0", None)


# =====================================================================
# COMBATE
# =====================================================================
@novo_comp("Escudo", "Combate", "Bloqueia os primeiros golpes (mostra um escudo).", [("golpes", "3", "e")])
def _(j, o, b, dt, st):
    st.setdefault("escudo", int(b["golpes"]))
    vida = num_seguro(o.vars.get("vida", 0), 0)
    if "v" in st and vida < st["v"] and st["escudo"] > 0:
        o.vars["vida"] = st["v"]
        st["escudo"] -= 1
        j.soltar_particulas(*_cm_c(o), [120, 200, 255], 10)
        j.texto_flutuante("BLOQUEOU!", o.x + o.w / 2, o.y - 10, (120, 200, 255))
        vida = st["v"]
    st["v"] = vida
    o.escudo_n = st["escudo"]


@novo_comp("Espinhos de volta", "Combate", "Quem encosta nele também leva dano (devolve).", [("dano", "1", "e")])
def _(j, o, b, dt, st):
    for z in j.objs:
        if z is not o and z.vivo and z.tem("Vida") or (z is j.player and z.vivo):
            if z is not o and sobrepoe(o, z) and _cm_pode(st, id(z), 0.6, j.tempo):
                j.dano(z, b["dano"])


@novo_comp("Empurrão ao levar dano", "Combate", "Quando leva dano é jogado para trás.", [("forca", "400", "e")])
def _(j, o, b, dt, st):
    vida = num_seguro(o.vars.get("vida", 0), 0)
    if "v" in st and vida < st["v"]:
        p = _cm_pl(j)
        lado = 1 if (p is None or _cm_c(o)[0] >= _cm_c(p)[0]) else -1
        o.vx, o.vy = lado * b["forca"], -b["forca"] * 0.6
        o.movel = True
    st["v"] = vida


@novo_comp("Soltar item ao morrer", "Combate", "Quando morre, solta um objeto (com chance %).",
           [("tipo", "Moeda", "s"), ("chance", "60", "e"), ("quantos", "1", "e")])
def _(j, o, b, dt, st):
    pass   # roda em "ao morrer" (lá embaixo)


@novo_comp("Dividir ao morrer", "Combate", "Quando morre vira 2 menores (slime que se divide).",
           [("pedacos", "2", "e"), ("geracoes", "2", "e")])
def _(j, o, b, dt, st):
    pass


@novo_comp("Pontos ao morrer", "Combate", "Soma pontos numa variável global quando morre.",
           [("variavel", "pontos", "s"), ("quanto", "100", "e")])
def _(j, o, b, dt, st):
    pass


@novo_comp("Explodir ao tocar no player", "Combate", "Explode quando encosta no player.",
           [("raio", "90", "e"), ("dano", "2", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and sobrepoe(o, p):
        j.explodir(o, b["raio"], b["dano"], "Player")
        o.vivo = False


@novo_comp("Hit kill (morre com 1 golpe)", "Combate", "Qualquer dano mata na hora.", [])
def _(j, o, b, dt, st):
    vida = num_seguro(o.vars.get("vida", 1), 1)
    if "v" in st and vida < st["v"] and o is not j.player:
        o.vars["vida"] = 0
        j.soltar_particulas(*_cm_c(o), o.d.get("cor", [255, 80, 80]), 20)
        o.vivo = False
    st["v"] = vida


@novo_comp("Arma que gira em volta", "Combate", "Bolas que giram em volta do objeto e machucam inimigos.",
           [("bolas", "2", "e"), ("raio", "60", "e"), ("voltas_por_seg", "0.8", "e"), ("em", "Inimigo", "s")])
def _(j, o, b, dt, st):
    cx, cy = _cm_c(o)
    n = max(1, int(b["bolas"]))
    for i in range(n):
        a = j.tempo * b["voltas_por_seg"] * math.tau + math.tau * i / n
        bx, by = cx + math.cos(a) * b["raio"], cy + math.sin(a) * b["raio"]
        _cm_particula(j, bx, by, [255, 200, 80], 0, 0, 0.05, 7)
        for z in j.buscar(b["em"]):
            if z is not o and z.vivo and z.x < bx < z.x + z.w and z.y < by < z.y + z.h and _cm_pode(st, id(z), 0.4,
                                                                                                 j.tempo):
                if z.tem("Vida"):
                    j.dano(z, 1)
                else:
                    z.vivo = False


@novo_comp("Aura de dano", "Combate", "Machuca quem ficar perto (a cada meio segundo).",
           [("raio", "90", "e"), ("dano", "1", "e"), ("em", "Player", "s")])
def _(j, o, b, dt, st):
    cx, cy = _cm_c(o)
    for z in j.buscar(b["em"]):
        if z is not o and z.vivo and math.hypot(_cm_c(z)[0] - cx, _cm_c(z)[1] - cy) < b["raio"] and \
                _cm_pode(st, id(z), 0.5, j.tempo):
            j.dano(z, b["dano"])
    if _cm_pode(st, "p", 0.05, j.tempo):
        a = random.uniform(0, math.tau)
        _cm_particula(j, cx + math.cos(a) * b["raio"], cy + math.sin(a) * b["raio"], [200, 80, 255], 0, 0, 0.4, 3)


@novo_comp("Curar quem está perto", "Combate", "Cura 1 de vida de quem fica perto (a cada tanto tempo).",
           [("raio", "100", "e"), ("a_cada_seg", "1", "e"), ("em", "Player", "s")])
def _(j, o, b, dt, st):
    cx, cy = _cm_c(o)
    for z in j.buscar(b["em"]):
        if z is not o and z.vivo and math.hypot(_cm_c(z)[0] - cx, _cm_c(z)[1] - cy) < b["raio"] and \
                _cm_pode(st, id(z), b["a_cada_seg"], j.tempo):
            antes = z.vars.get("vida")
            j.curar(z, 1)
            if z.vars.get("vida") != antes:
                j.texto_flutuante("+1", z.x + z.w / 2, z.y - 8, (120, 255, 140))


# =====================================================================
# ITENS E COLETÁVEIS
# =====================================================================
@novo_comp("Chave", "Itens e coletáveis", "O player pega a chave (vai para o inventário) e abre portas.",
           [("nome_chave", "chave", "s")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and sobrepoe(o, p):
        j.dar_item(b["nome_chave"])
        j.texto_flutuante("Pegou: " + b["nome_chave"], o.x + o.w / 2, o.y - 10, (255, 230, 90))
        j.soltar_particulas(*_cm_c(o), [255, 230, 90], 14)
        o.vivo = False


@novo_comp("Porta trancada", "Itens e coletáveis", "Só abre (some) se o player tiver a chave. Gasta a chave.",
           [("nome_chave", "chave", "s"), ("gastar", "Sim", "sn")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None:
        return
    perto = _cm_distancia(o, p) < max(o.w, o.h) / 2 + p.w + 6
    if perto and b["nome_chave"] in j.inventario:
        if b["gastar"]:
            j.remover_item(b["nome_chave"])
        j.soltar_particulas(*_cm_c(o), o.d.get("cor", [160, 120, 80]), 20)
        j.texto_flutuante("Abriu!", o.x + o.w / 2, o.y - 10, (255, 230, 90))
        o.vivo = False
    elif perto and _cm_pode(st, "aviso", 2, j.tempo):
        j.texto_flutuante("Precisa de: " + b["nome_chave"], o.x + o.w / 2, o.y - 10, (255, 160, 120))


@novo_comp("Moeda que volta", "Itens e coletáveis", "Depois de pega, a moeda volta depois de um tempo.",
           [("seg", "5", "e")])
def _(j, o, b, dt, st):
    pass   # roda em "ao morrer"


@novo_comp("Item: pulo extra", "Itens e coletáveis", "Ao pegar, o player ganha +1 pulo no ar para sempre.", [])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and sobrepoe(o, p):
        j.mudar_prop(p, "pulos_extras", "+=", 1)
        j.texto_flutuante("+1 PULO!", o.x + o.w / 2, o.y - 10, (120, 220, 255))
        o.vivo = False


@novo_comp("Item: vida máxima +1", "Itens e coletáveis", "Ao pegar, o player ganha +1 de vida máxima e cura.", [])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and sobrepoe(o, p):
        p.vars["vida_max"] = num_seguro(p.vars.get("vida_max", 3), 3) + 1
        p.vars["vida"] = p.vars["vida_max"]
        j.texto_flutuante("+1 VIDA MÁX!", o.x + o.w / 2, o.y - 10, (255, 120, 140))
        o.vivo = False


@novo_comp("Item: velocidade +20%", "Itens e coletáveis", "Ao pegar, o player fica 20% mais rápido para sempre.", [])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and sobrepoe(o, p):
        j.mudar_prop(p, "velocidade", "*=", 1.2)
        j.texto_flutuante("+VELOCIDADE!", o.x + o.w / 2, o.y - 10, (255, 230, 90))
        o.vivo = False


@novo_comp("Coletável que foge", "Itens e coletáveis", "Foge do player quando ele chega perto (pegue se puder!).",
           [("alcance", "120", "e"), ("velocidade", "160", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and _cm_distancia(o, p) < b["alcance"]:
        lado = 1 if _cm_c(o)[0] > _cm_c(p)[0] else -1
        o.x += lado * b["velocidade"] * dt


@novo_comp("Vencer ao juntar N", "Itens e coletáveis", "Quando o player juntar N moedas, ganha o jogo.",
           [("moedas", "10", "e")])
def _(j, o, b, dt, st):
    if j.moedas >= b["moedas"] and not st.get("feito"):
        st["feito"] = True
        j.vencer()


@novo_comp("Bloco ? (dá moeda)", "Itens e coletáveis", "Bater a cabeça por baixo dá moedas (até acabar).",
           [("moedas", "3", "e")])
def _(j, o, b, dt, st):
    st.setdefault("resta", int(b["moedas"]))
    p = _cm_pl(j)
    if p and st["resta"] > 0 and getattr(p, "teto_obj", None) is o and _cm_pode(st, "t", 0.25, j.tempo):
        st["resta"] -= 1
        j.moedas += 1
        j.texto_flutuante("+1", o.x + o.w / 2, o.y - 12, (255, 220, 60))
        _cm_particula(j, o.x + o.w / 2, o.y - 10, [255, 220, 60], 0, -300, 0.5, 8, 900)
        st["pulo"] = j.tempo
        if st["resta"] == 0:
            o.d["cor"] = [120, 100, 80]
    if st.get("pulo") is not None:
        k = j.tempo - st["pulo"]
        bx, by = _cm_base(o, st)
        o.y = by - (math.sin(min(1.0, k / 0.15) * math.pi) * 8 if k < 0.15 else 0)


# =====================================================================
# MECANISMOS
# =====================================================================
@novo_comp("Alavanca (liga/desliga grupo)", "Mecanismos", "Com E perto, liga/desliga: os objetos do grupo somem e "
           "aparecem (portas, pontes).", [("grupo", "Ponte", "s")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and _cm_distancia(o, p) < max(o.w, o.h) + 30 and j.apertadas & set(acao_jogo("acao")):
        st["ligado"] = not st.get("ligado", False)
        o.d["espelhar"] = st["ligado"]
        _cm_alternar_grupo(j, b["grupo"])
        j.texto_flutuante("Click!", o.x + o.w / 2, o.y - 10, (255, 255, 200))


def _cm_alternar_grupo(j, grupo, mostrar=None):
    for z in j.objs:
        if grupo and grupo in z.grupos:
            if not hasattr(z, "solido_orig"):
                z.solido_orig = bool(z.d.get("solido"))
            novo = (not z.visivel) if mostrar is None else mostrar
            z.visivel = novo
            z.d["solido"] = novo and z.solido_orig
            z.intocavel = not novo


@novo_comp("Botão de pressão", "Mecanismos", "Enquanto tem algo em cima, o grupo some (abre); saiu, volta.",
           [("grupo", "Porta", "s")])
def _(j, o, b, dt, st):
    em_cima = any(z is not o and z.vivo and z.movel and (_cm_acima_de(z, o, 8) or sobrepoe(o, z)) for z in j.objs)
    if em_cima != st.get("apertado", False):
        st["apertado"] = em_cima
        _cm_alternar_grupo(j, b["grupo"], mostrar=not em_cima)
        _cm_escala(o, st, 0.7 if em_cima else 1.0)


@novo_comp("Porta automática", "Mecanismos", "Abre (some) quando o player chega perto e fecha quando sai.",
           [("alcance", "100", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if "solido0" not in st:
        st["solido0"] = bool(o.d.get("solido"))
    aberta = bool(p and _cm_distancia(o, p) < b["alcance"])
    o.d["solido"] = st["solido0"] and not aberta
    alvo = 60 if aberta else 255
    atual = num_seguro(o.d.get("opacidade", 255), 255)
    o.d["opacidade"] = int(atual + (alvo - atual) * min(1.0, dt * 8))


@novo_comp("Subir com o tempo (lava/água)", "Mecanismos", "Cresce para cima sem parar (lava que sobe!).",
           [("velocidade", "25", "e"), ("altura_max", "2000", "e")])
def _(j, o, b, dt, st):
    if "fundo" not in st:
        st["fundo"] = o.y + o.h
    if o.h < b["altura_max"]:
        o.h += b["velocidade"] * dt
        o.y = st["fundo"] - o.h


@novo_comp("Canhão", "Mecanismos", "Atira sem parar para a direção que aponta (gire o objeto para mirar).",
           [("tipo", "Moeda", "s"), ("velocidade", "400", "e"), ("a_cada_seg", "1.5", "e")])
def _(j, o, b, dt, st):
    if _cm_pode(st, "t", b["a_cada_seg"], j.tempo) and j.tempo > 0.2:
        a = math.radians(-num_seguro(o.d.get("rotacao", 0)))
        lado = -1 if o.d.get("espelhar") else 1
        j.atirar(o, b["tipo"], math.cos(a) * b["velocidade"] * lado, math.sin(a) * b["velocidade"])
        j.soltar_particulas(o.x + (o.w if lado > 0 else 0), o.y + o.h / 2, [200, 200, 200], 6)


@novo_comp("Some e aparece no ritmo", "Mecanismos", "Some e aparece no ritmo (plataformas de ritmo).",
           [("seg_visivel", "2", "e"), ("seg_sumido", "1.5", "e"), ("atraso", "0", "e")])
def _(j, o, b, dt, st):
    ciclo = b["seg_visivel"] + b["seg_sumido"]
    fase = (j.tempo + b["atraso"]) % max(0.1, ciclo)
    if "solido0" not in st:
        st["solido0"] = bool(o.d.get("solido"))
    vis = fase < b["seg_visivel"]
    piscando = vis and fase > b["seg_visivel"] - 0.4
    o.visivel = vis and not (piscando and int(j.tempo * 12) % 2)
    o.d["solido"] = st["solido0"] and vis


@novo_comp("Serra giratória", "Mecanismos", "Gira rápido, solta faíscas e machuca o player.", [("dano", "1", "e")])
def _(j, o, b, dt, st):
    o.d["rotacao"] = (num_seguro(o.d.get("rotacao", 0)) + 720 * dt) % 360
    p = _cm_pl(j)
    if p and sobrepoe(o, p) and _cm_pode(st, "d", 0.5, j.tempo):
        j.dano(p, b["dano"])
    if _cm_pode(st, "f", 0.07, j.tempo):
        a = random.uniform(0, math.tau)
        _cm_particula(j, _cm_c(o)[0] + math.cos(a) * o.w / 2, _cm_c(o)[1] + math.sin(a) * o.h / 2, [255, 220, 120],
                   math.cos(a) * 200, math.sin(a) * 200, 0.25, 2, 600)


@novo_comp("Laser liga e desliga", "Mecanismos", "Um raio que liga e desliga; ligado, machuca o player.",
           [("seg_ligado", "1.5", "e"), ("seg_desligado", "1.5", "e"), ("dano", "1", "e")])
def _(j, o, b, dt, st):
    ciclo = b["seg_ligado"] + b["seg_desligado"]
    fase = j.tempo % max(0.1, ciclo)
    ligado = fase < b["seg_ligado"]
    aviso = not ligado and fase > ciclo - 0.4
    o.d["opacidade"] = 255 if ligado else (90 if aviso else 25)
    p = _cm_pl(j)
    if ligado and p and sobrepoe(o, p) and _cm_pode(st, "d", 0.6, j.tempo):
        j.dano(p, b["dano"])


@novo_comp("Checkpoint invisível", "Mecanismos", "Ao passar por aqui, o player volta daqui quando morrer.", [])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and sobrepoe(o, p) and not st.get("feito"):
        st["feito"] = True
        j.spawn = (o.x + o.w / 2 - p.w / 2, o.y + o.h - p.h)
        j.texto_flutuante("Checkpoint!", o.x + o.w / 2, o.y - 10, (120, 255, 140))


@novo_comp("Teleporte em par", "Mecanismos", "Leva o player para o outro objeto do mesmo grupo (portal duplo).",
           [("grupo", "Portais", "s")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None or j.tempo < getattr(p, "teleporte_ate", 0):
        return
    if sobrepoe(o, p):
        outros = [z for z in j.objs if z is not o and z.vivo and b["grupo"] in z.grupos]
        if outros:
            dest = outros[0]
            j.soltar_particulas(*_cm_c(p), [160, 120, 255], 16)
            p.x, p.y = dest.x + dest.w / 2 - p.w / 2, dest.y + dest.h - p.h
            p.teleporte_ate = j.tempo + 0.8
            j.soltar_particulas(*_cm_c(p), [160, 120, 255], 16)


# =====================================================================
# INTERFACE
# =====================================================================
@novo_comp("Mostrar variável", "Interface", "Um Texto que mostra uma variável global (ex: pontos).",
           [("variavel", "pontos", "s"), ("antes", "Pontos: ", "s")])
def _(j, o, b, dt, st):
    o.d["texto"] = b["antes"] + texto(j.globais.d.get(b["variavel"], 0))


@novo_comp("Botão: ir para fase", "Interface", "Um Botão que abre outra fase quando clica.", [("fase", "", "s")])
def _(j, o, b, dt, st):
    if _cm_clicou_ui(j, o) and b["fase"] in j.dados.get("fases", {}):
        j.ir_fase(b["fase"])


@novo_comp("Botão: reiniciar", "Interface", "Um Botão que reinicia a fase quando clica.", [])
def _(j, o, b, dt, st):
    if _cm_clicou_ui(j, o):
        j.reiniciar()


@novo_comp("Botão: pausar", "Interface", "Um Botão que pausa/despausa o jogo.", [])
def _(j, o, b, dt, st):
    if _cm_clicou_ui(j, o):
        j.alternar_pausa()


@novo_comp("Barra do tempo", "Interface", "Uma Barra que vai esvaziando; quando acaba, o player perde.",
           [("seg", "60", "e"), ("perder_no_fim", "Sim", "sn")])
def _(j, o, b, dt, st):
    st["t"] = st.get("t", 0.0) + dt
    k = max(0.0, 1 - st["t"] / max(0.1, b["seg"]))
    o.d["valor_de"], o.d["maximo"] = str(round(k, 4)), 1
    if k <= 0 and b["perder_no_fim"] and not st.get("fim"):
        st["fim"] = True
        j.perder()


@novo_comp("Balão de fala seguindo", "Interface", "Mostra um texto em balão em cima do objeto o tempo todo.",
           [("texto", "Olá!", "s")])
def _(j, o, b, dt, st):
    o.rotulo_em_cima = b["texto"]


def _cm_clicou_ui(j, o):
    c = j.clique_frame
    if c is None:
        return False
    if o.na_tela:
        a = j.area
        return pygame.Rect(a.x + o.x, a.y + o.y, o.w, o.h).collidepoint(c)
    m = j.clique_mundo_frame
    return m is not None and o.x <= m[0] <= o.x + o.w and o.y <= m[1] <= o.y + o.h


# =====================================================================
# SOM E TEMPO
# =====================================================================
@novo_comp("Som ao aparecer", "Som", "Toca um som quando o objeto aparece.", [("som", "moeda", "s")])
def _(j, o, b, dt, st):
    if not st.get("feito"):
        st["feito"] = True
        tocar_som(b["som"])


@novo_comp("Som quando o player chega perto", "Som", "Toca um som (uma vez) quando o player chega perto.",
           [("som", "", "s"), ("alcance", "200", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    perto = bool(p and _cm_distancia(o, p) < b["alcance"])
    if perto and not st.get("perto"):
        tocar_som(b["som"])
    st["perto"] = perto


@novo_comp("Música ao chegar perto", "Som", "Troca a música quando o player chega perto (sala do chefe).",
           [("musica", "", "s"), ("alcance", "300", "e")])
def _(j, o, b, dt, st):
    p = _cm_pl(j)
    if p and not st.get("feito") and _cm_distancia(o, p) < b["alcance"] and b["musica"]:
        st["feito"] = True
        tocar_musica(b["musica"])


@novo_comp("Som a cada tanto tempo", "Som", "Toca um som repetindo (relógio, goteira).",
           [("som", "", "s"), ("a_cada_seg", "2", "e")])
def _(j, o, b, dt, st):
    if _cm_pode(st, "t", b["a_cada_seg"], j.tempo) and b["som"]:
        tocar_som(b["som"], 0.6)


@novo_comp("Destruir depois de", "Tempo", "Some sozinho depois de alguns segundos.", [("seg", "3", "e")])
def _(j, o, b, dt, st):
    st["t"] = st.get("t", 0.0) + dt
    if st["t"] >= b["seg"]:
        o.vivo = False


@novo_comp("Aparecer depois de", "Tempo", "Fica escondido (sem colisão) e aparece depois de alguns segundos.",
           [("seg", "3", "e")])
def _(j, o, b, dt, st):
    st["t"] = st.get("t", 0.0) + dt
    if "solido0" not in st:
        st["solido0"] = bool(o.d.get("solido"))
    pronto = st["t"] >= b["seg"]
    if pronto and not st.get("apareceu"):
        st["apareceu"] = True
        j.soltar_particulas(*_cm_c(o), [255, 255, 200], 12)
    o.visivel = pronto
    o.d["solido"] = st["solido0"] and pronto
    o.intocavel = not pronto


@novo_comp("Ligado só de noite", "Tempo", "Só fica visível quando a cena está escura (escuridão > 100).", [])
def _(j, o, b, dt, st):
    o.visivel = num_seguro(j.cena.get("escuridao", 0), 0) > 100


# =====================================================================
# REAÇÕES: QUANDO acontece algo -> FAZ algo (cada par vira um comportamento)
# =====================================================================
def _g_tocar(j, o, b, dt, st):
    p = _cm_pl(j)
    agora = bool(p and sobrepoe(o, p))
    antes = st.get("toc", False)
    st["toc"] = agora
    return agora and not antes


def _g_dano(j, o, b, dt, st):
    v = num_seguro(o.vars.get("vida", 0), 0)
    antes = st.get("vida", v)
    st["vida"] = v
    return v < antes


def _g_clique(j, o, b, dt, st):
    m = j.clique_mundo_frame
    return m is not None and o.x <= m[0] <= o.x + o.w and o.y <= m[1] <= o.y + o.h


def _g_tempo(j, o, b, dt, st):
    st["t"] = st.get("t", 0.0) + dt
    if st["t"] >= max(0.05, b.get("a_cada_seg", 2)):
        st["t"] = 0.0
        return True
    return False


def _g_perto(j, o, b, dt, st):
    p = _cm_pl(j)
    agora = bool(p and _cm_distancia(o, p) < b.get("alcance", 150))
    antes = st.get("perto", False)
    st["perto"] = agora
    return agora and not antes


def _g_inicio(j, o, b, dt, st):
    if st.get("feito"):
        return False
    st["feito"] = True
    return True


def _g_pousar(j, o, b, dt, st):
    antes = st.get("chao", True)
    st["chao"] = o.chao
    return o.chao and not antes


def _g_parede(j, o, b, dt, st):
    pa = bool(getattr(o, "parede", 0))
    antes = st.get("par", False)
    st["par"] = pa
    return pa and not antes


def _g_player_pula(j, o, b, dt, st):
    p = _cm_pl(j)
    if p is None:
        return False
    subiu = p.vy < -200 and st.get("pvy", 0) >= -50
    st["pvy"] = p.vy
    return subiu


def _g_moedas(j, o, b, dt, st):
    antes = st.get("m", j.moedas)
    st["m"] = j.moedas
    return j.moedas > antes


GATILHOS_REACAO = {
    "Ao tocar no player": ([], _g_tocar),
    "Ao levar dano": ([], _g_dano),
    "Ao ser clicado": ([], _g_clique),
    "A cada tempo": ([("a_cada_seg", "2", "e")], _g_tempo),
    "Quando o player chega perto": ([("alcance", "150", "e")], _g_perto),
    "Ao começar": ([], _g_inicio),
    "Ao pousar": ([], _g_pousar),
    "Ao bater na parede": ([], _g_parede),
    "Quando o player pula": ([], _g_player_pula),
    "Quando pega moeda": ([], _g_moedas),
}


def _e_moedas(j, o, b):
    j.moedas += int(b["n"])
    j.texto_flutuante(f"+{int(b['n'])}", o.x + o.w / 2, o.y - 10, (255, 220, 60))


def _e_dano_player(j, o, b):
    if _cm_pl(j):
        j.dano(j.player, b["n"])


def _e_curar_player(j, o, b):
    if _cm_pl(j):
        j.curar(j.player, b["n"])
        j.texto_flutuante(f"+{texto(limpar(b['n']))}", j.player.x + j.player.w / 2, j.player.y - 10, (120, 255, 140))


def _e_destruir(j, o, b):
    j.soltar_particulas(*_cm_c(o), o.d.get("cor", [255, 255, 255]), 16)
    o.vivo = False


def _e_tremer(j, o, b):
    j.tremer(b["forca"], 0.35)


def _e_particulas(j, o, b):
    j.soltar_particulas(*_cm_c(o), [b["r"], b["g"], b["b"]], int(b["qtd"]))


def _e_texto(j, o, b):
    j.texto_flutuante(b["texto"], o.x + o.w / 2, o.y - 10, (255, 255, 255))


def _e_piscar(j, o, b):
    o.flash_t = o.flash_dur = 0.25
    o.piscar_t = 0.6


def _e_cor(j, o, b):
    o.d["cor"] = _cm_hsv(random.random())


def _e_mola(j, o, b):
    if _cm_pl(j):
        j.player.vy = -b["forca"]
        j.player.chao = False


def _e_vencer(j, o, b):
    j.vencer()


def _e_perder(j, o, b):
    j.perder()


def _e_fase(j, o, b):
    if b["fase"] in j.dados.get("fases", {}):
        j.ir_fase(b["fase"])
    else:
        j.proxima_fase()


def _e_lento(j, o, b):
    j.escala_tempo = 0.35
    j.escala_ate = j.tempo + b["seg"]


def _e_criar(j, o, b):
    try:
        j.criar(b["tipo"], o.x + o.w / 2 - 16, o.y - 40)
    except ErroBrasa as e:
        j.erro(o, e)


def _e_som(j, o, b):
    tocar_som(b["som"])


def _e_titulo(j, o, b):
    j.banner = [b["texto"], 2.0, 0.0]


def _e_global(j, o, b):
    atual = num_seguro(j.globais.d.get(b["variavel"], 0), 0)
    j.globais.d[b["variavel"]] = limpar(atual + b["n"])


def _e_invencivel(j, o, b):
    if _cm_pl(j):
        j.player.invencivel_t = j.player.piscar_t = b["seg"]


def _e_turbo(j, o, b):
    if _cm_pl(j):
        j.poder_temporario(j.player, "velocidade", 1.8, b["seg"])


def _e_superpulo(j, o, b):
    if _cm_pl(j):
        j.poder_temporario(j.player, "pulo", 1.4, b["seg"])


def _e_crescer(j, o, b):
    cx, cy = _cm_c(o)
    o.w *= 1.25
    o.h *= 1.25
    o.x, o.y = cx - o.w / 2, cy - o.h / 2


def _e_encolher(j, o, b):
    cx, cy = _cm_c(o)
    o.w = max(4, o.w * 0.8)
    o.h = max(4, o.h * 0.8)
    o.x, o.y = cx - o.w / 2, cy - o.h / 2


def _e_hitstop(j, o, b):
    j.congelar_t = max(j.congelar_t, 0.08)


def _e_dialogo(j, o, b):
    j.abrir_dialogo(b["texto"], o.d.get("nome", ""))


def _e_explodir(j, o, b):
    j.explodir(o, 100, 1, "Player")
    o.vivo = False


def _e_pular(j, o, b):
    o.vy = -b["forca"]
    o.chao = False
    o.movel = True


def _e_virar(j, o, b):
    o.vx = -o.vx
    o.d["espelhar"] = not o.d.get("espelhar", False)


def _e_teleporte_player(j, o, b):
    alvos = j.buscar(b["destino"])
    if alvos and _cm_pl(j):
        d = alvos[0]
        j.player.x, j.player.y = d.x + d.w / 2 - j.player.w / 2, d.y - j.player.h
        j.soltar_particulas(*_cm_c(j.player), [160, 120, 255], 16)


def _e_zoom(j, o, b):
    j.animar_zoom(b["zoom"], 0.4)


EFEITOS_REACAO = {
    "dar moedas": ([("n", "5", "e")], _e_moedas),
    "machucar o player": ([("n", "1", "e")], _e_dano_player),
    "curar o player": ([("n", "1", "e")], _e_curar_player),
    "se destruir": ([], _e_destruir),
    "tremer a tela": ([("forca", "8", "e")], _e_tremer),
    "soltar partículas": ([("r", "255", "e"), ("g", "220", "e"), ("b", "80", "e"), ("qtd", "20", "e")], _e_particulas),
    "mostrar texto": ([("texto", "Oi!", "s")], _e_texto),
    "piscar": ([], _e_piscar),
    "mudar de cor": ([], _e_cor),
    "jogar o player para cima": ([("forca", "1000", "e")], _e_mola),
    "vencer o jogo": ([], _e_vencer),
    "perder o jogo": ([], _e_perder),
    "ir para fase": ([("fase", "", "s")], _e_fase),
    "câmera lenta": ([("seg", "1.5", "e")], _e_lento),
    "criar objeto": ([("tipo", "Moeda", "s")], _e_criar),
    "tocar som": ([("som", "moeda", "s")], _e_som),
    "mostrar título": ([("texto", "MUITO BEM!", "s")], _e_titulo),
    "somar na variável": ([("variavel", "pontos", "s"), ("n", "1", "e")], _e_global),
    "deixar o player invencível": ([("seg", "3", "e")], _e_invencivel),
    "dar turbo ao player": ([("seg", "4", "e")], _e_turbo),
    "dar super pulo ao player": ([("seg", "4", "e")], _e_superpulo),
    "crescer": ([], _e_crescer),
    "encolher": ([], _e_encolher),
    "congelar um instante": ([], _e_hitstop),
    "abrir diálogo": ([("texto", "Olá!|Tudo bem?", "s")], _e_dialogo),
    "explodir": ([], _e_explodir),
    "pular": ([("forca", "600", "e")], _e_pular),
    "virar para o outro lado": ([], _e_virar),
    "teleportar o player": ([("destino", "Checkpoint", "s")], _e_teleporte_player),
    "dar zoom": ([("zoom", "1.4", "e")], _e_zoom),
}

PARES_REACAO = {
    "Ao tocar no player": ["dar moedas", "machucar o player", "curar o player", "se destruir", "tremer a tela",
                           "soltar partículas", "mostrar texto", "jogar o player para cima", "vencer o jogo",
                           "perder o jogo", "ir para fase", "câmera lenta", "tocar som", "mostrar título",
                           "somar na variável", "deixar o player invencível", "dar turbo ao player",
                           "dar super pulo ao player", "abrir diálogo", "explodir", "teleportar o player",
                           "criar objeto", "congelar um instante", "dar zoom", "piscar"],
    "Ao levar dano": ["piscar", "tremer a tela", "soltar partículas", "mostrar texto", "mudar de cor", "crescer",
                      "encolher", "criar objeto", "tocar som", "pular", "virar para o outro lado", "câmera lenta",
                      "somar na variável", "congelar um instante", "dar moedas"],
    "Ao ser clicado": ["se destruir", "dar moedas", "mostrar texto", "mudar de cor", "soltar partículas", "crescer",
                       "encolher", "tocar som", "pular", "criar objeto", "ir para fase", "somar na variável",
                       "abrir diálogo", "piscar", "explodir", "mostrar título"],
    "A cada tempo": ["criar objeto", "pular", "mudar de cor", "soltar partículas", "tocar som", "piscar",
                     "virar para o outro lado", "dar moedas", "somar na variável", "mostrar texto", "tremer a tela",
                     "crescer", "encolher"],
    "Quando o player chega perto": ["mostrar texto", "abrir diálogo", "tremer a tela", "mostrar título", "tocar som",
                                    "pular", "soltar partículas", "câmera lenta", "dar zoom", "criar objeto",
                                    "explodir", "piscar", "curar o player", "dar moedas", "virar para o outro lado"],
    "Ao começar": ["mostrar título", "tocar som", "dar zoom", "criar objeto", "soltar partículas", "abrir diálogo",
                   "mostrar texto", "piscar", "mudar de cor", "pular"],
    "Ao pousar": ["tremer a tela", "soltar partículas", "tocar som", "pular", "mudar de cor", "criar objeto",
                  "piscar", "se destruir"],
    "Ao bater na parede": ["virar para o outro lado", "tremer a tela", "soltar partículas", "tocar som", "pular",
                           "se destruir", "mudar de cor", "explodir"],
    "Quando o player pula": ["pular", "virar para o outro lado", "mudar de cor", "soltar partículas", "piscar",
                             "tocar som", "criar objeto", "mostrar texto"],
    "Quando pega moeda": ["mostrar texto", "soltar partículas", "pular", "mudar de cor", "crescer", "tocar som",
                          "somar na variável", "piscar"],
}


def _registrar_reacoes():
    for gat, efeitos in PARES_REACAO.items():
        params_g, fn_g = GATILHOS_REACAO[gat]
        for ef in efeitos:
            params_e, fn_e = EFEITOS_REACAO[ef]
            nome = f"{gat} → {ef}"

            def roda(j, o, b, dt, st, fn_g=fn_g, fn_e=fn_e):
                if fn_g(j, o, b, dt, st):
                    fn_e(j, o, b)
            novo_comp(nome, "Reações (quando → faz)", f"{gat}, este objeto faz: {ef}.",
                      list(params_g) + list(params_e))(roda)


_registrar_reacoes()

# =====================================================================
# LIGAÇÃO COM O JOGO
# =====================================================================
NOMES_REG = set(REG_COMP)
_comp_extra_antes_mais = JogoExtras.comportamentos_extra


def _comp_extra_mais(self, o, c, liga, dt):
    _comp_extra_antes_mais(self, o, c, liga, dt)
    if c.keys().isdisjoint(NOMES_REG):
        return
    est = o.__dict__.setdefault("est_comp", {})
    for nome in list(c):
        fn = REG_COMP.get(nome)
        if fn is not None and liga(nome):
            try:
                fn(self, o, c[nome], dt, est.setdefault(nome, {}))
            except ErroBrasa as e:
                self.erro(o, e)
            except (ValueError, TypeError, ZeroDivisionError, KeyError, AttributeError) as e:
                self.erro(o, ErroBrasa(f"comportamento '{nome}': {e}"))


JogoExtras.comportamentos_extra = _comp_extra_mais
_passo_comp_antigo = Jogo.passo_comportamentos


def _passo_comp_novo(self, dt, teclas, clique):
    self.clique_frame = clique
    if clique is not None:
        a = self.area
        self.clique_mundo_frame = ((clique[0] - a.x) / self.zoom + self.cam[0],
                                   (clique[1] - a.y) / self.zoom + self.cam[1])
    else:
        self.clique_mundo_frame = None
    return _passo_comp_antigo(self, dt, teclas, clique)


Jogo.passo_comportamentos = _passo_comp_novo
Jogo.clique_frame = None
Jogo.clique_mundo_frame = None
_morte_antiga = JogoExtras.morte_extra


def _morte_mais(self, o):
    _morte_antiga(self, o)
    c = getattr(o, "comp", None)
    if not c:
        return
    if "Soltar item ao morrer" in c:
        b = c["Soltar item ao morrer"]
        for _ in range(max(1, int(b["quantos"]))):
            if random.random() * 100 < b["chance"]:
                try:
                    novo = self.criar(b["tipo"], o.x + o.w / 2 - 10 + random.uniform(-15, 15), o.y)
                    if novo is not None:
                        novo.vy = -300
                        novo.movel = novo.movel or bool(novo.d.get("gravidade"))
                except ErroBrasa as e:
                    self.erro(o, e)
    if "Pontos ao morrer" in c:
        b = c["Pontos ao morrer"]
        atual = num_seguro(self.globais.d.get(b["variavel"], 0), 0)
        self.globais.d[b["variavel"]] = limpar(atual + b["quanto"])
        self.texto_flutuante(f"+{texto(limpar(b['quanto']))}", o.x + o.w / 2, o.y - 10, (255, 230, 90))
    if "Dividir ao morrer" in c:
        b = c["Dividir ao morrer"]
        ger = int(o.d.get("_geracao", 0))
        if ger + 1 < b["geracoes"] and o.w > 10:
            for i in range(max(1, int(b["pedacos"]))):
                d = copy.deepcopy(o.d)
                d["_geracao"] = ger + 1
                d["w"], d["h"] = o.w * 0.65, o.h * 0.65
                d["x"], d["y"] = o.x + i * o.w * 0.4, o.y
                filho = ObjJogo(d)
                filho.vx = (-1 if i % 2 == 0 else 1) * 160
                filho.vy = -350
                filho.movel = True
                self.novos.append(filho)
    if "Moeda que volta" in c:
        d = copy.deepcopy(o.d)
        seg = c["Moeda que volta"]["seg"]
        self.agendar(seg, self.cena_dono, lambda d=d: self.novos.append(ObjJogo(d)))
    reacoes = [n for n in c if n.startswith("Ao ser destruído")]
    for n in reacoes:
        REG_COMP[n](self, o, c[n], 0, {})


JogoExtras.morte_extra = _morte_mais

# Reações "Ao ser destruído" (rodam na hora que o objeto some)
for _ef in ["dar moedas", "soltar partículas", "tremer a tela", "criar objeto", "tocar som", "mostrar texto",
            "somar na variável", "vencer o jogo", "mostrar título", "explodir", "câmera lenta", "curar o player"]:
    _pe, _fe = EFEITOS_REACAO[_ef]
    novo_comp(f"Ao ser destruído → {_ef}", "Reações (quando → faz)", f"Quando este objeto some, faz: {_ef}.",
              list(_pe))(lambda j, o, b, dt, st, fe=_fe: fe(j, o, b) if dt == 0 else None)

# =====================================================================
# DESENHO: seta para objetos fora da tela, balões/rótulos em cima, combustível do jetpack
# =====================================================================
_desenhar_extra_antigo = JogoExtras.desenhar_extra


def _desenhar_extra_mais(self, tela, a):
    _desenhar_extra_antigo(self, tela, a)
    z = self.zoom
    for o in self.objs:
        if not o.vivo:
            continue
        rot = getattr(o, "rotulo_em_cima", None)
        if rot and o.visivel:
            x = (o.x + o.w / 2 - self.cam[0]) * z + a.x
            y = (o.y - self.cam[1]) * z + a.y - 10
            img = texto_cache(rot, 14, (255, 255, 255), True)
            caixa = pygame.Rect(0, 0, img.get_width() + 12, img.get_height() + 6)
            caixa.midbottom = (int(x), int(y))
            pygame.draw.rect(tela, (20, 22, 30), caixa, border_radius=8)
            pygame.draw.rect(tela, (255, 255, 255), caixa, 1, border_radius=8)
            tela.blit(img, (caixa.x + 6, caixa.y + 3))
        comb = getattr(o, "combustivel", None)
        if comb is not None and comb < 0.999:
            x = (o.x - self.cam[0]) * z + a.x
            y = (o.y - self.cam[1]) * z + a.y - 8
            pygame.draw.rect(tela, (40, 40, 50), (x, y, o.w * z, 4))
            pygame.draw.rect(tela, (255, 170, 60), (x, y, o.w * z * comb, 4))
        n = getattr(o, "escudo_n", 0)
        if n:
            cx = (o.x + o.w / 2 - self.cam[0]) * z + a.x
            cy = (o.y + o.h / 2 - self.cam[1]) * z + a.y
            pygame.draw.circle(tela, (120, 200, 255), (int(cx), int(cy)), int(max(o.w, o.h) * z * 0.7), 2)
        if id(o) in SETAS_FORA:
            sx = (o.x + o.w / 2 - self.cam[0]) * z + a.x
            sy = (o.y + o.h / 2 - self.cam[1]) * z + a.y
            if not a.inflate(-20, -20).collidepoint(sx, sy):
                cx, cy = a.center
                ang = math.atan2(sy - cy, sx - cx)
                bx = max(a.x + 24, min(a.right - 24, sx))
                by = max(a.y + 24, min(a.bottom - 24, sy))
                cor = getattr(o, "seta_cor", (255, 220, 80))
                pts = [(bx + math.cos(ang) * 14, by + math.sin(ang) * 14),
                       (bx + math.cos(ang + 2.5) * 10, by + math.sin(ang + 2.5) * 10),
                       (bx + math.cos(ang - 2.5) * 10, by + math.sin(ang - 2.5) * 10)]
                pygame.draw.polygon(tela, cor, pts)
                pygame.draw.polygon(tela, (20, 20, 20), pts, 2)


JogoExtras.desenhar_extra = _desenhar_extra_mais

# categorias no seletor
for _cat_m, _nomes_cm in CAT_COMP_MAIS.items():
    for _i_cm, (_nome_cat, _lista_cat) in enumerate(CATEGORIAS_COMPORTAMENTOS):
        if _nome_cat == _cat_m:      # mesma categoria: junta (sem repetir no seletor)
            CATEGORIAS_COMPORTAMENTOS[_i_cm] = (_nome_cat, list(_lista_cat) + list(_nomes_cm))
            break
    else:
        CATEGORIAS_COMPORTAMENTOS.append((_cat_m, list(_nomes_cm)))
OPCOES_PARAMS["comportamento"].extend(n for n in COMPORTAMENTOS if n not in OPCOES_PARAMS["comportamento"])
TOTAL_COMP_MAIS = len(REG_COMP)
