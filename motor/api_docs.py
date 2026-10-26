# Minha Engine - api_docs.py
# documentação das funções (aba API)
# Este arquivo é uma PARTE da engine: não rode ele sozinho, rode o minha_engine.py.

# ---------------------------------------------------------------------
# Documentacao da API (aparece na aba API)
# ---------------------------------------------------------------------
API_FUNCOES = [
    ("dizer(texto, segundos)", "Mostra um balão de fala em cima do objeto.", 'dizer("Oi!", 2)'),
    ("escrever(valor, ...)", "Escreve uma mensagem no console do jogo (canto da tela).", 'escrever("x = " + eu.x)'),
    ("destruir(objeto)", "Destrói um objeto. Sem nada destrói o próprio objeto. Aceita nome ou lista.",
     'destruir(achar("Bloco1"))'),
    ("destruir_todos(nome_ou_tipo)", "Destrói todos os objetos com esse nome ou tipo.", 'destruir_todos("Inimigo")'),
    ("criar(nome_ou_tipo, x, y)", "Cria um objeto. Pode ser um tipo, um modelo/variante ou o nome de um objeto da cena "
     "(copia ele com eventos e script). Retorna o objeto.", 'var m = criar("Moeda", eu.x, eu.y - 50)'),
    ("lancar(tipo, vx, vy)", "Cria um objeto saindo do objeto atual com velocidade (tiro).", 'lancar("Moeda", 600, 0)'),
    ("achar(nome_ou_tipo)", "Retorna o primeiro objeto com esse nome ou tipo (ou nulo).", 'var b = achar("Bloco1")'),
    ("achar_todos(nome_ou_tipo)", "Retorna uma lista com todos os objetos.", 'para i de 0 ate tamanho(achar_todos("Inimigo")) - 1:\n    escrever(i)'),
    ("chamar(nome)", "Chama uma função pelo nome (do script ou visual).", 'chamar("minha_funcao")'),
    ("depois(segundos, funcao)", "Espera e depois chama a função.", 'depois(2, minha_funcao)'),
    ("tecla(nome)", "Verdadeiro enquanto a tecla está segurada. Nomes: letras, espaco, enter, esquerda, direita, "
     "cima, baixo, shift, ctrl.", 'se tecla("d"):\n    eu.vx = 200'),
    ("apertou(nome)", "Verdadeiro só no frame em que a tecla foi apertada.", 'se apertou("e"):\n    dizer("E!", 1)'),
    ("soltou(nome)", "Verdadeiro só no frame em que a tecla foi solta.", 'se soltou("e"):\n    dizer("soltei", 1)'),
    ("mouse_x() / mouse_y()", "Posição do mouse no mundo do jogo.", 'eu.x = mouse_x()'),
    ("mouse_segurado()", "Verdadeiro enquanto o botão esquerdo está apertado.", 'se mouse_segurado():\n    eu.vy = -300'),
    ("aleatorio(a, b)", "Número aleatório entre a e b (inteiro se a e b forem inteiros).", 'var dado = aleatorio(1, 6)'),
    ("distancia(a, b)", "Distância entre os centros de dois objetos.", 'se distancia(eu, player) < 100:\n    dizer("Perto!", 1)'),
    ("dar_item(nome) / remover_item(nome)", "Coloca/tira um item do inventário.", 'dar_item("chave")'),
    ("tem_item(nome)", "Verdadeiro se o inventário tem o item.", 'se tem_item("chave"):\n    destruir(achar("Porta"))'),
    ("inventario()", "Lista com os itens do inventário.", 'escrever(inventario())'),
    ("moedas() / somar_moedas(n)", "Lê / soma moedas.", 'somar_moedas(5)'),
    ("vencer() / perder()", "Termina a fase com vitória ou derrota.", 'se moedas() >= 10:\n    vencer()'),
    ("reiniciar()", "Recomeça a fase do zero.", 'reiniciar()'),
    ("voltar_inicio()", "Leva o player para o início/checkpoint.", 'voltar_inicio()'),
    ("controles(ligado)", "Liga/desliga o controle do player.", 'controles(falso)'),
    ("hud(id, texto, x, y) / apagar_hud(id)", "Texto fixo na tela.", 'hud("vida", "Vida: " + player.vida, 12, 40)'),
    ("tremer(forca, segundos)", "Treme a câmera.", 'tremer(10, 0.4)'),
    ("camera(objeto)", "A câmera passa a seguir esse objeto.", 'camera(achar("Chefe"))'),
    ("fundo(r, g, b) / gravidade(valor)", "Muda a cor do fundo / a gravidade da cena.", 'gravidade(600)'),
    ("tela_cheia(ligado)", "Liga/desliga tela cheia.", 'tela_cheia(verdadeiro)'),
    ("ir_fase(nome) / proxima_fase()", "Vai para outra fase. Moedas, itens e variáveis globais continuam.",
     'ir_fase("Fase 2")'),
    ("fase_atual()", "Nome da fase que está rodando.", 'escrever(fase_atual())'),
    ("tocar_som(arquivo, volume)", "Toca um som da pasta 'sons' (wav, ogg, mp3).", 'tocar_som("pulo.wav")'),
    ("tocar_musica(arquivo, volume) / parar_musica()", "Música de fundo que repete.", 'tocar_musica("tema.ogg", 0.5)'),
    ("particulas(x, y, cor, qtd)", "Explosão de partículas.", 'particulas(eu.x, eu.y, [255, 100, 0], 30)'),
    ("animar(obj, prop, valor, seg)", "Muda uma propriedade aos poucos (x, y, w, h, opacidade, rotacao...).",
     'animar(eu, "y", eu.y - 100, 0.5)'),
    ("piscar(obj, seg)", "Faz o objeto piscar (bom pra invencibilidade).", 'piscar(player, 1.5)'),
    ("pausar()", "Pausa/despausa o jogo (o jogador também pausa com P).", 'pausar()'),
    ("salvar_jogo() / carregar_jogo()", "Salva/carrega fase, moedas, itens e globais em savegame.json.",
     'salvar_jogo()'),
    ("dano(obj, qtd) / curar(obj, qtd)", "Tira/dá vida (o objeto precisa do comportamento Vida ou de um valor vida).",
     'dano(player, 1)'),
    ("congelar(seg)", "Para o jogo por um instante no impacto (hit stop). 0.05 a 0.1 fica ótimo.", 'congelar(0.06)'),
    ("flash(obj, seg)", "Pisca o objeto de branco (quando leva dano).", 'flash(eu, 0.12)'),
    ("esticar(obj)", "Efeito de amassar e esticar (squash & stretch).", 'esticar(player)'),
    ("zoom(valor, seg)", "Zoom da câmera (1 = normal, 2 = perto, 0.5 = longe).", 'zoom(1.5, 0.5)'),
    ("linha_de_visao(a, b)", "Verdadeiro se nada sólido está entre os dois objetos.",
     'se linha_de_visao(eu, player):\n    dizer("Te vi!", 1)'),
    ("comportamento(obj, nome, ligado)", "Liga/desliga um comportamento.", 'comportamento(eu, "Bala", falso)'),
    ("no_grupo(obj, grupo)", "Verdadeiro se o objeto está no grupo.", 'se no_grupo(outro, "Inimigos"):\n    dano(outro, 1)'),
    ("fps()", "Quadros por segundo do jogo (F2 mostra na tela).", 'escrever(fps())'),
    ("dialogo(texto, nome)", "Abre a caixa de diálogo. Separe as falas com |. O jogo espera o jogador ler (E avança).",
     'dialogo("Oi!|Você achou a chave?", "Rei")'),
    ("dialogo_aberto()", "Verdadeiro enquanto a caixa de diálogo está aberta.", 'se nao dialogo_aberto():\n    eu.vx = 100'),
    ("texto_flutuante(texto, x, y, cor)", "Texto que sobe e some (dano, pontos, combos).",
     'texto_flutuante("+10", eu.x, eu.y, [255, 230, 80])'),
    ("escuridao(valor)", "Escuridão da cena de 0 (claro) a 255 (preto). Use o comportamento Luz para iluminar.",
     'escuridao(220)'),
    ("para cada x em lista:", "Repete para cada item de uma lista (ou letra de um texto).",
     'para cada ini em achar_todos("Inimigo"):\n    dano(ini, 1)'),
    ("x em lista", "Verdadeiro se o item está na lista (ou o pedaço está no texto).",
     'se "chave" em inventario():\n    vencer()'),
    ("maiusculo / minusculo / substituir", "Funções de texto.", 'escrever(maiusculo("oi"))'),
    ("dividir(texto, sep) / juntar(lista, sep)", "Quebra texto em lista e junta de volta.",
     'var partes = dividir("a,b,c", ",")'),
    ("contem / posicao / remover / ordenar / inverter", "Funções de lista.", 'var l = ordenar([3, 1, 2])'),
    ("sortear(lista) / embaralhar(lista)", "Item aleatório / lista misturada.",
     'dizer(sortear(["Oi", "Olá", "E aí"]), 1)'),
    ("lista_de(a, b)", "Lista com os números de a até b.", 'para cada n em lista_de(1, 5):\n    escrever(n)'),
    ("piso / teto / seno / cosseno", "Matemática (ângulos em graus).", 'eu.y = 200 + seno(tempo * 90) * 50'),
    ("angulo_ate(a, b)", "Ângulo (graus) de a até b.", 'eu.rotacao = angulo_ate(eu, player)'),
    ("mirar(obj, alvo, velocidade)", "Faz o objeto ir na direção do alvo (tiros que miram no player).",
     'var tiro = lancar("Moeda", 0, 0)\nmirar(tiro, player, 400)'),
    ("texto(v) / numero(v)", "Converte para texto / número.", 'var n = numero("42")'),
    ("abs, min, max, raiz, arredondar(v, casas)", "Funções de matemática.", 'var m = max(1, 5, 3)'),
    ("tamanho(lista) / adicionar(lista, v)", "Listas.", 'var l = []\nadicionar(l, 5)'),
]
API_PROPS = [
    ("eu", "O próprio objeto do script."), ("outro", "Quem tocou/foi tocado (eventos tocar)."),
    ("player", "O objeto Player."), ("global.nome", "Variável global (qualquer nome)."),
    ("tempo / dt", "Segundos desde o início / duração do frame."),
    ("obj.x obj.y", "Posição."), ("obj.vx obj.vy", "Velocidade."), ("obj.w obj.h", "Tamanho."),
    ("obj.cor", "Cor [r, g, b]."), ("obj.imagem", "Arquivo de imagem (pasta imagens)."),
    ("obj.texto", "Texto (Texto e Botão)."), ("obj.opacidade", "0 = invisível, 255 = normal."),
    ("obj.rotacao", "Rotação em graus."), ("obj.espelhar", "Vira a imagem na horizontal."),
    ("obj.camada", "Ordem de desenho (maior fica na frente)."), ("obj.visivel", "Aparece ou não."),
    ("obj.solido obj.gravidade", "Física do objeto."),
    ("obj.animacao obj.fps_anim", "Animação: imagens separadas por vírgula (andar1.png, andar2.png) e velocidade."),
    ("obj.grupo", "Grupo do objeto. Onde pede nome ou tipo, o grupo também vale (ex: Inimigos)."),
    ("obj.vida", "Vida atual (comportamento Vida)."), ("obj.no_chao", "Está em cima de algo (só leitura)."),
    ("obj.nome obj.tipo obj.vivo", "Informações do objeto."),
    ("obj.QUALQUER", "Os VALORES do objeto (painel direito) e variáveis que você criar: eu.vida, eu.dano..."),
]
DESC_EVENTOS = {
    "iniciar": "Quando o jogo começa (ou o objeto é criado).", "frame": "Toda vez que a tela atualiza (60x por segundo).",
    "cada": "A cada N segundos. Ex: quando cada 2:", "tecla": 'Quando aperta a tecla. Ex: quando tecla "e":',
    "soltar": 'Quando solta a tecla. Ex: quando soltar "e":',
    "tocar": 'Quando começa a encostar em algo (nome ou tipo). Ex: quando tocar "Moeda":',
    "parar_tocar": 'Quando para de encostar. Ex: quando parar_tocar "Bloco":',
    "pousar": "Quando cai em cima de algo sólido.", "clique": "Quando clicam no objeto (ótimo para Botão).",
    "clique_tela": "Quando clicam em qualquer lugar.", "destruido": "Quando o objeto é destruído.",
    "moeda": "Quando o player pega uma moeda.", "item": "Quando o player pega um item.",
    "respawn": "Quando o player morre/volta ao início.", "vitoria": "Quando vence a fase.",
    "dano": "Quando o objeto leva dano (comportamento Vida ou dano()).",
    "sem_vida": "Quando a vida do objeto chega a zero.",
    "fim_dialogo": "Quando o jogador fecha a caixa de diálogo.",
}

EXEMPLO_PLUGIN = '''# Plugin de exemplo da Minha Engine
# Cada arquivo .py nesta pasta pode criar funcoes NOVAS para a linguagem Brasa.
# Depois de salvar, reabra o editor. As funcoes aparecem na aba API.

import math


def registrar(api):
    api.funcao("dobro", lambda x: x * 2, "Retorna o dobro de um número. Ex: dobro(5)")
    api.funcao("gritar", lambda t: str(t).upper() + "!", 'Texto em maiúsculas. Ex: gritar("oi")')
    api.funcao("seno", lambda g: math.sin(math.radians(g)), "Seno de um ângulo em graus. Ex: seno(30)")
'''
