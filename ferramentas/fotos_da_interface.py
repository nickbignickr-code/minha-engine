# Tira "fotos" da interface com o pygame de verdade (sem abrir janela), para conferir o visual.
# Usado pelo GitHub (workflow "Fotos e testes"). Também roda no PC: python ferramentas/fotos_da_interface.py
import os
import sys
import shutil
import tempfile
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "fotos")
os.makedirs(SAIDA, exist_ok=True)

# a engine guarda config e projetos na pasta dela: usa uma cópia temporária para não sujar nada
TMP = tempfile.mkdtemp()
shutil.copy(os.path.join(RAIZ, "minha_engine.py"), TMP)
shutil.copytree(os.path.join(RAIZ, "motor"), os.path.join(TMP, "motor"))
sys.path.insert(0, TMP)
import minha_engine as me          # noqa: E402

pg = me.pygame
pg.init()
me.preparar_pastas()
me.carregar_config()
me.CONFIG["geral"]["tour_visto"] = True
me.aplicar_aparencia()
me.aplicar_resolucao()
tela = pg.display.set_mode((me.LARGURA, me.ALTURA))
erros = []


def foto(nome, desenhar, quadros=12):
    try:
        for _ in range(quadros):        # vários quadros para as animações terminarem
            desenhar()
            time.sleep(0.03)
        pg.image.save(tela, os.path.join(SAIDA, nome + ".png"))
        print("foto:", nome)
    except Exception as e:      # segue tirando as outras
        import traceback
        erros.append((nome, traceback.format_exc()))
        print("ERRO na foto", nome, e)


pasta = me.criar_projeto("Fotos", "Exemplo: RPG top-down (vila e masmorra)")
me.definir_projeto(pasta)
ed = me.Editor(pasta_projeto=pasta, tela=tela)
try:
    pg.mouse.set_pos(10, 10)
except (AttributeError, pg.error):
    pass
foto("01_editor_cena", ed.desenhar)
pl = next(d for d in ed.objetos if d["tipo"] == "Player")
ed.selecionar(pl)
foto("02_editor_selecionado", ed.desenhar)
ed.aba = "eventos"
foto("03_eventos", ed.desenhar)
ed.aba = "loja"
foto("04_loja", ed.desenhar)
ed.aba = "cena"
ed.abrir_busca()
for ch in "moeda":
    ed.seletor["busca"] += ch
foto("05_buscar", ed.desenhar)
ed.seletor = None
ed.iniciar_tour()
ed.tour["passo"] = 1
foto("06_tour_passo2", ed.desenhar, 20)
ed.tour["passo"] = 7
foto("07_tour_buscar", ed.desenhar, 20)
ed.tour = None
ed.play()
foto("08_play", lambda: (ed.jogo.update(1 / 60, pg.key.get_pressed(), set()), ed.desenhar()), 40)
ed.parar()
for tema in me.TEMAS_UI:
    me.CONFIG["aparencia"]["tema"] = tema
    me.aplicar_aparencia()
    foto("09_tema_" + me._slug(tema) if hasattr(me, "_slug") else "09_tema_" + tema, ed.desenhar)
me.CONFIG["aparencia"]["tema"] = "Grafite"
me.aplicar_aparencia()
pasta2 = me.criar_projeto("Vazio", "Projeto vazio (top-down)")
me.definir_projeto(pasta2)
ed2 = me.Editor(pasta_projeto=pasta2, tela=tela)
foto("12_topdown_vazio", ed2.desenhar)
ed2.objetos[:] = [d for d in ed2.objetos if d["tipo"] == "Peça"]
foto("13_cena_vazia", ed2.desenhar)
ed2.iniciar_tour()
ed2.tour["passo"] = 3
foto("14_tour_propriedades", ed2.desenhar, 20)
ini = me.Inicio(tela, pg.time.Clock())
foto("10_inicio", ini.desenhar)
ini.pagina = "config"
ini.config_aba = "aparencia"
foto("11_config_aparencia", ini.desenhar)
print("ERROS:", len(erros))
for nome, tb in erros:
    print("----", nome)
    print(tb)
with open(os.path.join(SAIDA, "erros.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(f"---- {n}\n{tb}" for n, tb in erros) or "sem erros")
sys.exit(1 if erros else 0)
