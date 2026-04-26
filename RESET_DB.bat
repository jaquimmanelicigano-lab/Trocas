@echo off
echo ========================================
echo Reset do Banco de Dados - Sistema Destaque
echo ========================================
echo.

echo Parando possíveis processos Python...
taskkill /F /IM python.exe /T 2>nul >nul
timeout /t 2 /nobreak >nul

echo Removendo banco antigo...
if exist instance\trocas.db (
    del /F /Q instance\trocas.db
    echo [OK] Banco removido.
) else (
    echo [INFO] Banco não existia.
)

echo Criando novo banco com schema atualizado...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Schema criado.')"

echo.
echo Concluído! Agora pode iniciar a aplicação normalmente.
pause
