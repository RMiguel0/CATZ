@echo off
rem Salir en caso de error
setlocal enabledelayedexpansion

rem Instalar dependencias con Poetry
poetry install

rem Recoger archivos estáticos
python manage.py collectstatic --no-input

rem Aplicar migraciones
python manage.py migrate
