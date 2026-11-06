# Minha Engine - objetos_mais.py
# +100 OBJETOS PRONTOS na paleta (já vêm com aparência e comportamentos ligados)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

PRESETS_MAIS = {}        # nome -> (tipo, extra, comportamentos)
GRUPOS_MAIS = {}         # grupo da paleta -> nomes


def _preset(grupo_paleta, nome, desc, tipo, w, h, cor, comps=(), **extra):
    assert nome not in PRESETS_MAIS, nome
    PRESETS_MAIS[nome] = (tipo, dict(extra, w=w, h=h, cor=list(cor)), list(comps))
    DESC_PRESETS[nome] = desc
    GRUPOS_MAIS.setdefault(grupo_paleta, []).append(nome)


def _cp(nome_c, **p):
    return (nome_c, p)


_preset_antigo = preset_objeto


def preset_objeto(nome):
    item = PRESETS_MAIS.get(nome)
    if item is None:
        return _preset_antigo(nome)
    tipo, extra, comps = item
    lista = []
    for nome_c, p in comps:
        base = params_padrao(COMPORTAMENTOS[nome_c])
        base.update({k: str(v) for k, v in p.items()})
        lista.append({"t": nome_c, "p": base})
    return nova_entidade(tipo, 0, 0, nome, comportamentos=lista, **copy.deepcopy(extra))


# ---------------- NATUREZA ----------------
_GP = "NATUREZA"
_preset(_GP, "Árvore", "Árvore grande (fica transparente quando o player passa atrás).", "Decoracao", 70, 110,
        (60, 150, 70), [_cp("Transparente perto do player")], forma="Círculo", material="Grama", camada=2)
_preset(_GP, "Pinheiro", "Pinheiro alto em forma de triângulo.", "Decoracao", 60, 120, (40, 120, 70),
        forma="Triângulo", material="Grama", camada=2)
_preset(_GP, "Arbusto", "Moitinha verde que balança.", "Decoracao", 50, 30, (70, 160, 80),
        [_cp("Balançar", graus=4)], forma="Círculo", material="Grama")
_preset(_GP, "Flor", "Florzinha que balança com o vento.", "Decoracao", 14, 22, (255, 120, 170),
        [_cp("Balançar", graus=12, vezes_por_seg=1)], forma="Círculo")
_preset(_GP, "Pedra grande", "Rocha sólida para subir em cima.", "Bloco", 70, 50, (130, 130, 140), material="Pedra",
        forma="Círculo")
_preset(_GP, "Tronco", "Tronco caído (sólido).", "Bloco", 110, 28, (120, 80, 45), material="Madeira")
_preset(_GP, "Cogumelo pula-pula", "Cogumelo que joga o player para o alto.", "Bloco", 50, 26, (230, 70, 80),
        [_cp("Mola (pula ao pisar)", forca=1250)], forma="Círculo")
_preset(_GP, "Água", "Água para nadar (cai devagar, pula sem parar).", "Decoracao", 200, 120, (60, 140, 230),
        [_cp("Pulsar entre duas cores", r=90, g=170, b=255, vezes_por_seg=0.3)], opacidade=150, grupo="Agua",
        material="Vidro", camada=3)
_preset(_GP, "Areia movediça", "Afunda e deixa lento.", "Decoracao", 160, 40, (200, 170, 100),
        [_cp("Areia movediça")], material="Areia")
_preset(_GP, "Bloco de gelo", "Bloco escorregadio.", "Bloco", 120, 40, (170, 220, 255), material="Gelo")
_preset(_GP, "Nuvem", "Nuvem fofa que flutua (dá para pisar por cima).", "Bloco", 110, 34, (245, 248, 255),
        [_cp("Flutuar suave", altura=6), _cp("Plataforma de mão única")], forma="Círculo")
