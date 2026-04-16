@echo off
cd /d "C:\Users\clash\Desktop\trocas"

echo A adicionar ficheiros...
git add .

echo A fazer commit...
git commit -m "Projeto Trocas - Removido Pillow para deploy no Render"

echo A fazer push para GitHub...
git push -f https://github.com/jaquimmanelicigano-lab/Trocas.git master

echo Concluido!
pause