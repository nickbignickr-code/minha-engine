# Minha Engine - editor.py
# a classe Editor: começo (__init__) e o loop principal
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

class Editor(EditorBase, EditorObjetos, EditorEventos, EditorScript, EditorEntrada, EditorTela, EditorSeletor,
             EditorToque):
    """O editor. Os métodos estão divididos nos arquivos editor_*.py (veja a lista em cima)."""
    MENU_POR_COLUNA = 20
    MENU_LARG = 200
    GRADES = [8, 10, 16, 20, 25, 32, 40, 50, 64]
    STUDS = [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64]
    AUTOSAVE_SEG = 90

    def __init__(self, pasta_projeto=None, tela=None, tela_cheia=False):
        self.dono_janela = tela is None
        self.fechar_no_inicio = False
        if self.dono_janela:            # aberto sozinho (sem o Inicio): cuida da janela
            pygame.init()
            preparar_pastas()
            colocar_icone_janela()
            try:
                tela = pygame.display.set_mode((LARGURA, ALTURA), flags_janela())
            except pygame.error:
                tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.tela = tela
        self.tela_cheia = JANELA["cheia"] or tela_cheia
        if pasta_projeto:
            definir_projeto(pasta_projeto)
        self.pasta_projeto = pasta_projeto or os.path.dirname(ARQUIVO)
        self.erros_plugins = carregar_plugins()
        self.controles = Controles()
        self.voltar_inicio = False
        pygame.display.set_caption("Minha Engine")
        if self.dono_janela and CONFIG["geral"].get("tela_carregamento", True):
            self.fechar_no_inicio = not mostrar_carregamento(
                self.tela, pygame.time.Clock(), 1.3,
                etapas=["Preparando o editor...", "Carregando plugins...", "Abrindo o projeto...", "Pronto!"])
        try:
            pygame.key.set_repeat(400, 35)   # segurar tecla repete (setas, apagar...)
        except (pygame.error, AttributeError):
            pass
        self.relogio = pygame.time.Clock()
        self.carregar_fontes()

        self.projeto = projeto_padrao()
        if os.path.exists(ARQUIVO):
            self.abrir(silencioso=True)

        self.selecao = []
        self.sel = None
        self.ferramenta = "Selecionar"
        self.aba = "cena"
        self.aba_esq = "objetos"
        self.cam = [-40.0, -100.0]
        self.zoom = 1.0
        self.grade = int(num_seguro(CONFIG["geral"].get("grade_padrao", GRADE), GRADE)) or GRADE
        self.AUTOSAVE_SEG = max(15, int(num_seguro(CONFIG["geral"].get("autosave_seg", 90), 90)))
        self.arrastando = None
        self.antes = None
        self.dir_inicio = None
        self.snap = True
        self.mostrar_grade = True
        self.historico = []
        self.refazer_pilha = []
        self.clipboard = []
        self.clip_eventos = []
        self.clip_txt = ""
        self.editando = None
        self.buffer = ""
        self.prompt = None
        self.mostrar_ajuda = False
        self.filtro_explorer = ""
        self.minimapa = bool(CONFIG["geral"].get("minimapa", True))
        self.passo_giro = 15.0
        self.saida_aberta = False
        self.saida = []
        self.saida_filtro = "Tudo"
        self.saida_scroll = 0
        self.saida_erros_novos = 0
        self.saida_lidos_jogo = 0
        self.hits_saida = []
        self.cats_fechadas = set()
        self.minimapa_rect = None
        self.minimapa_conv = None
        self.sujo = False
        self.ultimo_autosave = 0.0
        self.ultimo_clique = (-1.0, None)
        self.hover = (None, 0.0)
        self.toasts = []
        self.tempo = 0.0
        self.passos_feitos = set()
        self.mostrar_passos = bool(CONFIG["geral"].get("primeiros_passos", True))
        self.passos_min = False
        self.hits_passos = []
        self.hits_vazio = []
        self.msg = "Bem-vindo! Escolha um objeto na esquerda e clique na cena. F1 mostra todos os atalhos."
        self.msg_t = 6.0
        if self.erros_plugins:
            self.msg = "Erro em plugin: " + " | ".join(self.erros_plugins)
            self.msg_t = 10.0
        self.jogo = None
        self.play_cheio = False
        self.entrou_cheio = False
        self.clique_jogo = None
        self.rodando = True
        self.scroll = 0
        self.insp_scroll = 0
        self.insp_total = 0
        self.tempo = 0.0
        self.menu = None
        self.hits_insp = []
        self.hits_esq = []
        self.hits_ev = []
        self.hits_cod = []
        self.hits_api = []
        self.hits_prompt = []
        self.ev_scroll = 0
        self.ev_total = 0
        self.api_itens = construir_api()
        self.api_busca = ""
        self.api_cat = "Todos"
        self.api_scroll = 0
        self.api_total = 0

        # editor de codigo
        self.cod_alvo = None
        self.cod = [""]
        self.cur = [0, 0]
        self.ancora = None
        self.cod_scroll = 0
        self.cod_msg = ""
        self.cod_erro_linha = None
        self.cod_ajuda = False
        self.cod_undo = []
        self.cod_redo = []
        self.cod_ultimo = None
        self.cod_sujo = False
        self.auto = None
        self.busca_cod = ""
        self.gutter = 46
        self.barra_cod = pygame.Rect(VIEW.x, VIEW.y, VIEW.w, 34)
        self.area_cod = pygame.Rect(VIEW.x, VIEW.y + 34, VIEW.w, VIEW.h - 34 - 26)
        self.barra_erro = pygame.Rect(VIEW.x, VIEW.bottom - 26, VIEW.w, 26)

        self.botoes = {}
        x = 8
        for nome, w in [("inicio", 58), ("play", 82), ("playcheio", 100), ("novo", 50), ("salvar", 60),
                        ("desfazer", 70), ("refazer", 64), ("mover", 96), ("girar", 84), ("snap", 66), ("grade", 62),
                        ("modo", 112), ("saida", 62), ("exportar", 74), ("ajuda", 64)]:
            self.botoes[nome] = pygame.Rect(x, 8, w, 30)
            x += w + 5

        self.abas = {}
        x = PAINEL_ESQ + 8
        for nome in ("cena", "eventos", "script", "api", "desenho", "loja"):
            self.abas[nome] = pygame.Rect(x, TOPO + 4, 82, ABAS_H - 4)
            x += 86
        self.botao_fase = pygame.Rect(x + 6, TOPO + 4, 150, ABAS_H - 4)

        larg = (PAINEL_ESQ - 16) // 4
        self.abas_esq = {nome: pygame.Rect(8 + i * larg, TOPO + 6, larg - 2, 24)
                         for i, nome in enumerate(("objetos", "modelos", "imagens", "explorer"))}
        self.pixel = EditorPixel(self)
        self.loja = Loja(self)
        self.seletor = None
        self.img_escolhida = None

        for erro_plugin in self.erros_plugins:
            self.registrar("erro", "Plugin: " + erro_plugin)
        self.checar_autosave()
        if self.fechar_no_inicio:
            self.rodando = False

    @property
    def nome_projeto(self):
        return str(self.projeto.get("nome_projeto") or os.path.basename(self.pasta_projeto) or "Projeto")

    def ir_inicio(self):
        def sair(salvar):
            if salvar:
                self.salvar()
            elif self.sujo:
                self.autosave()
            self.voltar_inicio = True
            self.rodando = False
        if self.jogo:
            self.parar()
        if not self.sujo:
            sair(False)
            return
        opcoes = {"Salvar e voltar ao Início": lambda: sair(True),
                  "Voltar sem salvar (fica no autosave)": lambda: sair(False), "Cancelar": lambda: None}
        self.abrir_menu(self.botoes["inicio"].bottomleft, list(opcoes), lambda it: opcoes[it]())

    def carregar_fontes(self):
        self.f = fonte_ui(16)
        self.fp = fonte_ui(13)
        self.fpp = fonte_ui(11)
        self.fb = fonte_ui(14, True)
        self.fg = fonte_ui(40, True)
        self.fc = fonte_codigo()
        self.cw = max(1, self.fc.size("M")[0])
        self.lh = self.fc.get_linesize() + 2


    # ----------------- loop principal -----------------
    def rodar(self):
        while self.rodando:
            dt = min(self.relogio.tick(60) / 1000.0, 1 / 30)
            self.tempo += dt
            processar_tarefas()
            self.msg_t = max(0.0, self.msg_t - dt)
            apertadas = set()
            soltas = set()
            self.clique_jogo = None
            self.preparar_toque()
            for e in pegar_eventos(self.tela):
                if e.type == pygame.KEYDOWN:
                    apertadas.add(e.key)
                elif e.type == pygame.KEYUP:
                    soltas.add(e.key)
                self.controles.evento(e, apertadas, soltas)
                self.evento(e)
            if self.jogo:
                try:
                    self.jogo.update(dt, self.controles.misturar(pygame.key.get_pressed()), apertadas, soltas=soltas,
                                     mouse=pygame.mouse.get_pos(), clique=self.clique_jogo,
                                     mouse_seg=pygame.mouse.get_pressed()[0])
                    self.puxar_saida_do_jogo()
                    if self.jogo.pedir_reinicio:
                        self.reiniciar_jogo()
                    if self.jogo.pedir_tela is not None:
                        if self.jogo.pedir_tela != self.tela_cheia:
                            self.alternar_tela()
                        self.jogo.pedir_tela = None
                except Exception as ex:  # nunca deixa o editor fechar por causa do jogo
                    self.parar()
                    self.avisar(f"O jogo parou por um erro interno: {ex}")
            if self.sujo and self.tempo - self.ultimo_autosave > self.AUTOSAVE_SEG:
                self.ultimo_autosave = self.tempo
                self.autosave()
            if self.rodando:
                try:
                    self.desenhar()
                except Exception as ex:
                    if self.jogo:
                        self.parar()
                    self.avisar(f"Erro ao desenhar: {ex}")
                    pygame.display.flip()
                titulo = f"Minha Engine - {self.nome_projeto} - {self.projeto['fase_atual']}" + (" *" if self.sujo else "")
                if getattr(self, "_titulo", None) != titulo:
                    self._titulo = titulo
                    pygame.display.set_caption(titulo)
        parar_musica()
        if self.dono_janela:
            pygame.quit()
