# Minha Engine - editor_ajuda.py
# MAIS AJUDA E FACILIDADE no editor:
#  - Tour guiado (mostra onde fica cada coisa, com destaque animado)
#  - Buscar qualquer coisa (Ctrl+K): comandos, abas, objetos para colocar, objetos da fase e itens da Loja
#  - Explicação de cada propriedade ao passar o mouse
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

GERAL_PADRAO["tour_visto"] = False

DESC_PROPS = {
    "nome": "Nome do objeto. Os eventos e scripts usam esse nome para achar ele.",
    "x": "Posição na horizontal (para a direita aumenta).", "y": "Posição na vertical (para baixo aumenta).",
    "w": "Largura em pixels.", "h": "Altura em pixels.", "cor": "Cor do objeto (vermelho, verde, azul).",
    "solido": "Sim = ninguém atravessa (dá para pisar em cima).",
    "gravidade": "Sim = cai até encostar em algo sólido.", "velocidade": "Rapidez para andar.",
    "pulo": "Força do pulo (maior = pula mais alto).", "aceleracao": "Quão rápido chega na velocidade máxima.",
    "pulos_extras": "Quantos pulos a mais no ar (1 = pulo duplo).",
    "pulo_variavel": "Sim = soltar o botão cedo faz um pulo mais baixo.",
    "valor": "Quanto vale (moedas, pontos...).", "distancia": "Até onde anda antes de voltar.",
    "imagem": "Imagem no lugar do desenho padrão (Importe ou Desenhe).",
    "opacidade": "0 = invisível, 255 = totalmente visível.", "rotacao": "Giro em graus.",
    "espelhar": "Vira a imagem de lado.", "camada": "Quem tem camada maior aparece na frente.",
    "visivel": "Não = some (mas continua existindo).",
    "na_tela": "Fica preso na tela (não anda com a câmera): para textos, botões e barras.",
    "empurravel": "O player consegue empurrar.", "vel_x": "Velocidade de ir e voltar na horizontal.",
    "vel_y": "Velocidade de ir e voltar na vertical.", "forca": "Força do impulso.",
    "destino": "Nome do objeto para onde o portal leva.", "fala": "O que o personagem fala (use | para mais falas).",
    "item": "Nome do item que o player ganha.", "texto": "O texto que aparece. {moedas()} mostra as moedas.",
    "tamanho_fonte": "Tamanho da letra.", "cor_texto": "Cor da letra.", "cor_fundo": "Cor do fundo.",
    "valor_de": "De onde vem o número da barra (ex: player.vida).", "maximo": "Valor da barra cheia.",
    "arredondado": "Cantos arredondados (0 = quadrado).", "animacao": "Imagens que trocam sozinhas (desenhe na aba Desenho).",
    "fps_anim": "Quantas imagens da animação por segundo.", "anim_andando": "Animação quando anda.",
    "anim_pulando": "Imagem/animação quando está no ar.", "ir_para_fase": "Fase que abre ao encostar.",
    "grupo": "Grupos separados por vírgula: os eventos podem mexer em todos de um grupo de uma vez.",
    "material": "Material: muda o desenho e a física (gelo escorrega, borracha quica...).",
    "forma": "Formato do objeto.", "contorno": "Espessura da borda.", "cor_contorno": "Cor da borda.",
    "fonte": "Tipo de letra.", "negrito": "Letra mais grossa.", "italico": "Letra inclinada.",
    "alinhamento": "Texto à esquerda, no centro ou à direita.", "sombra_texto": "Sombra atrás da letra.",
    "travado": "Travado = não sai do lugar sem querer no editor.", "dano": "Quanto de vida ele tira.",
    "dash": "Shift dá um impulso rápido.", "pulo_parede": "Pula nas paredes.",
    "tiro": "Nome do modelo que vira tiro (F atira).", "vel_tiro": "Velocidade do tiro.",
    "espada": "Espaço/J dá golpe de espada.", "gravidade_escala": "1 = normal, 0.5 = cai devagar, 2 = cai rápido.",
    "pode_ser_pisado": "Sim = morre quando o player pula em cima.",
    "anim_baixo": "Animação andando para baixo (top-down).", "anim_cima": "Animação andando para cima (top-down).",
    "anim_lado": "Animação andando de lado (top-down).",
    "ordenar_por_y": "Top-down: quem está mais embaixo na tela aparece na frente.",
    "sombras": "Top-down: sombrinha embaixo dos personagens.", "visao_de_cima": "Jogo visto de cima (top-down), "
    "sem gravidade.", "escuridao": "0 = claro, 255 = escuro total (use Luz e Tocha).",
    "gravidade_cena": "Força que puxa tudo para baixo.", "olhar_a_frente": "A câmera mostra mais na direção que o "
    "player anda.", "zoom_camera": "Aproxima (maior que 1) ou afasta (menor que 1) a câmera do jogo.",
}


