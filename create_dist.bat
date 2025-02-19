@set mypath=%cd%

cd %mypath%

python -m PyInstaller run.py --icon "openradioss_flask/static/ross.ico" --add-data="openradioss_flask/static/bootstrap-5.3.3-dist/css/*:openradioss_flask/static/bootstrap-5.3.3-dist/css" --add-data="openradioss_flask/static/bootstrap-5.3.3-dist/js/*:openradioss_flask/static/bootstrap-5.3.3-dist/js" --add-data="openradioss_flask/templates/*:openradioss_flask/templates" --add-data="openradioss_flask/static/*:openradioss_flask/static" --add-data="openradioss_flask/data/*:openradioss_flask/data" --add-data="LICENSE:." --splash openradioss_flask/static/openradioss-splash.jpg --noconfirm

@Pause