_preset(_GP, "Folhas caindo", "Folhas caindo devagar pela tela.", "Zona", 40, 40, (230, 160, 60),
        [_cp("Emissor de partículas", estilo="neve", por_seg=6, r=230, g=150, b=60)])

# ---------------- INIMIGOS ----------------
_GP = "INIMIGOS+"
_preset(_GP, "Slime", "Pula atrás do player e se divide ao morrer.", "Inimigo", 34, 26, (110, 220, 110),
        [_cp("Vida", vida=2), _cp("Pular quando o player chega perto"), _cp("Dividir ao morrer"),
         _cp("Esticar ao pular")], forma="Círculo", velocidade=60)
_preset(_GP, "Morcego", "Voa atrás do player em ondas.", "Inimigo", 30, 20, (120, 80, 160),
        [_cp("Morcego (voa atrás do player)"), _cp("Vida", vida=1)], gravidade=False)
_preset(_GP, "Fantasma", "Só aparece perto e atravessa paredes.", "Inimigo", 34, 40, (220, 230, 255),
        [_cp("Invisível longe do player"), _cp("Perseguir", velocidade=70), _cp("Flutuar suave")],
        gravidade=False, velocidade=0)
_preset(_GP, "Touro", "Vê o player e dá uma investida.", "Inimigo", 46, 36, (150, 90, 60),
        [_cp("Investida"), _cp("Vida", vida=3), _cp("Virar para onde anda")], velocidade=0)
_preset(_GP, "Atirador", "Atira 3 tiros em leque.", "Inimigo", 32, 40, (200, 80, 200),
        [_cp("Atirar em leque", tipo="Moeda"), _cp("Vida", vida=2), _cp("Olhar para")], velocidade=0)
_preset(_GP, "Torre giratória", "Atira em todas as direções.", "Bloco", 40, 40, (110, 110, 130),
        [_cp("Atirar em círculo", tiros=6)], material="Metal")
_preset(_GP, "Bomba ambulante", "Corre até você e explode!", "Inimigo", 28, 28, (40, 40, 50),
        [_cp("Kamikaze")], forma="Círculo", velocidade=0)
_preset(_GP, "Guarda", "Patrulha sem cair das plataformas.", "Inimigo", 32, 44, (90, 110, 200),
        [_cp("Patrulhar sem cair"), _cp("Vida", vida=2)])
_preset(_GP, "Chefe", "Grandão com muita vida que fica bravo na metade.", "Inimigo", 90, 90, (180, 40, 60),
        [_cp("Vida", vida=20, barra="Sim"), _cp("Chefe que fica bravo"), _cp("Pular sozinho", a_cada_seg=3),
         _cp("Atirar em leque", tiros=5, a_cada_seg=2.5), _cp("Tremer a tela perto", alcance=400)],
        velocidade=70)
_preset(_GP, "Esmagador", "Bloco que despenca quando você passa embaixo.", "Bloco", 60, 60, (100, 100, 120),
        [_cp("Cair quando o player passa embaixo"), _cp("Dano", quanto=2)], material="Pedra")
_preset(_GP, "Toupeira", "Se esconde e aparece do chão.", "Inimigo", 30, 30, (140, 100, 70),
        [_cp("Toupeira (esconde e aparece)"), _cp("Vida", vida=1)], velocidade=0, gravidade=False)
_preset(_GP, "Ninho de inimigos", "Cria inimigos de tempos em tempos.", "Bloco", 60, 50, (90, 60, 90),
        [_cp("Gerar inimigos"), _cp("Vida", vida=5)], material="Pedra")
_preset(_GP, "Abelha", "Voa em 8 e machuca ao tocar.", "Inimigo", 20, 18, (255, 210, 40),
        [_cp("Oito (infinito)", largura=80, altura=40)], gravidade=False, velocidade=0)
_preset(_GP, "Dorminhoco", "Dorme até você chegar perto, aí persegue.", "Inimigo", 36, 32, (120, 140, 90),
        [_cp("Dormir até ver o player"), _cp("Perseguir", velocidade=150)], velocidade=0)

