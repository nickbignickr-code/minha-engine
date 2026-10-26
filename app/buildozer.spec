[app]
title = Minha Engine
package.name = minhaengine
package.domain = com.minhaengine
source.dir = .
source.include_exts = py,png,zip
source.exclude_dirs = bin,.buildozer,__pycache__
version = 17
requirements = python3,pygame,pyjnius,android,openssl,certifi
orientation = landscape
fullscreen = 1
icon.filename = %(source.dir)s/icone_512.png
presplash.filename = %(source.dir)s/presplash.png
android.presplash_color = #181A22
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,VIBRATE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True
p4a.bootstrap = sdl2
p4a.branch = v2023.02.10
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 0
