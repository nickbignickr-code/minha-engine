# Minha Engine - jogo_objetos.py
# os objetos dentro do jogo rodando (ObjJogo) e o dono da cena
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# RUNTIME (o jogo rodando quando aperta PLAY)
# =====================================================================
class ObjJogo:
    PROPS = ("x", "y", "vx", "vy", "w", "h")
    PROTEGIDAS = {"tipo", "eventos", "script", "valores", "modelo"}
    eh_cena = False

    def __init__(self, d):
        self.d = d
        self.tipo = d["tipo"]
        self.x = float(num_seguro(d.get("x", 0)))
        self.y = float(num_seguro(d.get("y", 0)))
        self.w = float(num_seguro(d.get("w", 40), 40))
        self.h = float(num_seguro(d.get("h", 40), 40))
        self.vx = 0.0
        self.vy = 0.0
        self.vivo = True
        self.na_tela = bool(d.get("na_tela"))
        self.visivel = bool(d.get("visivel", True)) and self.tipo != "Zona"
        self.chao = False
        self.apoio = None
        self.ult_dx = 0.0
        self.ult_dy = 0.0
        self.prog = 0.0
        self.dir_plat = 1
        self.inicio_x = self.x
        self.inicio_y = self.y
        self.base_y = self.y
        self.t = 0.0
        self.ativado = False
        self.perto = False
        self.progresso = None
        self.texto_atual = None
        self.movel = (bool(d.get("gravidade")) or self.tipo in ("Player", "Inimigo")) and not self.na_tela
        if self.tipo == "Inimigo":
            self.vx = abs(num_seguro(d.get("velocidade", 100), 100))
        # parte de programacao
        valores = d.get("valores", {})
        self.vars = copy.deepcopy(valores) if isinstance(valores, dict) else {}
        self.escopo = None
        self.handlers = []
        self.tocando = {}
        self.timers = {}
        self.quer_toque = False
        self.avisou_morte = False
        self.fala = ""
        self.fala_t = 0.0
        self.coyote = 0.0
        self.buffer_pulo = 0.0
        self.pulos_restantes = 0
        self.piscar_t = 0.0
        self.flash_t = 0.0
        self.flash_dur = 0.12
        self.squash_t = 0.0
        self.invencivel_t = 0.0
        self.grupos = {g.strip() for g in str(d.get("grupo", "") or "").split(",") if g.strip()}
        self.comp = {}          # comportamentos ja com os valores calculados
        self.comp_off = set()   # comportamentos desligados por acao/script
        self.gerados = []
        self.sen_base = None
        self.fade_t = 0.0
        self.ouve = None        # eventos que este objeto escuta (para pular rapido os outros)
        self.n_handlers = -1

    def imagem_atual(self, tempo):
        """Escolhe o quadro da animacao (lista de imagens separadas por virgula)."""
        anim = ""
        if self.tipo == "Player":
            if not self.chao and self.d.get("anim_pulando"):
                anim = self.d["anim_pulando"]
            elif abs(self.vx) > 5 and self.d.get("anim_andando"):
                anim = self.d["anim_andando"]
        if not anim:
            anim = self.d.get("animacao", "") or ""
        quadros = [q.strip() for q in str(anim).split(",") if q.strip()]
        if not quadros:
            return None
        fps = max(0.1, num_seguro(self.d.get("fps_anim", 8), 8))
        return quadros[int(tempo * fps) % len(quadros)]

    def brasa_get(self, n):
        if n in self.PROPS:
            return limpar(getattr(self, n))
        if n == "nome":
            return self.d.get("nome", "")
        if n == "tipo":
            return self.tipo
        if n == "vivo":
            return self.vivo
        if n == "no_chao":
            return self.chao
        if n == "visivel":
            return self.visivel
        if n == "cor":
            return list(self.d.get("cor", [255, 255, 255]))
        if n in self.d and n not in self.PROTEGIDAS:
            return self.d[n]
        return self.vars.get(n, 0)

    def brasa_set(self, n, v):
        if n in self.PROPS:
            setattr(self, n, float(num(v)))
            if n == "y":
                self.base_y = self.y
            if n in ("vx", "vy"):
                self.movel = True
        elif n == "cor" or n in ("cor_texto", "cor_fundo"):
            if not isinstance(v, list) or len(v) < 3:
                raise ErroBrasa("A cor precisa ser uma lista: [vermelho, verde, azul]")
            self.d[n] = [num(c) for c in v[:3]]
        elif n == "nome":
            self.d["nome"] = texto(v)
        elif n == "visivel":
            self.visivel = verdade(v)
        elif n in ("solido", "gravidade", "espelhar", "na_tela", "empurravel"):
            self.d[n] = verdade(v)
            if n == "gravidade" and self.d[n]:
                self.movel = True
            if n == "na_tela":
                self.na_tela = self.d[n]
        elif n in ("tipo", "vivo", "no_chao"):
            raise ErroBrasa(f"'{n}' só pode ser lido, não alterado")
        elif n == "grupo":
            self.d["grupo"] = texto(v)
            self.grupos = {g.strip() for g in self.d["grupo"].split(",") if g.strip()}
        elif n in self.d and n not in self.PROTEGIDAS:
            antigo = self.d[n]
            if isinstance(antigo, (int, float)) and not isinstance(antigo, bool):
                self.d[n] = num(v)
            elif isinstance(antigo, str):
                self.d[n] = texto(v)
            else:
                self.d[n] = v
        else:
            self.vars[n] = v

    def brasa_nome(self):
        return self.d.get("nome", self.tipo)

    def tem(self, nome):
        return nome in self.comp and nome not in self.comp_off


class CenaDono:
    """A cena tambem pode ter eventos e script (globais)."""
    eh_cena = True
    na_tela = False

    def __init__(self, cena):
        self.d = cena
        self.tipo = "Cena"
        self.vivo = True
        self.visivel = False
        self.vars = {}
        self.escopo = None
        self.handlers = []
        self.timers = {}
        self.fala = ""
        self.fala_t = 0.0
        self.ouve = None
        self.n_handlers = -1

    def brasa_get(self, n):
        return self.vars.get(n, 0)

    def brasa_set(self, n, v):
        self.vars[n] = v

    def brasa_nome(self):
        return "Cena"