# ---------------- PLATAFORMAS ----------------
_GP = "PLATAFORMAS"
_preset(_GP, "Elevador", "Sobe e desce parando nas pontas.", "Bloco", 100, 20, (120, 140, 160),
        [_cp("Elevador (para nas pontas)")], material="Metal")
_preset(_GP, "Plataforma circular", "Gira em círculo.", "Bloco", 90, 20, (90, 160, 220), [_cp("Círculo", raio=90)])
_preset(_GP, "Plataforma pêndulo", "Balança como pêndulo.", "Bloco", 80, 20, (200, 160, 90),
        [_cp("Pêndulo")], material="Madeira")
_preset(_GP, "Plataforma de nuvem", "Só sólida por cima (pule por baixo).", "Bloco", 120, 16, (230, 235, 255),
        [_cp("Plataforma de mão única")])
_preset(_GP, "Plataforma ritmada", "Some e aparece no ritmo.", "Bloco", 90, 20, (255, 140, 80),
        [_cp("Some e aparece no ritmo")], material="Neon")
_preset(_GP, "Plataforma que cai+", "Cai quando você pisa.", "Bloco", 90, 20, (170, 120, 80),
        [_cp("Plataforma que cai"), _cp("Tremer sempre", forca=0.5)], material="Madeira")
_preset(_GP, "Esteira →", "Carrega para a direita.", "Bloco", 160, 20, (70, 70, 80),
        [_cp("Esteira", velocidade=150)], material="Metal")
_preset(_GP, "Esteira ←", "Carrega para a esquerda.", "Bloco", 160, 20, (70, 70, 80),
        [_cp("Esteira", velocidade=-150)], material="Metal")
_preset(_GP, "Mola", "Joga para o alto.", "Bloco", 40, 20, (240, 200, 60), [_cp("Mola (pula ao pisar)")],
        material="Metal")
_preset(_GP, "Super mola", "Joga MUITO alto.", "Bloco", 40, 20, (255, 80, 200), [_cp("Mola (pula ao pisar)",
                                                                                    forca=1900)], material="Neon")
_preset(_GP, "Plataforma vai-e-volta", "Vai até um ponto e volta.", "Bloco", 100, 20, (90, 200, 160),
        [_cp("Ir e voltar até um ponto")])
_preset(_GP, "Plataforma quadrada", "Anda em quadrado.", "Bloco", 80, 20, (160, 120, 220),
        [_cp("Andar em quadrado")])
_preset(_GP, "Escada", "Suba com cima/baixo (precisa do comportamento 'Subir escadas' no player).", "Decoracao",
        40, 160, (150, 110, 60), grupo="Escada", material="Madeira")
_preset(_GP, "Rampa ◢", "Rampa para subir.", "Bloco", 120, 60, (90, 200, 120), forma="Rampa ◢", material="Grama")

# ---------------- ARMADILHAS ----------------
_GP = "ARMADILHAS"
_preset(_GP, "Serra", "Serra giratória que machuca.", "Decoracao", 48, 48, (200, 200, 210),
        [_cp("Serra giratória")], forma="Círculo", material="Metal")
_preset(_GP, "Serra que anda", "Serra que vai e volta.", "Decoracao", 48, 48, (200, 200, 210),
        [_cp("Serra giratória"), _cp("Ir e voltar até um ponto", dx=160)], forma="Círculo", material="Metal")
_preset(_GP, "Laser", "Raio que liga e desliga.", "Decoracao", 200, 10, (255, 50, 60),
        [_cp("Laser liga e desliga")], material="Neon")
_preset(_GP, "Canhão", "Atira bolas sem parar.", "Bloco", 40, 30, (60, 60, 70),
        [_cp("Canhão")], material="Metal")