# =====================================================================
# TOUR GUIADO
# =====================================================================
def _uniao(rs):
    rs = [r for r in rs if r is not None]
    if not rs:
        return None
    x0, y0 = min(r.x for r in rs), min(r.y for r in rs)
    x1, y1 = max(r.right for r in rs), max(r.bottom for r in rs)
    return pygame.Rect(x0, y0, x1 - x0, y1 - y0)


PASSOS_TOUR = [
    ("Bem-vindo à Minha Engine!", "Em 1 minuto eu te mostro onde fica cada coisa. Use os botões ou as setas do "
     "teclado. Dá para ver de novo quando quiser no botão de Ajuda (?).", lambda ed: None),
    ("Peças e personagens", "Aqui ficam as coisas para colocar na fase: blocos, player, inimigos, moedas, efeitos e "
     "interface. Clique num tipo e depois clique na cena.",
     lambda ed: pygame.Rect(0, TOPO, PAINEL_ESQ, ALTURA - TOPO - RODAPE)),
    ("A cena", "É a sua fase. Clique para selecionar, arraste para mover, roda do mouse dá zoom e botão direito "
     "abre o menu do objeto. No celular: dois dedos movem e dão zoom.", lambda ed: VIEW),
    ("Propriedades", "Tudo do objeto selecionado: cor, tamanho, velocidade, comportamentos (Vida, Patrulhar, "
     "Atirar...). Passe o mouse em cima de um nome para ver o que ele faz.",
     lambda ed: pygame.Rect(LARGURA - PAINEL_DIR, TOPO, PAINEL_DIR, ALTURA - TOPO - RODAPE)),
    ("As abas", "Eventos = programar sem código (QUANDO / SE / FAÇA). Script = código Brasa. Desenho = pixel art. "
     "Loja = centenas de coisas prontas.", lambda ed: _uniao(list(ed.abas.values()))),
    ("Testar o jogo", "Play testa a fase aqui mesmo. Play cheio usa a tela toda. Esc para.",
     lambda ed: _uniao([ed.botoes.get("play"), ed.botoes.get("playcheio")])),
    ("Plataforma ou visão de cima", "Troque a fase entre jogo de plataforma (com pulo e gravidade) e top-down "
     "(estilo Zelda, com espada).", lambda ed: ed.botoes.get("modo")),
    ("Buscar qualquer coisa", "Não achou algo? Clique aqui ou aperte Ctrl+K e digite: comandos, objetos para "
     "colocar, objetos da fase e itens da Loja.", lambda ed: ed.botoes.get("buscar")),
    ("Precisa de ajuda?", "Aqui tem este tour, os atalhos do teclado e o guia de Primeiros passos. "
     "Agora é com você: bom jogo!", lambda ed: ed.botoes.get("ajuda")),
]


