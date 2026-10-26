# Minha Engine - celular.py
# CELULAR (Android pelo app Pydroid 3) e telas de toque:
#  - toque vira clique; arrastar para cima/baixo rola as listas; segurar = botão direito
#  - dois dedos: arrastar move a câmera do editor e pinça dá zoom
#  - controles na tela durante o jogo (joystick + botões, com vários dedos ao mesmo tempo)
#  - teclado do celular abre sozinho quando precisa escrever
#  - tela cheia deitada, tamanho da interface ajustado à tela do celular, fontes do Android
# No PC nada muda (a não ser que você ligue "Controles de toque também no PC").
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

import time


def _eh_android():
    return (hasattr(sys, "getandroidapilevel") or "ANDROID_ROOT" in os.environ or "ANDROID_ARGUMENT" in os.environ
            or "ANDROID_DATA" in os.environ)


NO_CELULAR = _eh_android()
GERAL_PADRAO["toque_no_pc"] = False
NOMES_GERAL["toque_no_pc"] = ("Controles de toque também no PC (tela touch)",)
RESOLUCOES[:0] = ["Celular", "Celular nítido"]
if NO_CELULAR:
    APARENCIA_PADRAO["resolucao"] = "Celular"
    # tela deitada e sem o mouse "fantasma" atrasar os toques
    os.environ.setdefault("SDL_IOS_ORIENTATIONS", "LandscapeLeft LandscapeRight")
    os.environ.setdefault("SDL_ANDROID_TRAP_BACK_BUTTON", "1")
TOQUE_GESTO = pygame.USEREVENT + 21      # dois dedos: dx, dy (arrastar), fator (pinça), centro
APP_PAUSOU = pygame.USEREVENT + 22       # o app foi para o fundo (atendeu ligação, trocou de app...)


def modo_toque():
    return NO_CELULAR or bool(CONFIG.get("geral", {}).get("toque_no_pc"))


def flags_janela():
    if NO_CELULAR:
        return pygame.SCALED | pygame.FULLSCREEN
    return pygame.SCALED | pygame.RESIZABLE


def tamanho_celular(altura, minimo=1280):
    """Tamanho da interface com o mesmo formato da tela do aparelho (sem faixas pretas)."""
    try:
        info = pygame.display.Info()
        w, h = int(info.current_w), int(info.current_h)
    except (pygame.error, AttributeError, TypeError, ValueError):
        w, h = 0, 0
    if w <= 0 or h <= 0:
        return max(minimo, int(altura * 16 / 9)), altura
    w, h = max(w, h), min(w, h)          # sempre deitado
    return max(minimo, int(round(altura * w / h))), altura


_aplicar_resolucao_antiga = aplicar_resolucao


def aplicar_resolucao():
    global LARGURA, ALTURA, VIEW, TELA_INTEIRA
    res = str(CONFIG["aparencia"].get("resolucao", "1280x720"))
    if res in ("Celular", "Celular nítido"):
        LARGURA, ALTURA = tamanho_celular(900 if res == "Celular nítido" else 720)
        VIEW = pygame.Rect(PAINEL_ESQ, TOPO + ABAS_H, LARGURA - PAINEL_ESQ - PAINEL_DIR,
                           ALTURA - TOPO - ABAS_H - RODAPE)
        TELA_INTEIRA = pygame.Rect(0, 0, LARGURA, ALTURA)
    else:
        _aplicar_resolucao_antiga()
    suave = "0" if CONFIG["aparencia"].get("nitidez") == "Pixel" else "1"
    os.environ["SDL_HINT_RENDER_SCALE_QUALITY"] = suave
    os.environ["SDL_RENDER_SCALE_QUALITY"] = suave       # nome certo da dica do SDL


_alternar_tela_cheia_antiga = alternar_tela_cheia


def alternar_tela_cheia():
    if NO_CELULAR:          # no celular a engine já é sempre tela cheia
        return False
    return _alternar_tela_cheia_antiga()


