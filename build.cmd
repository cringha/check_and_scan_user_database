@call .venv\Scripts\activate.bat
chcp 65001


pyinstaller --onefile cmd_reorg_userinfo.py
pyinstaller --onefile export-user-image-to-docx.py
pyinstaller --onefile export-user-info-to-images.py
pyinstaller --onefile -F -w ui/main-to-snapshots.py
pyinstaller --onefile -F -w ui/main-to-docx.py
pyinstaller --onefile -F -w ui/main-scan-tools2.py

@call .venv\Scripts\deactivate.bat