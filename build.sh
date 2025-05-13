pyinstaller --onedir --clean --console --noconfirm \
  --paths=src --paths=src/lib --paths=src/utils \
  --icon "icon.ico" \
  --name league-ui-updater \
  --contents-directory deps \
  --add-data schemes:schemes \
  --add-data src/lib/cslol_tools:cslol_tools \
  --add-data src/lib/ritobin:ritobin \
  --hidden-import=lib \
  --hidden-import=utils \
  --hidden-import=lib.cslol_tools \
  --hidden-import=lib.ritobin \
  --hidden-import=utils.configuration \
  --hidden-import=utils.fs \
  src/main.py
