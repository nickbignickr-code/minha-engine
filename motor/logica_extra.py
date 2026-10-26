# Minha Engine - logica_extra.py
# MAIS comportamentos, ações, condições, eventos (QUANDO) e propriedades, com categorias para o seletor
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# =====================================================================
# NOVAS PROPRIEDADES
# =====================================================================
COMUNS["gravidade_escala"] = 1.0
MODELOS["Player"].update({"dano": 1, "dash": False, "forca_dash": 900, "pulo_parede": False, "tiro": "", "vel_tiro": 650,
                          "tecla_tiro": "f"})
MODELOS["Inimigo"].update({"dano": 1, "pode_ser_pisado": True})
MODELOS["Espinho"]["dano"] = 1
MODELOS["Lava"]["dano"] = 1
ROTULOS.update({
    "gravidade_escala": "Gravidade (x)", "dash": "Dash (Shift)", "forca_dash": "Força do dash",
    "pulo_parede": "Pulo na parede", "tiro": "Atira (tipo/modelo)", "vel_tiro": "Velocidade do tiro",
    "tecla_tiro": "Tecla do tiro", "dano": "Dano", "pode_ser_pisado": "Morre se pisar",
})

# =====================================================================
# NOVOS COMPORTAMENTOS
# =====================================================================
COMPORTAMENTOS.update({
    "Dano": COMPORTAMENTOS.get("Dano", [("quanto", "1", "e"), ("em", "Player", "s"), ("empurrar", "350", "e"),
                                        ("some_ao_acertar", "Não", "sn")]),
    "Patrulhar": [("velocidade", "100", "e"), ("distancia", "160", "e"), ("eixo", "x", "s")],
    "Andar sozinho": [("velocidade", "120", "e"), ("virar_na_parede", "Sim", "sn")],
    "Fugir de": [("alvo", "Player", "s"), ("velocidade", "160", "e"), ("alcance", "250", "e")],
    "Orbitar": [("alvo", "Player", "s"), ("raio", "80", "e"), ("voltas_por_seg", "0.5", "e")],
    "Mascote (segue de perto)": [("alvo", "Player", "s"), ("distancia", "50", "e"), ("suavidade", "5", "e")],
    "Pular sozinho": [("a_cada_seg", "2", "e"), ("forca", "650", "e")],
    "Atirar": [("tipo", "Moeda", "s"), ("a_cada_seg", "1.5", "e"), ("velocidade", "450", "e"),
               ("alvo", "Player", "s"), ("alcance", "500", "e")],
    "Olhar para": [("alvo", "Player", "s")],
    "Girar para o mouse": [],
    "Seguir o mouse": [("velocidade", "0", "e")],
    "Coletável": [("variavel", "pontos", "s"), ("valor", "1", "e")],
    "Cura ao tocar": [("quanto", "1", "e"), ("em", "Player", "s"), ("some", "Sim", "sn")],
    "Power-up ao tocar": [("propriedade", "velocidade", "s"), ("multiplicar", "1.5", "e"), ("seg", "5", "e"),
                          ("em", "Player", "s")],
    "Porta para fase": [("fase", "Fase 2", "s"), ("tecla", "", "s")],
    "Plataforma que cai": [("espera", "0.5", "e")],
    "Quebrar ao bater por baixo": [("solta", "", "s")],
    "Reaparecer": [("seg", "3", "e")],
    "Regenerar vida": [("a_cada_seg", "2", "e"), ("quanto", "1", "e")],
    "Ímã": [("tipo", "Moeda", "s"), ("raio", "160", "e"), ("forca", "450", "e")],
    "Explodir ao morrer": [("raio", "110", "e"), ("dano", "1", "e"), ("em", "Inimigo", "s")],
    "Pulsar": [("escala", "0.15", "e"), ("vezes_por_seg", "1", "e")],
    "Ricochetear": [],
    "Limitar velocidade": [("maximo", "400", "e")],
    "Cronômetro": [("variavel", "tempo", "s"), ("modo", "sobe", "s"), ("inicio", "0", "e")],
})
DESC_COMPORTAMENTOS.update({
    "Patrulhar": "Vai e volta sozinho (eixo x = lados, y = cima/baixo) na distância escolhida. Qualquer objeto.",
    "Andar sozinho": "Anda para frente sem parar e vira quando bate na parede (bom com gravidade).",
    "Fugir de": "Foge do alvo (nome, tipo ou grupo) quando ele chega perto.",
    "Orbitar": "Fica girando em volta do alvo (escudo, lua, satélite). Sem alvo, gira em volta de onde começou.",
    "Mascote (segue de perto)": "Segue o alvo de pertinho, atrás dele, com movimento suave (pet, ajudante).",
    "Pular sozinho": "Pula a cada X segundos quando está no chão (sapo, slime).",
    "Atirar": "Atira o 'tipo' (objeto ou modelo) a cada X segundos. Com alvo, mira nele quando está no alcance; "
              "sem alvo, atira para frente. Dica: dê o comportamento Dano para o tiro.",
    "Olhar para": "Vira a imagem para o lado do alvo.",
    "Girar para o mouse": "Gira apontando para o mouse (canhão, arma, torre).",
    "Seguir o mouse": "Vai até o mouse. Velocidade 0 = gruda no mouse na hora.",
    "Coletável": "Quando o Player encosta, some e soma 'valor' na variável global (ex: global.pontos).",
    "Cura ao tocar": "Cura quem encostar (em) e some (coração, poção, kit médico).",
    "Power-up ao tocar": "Quem encostar fica com a propriedade multiplicada por um tempo (ex: velocidade x1.5 "
                         "por 5 seg, pulo x1.4...). Depois volta ao normal.",
    "Porta para fase": "Leva para outra fase quando o Player encosta (ou aperta a tecla, se você escolher uma).",
    "Plataforma que cai": "Cai alguns instantes depois que alguém fica em cima.",
    "Quebrar ao bater por baixo": "Quebra quando o Player bate a cabeça nele (bloco do Mario). Pode soltar um objeto.",
    "Reaparecer": "Volta X segundos depois de ser destruído, no lugar de onde começou (moedas, inimigos).",
    "Regenerar vida": "Recupera vida aos poucos (precisa do comportamento Vida).",
    "Ímã": "Puxa objetos do tipo escolhido que estiverem perto (moedas, itens).",
    "Explodir ao morrer": "Quando é destruído, explode e dá dano em quem estiver perto (bomba, barril).",
    "Pulsar": "Cresce e diminui sem parar (estrela, coração, botão chamando atenção).",
    "Ricochetear": "Quica nas paredes, no chão e no teto em vez de parar (bola, tiro que rebate).",
    "Limitar velocidade": "Nunca passa da velocidade máxima.",
    "Cronômetro": "Conta o tempo numa variável global. modo 'sobe' (0, 1, 2...) ou 'desce' (do início até 0).",
})

# =====================================================================
# NOVOS EVENTOS (QUANDO)
# =====================================================================
GATILHOS.update({
    "Depois de X segundos (1 vez)": [("seg", "2", "e")],
    "Ao pular": [],
    "Ao bater na parede": [],
    "Ao bater a cabeça": [],
    "Ao sair da tela": [],
    "Ao entrar na tela": [],
    "Mouse entrou no objeto": [],
    "Mouse saiu do objeto": [],
    "Ao soltar o botão do mouse": [],
    "Quando o player chegar perto": [("distancia", "150", "e")],
    "Quando o player se afastar": [("distancia", "150", "e")],
    "Ao ser curado": [],
    "Quando perder o jogo": [],
    "Quando a variável global mudar": [("var", "pontos", "s")],
    "Quando as moedas chegarem a": [("valor", "10", "e")],
})
GATILHO_EVENTO.update({
    "Depois de X segundos (1 vez)": "depois", "Ao pular": "pulo", "Ao bater na parede": "parede",
    "Ao bater a cabeça": "teto", "Ao sair da tela": "saiu_tela", "Ao entrar na tela": "entrou_tela",
    "Mouse entrou no objeto": "mouse_entrou", "Mouse saiu do objeto": "mouse_saiu",
    "Ao soltar o botão do mouse": "mouse_solto", "Quando o player chegar perto": "perto",
    "Quando o player se afastar": "longe", "Ao ser curado": "curado", "Quando perder o jogo": "derrota",
    "Quando a variável global mudar": "var_global", "Quando as moedas chegarem a": "moedas_valor",
})
EVENTOS_SCRIPT.update({"depois": True, "pulo": False, "parede": False, "teto": False, "saiu_tela": False,
                       "entrou_tela": False, "mouse_entrou": False, "mouse_saiu": False, "mouse_solto": False,
                       "perto": True, "longe": True, "curado": False, "derrota": False, "var_global": True,
                       "moedas_valor": True})
