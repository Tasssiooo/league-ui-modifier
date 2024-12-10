pyinstaller --onedir --clean --console \
  --icon "NONE" \
  --name league-ui-updater \
  --contents-directory deps \
  --add-data schemes:schemes \
  src/main.py
