:: DEFINITIONS (care for blank spaces)
set PYI_MAIN=main_pyi.py

set PROJECT_FOLDER=Squale
set PROJECT_NAME=Squale
set RESOURCES_FOLDER=resources
set ICON_PATH=%RESOURCES_FOLDER%/icon.ico

if "%~1"=="--debug" (
	echo Debug
) else (
	:: PY-INSTALLER
	pyinstaller --onefile -i %ICON_PATH% -n %PROJECT_NAME% %PYI_MAIN%
	xcopy %RESOURCES_FOLDER% dist\%RESOURCES_FOLDER%\ /e /s /y
	cd dist
	tar.exe -c -a -f %PROJECT_NAME%.zip %RESOURCES_FOLDER% %PROJECT_NAME%.exe
	cd ..
)

:: PYGBAG
cd ..
if "%~1"=="--debug" (
    pygbag --width 960 --height 540 --package PROJECT_NAME --title PROJECT_NAME --icon %PROJECT_FOLDER%/%ICON_PATH% --can_close 1 %PROJECT_FOLDER%
) else (
    pygbag --width 960 --height 540 --build --archive --package PROJECT_NAME --title PROJECT_NAME --icon %PROJECT_FOLDER%/%ICON_PATH% --can_close 1 %PROJECT_FOLDER%
)
cd %PROJECT_FOLDER%/build
copy web.zip ..\dist\%PROJECT_NAME%-web.zip
cd ..

echo ==================================================