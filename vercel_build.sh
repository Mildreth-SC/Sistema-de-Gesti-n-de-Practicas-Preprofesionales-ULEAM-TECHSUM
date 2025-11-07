#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python3.9 manage.py collectstatic --no-input --clear
