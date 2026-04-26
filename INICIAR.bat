@echo off
title Trocas - Sistema de Anuncios
color 0A

echo ========================================
echo    TROCAS - Sistema de Anuncios
echo ========================================
echo.

REM Obter o IP local da rede
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
    set "ip=%%i"
    goto :found
)
:found

REM Remover espacos em branco do IP
set ip=%ip: =%

echo [INFO] A iniciar servidor Flask...
echo [INFO] Porta: 3000
echo.
echo ========================================
echo    O site esta disponivel em:
echo ========================================
echo.
echo   Local:   http://localhost:3000
echo   Rede:    http://%ip%:3000
echo.
echo ========================================
echo    Pressione CTRL+C para parar o servidor
echo ========================================
echo.

REM Iniciar o servidor Flask
python app.py

pause