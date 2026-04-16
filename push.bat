@echo off
cd /d "%~dp0"

echo Configurando Git...
git config --global user.email "jaquimmanelicigano@gmail.com"
git config --global user.name "jaquimmanelicigano"

echo Adicionando ficheiros...
git add .

echo A fazer commit...
git commit -m "Projeto Trocas - Versao inicial Flask com Flask, MySQL, autenticacao e chat"

echo A fazer push...
git push -u origin master

echo Concluido!
pause