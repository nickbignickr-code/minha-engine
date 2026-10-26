# Minha Engine - sistemas.py
# grade espacial, controle (gamepad) e plugins
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Grade espacial: cada objeto so testa colisao com os vizinhos (muito mais rapido)
# ---------------------------------------------------------------------
class GradeEspacial:
    def __init__(self, tam=128):
        self.tam = tam
        self.celulas = {}
        self.grandes = []

    def por(self, o):
        t = self.tam
        x0, x1 = int(o.x // t), int((o.x + o.w) // t)
        y0, y1 = int(o.y // t), int((o.y + o.h) // t)
        if x0 == x1 and y0 == y1:          # o caso mais comum: cabe numa celula so
            lista = self.celulas.get((x0, y0))
            if lista is None:
                self.celulas[(x0, y0)] = [o]
            else:
                lista.append(o)
            return
        if (x1 - x0 + 1) * (y1 - y0 + 1) > 300:   # objetos enormes (chao gigante) ficam numa lista a parte
            self.grandes.append(o)
            return
        cel = self.celulas
        for cx in range(x0, x1 + 1):
            for cy in range(y0, y1 + 1):
                lista = cel.get((cx, cy))
                if lista is None:
                    cel[(cx, cy)] = [o]
                else:
                    lista.append(o)

    def perto(self, x, y, w, h, margem=2.0):
        t = self.tam
        res = list(self.grandes)
        vistos = set(map(id, res))
        cel = self.celulas
        for cx in range(int((x - margem) // t), int((x + w + margem) // t) + 1):
            for cy in range(int((y - margem) // t), int((y + h + margem) // t) + 1):
                for o in cel.get((cx, cy), ()):
                    i = id(o)
                    if i not in vistos:
                        vistos.add(i)
                        res.append(o)
        return res


def linha_livre(x1, y1, x2, y2, obstaculos, ignorar=()):
    """Verdadeiro se o segmento (x1,y1)-(x2,y2) nao cruza nenhum retangulo (Liang-Barsky)."""
    dx, dy = x2 - x1, y2 - y1
    for o in obstaculos:
        if o in ignorar:
            continue
        t0, t1 = 0.0, 1.0
        ok = True
        for p, q in ((-dx, x1 - o.x), (dx, o.x + o.w - x1), (-dy, y1 - o.y), (dy, o.y + o.h - y1)):
            if p == 0:
                if q < 0:
                    ok = False
                    break
            else:
                r = q / p
                if p < 0:
                    t0 = max(t0, r)
                else:
                    t1 = min(t1, r)
                if t0 > t1:
                    ok = False
                    break
        if ok:
            return False
    return True


# ---------------------------------------------------------------------
# Controle (gamepad): analógico/direcional anda, A pula, B fala, Start pausa
# ---------------------------------------------------------------------
class Controles:
    BOTOES = {0: "pular", 1: "acao", 2: "acao", 7: "pausa", 9: "pausa"}

    def __init__(self):
        self.js = {}
        try:
            pygame.joystick.init()
            for i in range(pygame.joystick.get_count()):
                self.conectar(i)
        except (pygame.error, AttributeError):
            pass

    def conectar(self, indice):
        try:
            j = pygame.joystick.Joystick(indice)
            j.init()
            self.js[j.get_instance_id()] = j
        except (pygame.error, AttributeError):
            pass

    def evento(self, e, apertadas, soltas):
        tipo = e.type
        if tipo == getattr(pygame, "JOYDEVICEADDED", -1):
            self.conectar(e.device_index)
        elif tipo == getattr(pygame, "JOYDEVICEREMOVED", -1):
            self.js.pop(getattr(e, "instance_id", None), None)
        elif tipo == getattr(pygame, "JOYBUTTONDOWN", -1) and e.button in self.BOTOES:
            apertadas.update(acao_jogo(self.BOTOES[e.button])[:1])
        elif tipo == getattr(pygame, "JOYBUTTONUP", -1) and e.button in self.BOTOES:
            soltas.update(acao_jogo(self.BOTOES[e.button])[:1])

    def misturar(self, teclas):
        if not self.js:
            return teclas
        extra = set()
        for j in self.js.values():
            try:
                ax = j.get_axis(0) if j.get_numaxes() > 0 else 0
                ay = j.get_axis(1) if j.get_numaxes() > 1 else 0
                hx, hy = j.get_hat(0) if j.get_numhats() > 0 else (0, 0)
                if ax < -0.4 or hx < 0:
                    extra.update(acao_jogo("esquerda")[:1])
                if ax > 0.4 or hx > 0:
                    extra.update(acao_jogo("direita")[:1])
                if ay < -0.4 or hy > 0:
                    extra.update(acao_jogo("cima")[:1])
                if ay > 0.4 or hy < 0:
                    extra.update(acao_jogo("baixo")[:1])
                for b, acao in self.BOTOES.items():
                    if b < j.get_numbuttons() and j.get_button(b):
                        extra.update(acao_jogo(acao)[:1])
            except pygame.error:
                continue
        return TeclasMisturadas(teclas, extra) if extra else teclas


class TeclasMisturadas:
    def __init__(self, base, extra):
        self.base = base
        self.extra = extra

    def __getitem__(self, k):
        return k in self.extra or bool(self.base[k])


class SemTeclas(dict):
    def __getitem__(self, k):
        return self.get(k, False)


# ---------------------------------------------------------------------
# Plugins (API para criar funcoes novas em Python)
# ---------------------------------------------------------------------
PLUGIN_FUNCOES = {}


class APIPlugin:
    """O que um plugin recebe em registrar(api)."""

    def funcao(self, nome, fn, descricao=""):
        if not str(nome).isidentifier():
            raise ValueError(f"nome de função inválido: {nome}")
        PLUGIN_FUNCOES[str(nome)] = (fn, descricao)


def preparar_pastas():
    for pasta in (PASTA_IMAGENS, PASTA_PLUGINS, PASTA_SONS):
        try:
            os.makedirs(pasta, exist_ok=True)
        except OSError:
            pass
    try:
        if os.path.isdir(PASTA_PLUGINS) and not any(f.endswith(".py") for f in os.listdir(PASTA_PLUGINS)):
            with open(os.path.join(PASTA_PLUGINS, "exemplo_plugin.py"), "w", encoding="utf-8") as f:
                f.write(EXEMPLO_PLUGIN)
    except OSError:
        pass


def carregar_plugins():
    PLUGIN_FUNCOES.clear()
    erros = []
    if not os.path.isdir(PASTA_PLUGINS):
        return erros
    api = APIPlugin()
    for arq in sorted(os.listdir(PASTA_PLUGINS)):
        if not arq.endswith(".py"):
            continue
        try:
            spec = importlib.util.spec_from_file_location("plugin_" + arq[:-3], os.path.join(PASTA_PLUGINS, arq))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "registrar"):
                mod.registrar(api)
        except Exception as ex:  # um plugin com erro nao pode derrubar a engine
            erros.append(f"{arq}: {ex}")
    return erros


def plugin_seguro(nome, fn):
    def chamar(*args):
        try:
            return fn(*args)
        except (ErroBrasa, Retorno, Parar, Continuar):
            raise
        except Exception as ex:
            raise ErroBrasa(f"Erro no plugin '{nome}': {ex}")
    return chamar


JANELA = {"cheia": False}


def alternar_tela_cheia():
    try:
        pygame.display.toggle_fullscreen()
        JANELA["cheia"] = not JANELA["cheia"]
        return True
    except pygame.error:
        return False
