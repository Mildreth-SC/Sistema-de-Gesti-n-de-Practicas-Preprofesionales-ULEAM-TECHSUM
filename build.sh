#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Iniciando build para producción..."

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

# Recolectar archivos estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input --clear

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --no-input

# Poblar carreras de ULEAM (solo si no existen)
echo "🎓 Verificando carreras de ULEAM..."
python poblar_carreras_uleam.py || echo "⚠️ Error poblando carreras (probablemente ya existen)"

echo "✅ Build completado exitosamente!"
