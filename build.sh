#!/usr/bin/env bash#!/usr/bin/env bash

# Script de construcción para Render# exit on error

set -o errexit

set -o errexit  # Salir si hay algún error

echo "🚀 Iniciando build para producción..."

echo "🚀 Iniciando proceso de construcción..."

# Actualizar pip

# Instalar dependenciasecho "📦 Actualizando pip..."

echo "📦 Instalando dependencias de Python..."pip install --upgrade pip

pip install --upgrade pip

pip install -r requirements.txt# Instalar dependencias

echo "📚 Instalando dependencias..."

echo "🗄️ Recolectando archivos estáticos..."pip install -r requirements.txt

python manage.py collectstatic --no-input

# Recolectar archivos estáticos

echo "🔄 Aplicando migraciones de base de datos..."echo "🎨 Recolectando archivos estáticos..."

python manage.py migrate --no-inputpython manage.py collectstatic --no-input --clear



echo "✅ Construcción completada exitosamente!"# Ejecutar migraciones

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --no-input

# Poblar carreras de ULEAM (solo si no existen)
echo "🎓 Verificando carreras de ULEAM..."
python poblar_carreras_uleam.py || echo "⚠️ Error poblando carreras (probablemente ya existen)"

echo "✅ Build completado exitosamente!"
