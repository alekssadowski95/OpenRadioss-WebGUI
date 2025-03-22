@set mypath=%cd%

cd %mypath%

python -m PyInstaller run.py --icon "flask_app/static/ross.ico" --add-data="flask_app/static/bootstrap-5.3.3-dist/css/*:flask_app/static/bootstrap-5.3.3-dist/css" --add-data="flask_app/static/bootstrap-5.3.3-dist/js/*:flask_app/static/bootstrap-5.3.3-dist/js" --add-data="flask_app/templates/*:flask_app/templates" --add-data="flask_app/static/*:flask_app/static" --add-data="flask_app/data/*:flask_app/data" --add-data="LICENSE:." --splash flask_app/static/openradioss-splash.jpg --noconfirm

@Pause