_preset(_GP, "Lava que sobe", "Lava que vai subindo! Corra!", "Lava", 800, 40, (255, 90, 20),
        [_cp("Subir com o tempo (lava/água)"), _cp("Emissor de partículas", estilo="fogo", por_seg=20)])
_preset(_GP, "Bola de espinhos", "Gira em volta de um ponto.", "Espinho", 30, 30, (200, 200, 215),
        [_cp("Círculo", raio=70, voltas_por_seg=0.4), _cp("Girar sempre", graus_por_seg=200)], forma="Círculo")
_preset(_GP, "Mina", "Explode quando você encosta.", "Decoracao", 26, 14, (80, 80, 90),
        [_cp("Explodir ao tocar no player"), _cp("Piscar sempre", vezes_por_seg=1)], material="Metal")
_preset(_GP, "Ventilador", "Vento que empurra para cima.", "Zona", 80, 240, (200, 230, 255),
        [_cp("Zona de vento")])
_preset(_GP, "Buraco negro", "Puxa tudo para o centro.", "Decoracao", 50, 50, (40, 10, 60),
        [_cp("Buraco negro (atrai)"), _cp("Dano")], forma="Círculo")
_preset(_GP, "Pêndulo de espinhos", "Espinho balançando.", "Espinho", 34, 34, (200, 200, 215),
        [_cp("Pêndulo", comprimento=140)], forma="Losango")
_preset(_GP, "Bloco de fogo", "Fogo que liga e desliga.", "Decoracao", 40, 60, (255, 140, 40),
        [_cp("Laser liga e desliga", seg_ligado=1, seg_desligado=2), _cp("Emissor de partículas", estilo="fogo")])

# ---------------- ITENS ----------------
_GP = "ITENS+"
_preset(_GP, "Chave", "Pegue para abrir a Porta trancada.", "Decoracao", 22, 22, (255, 220, 60),
        [_cp("Chave"), _cp("Flutuar suave")], forma="Losango")
_preset(_GP, "Porta trancada", "Só abre com a Chave.", "Bloco", 30, 80, (140, 90, 50),
        [_cp("Porta trancada")], material="Madeira")
_preset(_GP, "Coração", "+1 vida máxima.", "Decoracao", 24, 22, (255, 80, 110),
        [_cp("Item: vida máxima +1"), _cp("Crescer e encolher", quanto=0.1)], forma="Círculo")
_preset(_GP, "Pena", "+1 pulo no ar.", "Decoracao", 20, 26, (220, 240, 255),
        [_cp("Item: pulo extra"), _cp("Flutuar suave")], forma="Losango")
_preset(_GP, "Bota veloz", "+20% velocidade.", "Decoracao", 24, 20, (255, 160, 40),
        [_cp("Item: velocidade +20%"), _cp("Flutuar suave")])
_preset(_GP, "Moeda fujona", "Foge de você!", "Moeda", 20, 20, (255, 210, 50),
        [_cp("Coletável que foge")], forma="Círculo")
_preset(_GP, "Moeda que volta", "Volta depois de pega.", "Moeda", 20, 20, (255, 230, 120),
        [_cp("Moeda que volta")], forma="Círculo")
_preset(_GP, "Bloco ?", "Bata por baixo para ganhar moedas.", "Bloco", 40, 40, (240, 180, 40),
        [_cp("Bloco ? (dá moeda)")])
_preset(_GP, "Estrela", "Invencível por uns segundos.", "Decoracao", 26, 26, (255, 240, 80),
        [_cp("Ao tocar no player → deixar o player invencível", seg=6), _cp("Ao tocar no player → se destruir"),
         _cp("Arco-íris")], forma="Losango")
_preset(_GP, "Poção", "Cura 1 de vida.", "Decoracao", 18, 24, (200, 60, 220),
        [_cp("Ao tocar no player → curar o player"), _cp("Ao tocar no player → se destruir"),
         _cp("Flutuar suave")])
