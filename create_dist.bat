@set mypath=%cd%

cd %mypath%

pyinstaller run.py --icon "openradioss_flask/static/ross.ico" --add-data="openradioss_flask/templates/*:openradioss_flask/templates" --add-data="openradioss_flask/static/*:openradioss_flask/static" --add-data="openradioss_flask/data/*:openradioss_flask/data" --add-data="LICENSE:." --noconsole --splash openradioss_flask/static/openradioss-splash.jpg --noconfirm

@Pause