class EditorAjuda:
    # ----------------- tour -----------------
    def iniciar_tour(self):
        self.menu = None
        self.seletor = None
        if self.jogo:
            self.parar()
        self.aba = "cena"
        self.tour = {"passo": 0, "t0": agora_ui(), "hits": []}

    def fechar_tour(self, concluido=True):
        self.tour = None
        if not CONFIG["geral"].get("tour_visto"):
            CONFIG["geral"]["tour_visto"] = True
            salvar_config()
        if concluido:
            self.avisar("Pronto! Se precisar, o tour está no botão de Ajuda (?). Ctrl+K busca qualquer coisa.", "ok")

    def mudar_passo_tour(self, d):
        n = self.tour["passo"] + d
        if n < 0:
            return
        if n >= len(PASSOS_TOUR):
            self.fechar_tour()
            return
        self.tour["passo"] = n
        self.tour["t0"] = agora_ui()

    def desenhar_tour(self, t, mouse):
        tour = getattr(self, "tour", None)
        if not tour:
            return
        tour["hits"] = []
        titulo, texto_, alvo_fn = PASSOS_TOUR[tour["passo"]]
        try:
            alvo = alvo_fn(self)
        except (AttributeError, KeyError, TypeError):
            alvo = None
        k = entrada(tour["t0"], 0.25)
        escuro = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        escuro.fill((5, 6, 10, 175))
        if alvo is not None:
            buraco = suave_rect(("tour",), alvo.inflate(12, 12))
            escuro.fill((0, 0, 0, 0), buraco)
        t.blit(escuro, (0, 0))
        if alvo is not None:
            pulso = 0.5 + 0.5 * math.sin(agora_ui() * 4)
            pygame.draw.rect(t, misturar_cor(C_DESTAQUE, (255, 255, 255), pulso * 0.5), buraco, 3, border_radius=10)
        # cartão
        cw, ch = 400, 0
        linhas = quebrar_texto(texto_, self.fp, cw - 36)
        ch = 78 + len(linhas) * 19 + 46
        if alvo is None:
            card = pygame.Rect(LARGURA // 2 - cw // 2, ALTURA // 2 - ch // 2, cw, ch)
        else:
            b = buraco
            opcoes = [pygame.Rect(b.right + 16, b.centery - ch // 2, cw, ch),
                      pygame.Rect(b.x - cw - 16, b.centery - ch // 2, cw, ch),
                      pygame.Rect(b.centerx - cw // 2, b.bottom + 16, cw, ch),
                      pygame.Rect(b.centerx - cw // 2, b.y - ch - 16, cw, ch)]
            def cabe(o):
                return o.x >= 8 and o.y >= 8 and o.right <= LARGURA - 8 and o.bottom <= ALTURA - 8
            card = next((o for o in opcoes if cabe(o)), None)
            if card is None:
                card = pygame.Rect(LARGURA // 2 - cw // 2, ALTURA - ch - 30, cw, ch)
            card = pygame.Rect(max(8, min(card.x, LARGURA - 8 - cw)), max(8, min(card.y, ALTURA - 8 - ch)), cw, ch)
        card = card.move(0, int((1 - k) * 14))
        sombra_painel(t, card, 14)
        pygame.draw.rect(t, C_PAINEL, card, border_radius=14)
        pygame.draw.rect(t, C_DESTAQUE, (card.x, card.y, card.w, 5), border_top_left_radius=14,
                         border_top_right_radius=14)
        n = len(PASSOS_TOUR)
        t.blit(self.fpp.render(f"{tour['passo'] + 1} de {n}", True, C_TEXTO2), (card.x + 18, card.y + 16))
        t.blit(self.ft.render(titulo, True, C_TEXTO), (card.x + 18, card.y + 36))
        for i, linha in enumerate(linhas):
            t.blit(self.fp.render(linha, True, C_TEXTO), (card.x + 18, card.y + 70 + i * 19))
        # bolinhas de progresso
        for i in range(n):
            c = (card.right - 18 - (n - i) * 12, card.y + 22)
            pygame.draw.circle(t, C_DESTAQUE if i <= tour["passo"] else C_BORDA, c, 4)
        yb = card.bottom - 44
        b_pular = pygame.Rect(card.x + 14, yb, 90, 32)
        b_voltar = pygame.Rect(card.right - 228, yb, 100, 32)
        b_prox = pygame.Rect(card.right - 120, yb, 106, 32)
        ultimo = tour["passo"] == n - 1
        desenhar_botao(t, self.fpp, b_pular, "Pular tour", mouse, cor=(60, 62, 74))
        if tour["passo"] > 0:
            desenhar_botao(t, self.fp, b_voltar, "Voltar", mouse)
            tour["hits"].append((b_voltar, -1))
        desenhar_botao(t, self.fb if ultimo else self.fp, b_prox, "Começar!" if ultimo else "Próximo", mouse,
                       cor=C_VERDE if ultimo else C_DESTAQUE)
        tour["hits"] += [(b_prox, 1), (b_pular, "pular")]

    def evento_tour(self, e):
        """Enquanto o tour está aberto ele recebe tudo. Devolve True se tratou."""
        tour = getattr(self, "tour", None)
        if not tour:
            return False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.fechar_tour(False)
            elif e.key in (pygame.K_RIGHT, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.mudar_passo_tour(1)
            elif e.key == pygame.K_LEFT:
                self.mudar_passo_tour(-1)
            return True
        if e.type == pygame.MOUSEBUTTONDOWN and getattr(e, "button", 1) == 1:
            for r, a in tour["hits"]:
                if r.collidepoint(e.pos):
                    if a == "pular":
                        self.fechar_tour(False)
                    else:
                        self.mudar_passo_tour(a)
                    return True
            return True
        return e.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL, pygame.MOUSEMOTION, TOQUE_GESTO)

    # ----------------- buscar qualquer coisa -----------------
    def comandos_busca(self):
        cmds = {}

        def add(cat, nome, desc, fn):
            if nome not in cmds:
                cmds[nome] = (cat, desc, fn)
        acoes = [
            ("Play (testar a fase)", "F5. Testa o jogo aqui no editor.", lambda: self.acao("play")),
            ("Play em tela cheia", "Testa o jogo usando a tela inteira.", lambda: self.acao("playcheio")),
            ("Salvar", "Salva o projeto.", lambda: self.acao("salvar")),
            ("Desfazer", "Ctrl+Z.", lambda: self.acao("desfazer")), ("Refazer", "Ctrl+Y.", lambda: self.acao("refazer")),
            ("Exportar o jogo", "Gera o jogo para jogar fora do editor.", lambda: self.acao("exportar")),
            ("Novo projeto / exemplo", "Começa outro projeto ou abre um exemplo pronto.", lambda: self.acao("novo")),
            ("Voltar para o Início", "Tela inicial com seus projetos.", lambda: self.acao("inicio")),
            ("Trocar modo: plataforma / top-down", "Muda a fase entre pulo e visão de cima.", self.trocar_modo),
            ("Mostrar / esconder a grade", "Linhas de ajuda na cena.", lambda: self.acao("grade")),
            ("Ligar / desligar snap", "Objetos andam de pouco em pouco (alinhados).", lambda: self.acao("snap")),
            ("Centralizar a câmera", "Mostra o objeto selecionado (ou o Player).", self.focar),
            ("Zoom 100%", "Volta o zoom ao normal.", self.zoom_100),
            ("Abrir a janela Saída", "Mensagens e erros dos scripts.", lambda: self.acao("saida")),
            ("Tour guiado", "Mostra onde fica cada coisa em 1 minuto.", self.iniciar_tour),
            ("Atalhos do teclado", "Lista de teclas do editor.", lambda: setattr(self, "mostrar_ajuda", True)),
            ("Primeiros passos (guia)", "Lista de tarefas para aprender o básico.", self.reabrir_passos),
        ]
        for nome, desc, fn in acoes:
            add("Comandos", nome, desc, fn)
        nomes_abas = {"cena": "Cena", "eventos": "Eventos (QUANDO/SE/FAÇA)", "script": "Script (código Brasa)",
                      "api": "API (tudo da engine)", "desenho": "Desenho (pixel art)", "loja": "Loja"}
        for chave, rot in nomes_abas.items():
            add("Ir para", f"Ir para a aba {rot}", "Abre essa aba.", lambda c=chave: setattr(self, "aba", c))
        for grupo, tipos in GRUPOS_TIPOS:
            for tipo in tipos:
                rot = tipo[7:] if tipo.startswith("preset:") else NOMES_CURTOS.get(tipo, tipo)
                desc = DESC_PRESETS.get(tipo[7:], "") if tipo.startswith("preset:") else DESC_TIPOS.get(tipo, "")
                add("Colocar na cena", f"Colocar: {rot}", desc + " (clique na cena depois)",
                    lambda tp=tipo: self.escolher_ferramenta_busca(tp))
        for d in self.objetos:
            add("Nesta fase", f"Objeto: {d.get('nome', d['tipo'])}  ({d['tipo']})", "Seleciona e mostra na cena.",
                lambda obj=d: self.ir_para_objeto(obj))
        for fase in self.projeto["fases"]:
            add("Nesta fase", f"Fase: {fase}", "Abre essa fase.", lambda f=fase: self.trocar_fase(f))
        for item in LOJA:
            preco = "grátis" if not item["preco"] and not item["plano"] else (
                f"plano {item['plano']}" if item["plano"] else f"{item['preco']} Brasas")
            add("Loja", f"Loja: {item['nome']}", f"{item['cat']} · {preco}. {item['desc']}",
                lambda it=item: self.inserir_da_busca(it))
        return cmds

    def abrir_busca(self):
        cmds = self.comandos_busca()
        self.busca_cmds = cmds
        BUSCA_DESC.clear()
        BUSCA_DESC.update({nome: c[1] for nome, c in cmds.items()})
        cats = {}
        for nome, (cat, _d, _f) in cmds.items():
            cats.setdefault(cat, []).append(nome)
        catalogo = {nome: [] for nome in cmds}

        def escolher(nome):
            c = self.busca_cmds.get(nome)
            if c:
                c[2]()
        self.abrir_seletor("Buscar qualquer coisa  (Ctrl+K)", "cmd", catalogo, list(cats.items()), escolher,
                           C_DESTAQUE)

    def escolher_ferramenta_busca(self, tipo):
        self.aba = "cena"
        self.ferramenta = tipo
        self.avisar("Agora clique na cena para colocar. Esc volta para Selecionar.", "info")

    def ir_para_objeto(self, d):
        self.aba = "cena"
        self.selecionar(d)
        self.focar()

    def inserir_da_busca(self, item):
        self.aba = "loja"
        self.loja.inserir(item)


_descricao_do_item_antiga = descricao_do_item


def descricao_do_item(tipo, nome):
    if tipo == "cmd":
        return BUSCA_DESC.get(nome, "")
    return _descricao_do_item_antiga(tipo, nome)


BUSCA_DESC = {}


# =====================================================================
# Brasa: "você quis dizer...?"
# =====================================================================
import difflib


def sugestao_nome(nome, opcoes):
    perto = difflib.get_close_matches(str(nome), [str(o) for o in opcoes if o], n=1, cutoff=0.72)
    return perto[0] if perto else None


def _get_com_sugestao(self, nome, linha=None):
    e = self.achar(nome)
    if e is None:
        nomes = set()
        esc = self
        while esc is not None:
            nomes.update(esc.vars)
            esc = esc.pai
        nomes.update(NOMES_PRONTOS)
        s = sugestao_nome(nome, nomes)
        if s:
            raise ErroBrasa(f"'{nome}' não existe. Você quis dizer '{s}'?", linha)
        raise ErroBrasa(f"'{nome}' não existe (crie antes com: var {nome} = ...)", linha)
    return e.vars[nome]


Escopo.get = _get_com_sugestao
