@echo off
title Fooocus Face Swap
echo 🎭 Iniciando Fooocus con Face Swap...
echo.

cd /d "%~dp0"
python launch_faceswap.py %*

if errorlevel 1 (
    echo.
    echo ❌ Error al ejecutar Fooocus
    echo Presiona cualquier tecla para salir...
    pause >nul
)
