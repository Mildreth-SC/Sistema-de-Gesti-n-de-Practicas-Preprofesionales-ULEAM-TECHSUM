@echo off
REM Script para ejecutar el servidor de desarrollo local
REM Ejecutar: .\run_local.bat

echo.
echo ╔════════════════════════════════════════════════╗
echo ║   Sistema de Practicas - Servidor Local       ║
echo ╚════════════════════════════════════════════════╝
echo.

REM Verificar que el entorno virtual esté activado
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Error: No se encuentra el entorno virtual
    echo    Ejecuta: python -m venv .venv
    pause
    exit /b 1
)

REM Activar entorno virtual
call .venv\Scripts\activate.bat

echo ✅ Entorno virtual activado
echo.

REM Verificar archivo .env
if not exist ".env" (
    echo ⚠️  Advertencia: No se encuentra el archivo .env
    echo    Copia .env.example a .env y configura las variables
    echo.
)

REM Aplicar migraciones
echo 📋 Verificando migraciones...
python manage.py migrate --no-input
echo.

REM Colectar archivos estáticos
echo 📦 Recolectando archivos estáticos...
python manage.py collectstatic --no-input
echo.

REM Iniciar servidor
echo.
echo ╔════════════════════════════════════════════════╗
echo ║   🚀 Iniciando servidor en                     ║
echo ║   http://127.0.0.1:8000                        ║
echo ╚════════════════════════════════════════════════╝
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver
