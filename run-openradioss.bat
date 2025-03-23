set arg1=%1
set arg2=%2
set arg3=%3
set OPENRADIOSS_PATH=%arg2%
set RAD_CFG_PATH=%OPENRADIOSS_PATH%\hm_cfg_files
set RAD_H3D_PATH=%OPENRADIOSS_PATH%\extlib\h3d\lib\win64
set PATH=%OPENRADIOSS_PATH%\extlib\hm_reader\win64;%PATH%
set PATH=%OPENRADIOSS_PATH%\extlib\intelOneAPI_runtime\win64;%PATH%
set KMP_STACKSIZE=4000m
%OPENRADIOSS_PATH%\exec\starter_win64.exe -i %arg1%\%arg3%_0000.rad -nt 8 -np 1
%OPENRADIOSS_PATH%\exec\engine_win64.exe -i %arg1%\%arg3%_0001.rad