_abrir_pasta_antiga = abrir_pasta


def abrir_pasta(pasta):
    if NO_CELULAR:
        try:
            os.makedirs(pasta, exist_ok=True)
        except OSError:
            pass
        AVISOS_CELULAR.append(f"A pasta fica em: {pasta}  (abra pelo gerenciador de arquivos do celular)")
        return
    _abrir_pasta_antiga(pasta)


AVISOS_CELULAR = []

# ---------------------------------------------------------------------
# Fontes do Android (as do Windows não existem no celular)
# ---------------------------------------------------------------------
_FONTES_ANDROID = {
    "normal": ["/system/fonts/Roboto-Regular.ttf", "/system/fonts/RobotoStatic-Regular.ttf",
               "/system/fonts/DroidSans.ttf", "/system/fonts/NotoSans-Regular.ttf"],
    "negrito": ["/system/fonts/Roboto-Bold.ttf", "/system/fonts/RobotoStatic-Bold.ttf",
                "/system/fonts/DroidSans-Bold.ttf", "/system/fonts/NotoSans-Bold.ttf"],
    "mono": ["/system/fonts/DroidSansMono.ttf", "/system/fonts/CutiveMono.ttf", "/system/fonts/RobotoMono-Regular.ttf",
             "/system/fonts/SourceCodePro-Regular.ttf"],
    "serif": ["/system/fonts/NotoSerif-Regular.ttf", "/system/fonts/DroidSerif-Regular.ttf"],
}


def _arquivo_fonte_android(familia, negrito):
    fam = str(familia).lower()
    tipo = "mono" if ("mono" in fam or "consol" in fam or "courier" in fam or "cascadia" in fam) else \
        ("serif" if ("serif" in fam and "sans" not in fam) or "times" in fam or "georgia" in fam else
         ("negrito" if negrito else "normal"))
    for caminho in _FONTES_ANDROID[tipo] + _FONTES_ANDROID["normal"]:
        if os.path.isfile(caminho):
            return caminho, tipo
    return None, tipo


_fonte_familia_antiga = fonte_familia


def fonte_familia(familia, tam, negrito=False, italico=False):
    if not NO_CELULAR:
        return _fonte_familia_antiga(familia, tam, negrito, italico)
    tam = max(6, min(200, int(num_seguro(tam, 16))))
    chave = ("android", familia, tam, negrito, italico)
    f = _fontes_familia.get(chave)
    if f is None:
        caminho, tipo = _arquivo_fonte_android(familia, negrito)
        try:
            f = pygame.font.Font(caminho, tam) if caminho else pygame.font.Font(None, int(tam * 1.25))
            if negrito and tipo != "negrito":
                f.set_bold(True)
            if italico:
                f.set_italic(True)
        except (pygame.error, OSError, TypeError, AttributeError):
            f = pygame.font.Font(None, int(tam * 1.25))
        _fontes_familia[chave] = f
    return f


# ---------------------------------------------------------------------
# Teclado do celular e Shift "grudado" (para selecionar vários com o dedo)
# ---------------------------------------------------------------------
_get_mods_original = pygame.key.get_mods
MODS_TOQUE = {"shift": False}


def _get_mods_toque():
    m = _get_mods_original()
    if MODS_TOQUE["shift"]:
        m |= pygame.KMOD_SHIFT
    return m


pygame.key.get_mods = _get_mods_toque
TECLADO = {"aberto": False, "queria": False}


def teclado_celular(abrir):
    """Abre/fecha o teclado na tela (só no celular; no PC o teclado já funciona sempre)."""
    if not NO_CELULAR or TECLADO["aberto"] == abrir:
        return
    try:
        if abrir:
            pygame.key.start_text_input()
        else:
            pygame.key.stop_text_input()
        TECLADO["aberto"] = abrir
    except (pygame.error, AttributeError):
        pass


