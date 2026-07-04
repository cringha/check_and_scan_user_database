@call .venv\Scripts\activate.bat
chcp 65001


pyinstaller --onefile export-user-image-to-docx.py
pyinstaller --onefile export-user-info-to-images.py
pyinstaller --onefile -F -w ui/main-to-snapshots.py


@call .venv\Scripts\deactivate.bat