DESC_EVENTOS.update({
    "depois": "Uma vez só, X segundos depois de começar. Ex: quando depois 3:",
    "pulo": "Quando o objeto pula.", "parede": "Quando bate numa parede (lado).",
    "teto": "Quando bate a cabeça em algo sólido.", "saiu_tela": "Quando sai da parte que a câmera mostra.",
    "entrou_tela": "Quando aparece na câmera.", "mouse_entrou": "Quando o mouse passa por cima.",
    "mouse_saiu": "Quando o mouse sai de cima.", "mouse_solto": "Quando solta o botão do mouse.",
    "perto": "Quando o player chega perto (distância). Ex: quando perto 150:",
    "longe": "Quando o player se afasta (distância). Ex: quando longe 150:",
    "curado": "Quando o objeto ganha vida.", "derrota": "Quando o jogador perde.",
    "var_global": 'Quando uma variável global muda. Ex: quando var_global "pontos":',
    "moedas_valor": "Quando as moedas chegam no valor. Ex: quando moedas_valor 10:",
})

# =====================================================================
# NOVAS CONDICOES
# =====================================================================
CONDICOES.update({
    "Velocidade X": [("op", ">", "cmp"), ("valor", "0", "e")],
    "Velocidade Y": [("op", ">", "cmp"), ("valor", "0", "e")],
    "Está se movendo": [],
    "Está parado": [],
    "Indo para a direita": [],
    "Indo para a esquerda": [],
    "Subindo": [],
    "Caindo": [],
    "Encostado na parede": [],
    "Bateu a cabeça": [],
    "Em cima de": [("alvo", "Bloco", "s")],
    "Em cima de material": [("material", "Gelo", "s")],
    "Pulos no ar restantes": [("op", ">", "cmp"), ("valor", "0", "e")],
    "Está invencível": [],
    "Vida máxima": [("op", ">=", "cmp"), ("valor", "5", "e")],
    "Vida em %": [("op", "<=", "cmp"), ("valor", "50", "e")],
    "Propriedade": [("prop", "velocidade", "s"), ("op", ">", "cmp"), ("valor", "300", "e")],
    "Propriedade de outro objeto": [("objeto", "Player", "s"), ("prop", "velocidade", "s"), ("op", ">", "cmp"),
                                    ("valor", "300", "e")],
    "Olhando para a esquerda": [],
    "Aparece na tela": [],
    "Fora da tela": [],
    "Nome é": [("nome", "Bloco1", "s")],
    "Tipo é": [("tipo", "Inimigo", "s")],
    "Tecla acabou de ser apertada": [("tecla", "e", "s")],
    "Itens no inventário": [("op", ">=", "cmp"), ("valor", "3", "e")],
    "Player perto": [("distancia", "150", "e")],
    "Mouse perto": [("distancia", "80", "e")],
    "Número aleatório": [("de", "1", "e"), ("ate", "10", "e"), ("op", "==", "cmp"), ("valor", "5", "e")],
})

# =====================================================================
# NOVAS ACOES
# =====================================================================
ACOES.update({
    # atributos
    "Mudar velocidade": [("op", "=", "atr"), ("valor", "450", "e")],
    "Mudar força do pulo": [("op", "=", "atr"), ("valor", "900", "e")],
    "Mudar pulos no ar": [("op", "=", "atr"), ("valor", "1", "e")],
    "Mudar aceleração": [("op", "=", "atr"), ("valor", "3000", "e")],
    "Mudar dano": [("op", "=", "atr"), ("valor", "2", "e")],
    "Mudar vida (somar ou tirar)": [("op", "+=", "atr"), ("valor", "1", "e")],
    "Mudar vida máxima": [("op", "=", "atr"), ("valor", "5", "e")],
    "Mudar escala da gravidade": [("valor", "0.5", "e")],
    "Mudar propriedade": [("prop", "velocidade", "s"), ("op", "=", "atr"), ("valor", "450", "e")],
    "Mudar propriedade de outro objeto": [("objeto", "Player", "s"), ("prop", "velocidade", "s"), ("op", "=", "atr"),
                                          ("valor", "450", "e")],
    "Mudar parâmetro de comportamento": [("comportamento", "Dano", "s"), ("parametro", "quanto", "s"),
                                         ("valor", "2", "e")],
    "Poder temporário": [("prop", "velocidade", "s"), ("multiplicar", "1.5", "e"), ("seg", "5", "e")],
    "Ficar invencível": [("seg", "2", "e")],
    # movimento
    "Dash (impulso para frente)": [("forca", "900", "e")],
    "Pular mesmo no ar": [("forca", "700", "e")],
    "Virar para o outro lado": [],
    "Olhar para objeto": [("objeto", "Player", "s")],
    "Mover no ângulo": [("angulo", "0", "e"), ("velocidade", "300", "e")],
    "Ir até o mouse": [("velocidade", "300", "e")],
    "Teleportar para o mouse": [],
    "Parar só na horizontal": [],
    "Parar só na vertical": [],
    "Limitar velocidade agora": [("maximo", "400", "e")],
    "Voltar para onde começou": [],
    "Empurrar para longe de": [("objeto", "Player", "s"), ("forca", "500", "e")],
    "Puxar objetos para perto": [("objeto", "Moeda", "s"), ("raio", "200", "e"), ("forca", "300", "e")],
    # combate
    "Atirar para frente": [("tipo", "Moeda", "s"), ("velocidade", "650", "e")],
    "Atirar em direção a": [("tipo", "Moeda", "s"), ("objeto", "Player", "s"), ("velocidade", "500", "e")],
    "Atirar para o mouse": [("tipo", "Moeda", "s"), ("velocidade", "650", "e")],
    "Explosão (dano em área)": [("raio", "120", "e"), ("qtd", "1", "e"), ("em", "Inimigo", "s")],
    "Dar dano em quem tocou": [("qtd", "1", "e")],
    "Empurrar quem tocou": [("forca", "500", "e")],
    "Curar objeto": [("objeto", "Player", "s"), ("qtd", "1", "e")],
    # criar
    "Clonar este objeto": [("dx", "50", "e"), ("dy", "0", "e")],
    "Criar em lugar aleatório": [("tipo", "Moeda", "s"), ("x1", "0", "e"), ("y1", "0", "e"), ("x2", "800", "e"),
                                 ("y2", "400", "e")],
    "Criar no mouse": [("tipo", "Moeda", "s")],
    # aparencia
    "Mudar camada": [("valor", "1", "e")],
    "Mudar escala": [("fator", "1.5", "e")],
    "Mudar material": [("material", "Neon", "s")],
    "Mudar forma": [("forma", "Círculo", "s")],
    "Cor aleatória": [],
    # jogo e tela
    "Câmera lenta": [("velocidade", "0.4", "e"), ("seg", "1.5", "e")],
    "Mudar moedas": [("op", "=", "atr"), ("valor", "0", "e")],
    "Mostrar título na tela": [("texto", "FASE 2", "s"), ("seg", "2", "e")],
    "Mudar zoom na hora": [("zoom", "1", "e")],
    "Câmera parar de seguir": [],
    # interface
    "Criar botão na tela": [("nome", "Botao1", "s"), ("texto", "Clique aqui", "s"), ("x", "300", "e"),
                            ("y", "200", "e"), ("largura", "200", "e"), ("altura", "50", "e"),
                            ("funcao", "", "s"), ("grupo", "Botoes", "s")],
    "Criar texto na tela": [("nome", "Texto1", "s"), ("texto", "Olá!", "s"), ("x", "300", "e"), ("y", "120", "e"),
                            ("tamanho", "32", "e"), ("grupo", "Botoes", "s")],
    "Apagar botões do grupo": [("grupo", "Botoes", "s")],
})

