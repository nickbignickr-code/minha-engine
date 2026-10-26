# Minha Engine - interface.py
# botões, balões de aviso, dicas, guia e a logo
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Coisas para deixar o editor mais amigavel
# ---------------------------------------------------------------------
CORES_AVISO = {"ok": (60, 175, 100), "erro": (215, 75, 75), "aviso": (235, 170, 50), "info": (70, 140, 255)}
PALAVRAS_ERRO = ("Erro", "Não consegui", "Não deu", "Tem erro", "O jogo parou", "Coloque um Player")
PALAVRAS_OK = ("Salvo", "Salvei", "Projeto salvo", "inserido", "aplicad", "criad", "Criad", "colad", "Pronto",
               "Exportado", "Parabéns", "Script ", "Imagem '")
PALAVRAS_AVISO = ("Selecione", "Só pode", "Precisa", "Cuidado", "A pasta", "Nada", "Nenhum")


def tipo_do_aviso(txt):
    txt = str(txt)
    if txt.startswith(PALAVRAS_ERRO):
        return "erro"
    if txt.startswith(PALAVRAS_AVISO):
        return "aviso"
    if any(p in txt for p in PALAVRAS_OK):
        return "ok"
    return "info"


def desenhar_icone_aviso(tela, tipo, centro, raio=10):
    cx, cy = centro
    cor = CORES_AVISO.get(tipo, CORES_AVISO["info"])
    pygame.draw.circle(tela, cor, centro, raio)
    branco = (255, 255, 255)
    if tipo == "ok":
        pygame.draw.lines(tela, branco, False, [(cx - 5, cy), (cx - 1, cy + 4), (cx + 5, cy - 4)], 2)
    elif tipo == "erro":
        pygame.draw.line(tela, branco, (cx - 4, cy - 4), (cx + 4, cy + 4), 2)
        pygame.draw.line(tela, branco, (cx + 4, cy - 4), (cx - 4, cy + 4), 2)
    elif tipo == "aviso":
        pygame.draw.line(tela, branco, (cx, cy - 5), (cx, cy + 1), 2)
        pygame.draw.circle(tela, branco, (cx, cy + 5), 1)
    else:
        pygame.draw.circle(tela, branco, (cx, cy - 5), 1)
        pygame.draw.line(tela, branco, (cx, cy - 1), (cx, cy + 5), 2)


def saudacao():
    import time as _t
    h = _t.localtime().tm_hour
    return "Bom dia" if 5 <= h < 12 else ("Boa tarde" if 12 <= h < 18 else "Boa noite")


DICAS_DO_DIA = [
    "Botão direito em qualquer objeto abre um menu com tudo que dá para fazer com ele.",
    "Arraste um tipo de objeto na cena para pintar vários de uma vez.",
    "Na aba Loja tem personagens, inimigos e fases prontas: é só clicar em Inserir.",
    "Na aba Desenho você faz pixel art e animações para as suas peças.",
    "F9 abre a Saída: clique num erro para ir direto na linha do script.",
    "Ctrl+D duplica a seleção. Ctrl+Z desfaz quase tudo.",
    "O material Gelo escorrega, a Areia deixa lento e a Borracha faz quicar.",
    "Crie uma variante: selecione um objeto pronto e clique em 'Criar variante'.",
    "Em Configurações dá para mudar as cores do script e a fonte do editor.",
    "Comportamentos (painel direito) fazem coisas sem programar: Perseguir, Vida, Luz...",
    "Escreva escrever(\"oi\") no script para ver mensagens na Saída enquanto testa.",
    "Use grupos (ex: Inimigos) para várias coisas reagirem do mesmo jeito.",
]


def dica_do_dia():
    import time as _t
    return DICAS_DO_DIA[_t.localtime().tm_yday % len(DICAS_DO_DIA)]


PASSOS = [
    ("peca", "Coloque uma Peça", "Clique em Peça (BÁSICO) e depois na cena."),
    ("aparencia", "Mude cor, forma ou material", "Selecione a Peça e mude no painel da direita."),
    ("player", "Coloque o Player", "Ele é o seu personagem (PERSONAGENS > Player)."),
    ("play", "Aperte Play para testar", "Botão verde lá em cima, ou F5. Esc para parar."),
    ("desenho", "Desenhe uma imagem", "Selecione a Peça e clique em 'Desenhar' (APARÊNCIA)."),
    ("loja", "Pegue algo pronto na Loja", "Aba Loja > Inserir."),
    ("script", "Programe alguma coisa", "Aba Eventos (sem digitar) ou aba Script (Brasa)."),
]


