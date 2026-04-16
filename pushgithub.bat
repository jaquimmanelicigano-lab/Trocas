@echo off
cd /d "C:\Users\clash\Desktop\trocas"

echo 1. A adicionar ficheiros...
git add .

echo 2. A fazer commit...
git commit -m "Updates"

echo 3. A fazer push para GitHub...
git push -f https://github.com/jaquimmanelicigano-lab/Trocas.git master

echo 4. Concluido! Vai ao Render e faz Manual Deploy.
pause