# =====================================================================
# CATEGORIAS E DESCRICOES (para o seletor com busca)
# =====================================================================
CATEGORIAS_ACOES = [
    ("Movimento", ["Mover", "Ir para", "Ir até objeto", "Velocidade X", "Velocidade Y (pulo)", "Pular (se no chão)",
                   "Pular mesmo no ar", "Dash (impulso para frente)", "Empurrar", "Parar movimento",
                   "Parar só na horizontal", "Parar só na vertical", "Seguir objeto", "Mover no ângulo",
                   "Ir até o mouse", "Teleportar para o mouse", "Mover suavemente para", "Virar para o outro lado",
                   "Olhar para objeto", "Limitar velocidade agora", "Voltar para onde começou",
                   "Empurrar para longe de", "Puxar objetos para perto"]),
    ("Atributos (vida, velocidade, pulo, dano...)", [
        "Mudar velocidade", "Mudar força do pulo", "Mudar pulos no ar", "Mudar aceleração", "Mudar dano",
        "Mudar vida", "Mudar vida (somar ou tirar)", "Mudar vida máxima", "Curar", "Mudar escala da gravidade",
        "Ficar invencível", "Poder temporário", "Mudar propriedade", "Mudar propriedade de outro objeto",
        "Mudar parâmetro de comportamento"]),
    ("Combate", ["Dar dano", "Dar dano em quem tocou", "Curar objeto", "Atirar para frente", "Atirar em direção a",
                 "Atirar para o mouse", "Lançar objeto (tiro)", "Explosão (dano em área)", "Empurrar quem tocou",
                 "Destruir quem tocou"]),
    ("Aparência", ["Mudar cor", "Cor aleatória", "Mudar imagem", "Mudar animação", "Mudar opacidade", "Girar",
                   "Espelhar", "Mudar tamanho", "Mudar escala", "Mudar camada", "Mudar material", "Mudar forma",
                   "Piscar", "Flash branco", "Esticar (squash)", "Esconder", "Mostrar", "Animar propriedade",
                   "Partículas", "Texto flutuante", "Mudar texto"]),
    ("Este objeto", ["Destruir", "Destruir depois de", "Ligar/desligar sólido", "Ligar/desligar gravidade",
                     "Ligar comportamento", "Desligar comportamento", "Mudar ângulo da bala", "Variável do objeto",
                     "Mostrar texto", "Clonar este objeto"]),
    ("Outros objetos", ["Destruir objeto", "Mover objeto", "Teleportar objeto", "Velocidade do objeto",
                        "Mudar cor do objeto", "Mudar texto do objeto", "Mudar imagem do objeto", "Esconder objeto",
                        "Mostrar objeto", "Sólido no objeto", "Variável de outro objeto"]),
    ("Criar", ["Criar objeto", "Criar objeto em", "Criar em lugar aleatório", "Criar no mouse",
               "Clonar este objeto", "Lançar objeto (tiro)"]),
    ("Variáveis, itens e lógica", ["Variável do objeto", "Variável global", "Variável de outro objeto", "Dar item",
                                   "Remover item", "Mudar moedas", "Somar moedas", "Esperar (segundos)",
                                   "Chamar função", "Executar código"]),
    ("Interface (botões e textos)", ["Criar botão na tela", "Criar texto na tela", "Apagar botões do grupo",
                                     "Texto na tela", "Apagar texto da tela", "Mostrar título na tela",
                                     "Controles do player"]),
    ("Textos e diálogos", ["Mostrar texto", "Mostrar diálogo", "Texto na tela", "Apagar texto da tela",
                           "Mostrar título na tela", "Texto flutuante", "Escrever no console"]),
    ("Câmera e efeitos", ["Tremer câmera", "Câmera seguir objeto", "Câmera parar de seguir", "Zoom da câmera",
                          "Mudar zoom na hora", "Câmera lenta", "Congelar tela (impacto)", "Mudar escuridão",
                          "Mudar cor do fundo", "Mudar gravidade da cena"]),
    ("Jogo, fases e sons", ["Ir para fase", "Próxima fase", "Reiniciar fase", "Vencer o jogo", "Perder o jogo",
                            "Voltar ao início", "Pausar jogo", "Controles do player", "Salvar progresso",
                            "Carregar progresso", "Tocar som", "Tocar música", "Parar música"]),
]
CATEGORIAS_CONDICOES = [
    ("Teclado e mouse", ["Tecla segurada", "Tecla acabou de ser apertada", "Botão do mouse segurado",
                         "Mouse em cima do objeto", "Mouse perto"]),
    ("Movimento", ["Está no chão", "Está se movendo", "Está parado", "Indo para a direita", "Indo para a esquerda",
                   "Subindo", "Caindo", "Encostado na parede", "Bateu a cabeça", "Velocidade X", "Velocidade Y",
                   "Pulos no ar restantes", "Olhando para a esquerda", "Em cima de", "Em cima de material"]),
    ("Posição e toque", ["Tocando em", "Distância até objeto", "Player perto", "Vê o objeto (linha de visão)",
                         "Posição X", "Posição Y", "Aparece na tela", "Fora da tela"]),
    ("Vida e combate", ["Vida do objeto", "Vida máxima", "Vida em %", "Está invencível"]),
    ("Este objeto", ["Está visível", "Nome é", "Tipo é", "Está no grupo", "Tem comportamento ligado", "Propriedade",
                     "Variável do objeto"]),
    ("Outros objetos", ["Objeto existe", "Quantidade de objetos", "Variável de outro objeto",
                        "Propriedade de outro objeto"]),
    ("Jogo e variáveis", ["Variável global", "Moedas", "Tem item", "Itens no inventário", "Fase atual é",
                          "Tempo de jogo (seg)", "Existe progresso salvo", "Diálogo aberto"]),
    ("Lógica e sorte", ["Comparar valores", "Chance (%)", "Número aleatório", "Expressão"]),
]
CATEGORIAS_GATILHOS = [
    ("Tempo", ["Ao iniciar", "A cada frame", "A cada X segundos", "Depois de X segundos (1 vez)"]),
    ("Teclado e mouse", ["Tecla apertada", "Tecla solta", "Ao clicar no objeto", "Clique em qualquer lugar",
                         "Ao soltar o botão do mouse", "Mouse entrou no objeto", "Mouse saiu do objeto"]),
    ("Toque e movimento", ["Ao tocar em", "Ao parar de tocar em", "Ao cair no chão", "Ao pular",
                           "Ao bater na parede", "Ao bater a cabeça", "Quando o player chegar perto",
                           "Quando o player se afastar", "Ao sair da tela", "Ao entrar na tela"]),
    ("Vida", ["Ao levar dano", "Ao ser curado", "Quando a vida acabar", "Ao ser destruído", "Quando o player morrer"]),
    ("Jogo", ["Quando pegar moeda", "Quando as moedas chegarem a", "Quando pegar item", "Quando vencer",
              "Quando perder o jogo", "Quando a variável global mudar", "Quando o diálogo terminar"]),
]
CATEGORIAS_COMPORTAMENTOS = [
    ("Movimento", ["Patrulhar", "Andar sozinho", "Senoide (vai e volta)", "Pular sozinho", "Perseguir", "Fugir de",
                   "Orbitar", "Mascote (segue de perto)", "8 direções (teclado)", "Seguir o mouse", "Bala",
                   "Ricochetear", "Limitar velocidade", "Plataforma que cai", "Plataforma atravessável",
                   "Preso no mapa", "Arrastável (mouse)"]),
    ("Combate", ["Vida", "Dano", "Atirar", "Regenerar vida", "Explodir ao morrer", "Olhar para",
                 "Girar para o mouse"]),
    ("Coletar e poderes", ["Coletável", "Cura ao tocar", "Power-up ao tocar", "Ímã", "Porta para fase",
                           "Quebrar ao bater por baixo", "Reaparecer", "Gerador"]),
    ("Efeitos", ["Luz", "Emissor de partículas", "Girar sempre", "Pulsar", "Sumir aos poucos",
                 "Destruir fora da tela"]),
    ("Jogo", ["Cronômetro"]),
]
DESC_ACOES = {
    "Mudar velocidade": "Muda a velocidade de andar do objeto (Player, inimigos e comportamentos).",
    "Mudar força do pulo": "Muda a força do pulo do Player.", "Mudar pulos no ar": "Quantos pulos extras no ar.",
    "Mudar aceleração": "Quão rápido o Player chega na velocidade (0 = na hora).",
    "Mudar dano": "Muda o dano do comportamento Dano (e do inimigo).",
    "Mudar vida (somar ou tirar)": "Soma ou tira vida sem piscar (use += ou -=).",
    "Mudar vida máxima": "Muda o máximo de vida (para a barra e para curar).",
    "Mudar escala da gravidade": "1 = normal, 0.5 = flutua (lua), 2 = pesado, 0 = sem gravidade.",
    "Mudar propriedade": "Muda QUALQUER propriedade do objeto pelo nome (velocidade, pulo, cor, opacidade...).",
    "Mudar propriedade de outro objeto": "Igual, mas em outro objeto (nome, tipo ou grupo).",
    "Mudar parâmetro de comportamento": "Muda uma opção de um comportamento (ex: Atirar > a_cada_seg).",
    "Poder temporário": "Multiplica uma propriedade por um tempo e depois volta (velocidade x2 por 5 seg).",
    "Ficar invencível": "Não leva dano por X segundos (pisca).",
    "Dash (impulso para frente)": "Dá um impulso rápido para o lado que está olhando.",
    "Pular mesmo no ar": "Pula na hora, mesmo sem estar no chão.",
    "Virar para o outro lado": "Inverte a direção e a imagem.", "Olhar para objeto": "Vira para o lado do objeto.",
    "Mover no ângulo": "Anda no ângulo (0 = direita, 90 = baixo, 180 = esquerda, 270 = cima).",
    "Ir até o mouse": "Anda em direção ao mouse.", "Teleportar para o mouse": "Vai para onde está o mouse.",
    "Limitar velocidade agora": "Corta a velocidade se passou do máximo.",
    "Voltar para onde começou": "Volta para a posição inicial.",
    "Empurrar para longe de": "Empurra este objeto para longe do outro.",
    "Puxar objetos para perto": "Puxa objetos perto (ímã por um instante; use no A cada frame).",
    "Atirar para frente": "Lança o objeto para o lado que está olhando.",
    "Atirar em direção a": "Lança o objeto mirando no alvo.", "Atirar para o mouse": "Lança o objeto na direção do mouse.",
    "Explosão (dano em área)": "Explode: dá dano em todos 'em' que estiverem no raio.",
    "Dar dano em quem tocou": "Dá dano em quem encostou (use no QUANDO Ao tocar em).",
    "Empurrar quem tocou": "Joga para longe quem encostou.", "Curar objeto": "Cura outro objeto.",
    "Clonar este objeto": "Cria uma cópia deste objeto ao lado.",
    "Criar em lugar aleatório": "Cria o objeto num lugar sorteado dentro da área.",
    "Criar no mouse": "Cria o objeto onde está o mouse.", "Mudar camada": "Quem tem camada maior fica na frente.",
    "Mudar escala": "Aumenta ou diminui o tamanho (2 = dobro, 0.5 = metade).", "Cor aleatória": "Sorteia uma cor.",
    "Câmera lenta": "Deixa o jogo mais devagar por um tempo (0.5 = metade da velocidade).",
    "Mudar moedas": "Muda a quantidade de moedas.", "Mostrar título na tela": "Texto grande no meio da tela.",
    "Mudar zoom na hora": "Muda o zoom sem animação.", "Câmera parar de seguir": "A câmera fica parada.",
    "Criar botão na tela": "Cria um botão clicável preso na tela. Ao clicar: a variável global 'botao_clicado' vira o "
                           "nome dele e (se tiver) chama a função. Use QUANDO 'Quando a variável global mudar' (botao_clicado) ou a condição 'Variável global' para reagir.",
    "Criar texto na tela": "Cria um texto preso na tela (dá para apagar junto com os botões pelo grupo).",
    "Apagar botões do grupo": "Destrói todos os botões e textos de um grupo (ex: fechar um menu).",
}
DESC_CONDICOES = {
    "Velocidade X": "Compara a velocidade para os lados.", "Velocidade Y": "Compara a velocidade para cima/baixo.",
    "Está se movendo": "Está andando ou caindo.", "Está parado": "Não está se mexendo.",
    "Subindo": "Está indo para cima.", "Caindo": "Está caindo (no ar, indo para baixo).",
    "Encostado na parede": "Bateu numa parede neste frame.", "Bateu a cabeça": "Bateu a cabeça neste frame.",
    "Em cima de": "Está em pé em cima de um objeto (nome, tipo ou grupo).",
    "Em cima de material": "Está em pé em cima de um material (Gelo, Areia...).",
    "Propriedade": "Compara qualquer propriedade do objeto pelo nome.",
    "Aparece na tela": "A câmera está mostrando o objeto.", "Fora da tela": "A câmera não mostra o objeto.",
    "Tecla acabou de ser apertada": "Só no frame em que apertou (não fica repetindo).",
    "Player perto": "O Player está a menos de X pixels.", "Mouse perto": "O mouse está a menos de X pixels.",
    "Número aleatório": "Sorteia um número de 'de' até 'ate' e compara.",
    "Vida em %": "Vida atual dividida pela máxima, em porcentagem.",
}
DESC_GATILHOS = {
    "Depois de X segundos (1 vez)": "Roda uma vez só, X segundos depois de começar.",
    "Ao pular": "Quando este objeto pula.", "Ao bater na parede": "Quando bate numa parede.",
    "Ao bater a cabeça": "Quando bate a cabeça em algo sólido.", "Ao sair da tela": "Quando a câmera para de mostrar.",
    "Ao entrar na tela": "Quando a câmera começa a mostrar.", "Mouse entrou no objeto": "Mouse passou por cima.",
    "Mouse saiu do objeto": "Mouse saiu de cima.", "Ao soltar o botão do mouse": "Soltou o clique.",
    "Quando o player chegar perto": "O Player chegou perto (distância).",
    "Quando o player se afastar": "O Player se afastou (distância).",
    "Ao ser curado": "Quando ganha vida.", "Quando perder o jogo": "Quando o jogador perde.",
    "Quando a variável global mudar": "Quando global.(var) muda de valor.",
    "Quando as moedas chegarem a": "Quando as moedas chegam no valor.",
}


