@echo off
cd /d "C:\Users\clash\Desktop\trocas"
git add .
git commit -m "Fix psycopg"
git push -f https://github.com/jaquimmanelicigano-lab/Trocas.git master
pause