_preset(_GP, "Relâmpago", "Turbo por alguns segundos.", "Decoracao", 18, 28, (255, 240, 80),
        [_cp("Ao tocar no player → dar turbo ao player"), _cp("Ao tocar no player → se destruir")],
        forma="Losango")
_preset(_GP, "Baú", "Clique para abrir e ganhar 10 moedas.", "Bloco", 44, 32, (150, 100, 50),
        [_cp("Ao ser clicado → dar moedas", n=10), _cp("Ao ser clicado → se destruir")], material="Madeira")
_preset(_GP, "Gema", "Vale 5 moedas e brilha.", "Decoracao", 20, 20, (80, 230, 255),
        [_cp("Ao tocar no player → dar moedas", n=5), _cp("Ao tocar no player → se destruir"),
         _cp("Brilho que pisca", raio=80)], forma="Losango")

# ---------------- MECANISMOS ----------------
_GP = "MECANISMOS"
_preset(_GP, "Alavanca", "Aperte E perto para abrir/fechar a Ponte.", "Decoracao", 20, 36, (180, 180, 190),
        [_cp("Alavanca (liga/desliga grupo)")], material="Metal")
_preset(_GP, "Ponte", "Some/aparece pela Alavanca (grupo Ponte).", "Bloco", 160, 20, (150, 110, 60),
        grupo="Ponte", material="Madeira")
_preset(_GP, "Botão de pressão", "Com algo em cima, abre a Porta (grupo Porta).", "Bloco", 40, 10, (220, 60, 60),
        [_cp("Botão de pressão")])
_preset(_GP, "Porta (grupo)", "Abre com o Botão de pressão.", "Bloco", 30, 100, (110, 110, 130), grupo="Porta",
        material="Metal")
_preset(_GP, "Porta automática", "Abre quando você chega perto.", "Bloco", 30, 100, (90, 160, 200),
        [_cp("Porta automática")], material="Vidro")
_preset(_GP, "Portal A", "Leva até o Portal B (mesmo grupo).", "Decoracao", 40, 60, (170, 80, 255),
        [_cp("Teleporte em par"), _cp("Pulsar entre duas cores", r=255, g=150, b=255)], grupo="Portais",
        forma="Círculo")
_preset(_GP, "Portal B", "Leva até o Portal A.", "Decoracao", 40, 60, (80, 200, 255),
        [_cp("Teleporte em par"), _cp("Pulsar entre duas cores", r=150, g=255, b=255)], grupo="Portais",
        forma="Círculo")
_preset(_GP, "Checkpoint invisível", "Salva o ponto de volta ao passar.", "Zona", 40, 120, (120, 255, 140),
        [_cp("Checkpoint invisível")])
_preset(_GP, "Caixa carregável", "Pegue com E e jogue.", "Caixa", 34, 34, (170, 120, 60),
        [_cp("Pegar e carregar (E)")], material="Madeira")
_preset(_GP, "Caixa frágil", "Quebra se cair de alto.", "Caixa", 40, 40, (190, 150, 90),
        [_cp("Quebrar ao cair de alto")], material="Madeira")
_preset(_GP, "Bola de borracha", "Quica muito.", "Caixa", 30, 30, (255, 90, 90),
        [_cp("Quicar ao cair"), _cp("Rolar (gira andando)")], forma="Círculo", material="Borracha",
        empurravel=True)
_preset(_GP, "Ímã gigante", "Puxa moedas.", "Bloco", 40, 40, (200, 60, 60), [_cp("Ímã", raio=300)],
        material="Metal")

# ---------------- EFEITOS ----------------
_GP = "EFEITOS+"
_preset(_GP, "Vela", "Luz que tremula.", "Decoracao", 10, 24, (250, 240, 220),
        [_cp("Brilho que pisca", raio=110), _cp("Emissor de partículas", estilo="fogo", por_seg=10)])
