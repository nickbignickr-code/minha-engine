# Minha Engine - linguagem_brasa.py
# a linguagem Brasa: tokenizador, parser e interpretador
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# LINGUAGEM BRASA - interpretador
# =====================================================================
PALAVRAS = {"var", "se", "senao", "enquanto", "repetir", "para", "de", "ate", "funcao", "retornar",
            "quando", "e", "ou", "nao", "verdadeiro", "falso", "nulo", "parar", "continuar", "em"}
EVENTOS_SCRIPT = {"iniciar": False, "frame": False, "cada": True, "tecla": True, "soltar": True,
                  "tocar": True, "parar_tocar": True, "pousar": False, "clique": False, "clique_tela": False,
                  "destruido": False, "moeda": False, "item": False, "respawn": False, "vitoria": False,
                  "dano": False, "sem_vida": False, "fim_dialogo": False}
LIMITE_PASSOS = 200000

RE_TOKEN = re.compile(r"""
 (?P<num>\d+\.\d+|\d+)
|(?P<str>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')
|(?P<nome>[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*)
|(?P<op>==|!=|<=|>=|\+=|-=|\*=|/=|[-+*/%<>=(),.:\[\]])
""", re.X)


class ErroBrasa(Exception):
    def __init__(self, msg, linha=None):
        super().__init__(msg)
        self.msg = msg
        self.linha = linha

    def __str__(self):
        return f"Linha {self.linha}: {self.msg}" if self.linha else self.msg


class Retorno(Exception):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor


class Parar(Exception):
    pass


class Continuar(Exception):
    pass


def tokenizar(texto, linha):
    toks = []
    i, n = 0, len(texto)
    while i < n:
        ch = texto[i]
        if ch in " \t":
            i += 1
            continue
        if ch == "#" or texto.startswith("//", i):
            break
        m = RE_TOKEN.match(texto, i)
        if not m:
            if ch in "\"'":
                raise ErroBrasa("Texto sem fechar as aspas", linha)
            raise ErroBrasa(f"Caractere estranho: '{ch}'", linha)
        k = m.lastgroup
        v = m.group(k)
        if k == "num":
            v = float(v) if "." in v else int(v)
        elif k == "str":
            v = v[1:-1].replace("\\n", "\n").replace('\\"', '"').replace("\\'", "'")
        elif k == "nome" and v in PALAVRAS:
            k = "kw"
        toks.append((k, v))
        i = m.end()
    return toks


