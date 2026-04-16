@echo off
cd /d "C:\Users\clash\Desktop\trocas"

echo A adicionar ficheiros...
git add .

echo A fazer commit...
git commit -m "Projeto Trocas - Suporte PostgreSQL para Render"

echo A fazer force push para GitHub...
git push -f https://github.com/jaquimmanelicigano-lab/Trocas.git master

echo Concluido!
pause