# ---------------------------------------------------------------------
# Logo da Minha Engine (desenhada pelo codigo, sem precisar de arquivo)
# ---------------------------------------------------------------------
LOGO_AZUL = (70, 140, 255)
LOGO_BRASA = (255, 138, 61)
LOGO_FUNDO = (30, 32, 38)
# "M" feito de blocos numa grade 5x5 (o do meio e a brasa)
LOGO_BLOCOS = [(0, 0), (4, 0), (0, 1), (1, 1), (3, 1), (4, 1), (0, 2), (2, 2), (4, 2),
               (0, 3), (4, 3), (0, 4), (4, 4)]


def desenhar_simbolo(tela, x, y, tam, cor=LOGO_AZUL, brasa=LOGO_BRASA, alpha=255):
    """Desenha o simbolo (quadrado azul com o M de blocos) no ponto x, y com o tamanho tam."""
    tam = max(8, int(tam))
    k = tam / 160.0
    surf = pygame.Surface((tam, tam), pygame.SRCALPHA)
    pygame.draw.rect(surf, cor, (0, 0, tam, tam), border_radius=max(2, int(34 * k)))
    lado = max(2, round(22 * k))
    raio = max(1, int(5 * k))
    for cx, cy in LOGO_BLOCOS:
        cor_bloco = brasa if (cx, cy) == (2, 2) else (255, 255, 255)
        pygame.draw.rect(surf, cor_bloco, (round((15 + cx * 27) * k), round((15 + cy * 27) * k), lado, lado),
                         border_radius=raio)
    if alpha < 255:
        surf.set_alpha(max(0, int(alpha)))
    tela.blit(surf, (int(x), int(y)))


def criar_icone(tam=64):
    """Superficie com o icone (usada na janela e para salvar icone.png)."""
    surf = pygame.Surface((tam, tam), pygame.SRCALPHA)
    desenhar_simbolo(surf, 0, 0, tam)
    return surf


def colocar_icone_janela():
    try:
        pygame.display.set_icon(criar_icone(64))
    except (pygame.error, AttributeError):
        pass


def salvar_icone(pasta, tam=256):
    """Salva icone.png e icone.ico (o .ico e o que o Windows usa nos atalhos)."""
    os.makedirs(pasta, exist_ok=True)
    png = os.path.join(pasta, "icone.png")
    ico = os.path.join(pasta, "icone.ico")
    pygame.image.save(criar_icone(tam), png)
    with open(png, "rb") as f:
        dados = f.read()
    # arquivo .ico com um PNG dentro (funciona do Windows Vista em diante)
    lado = 0 if tam >= 256 else tam
    cabecalho = bytes([0, 0, 1, 0, 1, 0])
    entrada = bytes([lado, lado, 0, 0, 1, 0, 32, 0]) + len(dados).to_bytes(4, "little") + (22).to_bytes(4, "little")
    with open(ico, "wb") as f:
        f.write(cabecalho + entrada + dados)
    return png, ico


def pasta_area_de_trabalho():
    if sys.platform.startswith("win"):
        try:
            r = subprocess.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
                               capture_output=True, text=True, timeout=20,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            caminho = r.stdout.strip()
            if caminho and os.path.isdir(caminho):
                return caminho
        except (OSError, subprocess.SubprocessError):
            pass
    else:
        try:
            r = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True, text=True, timeout=10)
            caminho = r.stdout.strip()
            if caminho and os.path.isdir(caminho):
                return caminho
        except (OSError, subprocess.SubprocessError):
            pass
    for nome in ("Desktop", "Área de Trabalho", "Area de Trabalho", "Escritorio"):
        caminho = os.path.join(os.path.expanduser("~"), nome)
        if os.path.isdir(caminho):
            return caminho
    return os.path.join(os.path.expanduser("~"), "Desktop")


def criar_atalho(nome, script, pasta_trabalho, argumentos=""):
    """Cria um atalho na area de trabalho que roda o script Python com o icone da Minha Engine.
    Retorna o caminho do atalho criado."""
    _, ico = salvar_icone(pasta_trabalho)
    png = os.path.join(pasta_trabalho, "icone.png")
    desktop = pasta_area_de_trabalho()
    os.makedirs(desktop, exist_ok=True)
    nome = re.sub(r'[\\/:*?"<>|]', "", nome).strip() or "Minha Engine"
    if sys.platform.startswith("win"):
        pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        alvo = pythonw if os.path.isfile(pythonw) else sys.executable
        q = lambda txt: str(txt).replace("'", "''")
        args = f'"{script}" {argumentos}'.strip()
        destino = os.path.join(desktop, nome + ".lnk")
        comando = (f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{q(destino)}');"
                   f"$s.TargetPath='{q(alvo)}';$s.Arguments='{q(args)}';"
                   f"$s.WorkingDirectory='{q(pasta_trabalho)}';$s.IconLocation='{q(ico)},0';"
                   f"$s.Description='{q(nome)}';$s.Save()")
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", comando],
                           capture_output=True, text=True, timeout=30,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if r.returncode != 0 or not os.path.exists(destino):
            raise OSError(r.stderr.strip() or "o Windows não deixou criar o atalho")
        return destino
    if sys.platform == "darwin":
        destino = os.path.join(desktop, nome + ".command")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(f'#!/bin/sh\ncd "{pasta_trabalho}"\n"{sys.executable}" "{script}" {argumentos}\n')
        os.chmod(destino, 0o755)
        return destino
    destino = os.path.join(desktop, nome + ".desktop")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("[Desktop Entry]\nType=Application\n"
                f"Name={nome}\nExec=\"{sys.executable}\" \"{script}\" {argumentos}\n"
                f"Path={pasta_trabalho}\nIcon={png}\nTerminal=false\n")
    os.chmod(destino, 0o755)
    return destino