class Parser:
    """Le as expressoes (contas, comparacoes, chamadas...)."""

    def __init__(self, toks, linha):
        self.t = toks
        self.i = 0
        self.linha = linha

    def ver(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else ("fim", None)

    def prox(self):
        tok = self.ver()
        self.i += 1
        return tok

    def fim(self):
        return self.i >= len(self.t)

    def e_op(self, v):
        tok = self.ver()
        return tok[0] == "op" and tok[1] == v

    def e_kw(self, v):
        tok = self.ver()
        return tok[0] == "kw" and tok[1] == v

    def esperar_op(self, v):
        if not self.e_op(v):
            achou = self.ver()[1]
            raise ErroBrasa(f"Esperava '{v}'" + (f" mas achei '{achou}'" if achou is not None else ""), self.linha)
        self.i += 1

    def esperar_kw(self, v):
        if not self.e_kw(v):
            raise ErroBrasa(f"Esperava a palavra '{v}'", self.linha)
        self.i += 1

    def esperar_nome(self):
        k, v = self.prox()
        if k != "nome":
            raise ErroBrasa(f"Esperava um nome, achei '{v}'", self.linha)
        return v

    def checar_fim(self):
        if not self.fim():
            raise ErroBrasa(f"Não entendi '{self.ver()[1]}'", self.linha)

    def expr(self):
        return self.ou()

    def ou(self):
        a = self.e_()
        while self.e_kw("ou"):
            self.i += 1
            a = ("ou", a, self.e_())
        return a

    def e_(self):
        a = self.nao()
        while self.e_kw("e"):
            self.i += 1
            a = ("e", a, self.nao())
        return a

    def nao(self):
        if self.e_kw("nao"):
            self.i += 1
            return ("nao", self.nao())
        return self.comp()

    def comp(self):
        a = self.soma()
        while (self.ver()[0] == "op" and self.ver()[1] in ("==", "!=", "<", ">", "<=", ">=")) or self.e_kw("em"):
            op = self.prox()[1]
            a = ("bin", op, a, self.soma())
        return a

    def soma(self):
        a = self.mult()
        while self.ver()[0] == "op" and self.ver()[1] in ("+", "-"):
            op = self.prox()[1]
            a = ("bin", op, a, self.mult())
        return a

    def mult(self):
        a = self.unario()
        while self.ver()[0] == "op" and self.ver()[1] in ("*", "/", "%"):
            op = self.prox()[1]
            a = ("bin", op, a, self.unario())
        return a

    def unario(self):
        if self.e_op("-"):
            self.i += 1
            return ("neg", self.unario())
        return self.posfixo()

    def posfixo(self):
        a = self.atomo()
        while True:
            if self.e_op("("):
                self.i += 1
                args = []
                if not self.e_op(")"):
                    args.append(self.expr())
                    while self.e_op(","):
                        self.i += 1
                        args.append(self.expr())
                self.esperar_op(")")
                a = ("call", a, args)
            elif self.e_op("."):
                self.i += 1
                a = ("attr", a, self.esperar_nome())
            elif self.e_op("["):
                self.i += 1
                idx = self.expr()
                self.esperar_op("]")
                a = ("idx", a, idx)
            else:
                return a

    def atomo(self):
        k, v = self.prox()
        if k in ("num", "str"):
            return ("val", v)
        if k == "nome":
            return ("nome", v)
        if k == "kw" and v in ("verdadeiro", "falso", "nulo"):
            return ("val", {"verdadeiro": True, "falso": False, "nulo": None}[v])
        if k == "op" and v == "(":
            e = self.expr()
            self.esperar_op(")")
            return e
        if k == "op" and v == "[":
            itens = []
            if not self.e_op("]"):
                itens.append(self.expr())
                while self.e_op(","):
                    self.i += 1
                    itens.append(self.expr())
            self.esperar_op("]")
            return ("lista", itens)
        if k == "fim":
            raise ErroBrasa("A linha acabou no meio de uma conta", self.linha)
        if k == "kw":
            raise ErroBrasa(f"A palavra '{v}' não pode ficar aqui", self.linha)
        raise ErroBrasa(f"Não esperava '{v}' aqui", self.linha)


def compilar(codigo):
    """Transforma o texto do script numa lista de comandos."""
    linhas = []
    for n, txt in enumerate(codigo.split("\n"), 1):
        txt = txt.replace("\t", "    ").rstrip()
        s = txt.strip()
        if not s or s.startswith("#") or s.startswith("//"):
            continue
        ind = len(txt) - len(txt.lstrip(" "))
        toks = tokenizar(s, n)
        if toks:
            linhas.append((ind, toks, n))
    pos = [0]

    def bloco(ind_min):
        cmds = []
        if pos[0] >= len(linhas):
            return cmds
        nivel = linhas[pos[0]][0]
        if nivel < ind_min:
            return cmds
        while pos[0] < len(linhas):
            ind, toks, n = linhas[pos[0]]
            if ind < nivel:
                break
            if ind > nivel:
                raise ErroBrasa("Espaço (indentação) a mais no começo da linha", n)
            pos[0] += 1
            cmds.append(comando(toks, n, ind))
        return cmds

    def corpo(ind, n):
        b = bloco(ind + 1)
        if not b:
            raise ErroBrasa("Depois de ':' precisa ter linhas com espaço na frente", n)
        return b

    def cabecalho_fim(p):
        p.esperar_op(":")
        p.checar_fim()

    def comando(toks, n, ind):
        p = Parser(toks, n)
        k, v = toks[0]
        if k == "kw":
            p.i = 1
            if v == "var":
                nome = p.esperar_nome()
                p.esperar_op("=")
                e = p.expr()
                p.checar_fim()
                return ("var", n, nome, e)
            if v == "se":
                c = p.expr()
                cabecalho_fim(p)
                ramos = [(c, corpo(ind, n))]
                senao = None
                while pos[0] < len(linhas) and linhas[pos[0]][0] == ind and linhas[pos[0]][1][0] == ("kw", "senao"):
                    _, t2, n2 = linhas[pos[0]]
                    pos[0] += 1
                    p2 = Parser(t2, n2)
                    p2.i = 1
                    if p2.e_kw("se"):
                        p2.i += 1
                        c2 = p2.expr()
                        cabecalho_fim(p2)
                        ramos.append((c2, corpo(ind, n2)))
                    else:
                        cabecalho_fim(p2)
                        senao = corpo(ind, n2)
                        break
                return ("se", n, ramos, senao)
            if v == "senao":
                raise ErroBrasa("'senao' sem um 'se' antes", n)
            if v == "enquanto":
                c = p.expr()
                cabecalho_fim(p)
                return ("enquanto", n, c, corpo(ind, n))
            if v == "repetir":
                c = p.expr()
                cabecalho_fim(p)
                return ("repetir", n, c, corpo(ind, n))
            if v == "para":
                if p.ver() == ("nome", "cada"):           # para cada item em lista:
                    p.i += 1
                    nome = p.esperar_nome()
                    p.esperar_kw("em")
                    lista = p.expr()
                    cabecalho_fim(p)
                    return ("paracada", n, nome, lista, corpo(ind, n))
                nome = p.esperar_nome()
                p.esperar_kw("de")
                a = p.expr()
                p.esperar_kw("ate")
                b = p.expr()
                cabecalho_fim(p)
                return ("para", n, nome, a, b, corpo(ind, n))
            if v == "funcao":
                nome = p.esperar_nome()
                p.esperar_op("(")
                params = []
                if not p.e_op(")"):
                    params.append(p.esperar_nome())
                    while p.e_op(","):
                        p.i += 1
                        params.append(p.esperar_nome())
                p.esperar_op(")")
                cabecalho_fim(p)
                return ("funcao", n, nome, params, corpo(ind, n))
            if v == "retornar":
                e = None if p.fim() else p.expr()
                p.checar_fim()
                return ("retornar", n, e)
            if v in ("parar", "continuar"):
                p.checar_fim()
                return (v, n)
            if v == "quando":
                ev = p.esperar_nome()
                if ev not in EVENTOS_SCRIPT:
                    s_ = sugestao_nome(ev, EVENTOS_SCRIPT) if "sugestao_nome" in globals() else None
                    if s_:
                        raise ErroBrasa(f"Evento '{ev}' não existe. Você quis dizer '{s_}'?", n)
                    raise ErroBrasa(f"Evento '{ev}' não existe. Use: " + ", ".join(EVENTOS_SCRIPT), n)
                arg = None
                if not p.e_op(":"):
                    arg = p.expr()
                if EVENTOS_SCRIPT[ev] and arg is None:
                    raise ErroBrasa(f"'quando {ev}' precisa de um valor. Ex: quando {ev} " +
                                    ('2:' if ev == 'cada' else '"e":'), n)
                if not EVENTOS_SCRIPT[ev] and arg is not None:
                    raise ErroBrasa(f"'quando {ev}' não leva valor", n)
                cabecalho_fim(p)
                return ("quando", n, ev, arg, corpo(ind, n))
            p.i = 0
        e = p.expr()
        if p.ver()[0] == "op" and p.ver()[1] in ("=", "+=", "-=", "*=", "/="):
            op = p.prox()[1]
            if e[0] not in ("nome", "attr", "idx"):
                raise ErroBrasa("Não dá para guardar valor aí", n)
            val = p.expr()
            p.checar_fim()
            return ("atrib", n, e, op, val)
        p.checar_fim()
        return ("expr", n, e)

    programa = bloco(0)
    if pos[0] < len(linhas):
        raise ErroBrasa("Espaço (indentação) errado", linhas[pos[0]][2])
    return programa


def compilar_expr(texto):
    p = Parser(tokenizar(str(texto).strip(), None), None)
    e = p.expr()
    p.checar_fim()
    return e


def texto(v):
    if v is None:
        return "nulo"
    if v is True:
        return "verdadeiro"
    if v is False:
        return "falso"
    if isinstance(v, float):
        if v.is_integer() and abs(v) < 1e15:
            return str(int(v))
        return str(round(v, 3))
    if isinstance(v, list):
        return "[" + ", ".join(texto(x) for x in v) + "]"
    if hasattr(v, "brasa_nome"):
        return v.brasa_nome()
    return str(v)


def num(v):
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        try:
            f = float(v.replace(",", "."))
            return int(f) if f.is_integer() else f
        except ValueError:
            pass
    raise ErroBrasa(f"'{texto(v)}' não é um número")


def limpar(r):
    if isinstance(r, float) and r.is_integer() and abs(r) < 1e15:
        return int(r)
    return r


def verdade(v):
    return bool(v)


def somar(a, b):
    if isinstance(a, str) or isinstance(b, str):
        return texto(a) + texto(b)
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    return limpar(num(a) + num(b))


def aplicar_op(op, atual, valor):
    if op == "=":
        return valor
    if op == "+=":
        return somar(atual, valor)
    a, b = num(atual), num(valor)
    if op == "-=":
        return limpar(a - b)
    if op == "*=":
        return limpar(a * b)
    if op == "/=":
        if b == 0:
            raise ErroBrasa("Divisão por zero")
        return limpar(a / b)
    raise ErroBrasa(f"Operação '{op}' não existe")


def comparar(a, op, b):
    try:
        if op == "==":
            return a == b
        if op == "!=":
            return a != b
        if isinstance(a, str) != isinstance(b, str):
            a, b = num(a), num(b)
        if op == "<":
            return a < b
        if op == ">":
            return a > b
        if op == "<=":
            return a <= b
        if op == ">=":
            return a >= b
    except TypeError:
        raise ErroBrasa(f"Não dá para comparar {texto(a)} com {texto(b)}")
    raise ErroBrasa(f"Comparação '{op}' não existe")


class Escopo:
    def __init__(self, pai=None, vars=None):
        self.pai = pai
        self.vars = vars if vars is not None else {}

    def achar(self, nome):
        e = self
        while e is not None:
            if nome in e.vars:
                return e
            e = e.pai
        return None

    def get(self, nome, linha=None):
        e = self.achar(nome)
        if e is None:
            raise ErroBrasa(f"'{nome}' não existe (use: var {nome} = ...)", linha)
        return e.vars[nome]

    def set(self, nome, valor):
        e = self.achar(nome)
        (e or self).vars[nome] = valor


class Namespace:
    """Usado no 'global.alguma_coisa'."""

    def __init__(self, nome):
        self.nome = nome
        self.d = {}

    def brasa_get(self, n):
        return self.d.get(n, 0)

    def brasa_set(self, n, v):
        self.d[n] = v

    def brasa_nome(self):
        return self.nome


class FuncaoBrasa:
    def __init__(self, nome, params, corpo, escopo, interp):
        self.nome = nome
        self.params = params
        self.corpo = corpo
        self.escopo = escopo
        self.interp = interp

    def __call__(self, *args):
        if len(args) != len(self.params):
            raise ErroBrasa(f"A função {self.nome} precisa de {len(self.params)} valor(es), recebeu {len(args)}")
        local = Escopo(self.escopo, dict(zip(self.params, args)))
        try:
            self.interp.executar(self.corpo, local)
        except Retorno as r:
            return r.valor
        return None

    def brasa_nome(self):
        return f"funcao {self.nome}"


class Interpretador:
    def __init__(self):
        self.passos = 0

    def executar(self, cmds, esc):
        for c in cmds:
            self.passos += 1
            if self.passos > LIMITE_PASSOS:
                raise ErroBrasa("O código demorou demais (loop infinito?)", c[1])
            try:
                self.comando(c, esc)
            except (Retorno, Parar, Continuar):
                raise
            except ErroBrasa as e:
                if e.linha is None:
                    e.linha = c[1]
                raise
            except RecursionError:
                raise
            except ZeroDivisionError:
                raise ErroBrasa("Divisão por zero", c[1])
            except (TypeError, ValueError, IndexError, KeyError, AttributeError) as ex:
                raise ErroBrasa(f"Erro: {ex}", c[1])

    def laco(self, corpo, esc):
        """Roda o corpo de um loop. Retorna False se deu 'parar'."""
        try:
            self.executar(corpo, esc)
        except Parar:
            return False
        except Continuar:
            pass
        return True

    def comando(self, c, esc):
        k = c[0]
        if k == "expr":
            self.avaliar(c[2], esc)
        elif k == "var":
            esc.vars[c[2]] = self.avaliar(c[3], esc)
        elif k == "atrib":
            self.atribuir(c[2], c[3], self.avaliar(c[4], esc), esc)
        elif k == "se":
            for cond, corpo in c[2]:
                if verdade(self.avaliar(cond, esc)):
                    self.executar(corpo, esc)
                    return
            if c[3]:
                self.executar(c[3], esc)
        elif k == "enquanto":
            while verdade(self.avaliar(c[2], esc)):
                self.passos += 1
                if self.passos > LIMITE_PASSOS:
                    raise ErroBrasa("O código demorou demais (loop infinito?)", c[1])
                if not self.laco(c[3], esc):
                    break
        elif k == "repetir":
            for _ in range(int(num(self.avaliar(c[2], esc)))):
                if not self.laco(c[3], esc):
                    break
        elif k == "para":
            a = int(num(self.avaliar(c[3], esc)))
            b = int(num(self.avaliar(c[4], esc)))
            passo = 1 if b >= a else -1
            for i in range(a, b + passo, passo):
                esc.set(c[2], i)
                if not self.laco(c[5], esc):
                    break
        elif k == "paracada":
            itens = self.avaliar(c[3], esc)
            if isinstance(itens, str):
                itens = list(itens)
            elif not isinstance(itens, list):
                raise ErroBrasa(f"'para cada' precisa de uma lista, recebeu {texto(itens)}")
            for item in list(itens):
                self.passos += 1
                if self.passos > LIMITE_PASSOS:
                    raise ErroBrasa("O código demorou demais (loop infinito?)", c[1])
                esc.set(c[2], item)
                if not self.laco(c[4], esc):
                    break
        elif k == "funcao":
            esc.vars[c[2]] = FuncaoBrasa(c[2], c[3], c[4], esc, self)
        elif k == "retornar":
            raise Retorno(self.avaliar(c[2], esc) if c[2] is not None else None)
        elif k == "parar":
            raise Parar()
        elif k == "continuar":
            raise Continuar()
        elif k == "quando":
            lista = esc.get("__quando__", c[1])
            arg = self.avaliar(c[3], esc) if c[3] is not None else None
            lista.append((c[2], arg, c[4], esc))

    def atribuir(self, alvo, op, valor, esc):
        t = alvo[0]
        if t == "nome":
            atual = esc.get(alvo[1]) if op != "=" else None
            esc.set(alvo[1], aplicar_op(op, atual, valor))
        elif t == "attr":
            obj = self.avaliar(alvo[1], esc)
            if not hasattr(obj, "brasa_set"):
                raise ErroBrasa(f"'{texto(obj)}' não tem a propriedade '{alvo[2]}'")
            atual = obj.brasa_get(alvo[2]) if op != "=" else None
            obj.brasa_set(alvo[2], aplicar_op(op, atual, valor))
        elif t == "idx":
            lista = self.avaliar(alvo[1], esc)
            i = int(num(self.avaliar(alvo[2], esc)))
            lista[i] = aplicar_op(op, lista[i] if op != "=" else None, valor)

    def avaliar(self, no, esc):
        t = no[0]
        if t == "val":
            return no[1]
        if t == "nome":
            return esc.get(no[1])
        if t == "lista":
            return [self.avaliar(x, esc) for x in no[1]]
        if t == "ou":
            a = self.avaliar(no[1], esc)
            return a if verdade(a) else self.avaliar(no[2], esc)
        if t == "e":
            a = self.avaliar(no[1], esc)
            return self.avaliar(no[2], esc) if verdade(a) else a
        if t == "nao":
            return not verdade(self.avaliar(no[1], esc))
        if t == "neg":
            return limpar(-num(self.avaliar(no[1], esc)))
        if t == "bin":
            op = no[1]
            a = self.avaliar(no[2], esc)
            b = self.avaliar(no[3], esc)
            if op == "+":
                return somar(a, b)
            if op in ("-", "*", "/", "%"):
                a, b = num(a), num(b)
                if op == "-":
                    return limpar(a - b)
                if op == "*":
                    return limpar(a * b)
                if b == 0:
                    raise ErroBrasa("Divisão por zero")
                return limpar(a / b) if op == "/" else limpar(a % b)
            if op == "em":
                if isinstance(b, str):
                    return texto(a) in b
                if isinstance(b, list):
                    return a in b
                raise ErroBrasa(f"'em' precisa de uma lista ou texto, recebeu {texto(b)}")
            return comparar(a, op, b)
        if t == "attr":
            obj = self.avaliar(no[1], esc)
            if not hasattr(obj, "brasa_get"):
                raise ErroBrasa(f"'{texto(obj)}' não tem a propriedade '{no[2]}'")
            return obj.brasa_get(no[2])
        if t == "idx":
            base = self.avaliar(no[1], esc)
            return base[int(num(self.avaliar(no[2], esc)))]
        if t == "call":
            f = self.avaliar(no[1], esc)
            if not callable(f):
                raise ErroBrasa(f"'{texto(f)}' não é uma função")
            return f(*[self.avaliar(a, esc) for a in no[2]])
        raise ErroBrasa("Expressão desconhecida")
