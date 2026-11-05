# Minha Engine - inicio.py
# tela Início: criações, novo projeto e configurações
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# INICIO (tela inicial estilo Godot / Roblox Studio): criacoes, novo projeto e configuracoes
# =====================================================================
DESC_MODELOS = {
    "Projeto vazio": "Só o chão e o player. Para começar do zero.",
    "Exemplo: plataforma (2 fases)": "Pulo duplo, vida, inimigos, chefe, checkpoint, lava, chuva e diálogo.",
    "Exemplo: aventura vista de cima": "Atire nos slimes, pegue a chave e fuja pelo portal.",
    "Exemplo: caverna escura (luzes)": "Escuridão com tochas, fogo, moedas que brilham e um morcego.",
    "Projeto vazio (top-down)": "Visão de cima: chão de grama, muros e o player com espada. Para começar do zero.",
    "Exemplo: RPG top-down (vila e masmorra)": "Vila com NPCs, espada, arbustos, baú, lago e uma masmorra com "
                                                "esqueletos, arqueiros e um chefe.",
}


def tempo_atras(ts):
    import time
    seg = max(0, time.time() - ts)
    if seg < 60:
        return "agora mesmo"
    if seg < 3600:
        return f"há {int(seg // 60)} min"
    if seg < 86400:
        return f"há {int(seg // 3600)} h"
    dias = int(seg // 86400)
    return "ontem" if dias == 1 else f"há {dias} dias"


def loop_jogo(tela, relogio, projeto, fase=None):
    """Roda um jogo ocupando a janela. Retorna False se fecharam a janela, True se apertaram Esc."""
    controles = Controles()
    fonte_ = fonte_ui(18)
    fonte_g = fonte_ui(44, True)
    fase = fase or projeto.get("fase_inicial")
    novo = lambda: Jogo(projeto, tela.get_rect(), sozinho=True, fase=fase)
    jogo = novo()
    while True:
        dt = min(relogio.tick(60) / 1000.0, 1 / 30)
        apertadas, soltas, clique = set(), set(), None
        TOQUE.areas_arrasto = []
        TOQUE.usar_pad(jogo, jogo.area)
        for e in pegar_eventos(tela):
            controles.evento(e, apertadas, soltas)
            if e.type == pygame.QUIT:
                TOQUE.usar_pad(None, None)
                parar_musica()
                return False
            if e.type == pygame.KEYUP:
                soltas.add(e.key)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                clique = e.pos
            elif e.type == pygame.KEYDOWN:
                apertadas.add(e.key)
                if e.key == pygame.K_ESCAPE:
                    TOQUE.usar_pad(None, None)
                    parar_musica()
                    return True
                if e.key == pygame.K_F11:
                    alternar_tela_cheia()
                elif jogo.quer_reiniciar(e.key) and (jogo.venceu or jogo.perdeu):
                    jogo = novo()
        jogo.update(dt, controles.misturar(pygame.key.get_pressed()), apertadas, soltas=soltas,
                    mouse=pygame.mouse.get_pos(), clique=clique, mouse_seg=pygame.mouse.get_pressed()[0])
        if jogo.pedir_reinicio:
            jogo = novo()
        if jogo.pedir_tela is not None:
            if jogo.pedir_tela != JANELA["cheia"]:
                alternar_tela_cheia()
            jogo.pedir_tela = None
        tela.fill((0, 0, 0))
        jogo.desenhar(tela, fonte_, fonte_g)
        TOQUE.desenhar_pad(tela)
        pygame.display.flip()


class Inicio:
    BARRA = 240
    CARD_W, CARD_H, THUMB_H, GAP = 236, 222, 133, 18

    def __init__(self, tela, relogio):
        self.tela = tela
        self.relogio = relogio
        self.tempo = 0.0
        self.pagina = "criacoes"
        self.config_aba = "atalhos"
        self.projetos = []
        self.busca = ""
        self.ordem = "recentes"
        self.foco = None
        self.sel = None
        self.scroll = 0
        self.scroll_cfg = 0
        self.hits = []
        self.menu = None
        self.modal = None
        self.capturando = None
        self.paleta = None
        self.ultimo_clique = (-1.0, None)
        self.msg, self.msg_t = "", 0.0
        self.thumbs = {}
        self.thumbs_modelo = {}
        self.novo_nome = ""
        self.novo_modelo = "Exemplo: plataforma (2 fases)"
        self.resultado = None
        self.jogos_ordem = "curtidos"
        self.jogos_fonte = "mundo"
        self.jogos_online = None
        self.jogos_erro = ""
        self.carregando_jogos = False
        self.espera = None
        self.sair_pedido = False
        self.jogos_filtro = "todos"
        self.scroll_jogos = 0
        self.recarregar()
        carteira()
        if len(listar_usuarios()) > 1 and not online_ativo() and not CONFIG["geral"].get("pular_usuarios"):
            self.pagina = "usuarios"
        if NOVIDADES_CARTEIRA:
            self.avisar(" · ".join(NOVIDADES_CARTEIRA))
            NOVIDADES_CARTEIRA.clear()

    # ----------------- dados -----------------
    def recarregar(self):
        self.projetos = listar_projetos()
        self.thumbs.clear()

    def visiveis(self):
        b = self.busca.lower().strip()
        lista = [p for p in self.projetos if not b or b in p["nome"].lower()]
        if self.ordem == "nome":
            lista.sort(key=lambda p: p["nome"].lower())
        else:
            lista.sort(key=lambda p: -p["mudado"])
        return lista

    def avisar(self, txt):
        self.msg, self.msg_t = txt, 4.0

    def miniatura(self, proj, w, h):
        chave = (proj["pasta"], w, h)
        if chave in self.thumbs:
            return self.thumbs[chave]
        img = None
        try:
            if os.path.isfile(proj["miniatura"]):
                img = pygame.transform.smoothscale(pygame.image.load(proj["miniatura"]), (w, h))
        except (pygame.error, OSError, ValueError, AttributeError):
            img = None
        if img is None:
            img = pygame.Surface((w, h))
            img.fill((34, 37, 46))
            desenhar_simbolo(img, w // 2 - 28, h // 2 - 28, 56, alpha=120)
        self.thumbs[chave] = img
        return img

    def miniatura_modelo(self, nome, w, h):
        if nome not in self.thumbs_modelo:
            try:
                if nome in EXEMPLOS:
                    proj = completar_projeto(EXEMPLOS[nome]())
                else:
                    proj = completar_projeto({"fases": {"Fase 1": fase_padrao()}})
                    proj["fases"]["Fase 1"]["objetos"].append(nova_entidade("Player", 80, 400))
                fase = proj["fases"][proj["fase_inicial"]]
                self.thumbs_modelo[nome] = pygame.transform.smoothscale(criar_miniatura(fase, (320, 180)), (w, h))
            except (pygame.error, ValueError, AttributeError):
                surf = pygame.Surface((w, h))
                surf.fill((34, 37, 46))
                self.thumbs_modelo[nome] = surf
        return self.thumbs_modelo[nome]

    # ----------------- acoes com projetos -----------------
    def abrir(self, proj):
        self.resultado = proj["pasta"]

    def jogar(self, proj):
        try:
            with open(os.path.join(proj["pasta"], "projeto.json"), encoding="utf-8") as f:
                dados = completar_projeto(json.load(f))
        except (OSError, ValueError) as ex:
            self.avisar(f"Não consegui abrir: {ex}")
            return True
        if not any(d.get("tipo") == "Player" for d in dados["fases"][dados["fase_inicial"]]["objetos"]):
            self.avisar("Esse projeto não tem Player na fase inicial.")
            return True
        definir_projeto(proj["pasta"])
        aplicar_controles(CONFIG["controles"])
        continuar = loop_jogo(self.tela, self.relogio, dados)
        pygame.display.set_caption("Minha Engine")
        return continuar

    def publicar(self, proj):
        if online_ativo():
            def fim(msg, erro):
                self.avisar(f"Não consegui publicar: {erro}" if erro else msg)
                if not erro:
                    self.pagina, self.jogos_fonte = "jogos", "mundo"
                    self.recarregar_jogos()
            self.tarefa_com_espera("Enviando o jogo para a internet...", publicar_online, fim, proj["pasta"])
            return
        try:
            ja = publicacao_de(proj["pasta"])
            m = publicar_projeto(proj["pasta"])
            self.avisar(("Publicação atualizada: " if ja else "Publicado! ") + f"'{m['titulo']}' está na área de "
                        f"Jogos. Cada visita dá +{BRASAS_VISITA} e cada like +{BRASAS_LIKE} {MOEDA}.")
            self.pagina = "jogos"
        except (OSError, ValueError, KeyError) as ex:
            self.avisar(f"Não consegui publicar: {ex}")

    def entrar_usuario(self, u, pin):
        if not confere_pin(u, pin):
            self.avisar("Senha errada.")
            return
        entrar(u["id"])
        self.pagina = "criacoes"
        self.avisar(f"Oi, {u['nome']}!")
        if NOVIDADES_CARTEIRA:
            self.avisar(" · ".join(NOVIDADES_CARTEIRA))
            NOVIDADES_CARTEIRA.clear()

    def novo_usuario_nome(self, nome):
        nome = nome.strip()
        if not nome:
            return
        self.pedir_texto(f"Senha (PIN) para {nome} - opcional, deixe vazio para não usar", "",
                         lambda pin: self.criar_usuario(nome, pin.strip()))

    def criar_usuario(self, nome, pin):
        try:
            criar_usuario(nome, pin)
        except ValueError as ex:
            self.avisar(str(ex))
            return
        self.pagina = "criacoes"
        self.avisar(f"Usuário '{nome}' criado! Ganhou {fmt_brasas(BONUS_BOAS_VINDAS)} de boas-vindas.")
        NOVIDADES_CARTEIRA.clear()

    # ----------------- paginas: jogos publicados e usuarios -----------------
    def desenhar_jogos(self, t, mouse, area):
        x0 = area.x + 32
        mundo = online_ativo() and self.jogos_fonte == "mundo"
        t.blit(texto_cache("Jogos publicados", 30, C_TEXTO, True), (x0, 30))
        sub = (f"Jogos do MUNDO TODO. Cada visita nova dá +{BRASAS_VISITA} e cada like +{BRASAS_LIKE} {MOEDA} para "
               f"quem fez (1 vez por pessoa)." if mundo else
               f"Jogos deste computador. Cada visita nova dá +{BRASAS_VISITA} e cada like +{BRASAS_LIKE} {MOEDA}.")
        t.blit(texto_cache(sub, 13, C_TEXTO2), (x0 + 2, 70))
        x = x0
        if online_ativo():
            for chave, rot in (("mundo", "Mundo todo"), ("local", "Neste PC")):
                w = texto_cache(rot, 13, C_TEXTO).get_width() + 24
                self.botao(pygame.Rect(x, 96, w, 28), rot, ("jogos_fonte", chave), mouse, fonte_tam=13,
                           ativo=self.jogos_fonte == chave, cor=(40, 110, 70) if chave == "mundo" else None)
                x += w + 6
            x += 14
        for chave, rot in (("curtidos", "Mais curtidos"), ("jogados", "Mais jogados"), ("recentes", "Recentes")):
            w = texto_cache(rot, 13, C_TEXTO).get_width() + 24
            self.botao(pygame.Rect(x, 96, w, 28), rot, ("jogos_ordem", chave), mouse, fonte_tam=13,
                       ativo=self.jogos_ordem == chave)
            x += w + 6
        x += 14
        for chave, rot in (("todos", "Todos"), ("meus", "Só os meus")):
            w = texto_cache(rot, 13, C_TEXTO).get_width() + 24
            self.botao(pygame.Rect(x, 96, w, 28), rot, ("jogos_filtro", chave), mouse, fonte_tam=13,
                       ativo=self.jogos_filtro == chave)
            x += w + 6
        if mundo:
            self.botao(pygame.Rect(x + 8, 96, 96, 28), "Atualizar", ("recarregar_jogos",), mouse, fonte_tam=13)
        elif not online_ativo():
            self.botao(pygame.Rect(area.right - 290, 30, 258, 36), "Entrar online (mundo todo)",
                       ("pagina", "usuarios"), mouse, cor=(40, 110, 70), fonte_tam=14, negrito=True)
        jogos = self.lista_de_jogos()
        if self.jogos_filtro == "meus":
            jogos = [m for m in jogos if m["meu"]]
        chave = {"curtidos": lambda m: (m["n_likes"], m["n_visitas"]),
                 "jogados": lambda m: (m["n_visitas"], m["n_likes"]),
                 "recentes": lambda m: (m.get("atualizado", 0),)}[self.jogos_ordem]
        jogos.sort(key=chave, reverse=True)
        grade = pygame.Rect(area.x + 20, 136, area.w - 40, ALTURA - 150)
        if mundo and self.jogos_online is None:
            t.blit(texto_cache("Carregando os jogos do mundo todo" + "." * (int(self.tempo * 3) % 4), 18, C_TEXTO, True),
                   (grade.x + 14, grade.y + 20))
            return
        if mundo and self.jogos_erro:
            t.blit(texto_cache(self.jogos_erro, 15, (240, 140, 140)), (grade.x + 14, grade.y + 20))
            return
        if not jogos:
            for i, linha in enumerate(["Nenhum jogo publicado ainda.",
                                       "Em 'Minhas criações', clique no ··· de um projeto e escolha 'Publicar'.",
                                       "Ou no editor: botão Exportar > Publicar."]):
                t.blit(texto_cache(linha, 18 if i == 0 else 14, C_TEXTO if i == 0 else C_TEXTO2, i == 0),
                       (grade.x + 14, grade.y + 20 + i * 30))
            return
        colunas = max(1, (grade.w + self.GAP) // (self.CARD_W + self.GAP))
        livre = grade.w - colunas * self.CARD_W - (colunas - 1) * self.GAP
        xi = grade.x + livre // 2
        alto = self.CARD_H + 20
        total = ((len(jogos) + colunas - 1) // colunas) * (alto + self.GAP)
        self.scroll_jogos = max(0, min(self.scroll_jogos, max(0, total - grade.h)))
        vis_j = suave((id(self), "jogos"), self.scroll_jogos)
        t.set_clip(grade)
        for i, m in enumerate(jogos):
            col, lin = i % colunas, i // colunas
            r = pygame.Rect(xi + col * (self.CARD_W + self.GAP), grade.y + 6 + lin * (alto + self.GAP) -
                            vis_j, self.CARD_W, alto)
            if r.bottom < grade.y or r.y > grade.bottom:
                continue
            self.desenhar_card_jogo(t, mouse, m, r, grade)
        t.set_clip(None)

    def lista_de_jogos(self):
        if online_ativo() and self.jogos_fonte == "mundo":
            if self.jogos_online is None and not self.carregando_jogos:
                self.recarregar_jogos()
            return list(self.jogos_online or [])
        res = []
        for m in listar_publicados():
            m.update({"n_likes": len(m["likes"]), "n_visitas": len(m["visitas"]), "meu": e_meu(m),
                      "eu_curti": usuario_atual()["id"] in m["likes"], "online": False})
            res.append(m)
        return res

    def recarregar_jogos(self):
        self.carregando_jogos = True
        self.jogos_online, self.jogos_erro = None, ""

        def pronto(lista, erro):
            self.carregando_jogos = False
            self.jogos_online = lista or []
            self.jogos_erro = erro or ""
            for m in self.jogos_online:
                if m.get("miniatura_url") and not os.path.isfile(m["miniatura"]):
                    em_segundo_plano(baixar_miniatura, lambda _r, _e, m=m: self.thumbs.pop((m["pasta"], self.CARD_W,
                                                                                         self.THUMB_H), None), m)
        em_segundo_plano(listar_publicados_online, pronto)

    def desenhar_card_jogo(self, t, mouse, m, r, grade):
        meu = m["meu"]
        pygame.draw.rect(t, (40, 43, 53) if r.collidepoint(mouse) else (34, 37, 45), r, border_radius=10)
        t.blit(self.miniatura(m, r.w, self.THUMB_H), r.topleft)
        if meu:
            pygame.draw.rect(t, C_DESTAQUE, r, 2, border_radius=10)
        if m.get("online"):
            pygame.draw.circle(t, (60, 200, 110), (r.right - 14, r.y + 14), 6)
        titulo = m["nome"] if len(m["nome"]) <= 24 else m["nome"][:23] + "…"
        t.blit(texto_cache(titulo, 15, C_TEXTO, True), (r.x + 12, r.y + self.THUMB_H + 8))
        t.blit(texto_cache(("por você" if meu else f"por {m.get('autor', '?')}") +
                           f" · {tempo_atras(m.get('atualizado', 0))}", 12, C_TEXTO2), (r.x + 12, r.y + self.THUMB_H + 28))
        yy = r.y + self.THUMB_H + 48
        desenhar_coracao(t, (r.x + 20, yy + 7), 6, cheio=True)
        t.blit(texto_cache(str(m["n_likes"]), 13, C_TEXTO, True), (r.x + 32, yy))
        pygame.draw.circle(t, (150, 160, 190), (r.x + 76, yy + 7), 6, 2)
        pygame.draw.circle(t, (150, 160, 190), (r.x + 76, yy + 7), 2)
        t.blit(texto_cache(f"{m['n_visitas']} visita(s)", 13, C_TEXTO2), (r.x + 88, yy))
        by = r.bottom - 34
        if by + 28 <= grade.bottom and by >= grade.y:
            self.botao(pygame.Rect(r.x + 10, by, 92, 26), "Jogar", ("jogar_pub", m), mouse, cor=(48, 120, 78),
                       fonte_tam=13, negrito=True)
            if meu:
                self.botao(pygame.Rect(r.x + 108, by, 82, 26), "Seu jogo", None, mouse, cor=(50, 54, 66), fonte_tam=12)
            else:
                curtiu = m["eu_curti"]
                br = pygame.Rect(r.x + 108, by, 82, 26)
                self.botao(br, "Curtido" if curtiu else f"  +{BRASAS_LIKE}", None if curtiu else ("like", m),
                           mouse, cor=(150, 50, 80) if curtiu else (200, 60, 95), fonte_tam=13)
                desenhar_coracao(t, (br.x + 14, br.centery), 5, cheio=curtiu, cor=(255, 255, 255))
            self.botao(pygame.Rect(r.x + 196, by, 30, 26), "···", ("pub_mais", m), mouse, fonte_tam=13)

    def projeto_da_publicacao(self, m):
        if not m.get("online"):
            return m.get("origem", "")
        for proj in listar_projetos():
            pub = publicacao_online_de(proj["pasta"])
            if pub and pub.get("id") == m["id"]:
                return proj["pasta"]
        return ""

    def tarefa_com_espera(self, texto, fn, ao_terminar, *args):
        self.espera = texto
        def fim(res, erro):
            self.espera = None
            ao_terminar(res, erro)
        em_segundo_plano(fn, fim, *args)

    def acao_online(self, k):
        def fim(msg, erro):
            self.avisar(erro or msg)
            if not erro and k in ("online_entrar", "online_criar") and online_ativo():
                self.pagina = "criacoes"
                self.jogos_online = None
        if k == "online_entrar":
            self.pedir_texto("Seu e-mail", "", lambda email: self.pedir_texto(
                "Sua senha", "", lambda senha: self.tarefa_com_espera("Entrando...", entrar_online, fim, email, senha),
                senha=True))
        elif k == "online_criar":
            self.pedir_texto("Nome que todo mundo vai ver (2 a 24 letras)", "", lambda nome: self.pedir_texto(
                "Seu e-mail", "", lambda email: self.pedir_texto(
                    "Crie uma senha (pelo menos 6 caracteres)", "", lambda senha: self.tarefa_com_espera(
                        "Criando sua conta...", cadastrar_online, fim, nome, email, senha), senha=True)))
        elif k == "online_sair":
            sair_online()
            self.jogos_online = None
            self.avisar("Você saiu da conta online. Agora está usando o modo sem internet.")
        elif k == "online_nome":
            self.pedir_texto("Novo nome", nome_usuario(), lambda txt: self.avisar(renomear_usuario(txt) or "Nome trocado."))
        elif k == "online_esqueci":
            self.pedir_texto("Seu e-mail (vamos mandar um link para trocar a senha)", "", lambda email:
                             self.tarefa_com_espera("Enviando...", esqueci_senha, fim, email))

    def desenhar_usuarios(self, t, mouse, area):
        x0 = area.x + 32
        t.blit(texto_cache("Sua conta", 30, C_TEXTO, True), (x0, 30))
        caixa = pygame.Rect(x0, 76, min(760, area.w - 64), 118)
        pygame.draw.rect(t, (32, 40, 36) if online_ativo() else (32, 35, 43), caixa, border_radius=14)
        pygame.draw.rect(t, (60, 200, 110) if online_ativo() else C_BORDA, caixa, 1, border_radius=14)
        if online_ativo():
            u = usuario_online()
            desenhar_avatar(t, u, (caixa.x + 52, caixa.centery), 34)
            t.blit(texto_cache(u["nome"], 22, C_TEXTO, True), (caixa.x + 100, caixa.y + 18))
            pygame.draw.circle(t, (60, 200, 110), (caixa.x + 106, caixa.y + 63), 5)
            t.blit(texto_cache(f"ONLINE  ·  {u['email']}", 13, (150, 220, 170)), (caixa.x + 116, caixa.y + 55))
            t.blit(texto_cache(f"{fmt_brasas(carteira()['saldo'])}  ·  plano {plano_atual()}", 13, C_TEXTO2),
                   (caixa.x + 100, caixa.y + 80))
            for i, (rot, acao, cor) in enumerate((("Trocar nome", ("online_nome",), None),
                                                   ("Sair da conta", ("online_sair",), (90, 50, 54)))):
                self.botao(pygame.Rect(caixa.right - 150, caixa.y + 18 + i * 44, 134, 34), rot, acao, mouse, cor=cor,
                           fonte_tam=13)
        else:
            t.blit(texto_cache("Conta online: jogue e publique com o MUNDO TODO", 18, C_TEXTO, True),
                   (caixa.x + 20, caixa.y + 16))
            t.blit(texto_cache("Visitas, likes e Brasas ficam guardados no servidor (ninguém trapaceia).", 13,
                               C_TEXTO2), (caixa.x + 20, caixa.y + 44))
            x = caixa.x + 20
            for rot, acao, cor in (("Entrar", ("online_entrar",), C_DESTAQUE), ("Criar conta", ("online_criar",), C_VERDE),
                                   ("Esqueci a senha", ("online_esqueci",), (60, 64, 78))):
                w = texto_cache(rot, 14, C_TEXTO, True).get_width() + 36
                self.botao(pygame.Rect(x, caixa.y + 70, w, 34), rot, acao, mouse, cor=cor, fonte_tam=14, negrito=True)
                x += w + 10
        t.blit(texto_cache("Usuários deste computador (funcionam sem internet)", 16, C_TEXTO, True), (x0, 214))
        usuarios = listar_usuarios()
        atual = "" if online_ativo() else usuario_atual()["id"]
        x, y = x0, 244
        lado = 130
        for u in usuarios + [None]:
            if x + lado > area.right - 20:
                x, y = x0, y + lado + 70
            r = pygame.Rect(x, y, lado, lado + 50)
            em_cima = r.collidepoint(mouse) and not self.modal and not self.menu
            pygame.draw.rect(t, (40, 43, 53) if em_cima else (32, 35, 43), r, border_radius=14)
            if u is None:
                pygame.draw.circle(t, (60, 64, 78), (r.centerx, r.y + 56), 36, 3)
                img = texto_cache("+", 40, C_TEXTO2, True)
                t.blit(img, (r.centerx - img.get_width() // 2, r.y + 56 - img.get_height() // 2))
                img = texto_cache("Novo usuário", 15, C_TEXTO, True)
                t.blit(img, (r.centerx - img.get_width() // 2, r.y + 120))
                self.hits.append((r, ("novo_usuario",)))
            else:
                desenhar_avatar(t, u, (r.centerx, r.y + 56), 36)
                if u["id"] == atual:
                    pygame.draw.rect(t, C_DESTAQUE, r, 2, border_radius=14)
                img = texto_cache(u["nome"][:16], 15, C_TEXTO, True)
                t.blit(img, (r.centerx - img.get_width() // 2, r.y + 114))
                c = u.get("carteira") or {}
                img = texto_cache(fmt_brasas(c.get("saldo", 0)), 12, C_TEXTO2)
                t.blit(img, (r.centerx - img.get_width() // 2 + 8, r.y + 136))
                desenhar_moeda(t, (r.centerx - img.get_width() // 2 - 4, r.y + 143), 6)
                plano = c.get("plano", "Grátis") if c.get("plano_ate", 0) > _tempo.time() else "Grátis"
                selo_w = texto_cache(PLANOS[plano]["selo"], 9, C_TEXTO, True).get_width() + 14
                desenhar_selo(t, r.centerx - selo_w // 2, r.y + 158, plano, 9)
                if u.get("pin"):
                    t.blit(texto_cache("com senha", 10, C_TEXTO2), (r.x + 8, r.y + 8))
                self.hits.append((r, ("entrar", u)))
            x += lado + 20
        if not online_ativo():
            self.botao(pygame.Rect(x0, ALTURA - 60, 200, 36), "Renomear meu usuário", ("renomear_usuario",), mouse,
                       fonte_tam=13)

    def renomear(self, proj, novo):
        novo = novo.strip()
        if not novo:
            return
        arq = os.path.join(proj["pasta"], "projeto.json")
        try:
            with open(arq, encoding="utf-8") as f:
                dados = json.load(f)
            dados["nome_projeto"] = novo
            with open(arq, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            destino = nome_pasta_livre(novo)
            try:
                os.rename(proj["pasta"], destino)
            except OSError:
                pass   # se a pasta estiver aberta em outro programa, so o nome muda
            self.avisar(f"Renomeado para '{novo}'.")
        except (OSError, ValueError) as ex:
            self.avisar(f"Não consegui renomear: {ex}")
        self.recarregar()

    def duplicar(self, proj):
        try:
            destino = nome_pasta_livre(proj["nome"] + " cópia")
            shutil.copytree(proj["pasta"], destino, ignore=shutil.ignore_patterns("exportado"))
            arq = os.path.join(destino, "projeto.json")
            with open(arq, encoding="utf-8") as f:
                dados = json.load(f)
            dados["nome_projeto"] = os.path.basename(destino)
            with open(arq, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            self.avisar(f"Cópia criada: {os.path.basename(destino)}")
        except (OSError, ValueError) as ex:
            self.avisar(f"Não consegui duplicar: {ex}")
        self.recarregar()

    def apagar(self, proj):
        """Nao apaga de verdade: move para a pasta 'lixeira' (dá para recuperar)."""
        import time
        pasta = proj["pasta"]
        lixeira = os.path.join(PASTA, "lixeira")
        try:
            os.makedirs(lixeira, exist_ok=True)
            shutil.move(pasta, os.path.join(lixeira, f"{os.path.basename(pasta)} {int(time.time())}"))
        except OSError:
            # plano B: se nao der para mover (arquivo aberto em outro programa), apaga de vez
            def tirar_trava(func, caminho, _):
                try:
                    os.chmod(caminho, 0o700)
                    func(caminho)
                except OSError:
                    pass
            shutil.rmtree(pasta, onerror=tirar_trava)
        if os.path.exists(os.path.join(pasta, "projeto.json")):
            self.avisar("Não consegui apagar: feche os programas que estão usando a pasta do projeto e tente de novo.")
        else:
            self.avisar(f"'{proj['nome']}' foi apagado (fica na pasta lixeira, dá para recuperar).")
            if CONFIG["geral"].get("ultimo_projeto") == pasta:
                CONFIG["geral"]["ultimo_projeto"] = ""
                salvar_config()
        self.sel = None
        self.recarregar()

    def criar(self):
        nome = self.novo_nome.strip() or f"Meu Jogo {len(self.projetos) + 1}"
        try:
            pasta = criar_projeto(nome, None if self.novo_modelo == "Projeto vazio" else self.novo_modelo)
            self.resultado = pasta
        except (OSError, pygame.error) as ex:
            self.avisar(f"Não consegui criar: {ex}")

    # ----------------- eventos -----------------
    def rodar(self):
        while self.resultado is None:
            dt = self.relogio.tick(60) / 1000.0
            self.tempo += dt
            self.msg_t = max(0.0, self.msg_t - dt)
            processar_tarefas()
            if self.sair_pedido:
                return None
            TOQUE.areas_arrasto = []
            TOQUE.usar_pad(None, None)
            pedir_teclado(bool((self.modal and self.modal.get("tipo") == "texto") or self.foco))
            for e in pegar_eventos(self.tela):
                if e.type == pygame.QUIT:
                    return None
                if self.evento(e) is False:
                    return None
                if self.resultado is not None:
                    break
            self.desenhar()
            pygame.display.flip()
        return self.resultado

    def evento(self, e):
        if e.type == TOQUE_GESTO:
            gesto_para_rodinha(e, self.evento)
            return None
        if e.type == pygame.KEYDOWN:
            return self.tecla(e)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            return self.clique(e.pos)
        if e.type == pygame.MOUSEWHEEL:
            if self.pagina == "criacoes":
                self.scroll = max(0, self.scroll - e.y * 60)
            elif self.pagina == "config":
                self.scroll_cfg = max(0, self.scroll_cfg - e.y * 50)
            elif self.pagina == "jogos":
                self.scroll_jogos = max(0, self.scroll_jogos - e.y * 60)
        return None

    def tecla(self, e):
        if self.capturando:
            self.capturar(e)
            return None
        if e.key == pygame.K_F11:
            alternar_tela_cheia()
            return None
        if self.modal and self.modal["tipo"] == "texto":
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                m, self.modal = self.modal, None
                m["fn"](m["texto"])
            elif e.key == pygame.K_ESCAPE:
                self.modal = None
            elif e.key == pygame.K_BACKSPACE:
                self.modal["texto"] = self.modal["texto"][:-1]
            elif e.key == pygame.K_v and e.mod & pygame.KMOD_CTRL:
                try:
                    if not pygame.scrap.get_init():
                        pygame.scrap.init()
                    colado = pygame.scrap.get_text() or ""
                except (pygame.error, AttributeError, NotImplementedError):
                    colado = ""
                self.modal["texto"] = (self.modal["texto"] + colado.strip().split("\n")[0])[:80]
            elif e.unicode and e.unicode.isprintable() and len(self.modal["texto"]) < 80:
                self.modal["texto"] += e.unicode
            return None
        if self.modal and e.key == pygame.K_ESCAPE:
            self.modal = None
            return None
        if self.paleta and e.key == pygame.K_ESCAPE:
            self.paleta = None
            return None
        if self.menu and e.key == pygame.K_ESCAPE:
            self.menu = None
            return None
        campo = {"busca": "busca", "nome": "novo_nome"}.get(self.foco)
        if campo:
            if e.key == pygame.K_BACKSPACE:
                setattr(self, campo, getattr(self, campo)[:-1])
            elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.foco == "nome":
                    self.criar()
                self.foco = None
            elif e.key == pygame.K_ESCAPE:
                self.foco = None
            elif e.unicode and e.unicode.isprintable() and len(getattr(self, campo)) < 50:
                setattr(self, campo, getattr(self, campo) + e.unicode)
                self.scroll = 0
            return None
        if self.pagina == "criacoes":
            vis = self.visiveis()
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.sel:
                self.abrir(self.sel)
            elif e.key == pygame.K_DELETE and self.sel:
                self.confirmar_apagar(self.sel)
            elif e.key in (pygame.K_RIGHT, pygame.K_LEFT) and vis:
                i = next((k for k, p in enumerate(vis) if self.sel and p["pasta"] == self.sel["pasta"]), -1)
                i = max(0, min(len(vis) - 1, i + (1 if e.key == pygame.K_RIGHT else -1)))
                self.sel = vis[i]
            elif e.unicode and e.unicode.isprintable():
                self.foco = "busca"
                self.busca += e.unicode
        return None

    def confirmar_apagar(self, proj):
        self.modal = {"tipo": "confirmar", "titulo": f"Apagar '{proj['nome']}'?",
                      "msg": "Ele vai para a pasta 'lixeira' ao lado da engine (dá para recuperar).",
                      "botao": "Apagar", "fn": lambda: self.apagar(proj)}

    def duplo(self, alvo):
        t0, anterior = self.ultimo_clique
        self.ultimo_clique = (self.tempo, alvo)
        return anterior == alvo and self.tempo - t0 < 0.4

    def clique(self, pos):
        if self.capturando:
            return None
        if self.menu:
            m, self.menu = self.menu, None
            for item, r in m["rects"]:
                if r.collidepoint(pos):
                    m["fn"](item)
            return None
        alvos = list(self.hits)
        self.foco = None
        if self.paleta:
            escolheu = next((a for r, a in reversed(alvos) if r.collidepoint(pos) and a[0] in ("sc_pick", "sc_cor")), None)
            if escolheu is None or escolheu[0] == "sc_pick":
                if escolheu:
                    self.executar(escolheu, pos)
                self.paleta = None
                return None
        for r, acao in reversed(alvos):
            if r.collidepoint(pos):
                return self.executar(acao, pos)
        if self.modal:
            return None
        if self.pagina == "criacoes":
            self.sel = None
        return None

    def executar(self, acao, pos):
        k = acao[0]
        if k in ("bonus", "assinar"):
            self.avisar(acao_carteira(acao))
            return
        if k == "secreto":
            self.pedir_texto("Código", "", lambda senha: self.avisar(usar_codigo_secreto(senha)[1]))
            return
        if k == "jogar_pub":
            m = acao[1]
            if m.get("online"):
                def baixou(pasta, erro, m=m):
                    if erro:
                        self.avisar(f"Não consegui baixar o jogo: {erro}")
                        return
                    try:
                        ganho = visitar_online(m)
                    except ErroOnline:
                        ganho = 0
                    if self.jogar({"pasta": pasta}) is False:
                        self.sair_pedido = True
                    if ganho:
                        self.avisar(f"Sua visita deu +{ganho} {MOEDA} para {m.get('autor')}. Gostou? Curta o jogo!")
                self.tarefa_com_espera(f"Baixando '{m['nome']}'...", baixar_jogo_online, baixou, m)
                return
            ganho = registrar_visita(m)
            continuar = self.jogar(m)
            if ganho:
                self.avisar(f"Sua visita deu +{ganho} {MOEDA} para {m.get('autor')}. Gostou? Clique em Curtir!")
            return False if continuar is False else None
        if k == "like":
            m = acao[1]
            if m.get("online"):
                try:
                    self.avisar(curtir_online(m))
                except ErroOnline as e:
                    self.avisar(str(e))
                return
            self.avisar(dar_like(m)[1])
            return
        if k == "jogos_fonte":
            self.jogos_fonte = acao[1]
            return
        if k == "recarregar_jogos":
            self.recarregar_jogos()
            return
        if k in ("online_entrar", "online_criar", "online_sair", "online_nome", "online_esqueci"):
            self.acao_online(k)
            return
        if k == "jogos_ordem":
            self.jogos_ordem = acao[1]
            return
        if k == "jogos_filtro":
            self.jogos_filtro = acao[1]
            return
        if k == "pub_mais":
            m = acao[1]
            if not m["meu"]:
                if not m.get("online"):
                    self.avisar(f"Jogo de {m.get('autor')}, publicado neste computador.")
                    return
                opcoes = {"Denunciar (conteúdo impróprio)": lambda: self.pedir_texto(
                    f"Por que denunciar '{m['nome']}'?", "", lambda motivo: self.avisar(denunciar_online(m, motivo)))}
                self.abrir_menu(pos, list(opcoes), lambda it: opcoes[it]())
                return
            origem = self.projeto_da_publicacao(m)
            opcoes = {}
            if origem and os.path.isdir(origem):
                opcoes["Atualizar com a versão atual do projeto"] = lambda: self.publicar({"pasta": origem,
                                                                                         "nome": m.get("titulo")})

            def tirar(it):
                if not it.startswith("Sim"):
                    return
                try:
                    despublicar_online(m) if m.get("online") else despublicar(m)
                    self.avisar("Jogo despublicado.")
                except ErroOnline as e:
                    self.avisar(str(e))
                if m.get("online"):
                    self.recarregar_jogos()
            opcoes["Tirar da internet" if m.get("online") else "Tirar da área de Jogos"] = lambda: self.abrir_menu(
                pos, [f"Sim, despublicar '{m.get('titulo')}'", "Cancelar"], tirar)
            self.abrir_menu(pos, list(opcoes), lambda it: opcoes[it]())
            return
        if k == "entrar":
            u = acao[1]
            if u.get("pin"):
                self.pedir_texto(f"Senha (PIN) de {u['nome']}", "", lambda pin, u=u: self.entrar_usuario(u, pin))
            else:
                self.entrar_usuario(u, "")
            return
        if k == "novo_usuario":
            self.pedir_texto("Nome do novo usuário", "", self.novo_usuario_nome)
            return
        if k == "renomear_usuario":
            self.pedir_texto("Novo nome do usuário", nome_usuario(), lambda txt: (renomear_usuario(txt),
                                                                                   self.avisar("Nome trocado.")))
            return
        if k == "pagina":
            self.pagina = acao[1]
            self.menu = None
            self.scroll = self.scroll_cfg = 0
            if acao[1] == "criacoes":
                self.recarregar()
            if acao[1] == "novo":
                self.novo_nome = ""
                self.foco = "nome"
        elif k == "modal_ok":
            m, self.modal = self.modal, None
            if m["tipo"] == "texto":
                m["fn"](m["texto"])
            else:
                m["fn"]()
        elif k == "modal_cancelar":
            self.modal = None
        elif k == "modal_campo":
            pass
        elif self.modal:
            return None
        elif k == "sair":
            return False
        elif k == "abrir_pasta":
            abrir_pasta(PASTA_PROJETOS)
        elif k == "foco":
            self.foco = acao[1]
        elif k == "ordem":
            self.ordem = "nome" if self.ordem == "recentes" else "recentes"
        elif k == "card":
            proj = acao[1]
            if self.duplo(proj["pasta"]):
                self.abrir(proj)
            self.sel = proj
        elif k == "editar":
            self.abrir(acao[1])
        elif k == "jogar":
            if self.jogar(acao[1]) is False:
                return False
        elif k == "mais":
            proj = acao[1]
            opcoes = {"Renomear": lambda: self.pedir_texto("Novo nome do projeto", proj["nome"],
                                                             lambda txt: self.renomear(proj, txt)),
                      "Duplicar": lambda: self.duplicar(proj),
                      "Abrir a pasta do projeto": lambda: abrir_pasta(proj["pasta"]),
                      (("Atualizar o jogo online" if publicacao_online_de(proj["pasta"]) else
                        "Publicar para o mundo todo") if online_ativo() else
                       ("Atualizar publicação" if publicacao_de(proj["pasta"]) else "Publicar na área de Jogos")):
                          lambda: self.publicar(proj),
                      "Apagar": lambda: self.confirmar_apagar(proj)}
            self.abrir_menu(pos, list(opcoes), lambda it: opcoes[it]())
        elif k == "modelo":
            self.novo_modelo = acao[1]
        elif k == "criar":
            self.criar()
        elif k == "cfg_aba":
            self.config_aba = acao[1]
            self.scroll_cfg = 0
        elif k == "tecla":            # ("tecla", categoria, acao, indice ou None para adicionar)
            self.capturando = acao[1:]
        elif k == "remover_tecla":
            self.remover_tecla(acao[1], acao[2], acao[3])
        elif k == "reset_um":
            cat, nome = acao[1], acao[2]
            padrao = ATALHOS_PADRAO if cat == "atalhos" else CONTROLES_PADRAO
            CONFIG[cat][nome] = list(padrao[nome])
            self.salvar_cfg()
        elif k == "reset_tudo":
            cat = acao[1]
            CONFIG[cat] = copy.deepcopy(ATALHOS_PADRAO if cat == "atalhos" else CONTROLES_PADRAO)
            self.salvar_cfg()
            self.avisar("Teclas voltaram para o padrão.")
        elif k == "ap_fonte":
            CONFIG["aparencia"]["fonte_interface"] = acao[1]
            aplicar_aparencia()
            self.salvar_cfg()
        elif k == "ap_destaque":
            CONFIG["aparencia"]["destaque"] = acao[1]
            aplicar_aparencia()
            self.salvar_cfg()
        elif k == "ap_tema":
            CONFIG["aparencia"]["tema"] = acao[1]
            aplicar_aparencia()
            self.salvar_cfg()
        elif k == "ap_anim":
            CONFIG["aparencia"]["animacoes"] = acao[1] == "Ligado"
            self.salvar_cfg()
        elif k == "ap_res":
            CONFIG["aparencia"]["resolucao"] = acao[1]
            self.salvar_cfg()
            self.avisar("O novo tamanho vale quando você abrir a engine de novo.")
        elif k == "ap_nitidez":
            CONFIG["aparencia"]["nitidez"] = acao[1]
            self.salvar_cfg()
            self.avisar("Vale quando você abrir a engine de novo.")
        elif k == "sc_cor":
            self.paleta = acao[1]
            return None
        elif k == "sc_pick":
            if self.paleta:
                CONFIG["script"]["cores"][self.paleta] = list(acao[1])
                _cache_txt.clear()
                self.salvar_cfg()
        elif k == "sc_fonte":
            CONFIG["script"]["fonte"] = acao[1]
            self.salvar_cfg()
        elif k == "sc_tam":
            CONFIG["script"]["tamanho"] = max(10, min(28, CONFIG["script"]["tamanho"] + acao[1]))
            self.salvar_cfg()
        elif k == "sc_reset":
            CONFIG["script"] = copy.deepcopy(SCRIPT_PADRAO)
            _cache_txt.clear()
            self.salvar_cfg()
        elif k == "geral_bool":
            CONFIG["geral"][acao[1]] = not CONFIG["geral"].get(acao[1])
            self.salvar_cfg()
        elif k == "geral_num":
            nome, passo = acao[1], acao[2]
            _, minimo, maximo, _ = NOMES_GERAL[nome]
            CONFIG["geral"][nome] = max(minimo, min(maximo, int(num_seguro(CONFIG["geral"].get(nome), 0)) + passo))
            self.salvar_cfg()
        return None

    def salvar_cfg(self):
        salvar_config()
        aplicar_controles(CONFIG["controles"])

    def pedir_texto(self, titulo, inicial, fn, senha=False):
        self.modal = {"tipo": "texto", "titulo": titulo, "texto": str(inicial), "fn": fn, "senha": senha}

    def abrir_menu(self, pos, itens, fn):
        x = min(pos[0], LARGURA - 230)
        y = min(pos[1], ALTURA - len(itens) * 30 - 10)
        rects = [(it, pygame.Rect(x, y + i * 30, 220, 28)) for i, it in enumerate(itens)]
        self.menu = {"rects": rects, "fn": fn}

    def capturar(self, e):
        cat, acao, idx = self.capturando
        if e.key == pygame.K_ESCAPE:
            self.capturando = None
            return
        modificadoras = {getattr(pygame, n, -1) for n in ("K_LCTRL", "K_RCTRL", "K_LSHIFT", "K_RSHIFT", "K_LALT",
                                                          "K_RALT", "K_LMETA", "K_RMETA")}
        if e.key in modificadoras:
            return
        combo = nome_da_tecla(e.key, e.mod) if cat == "atalhos" else nome_da_tecla(e.key, 0, com_mods=False)
        lista = list(CONFIG[cat].get(acao, []))
        if combo in lista and idx is None:
            self.capturando = None
            return
        if idx is None or idx >= len(lista):
            lista.append(combo)
        else:
            lista[idx] = combo
        CONFIG[cat][acao] = lista[:4]
        self.capturando = None
        self.salvar_cfg()
        self.avisar(f"{(NOMES_ATALHOS if cat == 'atalhos' else NOMES_CONTROLES)[acao]}: {texto_atalho(combo)}")

    def remover_tecla(self, cat, acao, idx):
        lista = list(CONFIG[cat].get(acao, []))
        if len(lista) > 1 and idx < len(lista):
            lista.pop(idx)
            CONFIG[cat][acao] = lista
            self.salvar_cfg()

    # ----------------- desenho -----------------
    def botao(self, r, txt, acao, mouse, cor=None, fonte_tam=14, negrito=False, ativo=False):
        base = cor or (C_DESTAQUE if ativo else C_BOTAO)
        if r.collidepoint(mouse) and not self.modal and not self.menu:
            base = clarear(base, 18)
        pygame.draw.rect(self.tela, base, r, border_radius=7)
        img = texto_cache(txt, fonte_tam, C_TEXTO, negrito)
        self.tela.blit(img, (r.centerx - img.get_width() // 2, r.centery - img.get_height() // 2))
        if acao is not None:
            self.hits.append((r, acao))

    def campo(self, r, valor, dica, foco_nome, mouse):
        focado = self.foco == foco_nome
        pygame.draw.rect(self.tela, C_CAMPO, r, border_radius=7)
        pygame.draw.rect(self.tela, C_DESTAQUE if focado else C_BORDA, r, 1, border_radius=7)
        piscar = "|" if focado and int(self.tempo * 2) % 2 == 0 else ""
        txt = (valor + piscar) if (valor or focado) else dica
        img = texto_cache(txt, 15, C_TEXTO if (valor or focado) else C_TEXTO2)
        self.tela.blit(img, (r.x + 12, r.centery - img.get_height() // 2))
        self.hits.append((r, ("foco", foco_nome)))

    def desenhar(self):
        t = self.tela
        mouse = pygame.mouse.get_pos()
        self.hits = []
        t.fill((26, 28, 34))
        self.desenhar_barra(t, mouse)
        area = pygame.Rect(self.BARRA, 0, LARGURA - self.BARRA, ALTURA)
        if self.pagina == "criacoes":
            self.desenhar_criacoes(t, mouse, area)
        elif self.pagina == "novo":
            self.desenhar_novo(t, mouse, area)
        elif self.pagina == "planos":
            self.hits += desenhar_planos(t, pygame.Rect(area.x + 32, 30, area.w - 64, ALTURA - 50), mouse)
        elif self.pagina == "jogos":
            self.desenhar_jogos(t, mouse, area)
        elif self.pagina == "usuarios":
            self.desenhar_usuarios(t, mouse, area)
        else:
            self.desenhar_config(t, mouse, area)
        if not self.modal and not self.menu:
            self.hits.append((pygame.Rect(LARGURA - 16, ALTURA - 16, 16, 16), ("secreto",)))
        if self.msg_t > 0:
            img = texto_cache(self.msg, 14, C_TEXTO)
            caixa = pygame.Rect(0, 0, img.get_width() + 56, 36)
            caixa.centerx = area.centerx
            caixa.bottom = ALTURA - 16
            pygame.draw.rect(t, (14, 15, 19), caixa.move(0, 3), border_radius=18)
            pygame.draw.rect(t, (50, 54, 66), caixa, border_radius=18)
            desenhar_icone_aviso(t, tipo_do_aviso(self.msg), (caixa.x + 20, caixa.centery), 9)
            t.blit(img, (caixa.x + 38, caixa.y + 10))
        if self.menu:
            for item, r in self.menu["rects"]:
                cor = C_VERMELHO if item == "Apagar" else ((70, 76, 92) if r.collidepoint(mouse) else (46, 49, 60))
                pygame.draw.rect(t, cor, r, border_radius=5)
                t.blit(texto_cache(item, 14, C_TEXTO), (r.x + 12, r.y + 6))
        if self.modal:
            self.desenhar_modal(t, mouse)
        if self.espera:
            sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 160))
            t.blit(sombra, (0, 0))
            img = texto_cache(self.espera, 18, C_TEXTO, True)
            caixa = pygame.Rect(0, 0, img.get_width() + 90, 64)
            caixa.center = (LARGURA // 2, ALTURA // 2)
            pygame.draw.rect(t, (40, 43, 52), caixa, border_radius=14)
            for i in range(8):
                ang = self.tempo * 6 + i * math.tau / 8
                cor = clarear(C_DESTAQUE, -i * 12)
                pygame.draw.circle(t, cor, (int(caixa.x + 34 + 12 * math.cos(ang)), int(caixa.centery + 12 * math.sin(ang))), 3)
            t.blit(img, (caixa.x + 64, caixa.centery - img.get_height() // 2))
            self.hits = []
        if self.capturando:
            self.desenhar_captura(t)

    def desenhar_barra(self, t, mouse):
        pygame.draw.rect(t, (20, 22, 27), (0, 0, self.BARRA, ALTURA))
        desenhar_simbolo(t, 22, 24, 44)
        t.blit(texto_cache("Minha", 22, C_TEXTO), (76, 26))
        t.blit(texto_cache("Engine", 22, C_TEXTO, True), (76 + texto_cache("Minha ", 22, C_TEXTO).get_width(), 26))
        t.blit(texto_cache(f"versão {VERSAO}", 11, C_TEXTO2), (77, 54))
        u = usuario_atual()
        ur = pygame.Rect(14, 74, self.BARRA - 28, 32)
        if ur.collidepoint(mouse):
            pygame.draw.rect(t, (34, 37, 46), ur, border_radius=8)
        desenhar_avatar(t, u, (ur.x + 16, ur.centery), 12)
        t.blit(texto_cache(u["nome"][:16], 14, C_TEXTO, True), (ur.x + 34, ur.y + 3))
        if u.get("online"):
            pygame.draw.circle(t, (60, 200, 110), (ur.x + 38, ur.y + 24), 3)
            t.blit(texto_cache("online · conta", 11, (150, 220, 170)), (ur.x + 45, ur.y + 18))
        else:
            t.blit(texto_cache("sem internet · trocar", 11, C_TEXTO2), (ur.x + 34, ur.y + 18))
        self.hits.append((ur, ("pagina", "usuarios")))
        sr = desenhar_saldo(t, 18, 112, 13, mouse)
        self.hits.append((sr, ("pagina", "planos")))
        selo = desenhar_selo(t, sr.right + 6, 116)
        self.hits.append((selo, ("pagina", "planos")))
        y = 148
        for nome, rot in (("criacoes", "Minhas criações"), ("jogos", "Jogos publicados"), ("novo", "+  Novo projeto"),
                          ("planos", "Planos e Brasas"), ("config", "Configurações")):
            r = pygame.Rect(14, y, self.BARRA - 28, 40)
            ativo = self.pagina == nome
            if ativo:
                pygame.draw.rect(t, (44, 52, 74), r, border_radius=8)
                pygame.draw.rect(t, C_DESTAQUE, (r.x, r.y + 8, 4, r.h - 16), border_radius=2)
            elif r.collidepoint(mouse):
                pygame.draw.rect(t, (34, 37, 46), r, border_radius=8)
            t.blit(texto_cache(rot, 16, C_TEXTO if ativo else (190, 192, 204), ativo), (r.x + 18, r.y + 11))
            self.hits.append((r, ("pagina", nome)))
            y += 44
        dica = pygame.Rect(14, ALTURA - 240, self.BARRA - 28, 116)
        if dica.y > y + 10:
            pygame.draw.rect(t, (30, 33, 42), dica, border_radius=10)
            desenhar_icone_aviso(t, "info", (dica.x + 18, dica.y + 18), 8)
            t.blit(texto_cache("Dica do dia", 13, C_TEXTO, True), (dica.x + 32, dica.y + 10))
            f_dica = fonte_ui(12)
            for i, linha in enumerate(quebrar_texto(dica_do_dia(), f_dica, dica.w - 22)[:5]):
                t.blit(texto_cache(linha, 12, C_TEXTO2), (dica.x + 11, dica.y + 34 + i * 16))
        r = pygame.Rect(14, ALTURA - 110, self.BARRA - 28, 36)
        self.botao(r, "Abrir pasta das criações", ("abrir_pasta",), mouse, cor=(40, 43, 52), fonte_tam=13)
        r = pygame.Rect(14, ALTURA - 64, self.BARRA - 28, 36)
        self.botao(r, "Sair", ("sair",), mouse, cor=(60, 40, 44), fonte_tam=14)

    def desenhar_criacoes(self, t, mouse, area):
        x0 = area.x + 32
        t.blit(texto_cache("Minhas criações", 30, C_TEXTO, True), (x0, 30))
        vis = self.visiveis()
        t.blit(texto_cache(f"{saudacao()}! O que vamos criar hoje?   ·   {len(self.projetos)} projeto(s), "
                           f"2 cliques ou Editar para abrir", 13, C_TEXTO2), (x0 + 2, 70))
        self.campo(pygame.Rect(area.right - 470, 30, 260, 36), self.busca, "Buscar criação...", "busca", mouse)
        self.botao(pygame.Rect(area.right - 200, 30, 120, 36),
                   "Recentes" if self.ordem == "recentes" else "Nome (A-Z)", ("ordem",), mouse)
        self.botao(pygame.Rect(area.right - 72, 30, 44, 36), "+", ("pagina", "novo"), mouse, cor=C_VERDE,
                   fonte_tam=22, negrito=True)
        grade = pygame.Rect(area.x + 20, 100, area.w - 40, ALTURA - 116)
        if not self.projetos:
            self.desenhar_vazio(t, mouse, grade)
            return
        colunas = max(1, (grade.w + self.GAP) // (self.CARD_W + self.GAP))
        livre = grade.w - colunas * self.CARD_W - (colunas - 1) * self.GAP
        xi = grade.x + livre // 2
        linhas = (len(vis) + colunas - 1) // colunas
        total = linhas * (self.CARD_H + self.GAP)
        self.scroll = max(0, min(self.scroll, max(0, total - grade.h)))
        vis_p = suave((id(self), "projetos", self.pagina), self.scroll)
        t.set_clip(grade)
        for i, proj in enumerate(vis):
            col, lin = i % colunas, i // colunas
            r = pygame.Rect(xi + col * (self.CARD_W + self.GAP), grade.y + 6 + lin * (self.CARD_H + self.GAP) - vis_p,
                            self.CARD_W, self.CARD_H)
            if r.bottom < grade.y or r.y > grade.bottom:
                continue
            self.desenhar_card(t, mouse, proj, r, grade)
        t.set_clip(None)
        if not vis:
            t.blit(texto_cache("Nada encontrado com essa busca.", 16, C_TEXTO2), (grade.x + 12, grade.y + 20))

    def desenhar_card(self, t, mouse, proj, r, grade):
        selecionado = self.sel is not None and self.sel["pasta"] == proj["pasta"]
        em_cima = r.collidepoint(mouse) and grade.collidepoint(mouse) and not self.menu and not self.modal
        pygame.draw.rect(t, (40, 43, 53) if (em_cima or selecionado) else (34, 37, 45), r, border_radius=10)
        thumb = self.miniatura(proj, r.w, self.THUMB_H)
        t.blit(thumb, r.topleft)
        if selecionado:
            pygame.draw.rect(t, C_DESTAQUE, r.inflate(4, 4), 2, border_radius=12)
        nome = proj["nome"] if len(proj["nome"]) <= 26 else proj["nome"][:25] + "…"
        t.blit(texto_cache(nome, 15, C_TEXTO, True), (r.x + 12, r.y + self.THUMB_H + 9))
        info = f"{proj['fases']} fase(s) · {proj['objetos']} obj · {tempo_atras(proj['mudado'])}"
        t.blit(texto_cache(info, 12, C_TEXTO2), (r.x + 12, r.y + self.THUMB_H + 31))
        if grade.collidepoint(r.centerx, r.y + self.THUMB_H // 2):
            self.hits.append((pygame.Rect(r.x, r.y, r.w, self.THUMB_H + 50).clip(grade), ("card", proj)))
        by = r.bottom - 34
        if by + 28 <= grade.bottom and by >= grade.y:
            self.botao(pygame.Rect(r.x + 10, by, 100, 26), "Editar", ("editar", proj), mouse, cor=C_DESTAQUE,
                       fonte_tam=13, negrito=True)
            self.botao(pygame.Rect(r.x + 116, by, 74, 26), "Jogar", ("jogar", proj), mouse, cor=(48, 120, 78),
                       fonte_tam=13)
            self.botao(pygame.Rect(r.x + 196, by, 30, 26), "···", ("mais", proj), mouse, fonte_tam=13)

    def desenhar_vazio(self, t, mouse, area):
        cx = area.centerx
        desenhar_simbolo(t, cx - 45, area.y + 40, 90, alpha=200)
        img = texto_cache("Você ainda não tem criações", 22, C_TEXTO, True)
        t.blit(img, (cx - img.get_width() // 2, area.y + 150))
        img = texto_cache("Comece com um exemplo pronto ou um projeto vazio.", 15, C_TEXTO2)
        t.blit(img, (cx - img.get_width() // 2, area.y + 184))
        self.botao(pygame.Rect(cx - 100, area.y + 226, 200, 44), "+  Criar meu primeiro jogo", ("pagina", "novo"),
                   mouse, cor=C_VERDE, fonte_tam=15, negrito=True)

    def desenhar_novo(self, t, mouse, area):
        x0 = area.x + 32
        t.blit(texto_cache("Novo projeto", 30, C_TEXTO, True), (x0, 30))
        t.blit(texto_cache("Nome do projeto", 14, C_TEXTO2), (x0, 86))
        self.campo(pygame.Rect(x0, 108, 420, 40), self.novo_nome, f"Meu Jogo {len(self.projetos) + 1}", "nome", mouse)
        t.blit(texto_cache("Começar com", 14, C_TEXTO2), (x0, 170))
        modelos = ["Projeto vazio"] + list(EXEMPLOS)
        w, h = 228, 128
        for i, nome in enumerate(modelos):
            r = pygame.Rect(x0 + i * (w + 18), 194, w, h + 92)
            ativo = nome == self.novo_modelo
            pygame.draw.rect(t, (44, 52, 74) if ativo else (34, 37, 45), r, border_radius=10)
            t.blit(self.miniatura_modelo(nome, w, h), r.topleft)
            if ativo:
                pygame.draw.rect(t, C_DESTAQUE, r.inflate(4, 4), 2, border_radius=12)
            titulo = nome.replace("Exemplo: ", "")
            t.blit(texto_cache(titulo[:1].upper() + titulo[1:], 14, C_TEXTO, True), (r.x + 10, r.y + h + 8))
            yy = r.y + h + 30
            for linha in quebrar_texto(DESC_MODELOS.get(nome, ""), fonte(12), w - 20)[:3]:
                t.blit(texto_cache(linha, 12, C_TEXTO2), (r.x + 10, yy))
                yy += 15
            self.hits.append((r, ("modelo", nome)))
        self.botao(pygame.Rect(x0, 444, 200, 46), "Criar e abrir", ("criar",), mouse, cor=C_VERDE, fonte_tam=16,
                   negrito=True)
        dica = ("Cada projeto fica numa pasta própria em 'projetos', com as suas imagens e sons. "
                "Dá para criar quantos quiser.")
        t.blit(texto_cache(dica, 13, C_TEXTO2), (x0, 506))

    def desenhar_config(self, t, mouse, area):
        x0 = area.x + 32
        t.blit(texto_cache("Configurações", 30, C_TEXTO, True), (x0, 30))
        abas = (("atalhos", "Atalhos do editor"), ("controles", "Controles do jogo"), ("script", "Editor de script"),
                ("aparencia", "Aparência"), ("geral", "Geral"))
        x = x0
        for nome, rot in abas:
            img = texto_cache(rot, 15, C_TEXTO, self.config_aba == nome)
            r = pygame.Rect(x, 82, img.get_width() + 30, 36)
            self.botao(r, rot, ("cfg_aba", nome), mouse, ativo=self.config_aba == nome, fonte_tam=15,
                       negrito=self.config_aba == nome)
            x = r.right + 8
        lista = pygame.Rect(x0, 134, area.right - 32 - x0, ALTURA - 134 - 70)
        pygame.draw.rect(t, (30, 32, 39), lista, border_radius=10)
        if self.config_aba == "geral":
            self.desenhar_geral(t, mouse, lista)
            return
        if self.config_aba == "aparencia":
            self.desenhar_aparencia(t, mouse, lista)
            return
        if self.config_aba == "script":
            self.desenhar_cfg_script(t, mouse, lista)
            return
        cat = self.config_aba
        nomes = NOMES_ATALHOS if cat == "atalhos" else NOMES_CONTROLES
        padrao = ATALHOS_PADRAO if cat == "atalhos" else CONTROLES_PADRAO
        uso = {}
        for acao, combos in CONFIG[cat].items():
            for c in combos:
                uso.setdefault(c, []).append(acao)
        t.set_clip(lista)
        vis_c = suave((id(self), "cfg", self.config_aba), self.scroll_cfg)
        y = lista.y + 12 - vis_c
        for acao in padrao:
            if lista.y - 40 < y < lista.bottom:
                t.blit(texto_cache(nomes[acao], 15, C_TEXTO), (lista.x + 18, y + 7))
                xx = lista.x + 330
                for i, combo in enumerate(CONFIG[cat].get(acao, [])):
                    conflito = len(uso.get(combo, [])) > 1
                    txt = texto_atalho(combo)
                    img = texto_cache(txt, 14, C_TEXTO, True)
                    r = pygame.Rect(xx, y + 2, max(48, img.get_width() + 22), 30)
                    self.botao(r, txt, ("tecla", cat, acao, i), mouse, cor=(150, 60, 60) if conflito else (56, 62, 80),
                               fonte_tam=14, negrito=True)
                    if len(CONFIG[cat].get(acao, [])) > 1:
                        rx = pygame.Rect(r.right - 6, r.y - 6, 16, 16)
                        pygame.draw.circle(t, (90, 45, 45), rx.center, 8)
                        img_x = texto_cache("x", 11, C_TEXTO)
                        t.blit(img_x, (rx.centerx - img_x.get_width() // 2, rx.centery - img_x.get_height() // 2))
                        self.hits.append((rx, ("remover_tecla", cat, acao, i)))
                    xx = r.right + 12
                self.botao(pygame.Rect(xx, y + 2, 30, 30), "+", ("tecla", cat, acao, None), mouse, cor=(44, 48, 60),
                           fonte_tam=16)
                if CONFIG[cat].get(acao) != padrao[acao]:
                    self.botao(pygame.Rect(lista.right - 110, y + 2, 92, 30), "padrão", ("reset_um", cat, acao), mouse,
                               cor=(44, 48, 60), fonte_tam=12)
            y += 42
        total = y + vis_c - lista.y
        self.scroll_cfg = max(0, min(self.scroll_cfg, max(0, total - lista.h + 10)))
        t.set_clip(None)
        dica = ("Clique numa tecla para trocar, no + para adicionar outra. Vermelho = a mesma tecla em duas coisas."
                if cat == "atalhos" else "Esses controles valem no Play do editor e vão junto quando você exporta o jogo.")
        t.blit(texto_cache(dica, 13, C_TEXTO2), (x0, ALTURA - 56))
        self.botao(pygame.Rect(area.right - 32 - 200, ALTURA - 62, 200, 34), "Restaurar tudo para o padrão",
                   ("reset_tudo", cat), mouse, cor=(60, 44, 48), fonte_tam=13)

    def chips(self, t, mouse, x, y, opcoes, atual, acao, fonte_de=None, largura_max=None):
        for nome in opcoes:
            f = fonte_de(nome) if fonte_de else fonte_ui(14)
            img = texto_cache_fonte(f, nome, C_TEXTO)
            r = pygame.Rect(x, y, img.get_width() + 26, 32)
            if largura_max and r.right > largura_max:
                x, y = r.x - (r.x - x), y + 40
            ativo = nome == atual
            cor = C_DESTAQUE if ativo else (70, 76, 92) if r.collidepoint(mouse) else (48, 52, 64)
            pygame.draw.rect(t, cor, r, border_radius=16)
            t.blit(img, (r.x + 13, r.centery - img.get_height() // 2))
            self.hits.append((r, (acao, nome)))
            x = r.right + 8
        return y

    def desenhar_aparencia(self, t, mouse, lista):
        ap = CONFIG["aparencia"]
        x, y = lista.x + 18, lista.y + 16
        t.blit(texto_cache("Fonte da interface", 15, C_TEXTO2), (x, y))
        self.chips(t, mouse, x, y + 24, list(FONTES_UI), ap["fonte_interface"], "ap_fonte",
                   fonte_de=lambda n: fonte_familia(FONTES_UI[n], 15))
        y += 80
        t.blit(texto_cache("Cor de destaque", 15, C_TEXTO2), (x, y))
        xx = x
        for nome, cor in CORES_DESTAQUE.items():
            r = pygame.Rect(xx, y + 24, 40, 40)
            pygame.draw.rect(t, cor, r, border_radius=20)
            if ap["destaque"] == nome:
                pygame.draw.rect(t, (255, 255, 255), r.inflate(6, 6), 3, border_radius=23)
            self.hits.append((r, ("ap_destaque", nome)))
            xx += 52
        y += 88
        t.blit(texto_cache("Tema (cores da engine)", 15, C_TEXTO2), (x, y))
        self.chips(t, mouse, x, y + 24, list(TEMAS_UI), ap.get("tema", "Grafite"), "ap_tema")
        t.blit(texto_cache("Movimento suave", 15, C_TEXTO2), (x + 560, y))
        self.chips(t, mouse, x + 560, y + 24, ["Ligado", "Desligado"],
                   "Ligado" if ap.get("animacoes", True) else "Desligado", "ap_anim")
        y += 80
        t.blit(texto_cache("Tamanho da interface  (use o tamanho da sua tela para letras bem nítidas)", 15, C_TEXTO2),
               (x, y))
        self.chips(t, mouse, x, y + 24, RESOLUCOES, ap["resolucao"], "ap_res")
        y += 80
        t.blit(texto_cache("Letras quando a janela estica", 15, C_TEXTO2), (x, y))
        self.chips(t, mouse, x, y + 24, ["Suave", "Pixel"], ap["nitidez"], "ap_nitidez")
        y += 80
        t.blit(texto_cache("O tamanho da interface e a nitidez valem quando você abrir a engine de novo. "
                           "Fonte e cor mudam na hora.", 13, C_TEXTO2), (x, y))
        t.blit(texto_cache("Dica: instale o pygame-ce (pip install pygame-ce) para letras ainda mais bonitas.", 13,
                           C_TEXTO2), (x, y + 20))

    def desenhar_cfg_script(self, t, mouse, lista):
        sc = CONFIG["script"]
        x, y = lista.x + 18, lista.y + 14
        for cat, rotulo in NOMES_CORES_SCRIPT.items():
            r = pygame.Rect(x, y, 28, 28)
            pygame.draw.rect(t, cor_ok(sc["cores"][cat]), r, border_radius=6)
            pygame.draw.rect(t, (255, 255, 255) if r.collidepoint(mouse) else C_BORDA, r, 2, border_radius=6)
            self.hits.append((r, ("sc_cor", cat)))
            linha = pygame.Rect(x + 36, y, 330, 28)
            t.blit(texto_cache(rotulo, 14, C_TEXTO), (linha.x, linha.y + 5))
            self.hits.append((linha, ("sc_cor", cat)))
            y += 36
        y += 6
        t.blit(texto_cache("Fonte do código", 14, C_TEXTO2), (x, y))
        self.chips(t, mouse, x, y + 22, list(FONTES_CODIGO), sc["fonte"], "sc_fonte",
                   fonte_de=lambda n: fonte_familia(FONTES_CODIGO[n], 14))
        y += 66
        t.blit(texto_cache("Tamanho", 14, C_TEXTO2), (x, y + 6))
        self.botao(pygame.Rect(x + 80, y, 32, 30), "-", ("sc_tam", -1), mouse, fonte_tam=16)
        img = texto_cache(str(sc["tamanho"]), 16, C_TEXTO, True)
        t.blit(img, (x + 130 - img.get_width() // 2, y + 5))
        self.botao(pygame.Rect(x + 150, y, 32, 30), "+", ("sc_tam", 1), mouse, fonte_tam=16)
        self.botao(pygame.Rect(x + 210, y, 170, 30), "Cores padrão", ("sc_reset",), mouse, cor=(60, 44, 48),
                   fonte_tam=13)
        # previa
        caixa = pygame.Rect(lista.x + 420, lista.y + 14, lista.right - lista.x - 438, lista.h - 28)
        pygame.draw.rect(t, cor_ok(sc["cores"]["fundo"]), caixa, border_radius=8)
        pygame.draw.rect(t, C_BORDA, caixa, 1, border_radius=8)
        t.blit(texto_cache("Prévia", 13, C_TEXTO2), (caixa.x + 12, caixa.y + 8))
        fc = fonte_codigo()
        cw = max(1, fc.size("M")[0])
        exemplo = ['# Meu script', 'var vida = 3', '', 'quando tocar "Inimigo":', '    vida -= 1',
                   '    dizer("Ai! Vida: " + vida, 1)', '    se vida <= 0:', '        voltar_inicio()', '',
                   'funcao pular_alto():', '    eu.vy = -900', '', 'quando tecla "e":', '    pular_alto()']
        yy = caixa.y + 32
        t.set_clip(caixa)
        for n, linha in enumerate(exemplo):
            num_img = texto_cache_fonte(fc, str(n + 1).rjust(2), (90, 95, 110))
            t.blit(num_img, (caixa.x + 10, yy))
            pintar_codigo(t, fc, cw, linha, caixa.x + 18 + cw * 3, yy, {"pular_alto"})
            yy += fc.get_linesize() + 2
        t.set_clip(None)
        if self.paleta:
            self.desenhar_paleta(t, mouse)

    def desenhar_paleta(self, t, mouse):
        cat = self.paleta
        caixa = pygame.Rect(self.BARRA + 60, 220, 8 * 44 + 20, 3 * 44 + 60)
        pygame.draw.rect(t, (40, 43, 52), caixa, border_radius=10)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 1, border_radius=10)
        t.blit(texto_cache(f"Cor para: {NOMES_CORES_SCRIPT[cat]}", 14, C_TEXTO, True), (caixa.x + 12, caixa.y + 10))
        for i, cor in enumerate(PALETA_CORES):
            r = pygame.Rect(caixa.x + 12 + (i % 8) * 44, caixa.y + 40 + (i // 8) * 44, 36, 36)
            pygame.draw.rect(t, cor, r, border_radius=8)
            if r.collidepoint(mouse):
                pygame.draw.rect(t, (255, 255, 255), r, 2, border_radius=8)
            self.hits.append((r, ("sc_pick", tuple(cor))))

    def desenhar_geral(self, t, mouse, lista):
        y = lista.y + 14
        for nome, info in NOMES_GERAL.items():
            valor = CONFIG["geral"].get(nome, GERAL_PADRAO[nome])
            t.blit(texto_cache(info[0], 15, C_TEXTO), (lista.x + 18, y + 7))
            xx = lista.x + 470
            if len(info) == 1:
                r = pygame.Rect(xx, y + 3, 64, 28)
                pygame.draw.rect(t, C_VERDE if valor else (70, 72, 84), r, border_radius=14)
                pygame.draw.circle(t, (255, 255, 255), (r.right - 14 if valor else r.x + 14, r.centery), 10)
                self.hits.append((r, ("geral_bool", nome)))
            else:
                _, minimo, maximo, passo = info
                self.botao(pygame.Rect(xx, y + 3, 32, 28), "-", ("geral_num", nome, -passo), mouse, fonte_tam=16)
                img = texto_cache(str(valor), 16, C_TEXTO, True)
                t.blit(img, (xx + 70 - img.get_width() // 2, y + 8))
                self.botao(pygame.Rect(xx + 108, y + 3, 32, 28), "+", ("geral_num", nome, passo), mouse, fonte_tam=16)
            y += 44
        t.blit(texto_cache("Tudo é salvo na hora em config.json, ao lado da engine.", 13, C_TEXTO2),
               (lista.x + 18, y + 10))

    def desenhar_modal(self, t, mouse):
        m = self.modal
        sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        t.blit(sombra, (0, 0))
        caixa = pygame.Rect(LARGURA // 2 - 240, ALTURA // 2 - 90, 480, 180)
        pygame.draw.rect(t, (40, 43, 52), caixa, border_radius=12)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 1, border_radius=12)
        t.blit(texto_cache(m["titulo"], 18, C_TEXTO, True), (caixa.x + 22, caixa.y + 20))
        if m["tipo"] == "texto":
            r = pygame.Rect(caixa.x + 22, caixa.y + 62, caixa.w - 44, 38)
            pygame.draw.rect(t, C_CAMPO, r, border_radius=7)
            pygame.draw.rect(t, C_DESTAQUE, r, 1, border_radius=7)
            piscar = "|" if int(self.tempo * 2) % 2 == 0 else ""
            visivel = "•" * len(m["texto"]) if m.get("senha") else m["texto"]
            t.blit(texto_cache(visivel + piscar, 16, C_TEXTO), (r.x + 12, r.y + 10))
            self.hits.append((r, ("modal_campo",)))
            rotulo = "OK"
        else:
            for i, linha in enumerate(quebrar_texto(m["msg"], fonte(14), caixa.w - 44)[:3]):
                t.blit(texto_cache(linha, 14, C_TEXTO2), (caixa.x + 22, caixa.y + 62 + i * 19))
            rotulo = m.get("botao", "OK")
        self.botao(pygame.Rect(caixa.right - 250, caixa.bottom - 54, 110, 36), "Cancelar", ("modal_cancelar",), mouse)
        self.botao(pygame.Rect(caixa.right - 130, caixa.bottom - 54, 108, 36), rotulo, ("modal_ok",), mouse,
                   cor=C_VERMELHO if rotulo == "Apagar" else C_VERDE, negrito=True)

    def desenhar_captura(self, t):
        cat, acao, _ = self.capturando
        sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 170))
        t.blit(sombra, (0, 0))
        caixa = pygame.Rect(LARGURA // 2 - 260, ALTURA // 2 - 70, 520, 140)
        pygame.draw.rect(t, (40, 43, 52), caixa, border_radius=12)
        pygame.draw.rect(t, C_DESTAQUE, caixa, 2, border_radius=12)
        nome = (NOMES_ATALHOS if cat == "atalhos" else NOMES_CONTROLES)[acao]
        img = texto_cache("Aperte a nova tecla", 22, C_TEXTO, True)
        t.blit(img, (caixa.centerx - img.get_width() // 2, caixa.y + 26))
        img = texto_cache(f"para: {nome}", 16, C_DESTAQUE)
        t.blit(img, (caixa.centerx - img.get_width() // 2, caixa.y + 62))
        dica = "Pode usar Ctrl e Shift junto.  Esc cancela." if cat == "atalhos" else "Esc cancela."
        img = texto_cache(dica, 13, C_TEXTO2)
        t.blit(img, (caixa.centerx - img.get_width() // 2, caixa.y + 98))
