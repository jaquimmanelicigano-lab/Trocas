@echo off
cd /d "%~dp0"

echo A remover pasta .git e recomecar...
rmdir /s /q ".git"

echo A inicializar novo repositorio...
git init

echo A adicionar ficheiros...
git add .

echo A fazer commit...
git commit -m "Projeto Trocas - Versao inicial Flask"

echo A criar branch master...
git branch -m master

echo A fazer push para GitHub...
git push -u https://github.com/jaquimmanelicigano-lab/Trocas.git master

echo Concluido! Abre https://github.com/jaquimmanelicigano-lab/Trocas para ver.
pause