# opcoes prontas para os campos de texto dos eventos (clicar abre a lista)
PROPS_SUGERIDAS = ["velocidade", "pulo", "pulos_extras", "aceleracao", "dano", "gravidade_escala", "opacidade",
                   "rotacao", "camada", "w", "h", "x", "y", "vx", "vy", "forca_dash", "vel_tiro", "fps_anim", "texto",
                   "tamanho_fonte"]
OPCOES_PARAMS = {"material": MATERIAIS, "forma": FORMAS, "comportamento": list(COMPORTAMENTOS),
                 "prop": PROPS_SUGERIDAS, "propriedade": PROPS_SUGERIDAS, "eixo": ["x", "y"], "modo": ["sobe", "desce"],
                 "estilo": ["fogo", "fumaca", "brilho", "chuva", "neve"]}


# =====================================================================
# O QUE TUDO ISSO FAZ NO JOGO (metodos do Jogo)
# =====================================================================
def _lado(o):
    """Para que lado o objeto esta olhando: 1 direita, -1 esquerda."""
    if abs(o.vx) > 1:
        return 1 if o.vx > 0 else -1
    return getattr(o, "olhar", -1 if o.d.get("espelhar") else 1)


def _centro(o):
    return o.x + o.w / 2, o.y + o.h / 2


def _dist(a, b):
    ax, ay = _centro(a)
    bx, by = _centro(b)
    return math.hypot(ax - bx, ay - by)


EVENTOS_EXTRA = {"depois", "parede", "teto", "saiu_tela", "entrou_tela", "mouse_entrou", "mouse_saiu", "mouse_solto",
                 "perto", "longe", "var_global", "moedas_valor"}
NOMES_COMP_EXTRA = {"Patrulhar", "Andar sozinho", "Fugir de", "Orbitar", "Mascote (segue de perto)", "Pular sozinho",
                    "Atirar", "Olhar para", "Girar para o mouse", "Seguir o mouse", "Coletável", "Cura ao tocar",
                    "Power-up ao tocar", "Porta para fase", "Plataforma que cai", "Quebrar ao bater por baixo",
                    "Regenerar vida", "Ímã", "Pulsar", "Limitar velocidade", "Cronômetro"}


