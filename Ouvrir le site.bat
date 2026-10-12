@echo off
chcp 65001 >nul
title Le Pere Lucien - serveur local
cd /d "%~dp0site"
echo.
echo  Le site s'ouvre dans votre navigateur : http://localhost:8792
echo  Laissez cette fenetre ouverte pendant la visite. Fermez-la pour arreter.
echo.
start "" http://localhost:8792
python -m http.server 8792
