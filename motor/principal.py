# Minha Engine - principal.py
# modo 'só o jogo' e o programa principal
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# MODO "SO O JOGO" (python minha_engine.py --jogar projeto.json)
# =====================================================================
def jogar_sozinho(caminho):
    with open(caminho, encoding="utf-8") as f:
        projeto = completar_projeto(json.load(f))
    pygame.init()
    definir_projeto(os.path.dirname(os.path.abspath(caminho)))
    aplicar_controles(projeto.get("controles") or CONTROLES_PADRAO)
    carregar_plugins()
    fase_ini = projeto["fase_inicial"]
    cena = projeto["fases"][fase_ini]["cena"]
    colocar_icone_janela()
    w = int(num_seguro(cena.get("largura_tela", 960), 960))
    h = int(num_seguro(cena.get("altura_tela", 540), 540))
    if NO_CELULAR:           # mesmo formato da tela do celular: nada de faixa preta
        w = tamanho_celular(h, minimo=w)[0]
    try:
        tela = pygame.display.set_mode((w, h), flags_janela())
    except pygame.error:
        tela = pygame.display.set_mode((w, h))
    if cena.get("tela_cheia"):
        alternar_tela_cheia()
    pygame.display.set_caption(str(cena.get("titulo", "Meu Jogo")))
    relogio = pygame.time.Clock()
    if mostrar_carregamento(tela, relogio, 1.6, titulo=cena.get("titulo", "Meu Jogo"),
                            etapas=["Carregando imagens...", "Carregando sons...", "Montando a fase...", "Vamos lá!"]):
        loop_jogo(tela, relogio, projeto, fase_ini)
    parar_musica()
    pygame.quit()


# =====================================================================
# PROGRAMA PRINCIPAL: Inicio -> Editor -> Inicio ...
# =====================================================================
def main():
    pygame.init()
    preparar_pastas()
    carregar_config()
    carregar_sessao()
    carteira()
    aplicar_aparencia()
    aplicar_resolucao()
    colocar_icone_janela()
    try:
        tela = pygame.display.set_mode((LARGURA, ALTURA), flags_janela())
    except pygame.error:
        tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Minha Engine")
    try:
        pygame.key.set_repeat(400, 35)
    except (pygame.error, AttributeError):
        pass
    if CONFIG["geral"].get("tela_cheia_ao_abrir"):
        alternar_tela_cheia()
    relogio = pygame.time.Clock()
    if CONFIG["geral"].get("tela_carregamento", True):
        if not mostrar_carregamento(tela, relogio, 1.3, etapas=["Preparando a engine...", "Carregando plugins...",
                                                                  "Procurando suas criações...", "Pronto!"]):
            pygame.quit()
            return
    try:
        migrar_projeto_antigo()
    except OSError:
        pass
    caminho = None
    ultimo = CONFIG["geral"].get("ultimo_projeto", "")
    if CONFIG["geral"].get("abrir_ultimo") and ultimo and os.path.isfile(os.path.join(ultimo, "projeto.json")):
        caminho = ultimo
    while True:
        if caminho is None:
            caminho = Inicio(tela, relogio).rodar()
            if caminho is None:
                break
        CONFIG["geral"]["ultimo_projeto"] = caminho
        salvar_config()
        aplicar_controles(CONFIG["controles"])
        editor = Editor(pasta_projeto=caminho, tela=tela)
        editor.rodar()
        if not editor.voltar_inicio:
            break
        caminho = None
        pygame.display.set_caption("Minha Engine")
    parar_musica()
    pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--jogar":
        jogar_sozinho(sys.argv[2])
    else:
        main()
