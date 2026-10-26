# Minha Engine - app Android (APK)
# Este arquivo é o começo do app no celular: ele escolhe a pasta onde ficam os seus projetos,
# copia a engine para lá (quando o app é instalado ou atualizado) e abre a engine.
import os
import runpy
import shutil
import sys
import traceback
import zipfile

APP = os.path.dirname(os.path.abspath(__file__))
PACOTE = os.path.join(APP, "engine.zip")      # a engine que veio dentro do APK (em .zip para manter os .py)
NOME_PASTA = "MinhaEngine"


def _jnius():
    try:
        from jnius import autoclass
        return autoclass
    except Exception:
        return None


def _atividade(autoclass):
    return autoclass("org.kivy.android.PythonActivity").mActivity


def tem_acesso_a_tudo(autoclass):
    """Android 11+: permissão 'acesso a todos os arquivos' (para a pasta MinhaEngine ficar fácil de achar)."""
    try:
        versao = autoclass("android.os.Build$VERSION").SDK_INT
        if versao >= 30:
            return bool(autoclass("android.os.Environment").isExternalStorageManager())
        ctx = _atividade(autoclass)
        perm = "android.permission.WRITE_EXTERNAL_STORAGE"
        return ctx.checkSelfPermission(perm) == 0
    except Exception:
        return False


def pedir_acesso(autoclass):
    try:
        versao = autoclass("android.os.Build$VERSION").SDK_INT
        ctx = _atividade(autoclass)
        if versao >= 30:
            Intent = autoclass("android.content.Intent")
            Settings = autoclass("android.provider.Settings")
            Uri = autoclass("android.net.Uri")
            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION,
                            Uri.parse("package:" + ctx.getPackageName()))
            ctx.startActivity(intent)
        else:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    except Exception:
        traceback.print_exc()


def pasta_do_app(autoclass):
    """Pasta só do app (não precisa de permissão; não some quando atualiza o app)."""
    try:
        return _atividade(autoclass).getExternalFilesDir(None).getAbsolutePath()
    except Exception:
        return os.environ.get("ANDROID_PRIVATE") or APP


def escolher_pasta():
    autoclass = _jnius()
    if autoclass is None:                       # rodando no PC (teste)
        return os.path.join(APP, NOME_PASTA)
    privada = os.path.join(pasta_do_app(autoclass), NOME_PASTA)
    publica = os.path.join(os.environ.get("EXTERNAL_STORAGE", "/storage/emulated/0"), NOME_PASTA)
    marca = os.path.join(pasta_do_app(autoclass), "ja_pediu_permissao")
    if tem_acesso_a_tudo(autoclass):
        try:
            os.makedirs(publica, exist_ok=True)
            # se antes usava a pasta privada, leva os projetos para a pasta pública uma vez
            if os.path.isdir(privada) and not os.path.exists(os.path.join(publica, "projetos")):
                shutil.copytree(privada, publica, dirs_exist_ok=True)
            return publica
        except OSError:
            traceback.print_exc()
    elif not os.path.exists(marca):
        try:
            os.makedirs(os.path.dirname(marca), exist_ok=True)
            open(marca, "w").close()
        except OSError:
            pass
        pedir_acesso(autoclass)
    return privada


def copiar_engine(destino):
    """Copia a engine do APK para a pasta (só quando é uma versão nova). Não mexe nos seus projetos."""
    os.makedirs(destino, exist_ok=True)
    try:
        with zipfile.ZipFile(PACOTE) as z:
            nova = z.read("VERSAO_APK.txt").decode("utf-8").strip()
            marca = os.path.join(destino, "VERSAO_APK.txt")
            try:
                with open(marca, encoding="utf-8") as f:
                    atual = f.read().strip()
            except OSError:
                atual = ""
            if atual == nova and os.path.isfile(os.path.join(destino, "minha_engine.py")):
                return
            z.extractall(destino)
    except (OSError, KeyError, zipfile.BadZipFile):
        traceback.print_exc()


def preparar_ssl():
    try:
        import certifi
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    except Exception:
        pass


def main():
    os.environ.setdefault("SDL_IOS_ORIENTATIONS", "LandscapeLeft LandscapeRight")
    os.environ.setdefault("SDL_ANDROID_TRAP_BACK_BUTTON", "1")
    preparar_ssl()
    pasta = escolher_pasta()
    copiar_engine(pasta)
    os.chdir(pasta)
    sys.path.insert(0, pasta)
    sys.argv = [os.path.join(pasta, "minha_engine.py")] + sys.argv[1:]
    try:
        runpy.run_path(os.path.join(pasta, "minha_engine.py"), run_name="__main__")
    except SystemExit:
        pass
    except Exception:
        # guarda o erro num arquivo para dar para consertar
        try:
            with open(os.path.join(pasta, "erro_do_app.txt"), "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
        except OSError:
            pass
        raise


main()
