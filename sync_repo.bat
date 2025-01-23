@echo off
cd C:\Users\goblo\Downloads\new srts\current development
git pull origin main
git add .
git commit -m "Auto-sync: %date% %time%"
git push origin main