_preset(_GP, "Cristal", "Cristal brilhante.", "Decoracao", 24, 36, (120, 220, 255),
        [_cp("Brilho que pisca", raio=140, vezes_por_seg=0.6), _cp("Flutuar suave")], forma="Losango",
        material="Neon")
_preset(_GP, "Neon arco-íris", "Barra que troca de cor.", "Decoracao", 120, 12, (255, 0, 200),
        [_cp("Arco-íris")], material="Neon")
_preset(_GP, "Fumaça", "Fumaça subindo.", "Zona", 30, 30, (150, 150, 150),
        [_cp("Emissor de partículas", estilo="fumaca", por_seg=10)])
_preset(_GP, "Faíscas", "Faíscas elétricas.", "Zona", 30, 30, (255, 240, 120),
        [_cp("Emissor de partículas", estilo="brilho", por_seg=30, r=255, g=240, b=120)])
_preset(_GP, "Escuridão de caverna", "Escurece a tela quando o player entra.", "Zona", 300, 300, (40, 40, 60),
        [_cp("Escurecer perto")])
_preset(_GP, "Tremor", "Treme a tela perto (cachoeira, máquina).", "Zona", 60, 60, (180, 180, 180),
        [_cp("Tremer a tela perto")])
_preset(_GP, "Câmera lenta", "Tudo fica lento quando você entra.", "Zona", 120, 120, (150, 200, 255),
        [_cp("Câmera lenta perto")])
_preset(_GP, "Zoom dramático", "Câmera aproxima quando você chega.", "Zona", 120, 120, (255, 200, 150),
        [_cp("Zoom quando chegar perto")])
_preset(_GP, "Objetivo com seta", "Mostra uma seta na borda quando está fora da tela.", "Decoracao", 30, 30,
        (255, 220, 80), [_cp("Seta apontando (fora da tela)"), _cp("Crescer e encolher")], forma="Losango")

# ---------------- PERSONAGENS ----------------
_GP = "PERSONAGENS+"
_preset(_GP, "Player ninja", "Corre com Shift, escala parede, agacha.", "Player", 30, 46, (60, 60, 80),
        [_cp("Correr com Shift"), _cp("Escalar paredes"), _cp("Agachar"), _cp("Poeira ao andar"),
         _cp("Esticar ao pular")])
_preset(_GP, "Player jetpack", "Voa segurando o pulo.", "Player", 32, 48, (240, 140, 60),
        [_cp("Jetpack"), _cp("Poeira ao andar")])
_preset(_GP, "Player planador", "Plana segurando o pulo.", "Player", 32, 48, (120, 200, 255),
        [_cp("Planar (segurar pulo)"), _cp("Girar ao pular")])
_preset(_GP, "Player atirador", "Atira para o mouse (clique).", "Player", 32, 48, (80, 220, 140),
        [_cp("Atirar para o mouse"), _cp("Pisar em qualquer inimigo")])
_preset(_GP, "Player herói", "Pisa em inimigos, nada e sobe escadas.", "Player", 32, 48, (80, 170, 255),
        [_cp("Pisar em qualquer inimigo"), _cp("Nadar (dentro da água)"), _cp("Subir escadas"),
         _cp("Invencível no começo"), _cp("Esticar ao pular")])
_preset(_GP, "Mascote", "Segue o player de perto.", "Decoracao", 20, 20, (255, 200, 120),
        [_cp("Mascote (segue de perto)"), _cp("Flutuar suave")], forma="Círculo")
_preset(_GP, "NPC falante", "Mostra um balão quando você chega perto.", "NPC", 32, 48, (240, 180, 90),
        [_cp("Quando o player chega perto → mostrar texto", texto="Olá!")])
_preset(_GP, "Vendedor", "Abre diálogo ao chegar perto.", "NPC", 34, 50, (200, 150, 220),
        [_cp("Quando o player chega perto → abrir diálogo", texto="Bem-vindo à loja!|Volte sempre!"),
         _cp("Balão de fala seguindo", texto="LOJA")])