def pedir_teclado(quer):
    """Chamado todo frame: abre o teclado quando a tela passa a precisar de texto e fecha quando não precisa."""
    if quer and not TECLADO["queria"]:
        teclado_celular(True)
    elif not quer and TECLADO["queria"]:
        teclado_celular(False)
    TECLADO["queria"] = quer


def _ev_toque(tipo, **k):
    k.setdefault("toque", True)
    return pygame.event.Event(tipo, **k)


def _tecla_ev(tipo, key, mod=0, unicode=""):
    return _ev_toque(tipo, key=key, mod=mod, unicode=unicode, scancode=0)


# =====================================================================
# O TOQUE: transforma dedos em cliques, rolagem, botão direito, gestos e controles do jogo
# =====================================================================
class Toque:
    MOVE = 14          # quanto o dedo anda até virar arrasto (pixels da interface)
    SEGURAR = 0.55     # segundos parado = botão direito

    def __init__(self):
        self.dedos = {}
        self.ultimo_dedo = -10.0
        self.areas_arrasto = []        # onde arrastar com 1 dedo é arrastar mesmo (cena, desenho...)
        self.pad = None                # (jogo, area) enquanto um jogo está rodando
        self.pad_dedos = {}            # dedo -> controle
        self.stick = None              # [dedo, cx, cy, dx, dy]
        self.seguradas = set()         # teclas seguradas pelos controles na tela
        self.controles_pad = []
        self.extras_cache = (None, [])
        self.tela = None
        self.saida = []

    # ----------------- coordenadas -----------------
    def pos(self, e):
        tela = self.tela or pygame.display.get_surface()
        if tela is None:
            return 0, 0
        lw, lh = tela.get_size()
        try:
            ww, wh = pygame.display.get_window_size()
        except (pygame.error, AttributeError):
            ww, wh = lw, lh
        if ww <= 0 or wh <= 0:
            return int(e.x * lw), int(e.y * lh)
        k = min(ww / lw, wh / lh)
        ox, oy = (ww - lw * k) / 2, (wh - lh * k) / 2
        return int((e.x * ww - ox) / k), int((e.y * wh - oy) / k)

    def sintetico(self, e):
        """Clique de mouse que o próprio SDL inventou a partir do dedo (a gente faz o nosso)."""
        if hasattr(e, "touch"):
            return bool(e.touch) and not getattr(e, "toque", False)
        return bool(self.dedos) or (time.time() - self.ultimo_dedo) < 0.2

    # ----------------- eventos -----------------
    def processar(self, eventos):
        self.saida = out = []
        agora = time.time()
        for e in eventos:
            t = e.type
            if t in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION) and self.sintetico(e):
                continue
            if t in (getattr(pygame, "APP_WILLENTERBACKGROUND", -1), getattr(pygame, "APP_DIDENTERBACKGROUND", -1)):
                out.append(_ev_toque(APP_PAUSOU))
                self.dedos.clear()
                self.soltar_tudo()
                continue
            if t == getattr(pygame, "FINGERDOWN", -1):
                self.ultimo_dedo = agora
                self.dedo_desceu(e, agora)
            elif t == getattr(pygame, "FINGERMOTION", -1):
                self.ultimo_dedo = agora
                self.dedo_mexeu(e)
            elif t == getattr(pygame, "FINGERUP", -1):
                self.ultimo_dedo = agora
                self.dedo_subiu(e)
            elif t == getattr(pygame, "TEXTINPUT", -1) and NO_CELULAR:
                for ch in e.text:
                    out.append(_tecla_ev(pygame.KEYDOWN, 0, 0, ch))
            elif t in (pygame.KEYDOWN, pygame.KEYUP) and NO_CELULAR and \
                    e.key == getattr(pygame, "K_AC_BACK", -999):
                out.append(_tecla_ev(t, pygame.K_ESCAPE))           # botão voltar do Android = Esc
            elif t == pygame.KEYDOWN and NO_CELULAR and getattr(e, "unicode", "") and e.unicode.isprintable() \
                    and not (e.mod & pygame.KMOD_CTRL) and not getattr(e, "toque", False):
                out.append(_tecla_ev(pygame.KEYDOWN, e.key, e.mod, ""))  # o texto vem pelo TEXTINPUT
            elif self.pad and modo_toque() and t == pygame.MOUSEBUTTONDOWN and e.button == 1 and \
                    self.pad_tocar("mouse", e.pos):
                continue                                             # mouse do PC apertando o controle na tela
            elif self.pad and t == pygame.MOUSEMOTION and "mouse" in self.pad_dedos:
                self.pad_mover("mouse", e.pos)
            elif self.pad and t == pygame.MOUSEBUTTONUP and e.button == 1 and "mouse" in self.pad_dedos:
                self.pad_soltar("mouse")
                continue
            else:
                out.append(e)
        self.checar_segurar(agora)
        self.atualizar_teclas()
        return out

    def dedo_desceu(self, e, agora):
        p = self.pos(e)
        if self.pad and self.pad_tocar(e.finger_id, p):
            return
        livres = [d for d in self.dedos.values() if d["modo"] not in ("pad", "fim")]
        d = {"x": p[0], "y": p[1], "x0": p[0], "y0": p[1], "t0": agora, "modo": None, "acc": 0.0}
        self.dedos[e.finger_id] = d
        if len(livres) == 1 and not self.pad:      # segundo dedo: começa a pinça / arrasto com 2 dedos
            outro = livres[0]
            if outro["modo"] == "arrasto":
                self.saida.append(_ev_toque(pygame.MOUSEBUTTONUP, pos=(outro["x"], outro["y"]), button=1))
            outro["modo"] = d["modo"] = "pinca"
            d["par"] = outro

    def dedo_mexeu(self, e):
        if e.finger_id in self.pad_dedos:
            self.pad_mover(e.finger_id, self.pos(e))
            return
        d = self.dedos.get(e.finger_id)
        if d is None:
            return
        p = self.pos(e)
        ant = (d["x"], d["y"])
        d["x"], d["y"] = p
        modo = d["modo"]
        if modo == "pinca":
            outro = d.get("par") or next((o for o in self.dedos.values() if o is not d and o["modo"] == "pinca"),
                                         None)
            if outro is None:
                return
            c_ant = ((ant[0] + outro["x"]) / 2, (ant[1] + outro["y"]) / 2)
            c_novo = ((p[0] + outro["x"]) / 2, (p[1] + outro["y"]) / 2)
            dist_ant = math.hypot(ant[0] - outro["x"], ant[1] - outro["y"]) or 1
            dist_nova = math.hypot(p[0] - outro["x"], p[1] - outro["y"]) or 1
            self.saida.append(_ev_toque(TOQUE_GESTO, dx=c_novo[0] - c_ant[0], dy=c_novo[1] - c_ant[1],
                                  fator=dist_nova / dist_ant, centro=(int(c_novo[0]), int(c_novo[1]))))
        elif modo is None:
            dx, dy = p[0] - d["x0"], p[1] - d["y0"]
            if abs(dx) + abs(dy) < self.MOVE:
                return
            inicio = (d["x0"], d["y0"])
            pode_arrastar = self.pad is not None or any(r.collidepoint(inicio) for r in self.areas_arrasto)
            if not pode_arrastar and abs(dy) >= abs(dx):
                d["modo"] = "rolar"
                d["acc"] = dy
            else:
                d["modo"] = "arrasto"
                self.saida.append(_ev_toque(pygame.MOUSEMOTION, pos=inicio, rel=(0, 0), buttons=(0, 0, 0)))
                self.saida.append(_ev_toque(pygame.MOUSEBUTTONDOWN, pos=inicio, button=1))
                self.saida.append(_ev_toque(pygame.MOUSEMOTION, pos=p, rel=(dx, dy), buttons=(1, 0, 0)))
        elif modo == "rolar":
            d["acc"] += p[1] - ant[1]
            while abs(d["acc"]) >= 36:
                passo = 1 if d["acc"] > 0 else -1
                d["acc"] -= passo * 36
                self.saida.append(_ev_toque(pygame.MOUSEWHEEL, x=0, y=passo, flipped=False, pos=p))
        elif modo == "arrasto":
            self.saida.append(_ev_toque(pygame.MOUSEMOTION, pos=p, rel=(p[0] - ant[0], p[1] - ant[1]),
                                  buttons=(1, 0, 0)))

    def dedo_subiu(self, e):
        if e.finger_id in self.pad_dedos:
            self.pad_soltar(e.finger_id)
            return
        d = self.dedos.pop(e.finger_id, None)
        if d is None:
            return
        p = (d["x"], d["y"])
        if d["modo"] is None:           # toque rápido = clique
            self.saida.append(_ev_toque(pygame.MOUSEMOTION, pos=p, rel=(0, 0), buttons=(0, 0, 0)))
            self.saida.append(_ev_toque(pygame.MOUSEBUTTONDOWN, pos=p, button=1))
            self.saida.append(_ev_toque(pygame.MOUSEBUTTONUP, pos=p, button=1))
        elif d["modo"] == "arrasto":
            self.saida.append(_ev_toque(pygame.MOUSEBUTTONUP, pos=p, button=1))
        elif d["modo"] == "pinca":
            for o in self.dedos.values():
                if o["modo"] == "pinca":
                    o["modo"] = "fim"       # o outro dedo não vira clique quando soltar

    def checar_segurar(self, agora):
        for d in self.dedos.values():
            if d["modo"] is None and agora - d["t0"] >= self.SEGURAR and not self.pad:
                d["modo"] = "longo"
                p = (d["x"], d["y"])
                self.saida.append(_ev_toque(pygame.MOUSEMOTION, pos=p, rel=(0, 0), buttons=(0, 0, 0)))
                self.saida.append(_ev_toque(pygame.MOUSEBUTTONDOWN, pos=p, button=3))
                self.saida.append(_ev_toque(pygame.MOUSEBUTTONUP, pos=p, button=3))

    # =================================================================
    # CONTROLES NA TELA (joystick + botões) durante o jogo
    # =================================================================
    def usar_pad(self, jogo, area):
        if not modo_toque() or jogo is None:
            if self.pad is not None:
                self.soltar_tudo()
            self.pad = None
            return
        a = pygame.Rect(area.x, area.y, area.w, area.h)
        self.pad = (jogo, a)
        self.controles_pad = self.montar_controles(jogo, a)

    def soltar_tudo(self):
        self.pad_dedos.clear()
        self.stick = None
        self.atualizar_teclas()

    def teclas_extras(self, jogo):
        """Teclas que os scripts/eventos do jogo usam (vira botão na tela)."""
        if self.extras_cache[0] is jogo:
            return self.extras_cache[1]
        usadas = []
        fontes = []
        for fase in jogo.dados.get("fases", {}).values():
            fontes.append(fase.get("cena", {}))
            fontes += fase.get("objetos", [])
        fontes += list(jogo.dados.get("modelos", {}).values())
        padrao = re.compile(r'(?:tecla|apertou|soltou)\s*\(\s*"([^"]+)"|quando\s+(?:tecla|soltar)\s+"([^"]+)"')
        for d in fontes:
            for m in padrao.finditer(str(d.get("script", "") or "")):
                usadas.append(m.group(1) or m.group(2))
            for ev in d.get("eventos", []) or []:
                if ev.get("gatilho") in ("Tecla apertada", "Tecla solta"):
                    usadas.append((ev.get("gp") or {}).get("tecla", ""))
                for c in ev.get("condicoes", []) or []:
                    if c.get("t") in ("Tecla segurada", "Tecla acabou de ser apertada"):
                        usadas.append((c.get("p") or {}).get("tecla", ""))
        cobertas = set()
        for acao in ("esquerda", "direita", "cima", "baixo", "pular", "acao", "pausa", "reiniciar", "debug"):
            cobertas.update(acao_jogo(acao))
        extras = []
        for nome in usadas:
            nome = str(nome).strip().lower()
            cod = codigo_tecla(nome) if nome else None
            if cod is None or cod in cobertas or nome in ("shift", "f", "j") or any(n == nome for n, _ in extras):
                continue
            extras.append((nome, cod))
        self.extras_cache = (jogo, extras[:4])
        return extras[:4]

    def montar_controles(self, jogo, a):
        """Lista de botões: (id, centro, raio, rótulo, tecla)."""
        p = jogo.player if getattr(jogo, "player", None) is not None and jogo.player.vivo else None
        td = bool(jogo.cena.get("visao_de_cima"))
        rb = max(26, int(a.h * 0.085))
        botoes = []
        if p is not None and not td:
            botoes.append(("pular", "PULAR", acao_jogo("pular")[0]))
        if p is not None and p.d.get("espada"):
            botoes.append(("espada", "ESPADA", codigo_tecla(str(p.d.get("tecla_espada", "j") or "j"))))
        if p is not None and str(p.d.get("tiro", "") or "").strip():
            botoes.append(("tiro", "TIRO", codigo_tecla(str(p.d.get("tecla_tiro", "f") or "f"))))
        if p is not None and p.d.get("dash"):
            botoes.append(("dash", "DASH", pygame.K_LSHIFT))
        if getattr(jogo, "dialogo", None) is not None or any(o.tipo == "NPC" and o.vivo for o in jogo.objs):
            botoes.append(("acao", "FALAR", acao_jogo("acao")[0]))
        for nome, cod in self.teclas_extras(jogo):
            botoes.append(("x_" + nome, nome.upper()[:6], cod))
        vagas = [(-1.25, -1.25), (-3.55, -0.95), (-1.0, -3.55), (-3.4, -3.35), (-5.85, -0.95), (-5.6, -3.3),
                 (-1.0, -5.85), (-3.3, -5.65), (-7.9, -0.95)]
        controles = []
        for (bid, rot, cod), (vx, vy) in zip(botoes, vagas):
            if cod is None:
                continue
            controles.append((bid, (int(a.right + vx * rb), int(a.bottom + vy * rb)), rb, rot, cod))
        rp = max(18, int(rb * 0.62))
        controles.append(("pausa", (a.right - rp - 10, a.y + rp + 10), rp, "II", acao_jogo("pausa")[0]))
        if jogo.venceu or jogo.perdeu:
            controles.append(("reiniciar", (a.centerx, a.bottom - rb - 14), rb, "DE NOVO",
                              acao_jogo("reiniciar")[0]))
        return controles

    def zona_stick(self):
        _jogo, a = self.pad
        return pygame.Rect(a.x, a.y + int(a.h * 0.18), int(a.w * 0.42), int(a.h * 0.82))

    def pad_tocar(self, dedo, pos):
        for c in self.controles_pad:
            bid, (cx, cy), r, _rot, _cod = c
            if math.hypot(pos[0] - cx, pos[1] - cy) <= r * 1.15:
                self.pad_dedos[dedo] = bid
                return True
        if self.stick is None and self.zona_stick().collidepoint(pos):
            self.stick = [dedo, pos[0], pos[1], 0.0, 0.0]
            self.pad_dedos[dedo] = "stick"
            return True
        return False

    def pad_mover(self, dedo, pos):
        if self.pad_dedos.get(dedo) == "stick" and self.stick and self.stick[0] == dedo:
            _jogo, a = self.pad
            raio = max(40, a.h * 0.12)
            dx, dy = pos[0] - self.stick[1], pos[1] - self.stick[2]
            n = math.hypot(dx, dy)
            if n > raio:      # o centro acompanha o dedo (joystick flutuante)
                self.stick[1] += dx - dx / n * raio
                self.stick[2] += dy - dy / n * raio
                dx, dy = dx / n * raio, dy / n * raio
            self.stick[3], self.stick[4] = dx / raio, dy / raio

    def pad_soltar(self, dedo):
        bid = self.pad_dedos.pop(dedo, None)
        if bid == "stick":
            self.stick = None

    def atualizar_teclas(self):
        novas = set()
        if self.pad:
            jogo, _a = self.pad
            td = bool(jogo.cena.get("visao_de_cima"))
            if self.stick:
                sx, sy = self.stick[3], self.stick[4]
                if sx < -0.38:
                    novas.add(acao_jogo("esquerda")[0])
                if sx > 0.38:
                    novas.add(acao_jogo("direita")[0])
                if sy > 0.5 if not td else sy > 0.38:
                    novas.add(acao_jogo("baixo")[0])
                if td and sy < -0.38:
                    novas.add(acao_jogo("cima")[0])
            por_id = {c[0]: c[4] for c in self.controles_pad}
            for bid in self.pad_dedos.values():
                if bid in por_id and por_id[bid] is not None:
                    novas.add(por_id[bid])
        for k in novas - self.seguradas:
            self.saida.append(_tecla_ev(pygame.KEYDOWN, k))
        for k in self.seguradas - novas:
            self.saida.append(_tecla_ev(pygame.KEYUP, k))
        self.seguradas = novas

    def desenhar_pad(self, t):
        if not self.pad or not modo_toque():
            return
        _jogo, a = self.pad
        camada = pygame.Surface(t.get_size(), pygame.SRCALPHA)
        apertados = set(self.pad_dedos.values())
        for bid, (cx, cy), r, rot, _cod in self.controles_pad:
            ativo = bid in apertados
            pygame.draw.circle(camada, (255, 255, 255, 120 if ativo else 55), (cx, cy), r)
            pygame.draw.circle(camada, (255, 255, 255, 170), (cx, cy), r, 3)
            img = fonte(max(11, int(r * (0.42 if len(rot) <= 3 else 0.3))), True).render(rot, True, (255, 255, 255))
            img.set_alpha(230)
            camada.blit(img, (cx - img.get_width() // 2, cy - img.get_height() // 2))
        raio = max(40, a.h * 0.12)
        if self.stick:
            _d, cx, cy, sx, sy = self.stick
        else:
            z = self.zona_stick()
            cx, cy, sx, sy = z.x + raio + 30, z.bottom - raio - 30, 0.0, 0.0
        pygame.draw.circle(camada, (255, 255, 255, 45), (int(cx), int(cy)), int(raio))
        pygame.draw.circle(camada, (255, 255, 255, 140), (int(cx), int(cy)), int(raio), 3)
        pygame.draw.circle(camada, (255, 255, 255, 150 if self.stick else 90),
                           (int(cx + sx * raio), int(cy + sy * raio)), int(raio * 0.45))
        t.blit(camada, (0, 0))


TOQUE = Toque()


def pegar_eventos(tela=None):
    """Use no lugar de pygame.event.get(): no celular transforma os toques."""
    eventos = pygame.event.get()
    if not modo_toque():
        return eventos
    TOQUE.tela = tela or pygame.display.get_surface()
    return TOQUE.processar(eventos)


_misturar_antigo = Controles.misturar


def _misturar_com_toque(self, teclas):
    teclas = _misturar_antigo(self, teclas)
    if TOQUE.seguradas:
        return TeclasMisturadas(teclas, set(TOQUE.seguradas))
    return teclas


Controles.misturar = _misturar_com_toque


def gesto_para_rodinha(e, tratar):
    """Arrastar com 2 dedos fora da cena = rodinha do mouse."""
    passos = int(e.dy / 30)
    if passos:
        tratar(pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=passos, flipped=False, toque=True))


# =====================================================================
# EDITOR NO CELULAR: barra de toque (teclado, apagar, duplicar, copiar, colar, selecionar vários...)
# =====================================================================
class EditorToque:
    BARRA_TOQUE = [("teclado", "Teclado"), ("apagar", "Apagar"), ("duplicar", "Duplicar"), ("copiar", "Copiar"),
                   ("colar", "Colar"), ("varios", "Vários"), ("tudo", "Tudo"), ("esc", "Fechar")]

    def rects_barra_toque(self):
        if not modo_toque() or self.jogo:
            return []
        w, h, gap = 74, 38, 5
        x = VIEW.right - (w + gap) * len(self.BARRA_TOQUE) - 4
        y = VIEW.bottom - h - 6
        return [(pygame.Rect(x + i * (w + gap), y, w, h), bid, rot) for i, (bid, rot) in enumerate(self.BARRA_TOQUE)]

    def desenhar_barra_toque(self, t, mouse):
        rects = self.rects_barra_toque()
        if not rects:
            return
        r0, r1 = rects[0][0], rects[-1][0]
        fundo = pygame.Rect(r0.x - 5, r0.y - 5, r1.right - r0.x + 10, r0.h + 10)
        sombra = pygame.Surface(fundo.size, pygame.SRCALPHA)
        sombra.fill((10, 12, 18, 170))
        t.blit(sombra, fundo.topleft)
        for r, bid, rot in rects:
            ligado = (bid == "varios" and MODS_TOQUE["shift"]) or (bid == "teclado" and TECLADO["aberto"])
            desenhar_botao(t, self.fp, r, rot, mouse, cor=C_DESTAQUE if ligado else (58, 62, 78))
        while AVISOS_CELULAR:
            self.avisar(AVISOS_CELULAR.pop(0))

    def clique_barra_toque(self, pos):
        for r, bid, _rot in self.rects_barra_toque():
            if not r.collidepoint(pos):
                continue
            ctrl = pygame.KMOD_CTRL
            if bid == "teclado":
                teclado_celular(not TECLADO["aberto"])
                if not NO_CELULAR:
                    self.avisar("O teclado do celular abre aqui. No PC use o teclado normal.")
            elif bid == "varios":
                MODS_TOQUE["shift"] = not MODS_TOQUE["shift"]
                self.avisar("Selecionar vários: LIGADO (toque nos objetos para juntar)" if MODS_TOQUE["shift"]
                            else "Selecionar vários: desligado")
            else:
                key, mod = {"apagar": (pygame.K_DELETE, 0), "duplicar": (pygame.K_d, ctrl),
                            "copiar": (pygame.K_c, ctrl), "colar": (pygame.K_v, ctrl), "tudo": (pygame.K_a, ctrl),
                            "esc": (pygame.K_ESCAPE, 0)}[bid]
                self.tecla(_tecla_ev(pygame.KEYDOWN, key, mod))
            return True
        return False

    def quer_texto(self):
        return bool(self.prompt or self.seletor or self.editando or
                    (self.aba == "script" and not self.jogo and self.cod_alvo is not None) or
                    (self.aba == "loja" and getattr(self.loja, "digitando", False)))

    def preparar_toque(self):
        """Todo frame: onde o dedo arrasta de verdade, controles do jogo e teclado."""
        if not modo_toque():
            return
        areas = []
        if not (self.menu or self.prompt or self.seletor):
            if self.aba in ("cena", "desenho"):
                areas.append(VIEW)
        TOQUE.areas_arrasto = areas
        TOQUE.usar_pad(self.jogo, self.jogo.area if self.jogo else VIEW)
        pedir_teclado(self.quer_texto())

    def gesto_toque(self, e):
        """Dois dedos: na cena move a câmera e dá zoom; no resto rola."""
        if self.jogo:
            return
        cx, cy = e.centro
        if self.aba == "cena" and VIEW.collidepoint((cx, cy)) and not self.menu and not self.seletor:
            self.cam[0] -= e.dx / self.zoom
            self.cam[1] -= e.dy / self.zoom
            if abs(e.fator - 1) > 0.002:
                self.mudar_zoom(e.fator, (cx, cy))
        else:
            gesto_para_rodinha(e, self.evento)