def desenhar_logo(tela, cx, cy, escala=1.0, alpha=255, frase="CRIE SEUS JOGOS 2D", cor_texto=(255, 255, 255)):
    """Logo completa (simbolo + 'Minha Engine') centralizada em cx, cy."""
    tam = int(150 * escala)
    f_fina = fonte(int(70 * escala))
    f_negrito = fonte(int(70 * escala), True)
    f_frase = fonte(max(8, int(18 * escala)))
    img1 = f_fina.render("Minha ", True, cor_texto)
    img2 = f_negrito.render("Engine", True, cor_texto)
    img3 = f_frase.render("  ".join(frase), True, (169, 174, 188)) if frase else None
    larg_txt = img1.get_width() + img2.get_width()
    gap = int(34 * escala)
    total = tam + gap + larg_txt
    x0 = int(cx - total / 2)
    y0 = int(cy - tam / 2)
    desenhar_simbolo(tela, x0, y0, tam, alpha=alpha)
    tx = x0 + tam + gap
    altura_txt = img1.get_height() + (img3.get_height() + 6 if img3 else 0)
    ty = int(cy - altura_txt / 2)
    for img, px, py in ((img1, tx, ty), (img2, tx + img1.get_width(), ty)):
        if alpha < 255:
            img.set_alpha(alpha)
        tela.blit(img, (px, py))
    if img3:
        if alpha < 255:
            img3.set_alpha(alpha)
        tela.blit(img3, (tx + 4, ty + img1.get_height() + 6))


def tela_carregamento(tela, progresso, mensagem="", titulo=None, area=None):
    """Tela de carregamento com a logo e uma barra de progresso (0 a 1)."""
    area = area or tela.get_rect()
    pygame.draw.rect(tela, LOGO_FUNDO, area)
    cx, cy = area.centerx, area.centery - 30
    escala = min(1.0, area.w / 1100)
    if titulo:
        f_tit = fonte(int(52 * max(0.6, escala)), True)
        img = f_tit.render(str(titulo), True, (255, 255, 255))
        tela.blit(img, (cx - img.get_width() // 2, cy - img.get_height() - 10))
        desenhar_logo(tela, cx, cy + 70, escala * 0.45, frase="")
        rodape = fonte(14).render("feito com", True, (140, 145, 160))
        tela.blit(rodape, (cx - rodape.get_width() // 2, cy + 22))
    else:
        desenhar_logo(tela, cx, cy, escala)
    larg = int(min(420, area.w * 0.5))
    barra = pygame.Rect(cx - larg // 2, area.bottom - 110, larg, 8)
    pygame.draw.rect(tela, (55, 58, 68), barra, border_radius=4)
    p = max(0.0, min(1.0, progresso))
    if p > 0:
        pygame.draw.rect(tela, LOGO_AZUL, (barra.x, barra.y, max(8, int(larg * p)), barra.h), border_radius=4)
    if mensagem:
        img = fonte(15).render(mensagem, True, (150, 155, 170))
        tela.blit(img, (cx - img.get_width() // 2, barra.bottom + 14))


def mostrar_carregamento(tela, relogio, segundos=1.2, titulo=None, etapas=None):
    """Mostra a tela de carregamento por um tempo. Qualquer tecla ou clique pula."""
    etapas = etapas or ["Carregando..."]
    t = 0.0
    while t < segundos:
        t += relogio.tick(60) / 1000.0
        for e in pegar_eventos(tela):
            if e.type == pygame.QUIT:
                return False
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return True
        p = min(1.0, t / segundos)
        msg = etapas[min(len(etapas) - 1, int(p * len(etapas)))]
        tela_carregamento(tela, p, msg, titulo)
        pygame.display.flip()
    return True