_preset(_GP, "Galinha", "Anda à toa (top-down ou plataforma).", "NPC", 22, 22, (250, 250, 240),
        [_cp("Vagar (anda à toa)"), _cp("Virar para onde anda")], fala="Có có!")
_preset(_GP, "Carro", "Anda acelerando.", "Decoracao", 70, 30, (220, 60, 60),
        [_cp("Acelerar aos poucos"), _cp("Destruir fora da tela", margem=600)], gravidade=True)

# ---------------- CENÁRIO ----------------
_GP = "CENÁRIO"
_preset(_GP, "Casa", "Casinha (decoração).", "Decoracao", 120, 100, (200, 120, 90), material="Tijolo", camada=-1)
_preset(_GP, "Muro de tijolo", "Muro sólido.", "Bloco", 40, 120, (170, 80, 60), material="Tijolo")
_preset(_GP, "Chão de pedra", "Chão sólido de pedra.", "Bloco", 240, 40, (120, 120, 130), material="Pedra")
_preset(_GP, "Chão de areia", "Chão de areia.", "Bloco", 240, 40, (220, 200, 140), material="Areia")
_preset(_GP, "Chão de metal", "Chão de metal.", "Bloco", 240, 40, (140, 150, 160), material="Metal")
_preset(_GP, "Placa", "Placa com texto em cima.", "Decoracao", 40, 40, (170, 120, 60),
        [_cp("Nome em cima", texto="→ Saída"), _cp("Balançar", graus=3)], material="Madeira")
_preset(_GP, "Poste de luz", "Poste que ilumina à noite.", "Decoracao", 12, 100, (80, 80, 90),
        [_cp("Luz", raio=180)], material="Metal")
_preset(_GP, "Cerca", "Cerca de madeira.", "Decoracao", 100, 30, (180, 140, 90), material="Madeira")
_preset(_GP, "Vidraça", "Vidro sólido transparente.", "Bloco", 20, 100, (180, 220, 255), material="Vidro")
_preset(_GP, "Barril", "Barril que rola.", "Caixa", 34, 40, (140, 90, 50), [_cp("Rolar (gira andando)")],
        material="Madeira", empurravel=True)

# ---------------- INTERFACE ----------------
_GP = "INTERFACE+"
_preset(_GP, "Contador de pontos", "Mostra global.pontos.", "Texto", 220, 32, (255, 230, 90),
        [_cp("Mostrar variável")])
_preset(_GP, "Barra de tempo", "Esvazia; quando acaba, perde.", "Barra", 240, 18, (255, 200, 60),
        [_cp("Barra do tempo")])
_preset(_GP, "Botão reiniciar", "Reinicia a fase.", "Botao", 150, 40, (220, 90, 90), [_cp("Botão: reiniciar")],
        texto="Reiniciar")
_preset(_GP, "Botão pausar", "Pausa o jogo.", "Botao", 130, 40, (90, 120, 220), [_cp("Botão: pausar")],
        texto="Pausar")
_preset(_GP, "Título de início", "Mostra um título grande ao começar.", "Zona", 30, 30, (255, 255, 255),
        [_cp("Ao começar → mostrar título", texto="FASE 1")])
_preset(_GP, "Meta de moedas", "Vence ao juntar 10 moedas.", "Zona", 30, 30, (255, 210, 50),
        [_cp("Vencer ao juntar N")])

TOTAL_PRESETS_MAIS = len(PRESETS_MAIS)

# coloca os grupos novos na paleta (começam FECHADOS para não poluir; clique no nome para abrir)
for _gp_m, _nomes_m in GRUPOS_MAIS.items():
    GRUPOS_TIPOS.append((_gp_m, ["preset:" + n for n in _nomes_m]))
GRUPOS_FECHADOS_PADRAO = set(GRUPOS_MAIS)