class JogoExtras:
    # ----------------- acoes -----------------
    def mudar_prop(self, o, prop, op, valor):
        prop = texto(prop).strip()
        if not prop:
            return
        if prop in ("vida", "vida_max"):
            o.vars[prop] = limpar(aplicar_op(op, o.vars.get(prop, 0), valor))
            if prop == "vida_max" and "Vida" in o.comp:
                o.comp["Vida"]["vida"] = num_seguro(o.vars[prop], 1)
            return
        novo = aplicar_op(op, o.brasa_get(prop), valor)
        o.brasa_set(prop, novo)
        if prop == "pulos_extras":
            o.pulos_restantes = int(num_seguro(novo, 0))
        if prop == "velocidade":
            for nome, cfg in o.comp.items():
                if "velocidade" in cfg and nome != "Bala":
                    cfg["velocidade"] = num_seguro(novo, cfg["velocidade"])
        if prop == "dano" and "Dano" in o.comp:
            o.comp["Dano"]["quanto"] = num_seguro(novo, 1)

    def criar_botao(self, nome, txt, x, y, w, h, funcao="", grupo=""):
        acoes = [{"t": "Variável global", "p": {"var": "botao_clicado", "op": "=", "valor": f'"{nome}"'}}]
        if funcao:
            acoes.append({"t": "Chamar função", "p": {"nome": funcao}})
        d = nova_entidade("Botao", int(x), int(y), nome, texto=txt, na_tela=True, grupo=grupo,
                          eventos=[{"gatilho": "Ao clicar no objeto", "gp": {}, "condicoes": [], "acoes": acoes}])
        d["w"], d["h"] = int(max(20, w)), int(max(16, h))
        o = ObjJogo(d)
        self.novos.append(o)
        return o

    def atirar(self, o, tipo, vx, vy):
        try:
            tiro = self.lancar(tipo, o, vx, vy)
        except ErroBrasa as e:
            self.erro(o, e)
            return None
        cx, cy = _centro(o)
        if abs(vy) > abs(vx):
            tiro.x = cx - tiro.w / 2
            tiro.y = (o.y + o.h + 2) if vy > 0 else (o.y - tiro.h - 2)
            tiro.base_y = tiro.y
        if o is self.player:
            tiro.grupos.add("TirosDoPlayer")
            bonus = num_seguro(o.d.get("dano", 1), 1)
            if tiro.comp and "Dano" in tiro.comp and bonus != 1:
                tiro.comp["Dano"] = dict(tiro.comp["Dano"])
                tiro.comp["Dano"]["quanto"] = num_seguro(tiro.comp["Dano"].get("quanto", 1), 1) * bonus
        return tiro

    def acao_extra(self, dono, corpo, t, p, v, sim, alvos, esc):
        op = p.get("op", "=")
        outro = esc.get("outro") if esc.achar("outro") else None
        outro = outro if isinstance(outro, ObjJogo) else None
        if t == "Mudar velocidade" and corpo:
            self.mudar_prop(corpo, "velocidade", op, v("valor", "450"))
        elif t == "Mudar força do pulo" and corpo:
            self.mudar_prop(corpo, "pulo", op, v("valor", "900"))
        elif t == "Mudar pulos no ar" and corpo:
            self.mudar_prop(corpo, "pulos_extras", op, v("valor", "1"))
            corpo.pulos_restantes = int(num_seguro(corpo.d.get("pulos_extras", 0)))
        elif t == "Mudar aceleração" and corpo:
            self.mudar_prop(corpo, "aceleracao", op, v("valor", "3000"))
        elif t == "Mudar dano" and corpo:
            atual = corpo.comp["Dano"]["quanto"] if "Dano" in corpo.comp else num_seguro(corpo.d.get("dano", 1), 1)
            novo = aplicar_op(op, atual, v("valor", "2"))
            if "Dano" in corpo.comp:
                corpo.comp["Dano"]["quanto"] = num_seguro(novo, 1)
            corpo.d["dano"] = novo
        elif t == "Mudar vida (somar ou tirar)" and corpo:
            antes = num_seguro(corpo.vars.get("vida", 0), 0)
            depois = aplicar_op(op, antes, v("valor", "1"))
            maximo = num_seguro(corpo.vars.get("vida_max", 0), 0)
            if maximo > 0:
                depois = min(depois, maximo)
            corpo.vars["vida"] = limpar(depois)
            if depois > antes:
                self.disparar(corpo, "curado")
            elif num_seguro(depois, 0) <= 0 < antes:
                self.disparar(corpo, "sem_vida")
                if corpo is self.player:
                    corpo.vars["vida"] = corpo.vars.get("vida_max", 3)
                    self.respawn()
                else:
                    corpo.vivo = False
        elif t == "Mudar vida máxima" and corpo:
            corpo.vars["vida_max"] = limpar(aplicar_op(op, corpo.vars.get("vida_max", 0), v("valor", "5")))
        elif t == "Mudar escala da gravidade" and corpo:
            corpo.d["gravidade_escala"] = num(v("valor", "1"))
            corpo.movel = True
        elif t == "Mudar propriedade" and corpo:
            self.mudar_prop(corpo, p.get("prop", ""), op, v("valor"))
        elif t == "Mudar propriedade de outro objeto":
            valor = v("valor")
            for o in alvos():
                self.mudar_prop(o, p.get("prop", ""), op, valor)
        elif t == "Mudar parâmetro de comportamento" and corpo:
            cfg = corpo.comp.get(p.get("comportamento", ""))
            if cfg is not None:
                atual = cfg.get(p.get("parametro", ""))
                novo = v("valor")
                cfg[p.get("parametro", "")] = (num(novo) if isinstance(atual, (int, float)) and
                                               not isinstance(atual, bool) else
                                               (verdade(novo) if isinstance(atual, bool) else texto(novo)))
        elif t == "Poder temporário" and corpo:
            self.poder_temporario(corpo, p.get("prop", "velocidade"), num(v("multiplicar", "1.5")),
                                  num(v("seg", "5")))
        elif t == "Ficar invencível" and corpo:
            corpo.invencivel_t = corpo.piscar_t = float(num(v("seg", "2")))
        # movimento
        elif t == "Dash (impulso para frente)" and corpo:
            corpo.vx = _lado(corpo) * float(num(v("forca", "900")))
            corpo.vy = min(corpo.vy, 0.0)
            corpo.dash_t = 0.16
            corpo.movel = True
            corpo.squash_t = 0.12
        elif t == "Pular mesmo no ar" and corpo:
            corpo.vy = -float(num(v("forca", "700")))
            corpo.chao = False
            corpo.movel = True
            self.disparar(corpo, "pulo")
        elif t == "Virar para o outro lado" and corpo:
            corpo.olhar = -_lado(corpo)
            corpo.vx = -corpo.vx
            corpo.d["espelhar"] = corpo.olhar < 0
        elif t == "Olhar para objeto" and corpo:
            lista = [o for o in alvos() if o is not corpo]
            if lista:
                corpo.olhar = -1 if _centro(lista[0])[0] < _centro(corpo)[0] else 1
                corpo.d["espelhar"] = corpo.olhar < 0
        elif t == "Mover no ângulo" and corpo:
            ang = math.radians(num(v("angulo", "0")))
            vel = float(num(v("velocidade", "300")))
            corpo.vx, corpo.vy = math.cos(ang) * vel, math.sin(ang) * vel
            corpo.movel = True
        elif t == "Ir até o mouse" and corpo:
            mx, my = self.mouse_tela if corpo.na_tela else self.mouse_mundo
            cx, cy = _centro(corpo)
            d = math.hypot(mx - cx, my - cy) or 1
            vel = float(num(v("velocidade", "300")))
            corpo.vx = (mx - cx) / d * vel
            if not corpo.d.get("gravidade"):
                corpo.vy = (my - cy) / d * vel
            corpo.movel = True
        elif t == "Teleportar para o mouse" and corpo:
            mx, my = self.mouse_tela if corpo.na_tela else self.mouse_mundo
            corpo.x, corpo.y = mx - corpo.w / 2, my - corpo.h / 2
            corpo.base_y = corpo.y
        elif t == "Parar só na horizontal" and corpo:
            corpo.vx = 0.0
        elif t == "Parar só na vertical" and corpo:
            corpo.vy = 0.0
        elif t == "Limitar velocidade agora" and corpo:
            self.limitar(corpo, num(v("maximo", "400")))
        elif t == "Voltar para onde começou" and corpo:
            corpo.x, corpo.y = corpo.inicio_x, corpo.inicio_y
            corpo.base_y = corpo.y
            corpo.vx = corpo.vy = 0.0
        elif t == "Empurrar para longe de" and corpo:
            lista = [o for o in alvos() if o is not corpo]
            if lista:
                self.empurrar_de(corpo, lista[0], num(v("forca", "500")))
        elif t == "Puxar objetos para perto" and corpo:
            self.puxar(corpo, p.get("objeto", "Moeda"), num(v("raio", "200")), num(v("forca", "300")), 1 / 60)
        # combate
        elif t == "Atirar para frente" and corpo:
            self.atirar(corpo, p.get("tipo", "Moeda"), _lado(corpo) * num(v("velocidade", "650")), 0)
        elif t == "Atirar em direção a" and corpo:
            lista = [o for o in alvos() if o is not corpo]
            if lista:
                self.atirar_em(corpo, p.get("tipo", "Moeda"), _centro(lista[0]), num(v("velocidade", "500")))
        elif t == "Atirar para o mouse" and corpo:
            alvo = self.mouse_tela if corpo.na_tela else self.mouse_mundo
            self.atirar_em(corpo, p.get("tipo", "Moeda"), alvo, num(v("velocidade", "650")))
        elif t == "Explosão (dano em área)":
            self.explodir(corpo or dono, num(v("raio", "120")), v("qtd", "1"), p.get("em", "Inimigo"))
        elif t == "Dar dano em quem tocou" and outro:
            self.dano(outro, v("qtd", "1"))
        elif t == "Empurrar quem tocou" and outro and corpo:
            self.empurrar_de(outro, corpo, num(v("forca", "500")))
        elif t == "Curar objeto":
            qtd = v("qtd", "1")
            for o in alvos():
                self.curar(o, qtd)
        # criar
        elif t == "Clonar este objeto" and corpo:
            novo = ObjJogo(copy.deepcopy(corpo.d))
            novo.x, novo.y = corpo.x + num(v("dx", "50")), corpo.y + num(v("dy", "0"))
            novo.base_y = novo.y
            novo.inicio_x, novo.inicio_y = novo.x, novo.y
            self.novos.append(novo)
        elif t == "Criar em lugar aleatório":
            x1, x2 = sorted((num(v("x1", "0")), num(v("x2", "800"))))
            y1, y2 = sorted((num(v("y1", "0")), num(v("y2", "400"))))
            self.criar(p.get("tipo", "Moeda"), random.uniform(x1, x2), random.uniform(y1, y2))
        elif t == "Criar no mouse":
            mx, my = self.mouse_mundo
            o = self.criar(p.get("tipo", "Moeda"), mx, my)
            o.x, o.y = mx - o.w / 2, my - o.h / 2
            o.base_y = o.y
        # aparencia
        elif t == "Mudar camada":
            dono.d["camada"] = num(v("valor", "1"))
        elif t == "Mudar escala" and corpo:
            f = max(0.01, float(num(v("fator", "1.5"))))
            cx, cy = _centro(corpo)
            corpo.w, corpo.h = corpo.w * f, corpo.h * f
            corpo.x, corpo.y = cx - corpo.w / 2, cy - corpo.h / 2
            corpo.base_y = corpo.y
        elif t == "Mudar material":
            dono.d["material"] = p.get("material", "Plástico")
        elif t == "Mudar forma":
            dono.d["forma"] = p.get("forma", "Retângulo")
        elif t == "Cor aleatória":
            dono.d["cor"] = [random.randint(40, 255) for _ in range(3)]
        # jogo e tela
        elif t == "Câmera lenta":
            self.escala_tempo = max(0.05, min(4.0, float(num(v("velocidade", "0.4")))))
            self.escala_ate = self.tempo + float(num(v("seg", "1.5"))) * self.escala_tempo
        elif t == "Mudar moedas":
            self.moedas = int(num_seguro(aplicar_op(op, self.moedas, v("valor", "0")), 0))
        elif t == "Mostrar título na tela":
            self.banner = [self.interpolar(p.get("texto", ""), esc), float(num(v("seg", "2"))), 0.0]
        elif t == "Mudar zoom na hora":
            self.zoom = max(0.1, float(num(v("zoom", "1"))))
        elif t == "Câmera parar de seguir":
            self.cam_alvo = None
        elif t == "Criar botão na tela":
            self.criar_botao(p.get("nome", "") or "Botao", self.interpolar(p.get("texto", ""), esc), num(v("x", "300")),
                             num(v("y", "200")), num(v("largura", "200")), num(v("altura", "50")),
                             p.get("funcao", "").strip(), p.get("grupo", "").strip())
        elif t == "Criar texto na tela":
            d = nova_entidade("Texto", int(num(v("x", "300"))), int(num(v("y", "120"))), p.get("nome", "") or "Texto",
                              texto=self.interpolar(p.get("texto", ""), esc), na_tela=True,
                              grupo=p.get("grupo", "").strip())
            d["tamanho_fonte"] = int(max(8, min(160, num(v("tamanho", "32")))))
            self.novos.append(ObjJogo(d))
        elif t == "Apagar botões do grupo":
            g = p.get("grupo", "").strip()
            for o in self.objs + self.novos:
                if g and g in o.grupos:
                    o.vivo = False
        else:
            return False
        return True

    def limitar(self, o, maximo):
        vel = math.hypot(o.vx, o.vy)
        if maximo >= 0 and vel > maximo and vel > 0:
            o.vx, o.vy = o.vx / vel * maximo, o.vy / vel * maximo

    def empurrar_de(self, o, de, forca):
        lado = -1 if _centro(o)[0] < _centro(de)[0] else 1
        o.vx = lado * forca
        o.vy = -forca * 0.6
        o.movel = True

    def puxar(self, o, tipo, raio, forca, dt):
        cx, cy = _centro(o)
        for z in self.buscar(tipo):
            if z is o:
                continue
            zx, zy = _centro(z)
            d = math.hypot(cx - zx, cy - zy)
            if 1 < d <= raio:
                passo = min(d, forca * dt)
                z.x += (cx - zx) / d * passo
                z.y += (cy - zy) / d * passo
                z.base_y = z.y

    def atirar_em(self, o, tipo, alvo, vel):
        cx, cy = _centro(o)
        dx, dy = alvo[0] - cx, alvo[1] - cy
        d = math.hypot(dx, dy) or 1
        tiro = self.atirar(o, tipo, dx / d * vel, dy / d * vel)
        if tiro is not None:
            tiro.x, tiro.y = cx - tiro.w / 2 + dx / d * (o.w / 2 + 4), cy - tiro.h / 2 + dy / d * (o.h / 2 + 4)
            tiro.base_y = tiro.y
        return tiro

    def explodir(self, o, raio, qtd, em):
        cx, cy = _centro(o) if isinstance(o, ObjJogo) else (self.cam[0], self.cam[1])
        self.soltar_particulas(cx, cy, [255, 160, 40], 40)
        self.soltar_particulas(cx, cy, [255, 240, 140], 20)
        self.tremer(9, 0.35)
        for z in self.buscar(em):
            if z is not o and math.hypot(_centro(z)[0] - cx, _centro(z)[1] - cy) <= raio:
                if self.dano(z, qtd) and z.vivo:
                    lado = -1 if _centro(z)[0] < cx else 1
                    z.vx, z.vy = lado * 420, -380
                    z.movel = True

    def poder_temporario(self, o, prop, mult, seg):
        prop = texto(prop).strip() or "velocidade"
        try:
            antes = num(o.brasa_get(prop))
        except ErroBrasa:
            return
        self.mudar_prop(o, prop, "*=", mult)
        o.flash_t = o.flash_dur = 0.2
        self.texto_flutuante("PODER!", o.x + o.w / 2, o.y - 10, (255, 230, 80))
        self.agendar(seg, self.cena_dono, lambda: self.mudar_prop(o, prop, "=", antes) if o.vivo else None)

    # ----------------- condicoes -----------------
    def testar_extra(self, dono, corpo, t, p, val, op, esc):
        if t == "Velocidade X":
            return bool(corpo) and comparar(corpo.vx, op, val("valor"))
        if t == "Velocidade Y":
            return bool(corpo) and comparar(corpo.vy, op, val("valor"))
        if t == "Está se movendo":
            return bool(corpo) and (abs(corpo.vx) > 5 or abs(corpo.vy) > 5)
        if t == "Está parado":
            return bool(corpo) and abs(corpo.vx) <= 5 and abs(corpo.vy) <= 5
        if t == "Indo para a direita":
            return bool(corpo) and corpo.vx > 5
        if t == "Indo para a esquerda":
            return bool(corpo) and corpo.vx < -5
        if t == "Subindo":
            return bool(corpo) and corpo.vy < -5
        if t == "Caindo":
            return bool(corpo) and not corpo.chao and corpo.vy > 5
        if t == "Encostado na parede":
            return bool(corpo) and bool(getattr(corpo, "parede", 0))
        if t == "Bateu a cabeça":
            return bool(corpo) and bool(getattr(corpo, "bateu_teto", False))
        if t == "Em cima de":
            return bool(corpo and corpo.chao and corpo.apoio is not None and self.combina(p.get("alvo", ""),
                                                                                       corpo.apoio))
        if t == "Em cima de material":
            return bool(corpo and corpo.chao and corpo.apoio is not None and
                        corpo.apoio.d.get("material") == p.get("material", ""))
        if t == "Pulos no ar restantes":
            return bool(corpo) and comparar(corpo.pulos_restantes, op, val("valor"))
        if t == "Está invencível":
            return bool(corpo) and corpo.invencivel_t > 0
        if t == "Vida máxima":
            return bool(corpo) and comparar(corpo.vars.get("vida_max", 0), op, val("valor"))
        if t == "Vida em %":
            if not corpo:
                return False
            maximo = num_seguro(corpo.vars.get("vida_max", 0), 0) or 1
            return comparar(num_seguro(corpo.vars.get("vida", 0), 0) * 100 / maximo, op, val("valor"))
        if t == "Propriedade":
            return bool(corpo) and comparar(corpo.brasa_get(texto(p.get("prop", "")).strip()), op, val("valor"))
        if t == "Propriedade de outro objeto":
            alvos = self.buscar(p.get("objeto", ""))
            return bool(alvos) and comparar(alvos[0].brasa_get(texto(p.get("prop", "")).strip()), op, val("valor"))
        if t == "Olhando para a esquerda":
            return bool(corpo) and _lado(corpo) < 0
        if t == "Aparece na tela":
            return bool(corpo) and self.na_vista(corpo)
        if t == "Fora da tela":
            return bool(corpo) and not self.na_vista(corpo)
        if t == "Nome é":
            return bool(corpo) and corpo.d.get("nome") == p.get("nome", "")
        if t == "Tipo é":
            return bool(corpo) and corpo.tipo == p.get("tipo", "")
        if t == "Tecla acabou de ser apertada":
            return self.apertou(p.get("tecla", ""))
        if t == "Itens no inventário":
            return comparar(len(self.inventario), op, val("valor"))
        if t == "Player perto":
            pl = self.player
            return bool(corpo and pl and pl.vivo and pl is not corpo and _dist(corpo, pl) <= num(val("distancia")))
        if t == "Mouse perto":
            if not corpo:
                return False
            mx, my = self.mouse_tela if corpo.na_tela else self.mouse_mundo
            cx, cy = _centro(corpo)
            return math.hypot(mx - cx, my - cy) <= num(val("distancia"))
        if t == "Número aleatório":
            a, b = int(num(val("de", "1"))), int(num(val("ate", "10")))
            return comparar(random.randint(min(a, b), max(a, b)), op, val("valor"))
        return None

    def na_vista(self, o):
        if o.na_tela:
            return True
        vw, vh = self.area.w / self.zoom, self.area.h / self.zoom
        return (o.x + o.w > self.cam[0] and o.x < self.cam[0] + vw and
                o.y + o.h > self.cam[1] and o.y < self.cam[1] + vh)

    # ----------------- comportamentos -----------------
    def comportamentos_extra(self, o, c, liga, dt):
        if c.keys().isdisjoint(NOMES_COMP_EXTRA):
            return
        p = self.player if (self.player and self.player.vivo) else None
        if liga("Patrulhar"):
            b = c["Patrulhar"]
            vel, dist = abs(b["velocidade"]), b["distancia"]
            if str(b["eixo"]).lower().startswith("y"):
                if o.y > o.inicio_y + dist:
                    o.vy = -vel
                elif o.y < o.inicio_y:
                    o.vy = vel
                elif not o.vy:
                    o.vy = vel
            else:
                if o.x > o.inicio_x + dist:
                    o.vx = -vel
                elif o.x < o.inicio_x:
                    o.vx = vel
                elif not o.vx:
                    o.vx = vel
                if o.d.get("imagem") or o.d.get("animacao"):
                    o.d["espelhar"] = o.vx < 0
            o.movel = True
        if liga("Andar sozinho"):
            b = c["Andar sozinho"]
            if not hasattr(o, "olhar"):
                o.olhar = -1 if o.d.get("espelhar") else 1
            if getattr(o, "parede", 0) and b["virar_na_parede"]:
                o.olhar = -o.parede
            o.vx = o.olhar * abs(b["velocidade"])
            if o.d.get("imagem") or o.d.get("animacao"):
                o.d["espelhar"] = o.olhar < 0
            o.movel = True
        if liga("Fugir de"):
            b = c["Fugir de"]
            alvos = [z for z in self.buscar(b["alvo"]) if z is not o]
            if alvos:
                z = min(alvos, key=lambda q: _dist(o, q))
                d = _dist(o, z)
                if d <= b["alcance"]:
                    dx, dy = _centro(o)[0] - _centro(z)[0], _centro(o)[1] - _centro(z)[1]
                    n = math.hypot(dx, dy) or 1
                    o.vx = dx / n * b["velocidade"]
                    if not o.d.get("gravidade"):
                        o.vy = dy / n * b["velocidade"]
                elif not o.d.get("gravidade"):
                    o.vx = o.vy = 0.0
                o.movel = True
        if liga("Orbitar"):
            b = c["Orbitar"]
            alvos = [z for z in self.buscar(b["alvo"]) if z is not o] if str(b["alvo"]).strip() else []
            centro = _centro(alvos[0]) if alvos else (o.inicio_x + o.w / 2, o.inicio_y + o.h / 2)
            o.orb_ang = getattr(o, "orb_ang", 0.0) + dt * math.tau * b["voltas_por_seg"]
            o.x = centro[0] + math.cos(o.orb_ang) * b["raio"] - o.w / 2
            o.y = centro[1] + math.sin(o.orb_ang) * b["raio"] - o.h / 2
            o.base_y = o.y
            o.vx = o.vy = 0.0
        if liga("Mascote (segue de perto)"):
            b = c["Mascote (segue de perto)"]
            alvos = [z for z in self.buscar(b["alvo"]) if z is not o]
            if alvos:
                z = alvos[0]
                zx, zy = _centro(z)
                alvo_x = zx - _lado(z) * b["distancia"] - o.w / 2
                alvo_y = zy - z.h / 2 - o.h / 2 - 6
                k = min(1.0, max(0.1, b["suavidade"]) * dt)
                o.x += (alvo_x - o.x) * k
                o.y += (alvo_y - o.y) * k
                o.base_y = o.y
                o.d["espelhar"] = _lado(z) < 0
        if liga("Pular sozinho"):
            b = c["Pular sozinho"]
            if self.contar_timer(o, "__pular", b["a_cada_seg"], dt) and o.chao:
                o.vy = -abs(b["forca"])
                o.chao = False
                o.movel = True
                self.disparar(o, "pulo")
        if liga("Atirar"):
            b = c["Atirar"]
            if self.contar_timer(o, "__atirar", b["a_cada_seg"], dt):
                alvo_nome = str(b["alvo"]).strip()
                if alvo_nome:
                    alvos = [z for z in self.buscar(alvo_nome) if z is not o and _dist(o, z) <= b["alcance"]]
                    if alvos:
                        self.atirar_em(o, b["tipo"], _centro(min(alvos, key=lambda q: _dist(o, q))), b["velocidade"])
                else:
                    self.atirar(o, b["tipo"], _lado(o) * b["velocidade"], 0)
        if liga("Olhar para"):
            alvos = [z for z in self.buscar(c["Olhar para"]["alvo"]) if z is not o]
            if alvos:
                o.olhar = -1 if _centro(alvos[0])[0] < _centro(o)[0] else 1
                o.d["espelhar"] = o.olhar < 0
        if liga("Girar para o mouse"):
            mx, my = self.mouse_tela if o.na_tela else self.mouse_mundo
            cx, cy = _centro(o)
            o.d["rotacao"] = -math.degrees(math.atan2(my - cy, mx - cx))
        if liga("Seguir o mouse"):
            mx, my = self.mouse_tela if o.na_tela else self.mouse_mundo
            vel = c["Seguir o mouse"]["velocidade"]
            if vel <= 0:
                o.x, o.y = mx - o.w / 2, my - o.h / 2
                o.base_y = o.y
            else:
                cx, cy = _centro(o)
                d = math.hypot(mx - cx, my - cy)
                if d > 2:
                    passo = min(d, vel * dt)
                    o.x += (mx - cx) / d * passo
                    o.y += (my - cy) / d * passo
                    o.base_y = o.y
        if liga("Coletável") and p and sobrepoe(p, o):
            b = c["Coletável"]
            nome = str(b["variavel"]).strip() or "pontos"
            self.globais.d[nome] = limpar(num_seguro(self.globais.d.get(nome, 0), 0) + b["valor"])
            self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, o.d.get("cor", [255, 220, 80]), 12)
            self.texto_flutuante(f"+{texto(limpar(b['valor']))}", o.x + o.w / 2, o.y - 6, (255, 230, 90))
            o.vivo = False
            return
        if liga("Cura ao tocar"):
            b = c["Cura ao tocar"]
            for z in self.buscar(b["em"]):
                if z is not o and z.vivo and sobrepoe(z, o):
                    self.curar(z, b["quanto"])
                    self.texto_flutuante(f"+{texto(limpar(b['quanto']))}", z.x + z.w / 2, z.y - 8, (120, 255, 140))
                    if b["some"]:
                        o.vivo = False
                        return
        if liga("Power-up ao tocar"):
            b = c["Power-up ao tocar"]
            for z in self.buscar(b["em"]):
                if z is not o and z.vivo and sobrepoe(z, o):
                    self.poder_temporario(z, b["propriedade"], b["multiplicar"], b["seg"])
                    self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, [255, 230, 80], 16)
                    o.vivo = False
                    return
        if liga("Porta para fase") and p and sobrepoe(p, o):
            b = c["Porta para fase"]
            tecla = str(b["tecla"]).strip()
            if not tecla or self.apertou(tecla):
                fase = str(b["fase"]).strip()
                if fase in self.dados["fases"]:
                    self.pedir_fase = fase
                elif not getattr(o, "avisou_porta", False):
                    o.avisou_porta = True
                    self.erro(o, ErroBrasa(f"Porta para fase: a fase '{fase}' não existe"))
        if liga("Plataforma que cai"):
            b = c["Plataforma que cai"]
            pisado = any(z.apoio is o and z.chao for z in self.objs if z is not o and z.vivo and z.movel)
            if pisado or getattr(o, "cair_t", 0) > 0:
                o.cair_t = getattr(o, "cair_t", 0.0) + dt
                if o.cair_t >= b["espera"] and not o.d.get("gravidade"):
                    o.d["gravidade"] = True
                    o.movel = True
                elif o.cair_t < b["espera"]:
                    o.x = o.inicio_x + random.uniform(-1.5, 1.5)   # treme antes de cair
                if o.cair_t > b["espera"] + 3:
                    o.vivo = False
        if liga("Quebrar ao bater por baixo") and p and getattr(p, "teto_obj", None) is o:
            solta = str(c["Quebrar ao bater por baixo"]["solta"]).strip()
            self.soltar_particulas(o.x + o.w / 2, o.y + o.h / 2, o.d.get("cor", [180, 120, 70]), 20)
            self.tremer(4, 0.15)
            o.vivo = False
            if solta:
                try:
                    novo = self.criar(solta, 0, 0)
                    novo.x, novo.y = o.x + o.w / 2 - novo.w / 2, o.y - novo.h - 2
                    novo.base_y = novo.y
                except ErroBrasa as e:
                    self.erro(o, e)
            return
        if liga("Regenerar vida") and self.contar_timer(o, "__regen", c["Regenerar vida"]["a_cada_seg"], dt):
            maximo = num_seguro(o.vars.get("vida_max", 0), 0)
            if not maximo or num_seguro(o.vars.get("vida", 0), 0) < maximo:
                self.curar(o, c["Regenerar vida"]["quanto"])
        if liga("Ímã"):
            b = c["Ímã"]
            self.puxar(o, b["tipo"], b["raio"], b["forca"], dt)
        if liga("Pulsar"):
            b = c["Pulsar"]
            if not hasattr(o, "pulsar_base"):
                o.pulsar_base = (o.w, o.h, o.x + o.w / 2, o.y + o.h / 2)
            bw, bh, cx, cy = o.pulsar_base
            if o.vx or o.vy:
                cx, cy = o.x + o.w / 2, o.y + o.h / 2
                o.pulsar_base = (bw, bh, cx, cy)
            f = 1 + math.sin(self.tempo * math.tau * b["vezes_por_seg"]) * b["escala"]
            o.w, o.h = max(1.0, bw * f), max(1.0, bh * f)
            o.x, o.y = cx - o.w / 2, cy - o.h / 2
            o.base_y = o.y
        if liga("Limitar velocidade"):
            self.limitar(o, c["Limitar velocidade"]["maximo"])
        if liga("Cronômetro"):
            b = c["Cronômetro"]
            nome = str(b["variavel"]).strip() or "tempo"
            if not getattr(o, "crono_ok", False):
                o.crono_ok = True
                self.globais.d[nome] = limpar(b["inicio"])
            atual = num_seguro(self.globais.d.get(nome, 0), 0)
            if str(b["modo"]).lower().startswith("d"):
                self.globais.d[nome] = limpar(max(0.0, atual - dt)) if atual > 0 else 0
            else:
                self.globais.d[nome] = limpar(atual + dt)

    def morte_extra(self, o):
        """Chamado quando um objeto e destruido."""
        if not getattr(o, "comp", None):
            return
        if o.tem("Explodir ao morrer"):
            b = o.comp["Explodir ao morrer"]
            self.explodir(o, b["raio"], b["dano"], b["em"])
        if o.tem("Reaparecer"):
            copia = copy.deepcopy(o.d)
            copia["x"], copia["y"] = o.inicio_x, o.inicio_y

            def voltar(copia=copia):
                novo = ObjJogo(copia)
                self.novos.append(novo)
            self.agendar(o.comp["Reaparecer"]["seg"], self.cena_dono, voltar)

    # ----------------- eventos novos -----------------
    def disparar_com(self, dono, evento, teste):
        """Como disparar(), mas cada QUANDO tem o seu valor (distancia, segundos...) testado por teste(valor, chave)."""
        if evento not in self.ouvidos(dono):
            return
        for i, (ev, arg, corpo, esc) in enumerate(list(dono.handlers)):
            if ev == evento and teste(arg, ("s", i)):
                local = Escopo(esc, {"outro": None})
                self.rodar(dono, lambda c=corpo, l=local: self.interp.executar(c, l))
        chave_param = {"depois": "seg", "perto": "distancia", "longe": "distancia", "var_global": "var",
                       "moedas_valor": "valor"}.get(evento)
        for i, ev in enumerate(dono.d.get("eventos", [])):
            if GATILHO_EVENTO.get(ev.get("gatilho")) != evento or ev.get("ativo") is False:
                continue
            bruto = ev.get("gp", {}).get(chave_param, "0")
            try:
                arg = bruto if evento == "var_global" else self.valor(bruto, dono.escopo)
            except ErroBrasa as e:
                self.erro(dono, e)
                continue
            if teste(arg, ("v", i)):
                self.rodar_visual(dono, ev, None)

    def eventos_extra(self, dt, p):
        mouse_agora = self.mouse_seg
        solto = getattr(self, "mouse_antes", False) and not mouse_agora
        self.mouse_antes = mouse_agora
        cache = getattr(self, "_cache_ev_extra", None)
        self._quadro_extra = getattr(self, "_quadro_extra", 0) + 1
        if cache is None or cache[0] != len(self.donos) or self._quadro_extra % 30 == 0:
            cache = (len(self.donos), [d for d in self.donos if not self.ouvidos(d).isdisjoint(EVENTOS_EXTRA)])
            self._cache_ev_extra = cache
        for d in list(cache[1]):
            if not d.vivo:
                continue
            ouve = self.ouvidos(d)
            if not ouve:
                continue
            corpo = d if isinstance(d, ObjJogo) else None
            if "depois" in ouve:
                def depois(arg, chave, d=d):
                    k = ("depois", chave)
                    if d.timers.get(k) == "feito":
                        return False
                    t = d.timers.get(k, 0.0) + dt
                    if t >= num_seguro(arg, 0):
                        d.timers[k] = "feito"
                        return True
                    d.timers[k] = t
                    return False
                self.disparar_com(d, "depois", depois)
            if corpo is not None:
                if "parede" in ouve:
                    agora_parede = getattr(corpo, "parede", 0)
                    if agora_parede and not getattr(corpo, "parede_antes", 0):
                        self.disparar(corpo, "parede")
                    corpo.parede_antes = agora_parede
                if "teto" in ouve and getattr(corpo, "bateu_teto", False):
                    self.disparar(corpo, "teto")
                if "saiu_tela" in ouve or "entrou_tela" in ouve:
                    agora = self.na_vista(corpo)
                    antes = getattr(corpo, "estava_na_vista", None)
                    corpo.estava_na_vista = agora
                    if antes is not None and agora != antes:
                        self.disparar(corpo, "entrou_tela" if agora else "saiu_tela")
                if "mouse_entrou" in ouve or "mouse_saiu" in ouve:
                    agora = self.mouse_em_cima(corpo)
                    antes = getattr(corpo, "mouse_estava", False)
                    corpo.mouse_estava = agora
                    if agora != antes:
                        self.disparar(corpo, "mouse_entrou" if agora else "mouse_saiu")
                if ("perto" in ouve or "longe" in ouve) and p is not None and p is not corpo:
                    dist = _dist(corpo, p)
                    for evento in ("perto", "longe"):
                        if evento not in ouve:
                            continue

                        def teste(arg, chave, evento=evento, dist=dist, corpo=corpo):
                            k = (evento, chave)
                            dentro = dist <= num_seguro(arg, 150)
                            antes = corpo.timers.get(k)
                            corpo.timers[k] = dentro
                            if antes is None:
                                return evento == "perto" and dentro
                            return (dentro and not antes) if evento == "perto" else (antes and not dentro)
                        self.disparar_com(corpo, evento, teste)
            if "mouse_solto" in ouve and solto:
                self.disparar(d, "mouse_solto")
            if "var_global" in ouve:
                def mudou(arg, chave, d=d):
                    k = ("var_global", chave)
                    atual = self.globais.d.get(texto(arg).strip())
                    antes = d.timers.get(k, "__nada__")
                    d.timers[k] = atual
                    return antes != "__nada__" and antes != atual
                self.disparar_com(d, "var_global", mudou)
            if "moedas_valor" in ouve:
                def chegou(arg, chave, d=d):
                    k = ("moedas_valor", chave)
                    agora = self.moedas >= num_seguro(arg, 0)
                    antes = d.timers.get(k, False)
                    d.timers[k] = agora
                    return agora and not antes
                self.disparar_com(d, "moedas_valor", chegou)
        self.juntar_novos()

    def tempo_do_jogo(self, dt):
        """Camera lenta: devolve o dt ajustado."""
        escala = getattr(self, "escala_tempo", 1.0)
        if escala != 1.0 and self.tempo >= getattr(self, "escala_ate", 0):
            self.escala_tempo = escala = 1.0
        return dt * escala

    def controles_extra(self, p, dt, teclas, apertadas, direcao):
        """Dash, pulo na parede e tiro do Player (propriedades novas)."""
        if direcao:
            p.olhar = 1 if direcao > 0 else -1
        if getattr(p, "dash_t", 0) > 0:
            p.dash_t -= dt
        if p.d.get("dash") and getattr(p, "dash_cd", 0) <= 0 and (apertadas & {pygame.K_LSHIFT, pygame.K_RSHIFT}):
            forca_d = float(num_seguro(p.d.get("forca_dash", 900), 900))
            if getattr(self, "topdown", False):
                vx_, vy_ = olhar_de(p)
                p.vx, p.vy = vx_ * forca_d, vy_ * forca_d
            else:
                p.vx = _lado(p) * forca_d
                p.vy = min(p.vy, 0.0) * 0.3
            p.dash_t, p.dash_cd = 0.16, 0.45
            p.squash_t = 0.12
            self.soltar_particulas(p.x + p.w / 2, p.y + p.h / 2, [200, 220, 255], 10)
        p.dash_cd = max(0.0, getattr(p, "dash_cd", 0) - dt)
        if p.d.get("pulo_parede") and not p.chao and getattr(p, "parede", 0) and \
                apertadas & set(acao_jogo("pular")):
            p.vy = -float(num_seguro(p.d.get("pulo", 720), 720))
            p.vx = -p.parede * float(num_seguro(p.d.get("velocidade", 320), 320)) * 1.2
            p.olhar = -p.parede
            p.dash_t = 0.12
            self.disparar(p, "pulo")
        tipo_tiro = str(p.d.get("tiro", "") or "").strip()
        if tipo_tiro and self.apertou(str(p.d.get("tecla_tiro", "f") or "f")):
            self.tiro_para_onde_olha(p, tipo_tiro, float(num_seguro(p.d.get("vel_tiro", 650), 650)))

    def desenhar_extra(self, tela, a):
        b = getattr(self, "banner", None)
        if not b:
            return
        texto_, dur, t = b
        b[2] = t + 1 / 60
        if b[2] >= dur:
            self.banner = None
            return
        alpha = int(255 * min(1.0, b[2] / 0.25, (dur - b[2]) / 0.4))
        img = fonte(min(64, max(28, a.h // 9)), True).render(texto_, True, (255, 255, 255))
        sombra = fonte(min(64, max(28, a.h // 9)), True).render(texto_, True, (0, 0, 0))
        img.set_alpha(alpha)
        sombra.set_alpha(alpha // 2)
        x, y = a.centerx - img.get_width() // 2, a.y + a.h // 3 - img.get_height() // 2
        tela.blit(sombra, (x + 3, y + 3))
        tela.blit(img, (x, y))
