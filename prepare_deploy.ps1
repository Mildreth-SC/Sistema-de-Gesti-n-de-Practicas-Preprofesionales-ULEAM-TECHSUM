# Script para preparar el proyecto para deploy en PythonAnywhere
# Ejecutar antes de hacer git push

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*59 -ForegroundColor Cyan
Write-Host "🚀 PREPARANDO PROYECTO PARA PYTHONANYWHERE" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*59 -ForegroundColor Cyan
Write-Host ""

# 1. Verificar que .env NO esté en el repositorio
Write-Host "📝 1. Verificando .gitignore..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.env") {
        Write-Host "   ✅ .env está en .gitignore (correcto)" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  .env NO está en .gitignore" -ForegroundColor Red
        Write-Host "   Agregando .env a .gitignore..." -ForegroundColor Yellow
        Add-Content ".gitignore" "`n# Environment variables`n.env`n.env.local`n*.env"
        Write-Host "   ✅ .env agregado a .gitignore" -ForegroundColor Green
    }
} else {
    Write-Host "   ⚠️  .gitignore no existe" -ForegroundColor Red
}

Write-Host ""

# 2. Verificar requirements.txt
Write-Host "📦 2. Verificando requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    $requirementsContent = Get-Content "requirements.txt" -Raw
    $requiredPackages = @(
        "Django",
        "psycopg2-binary",
        "supabase",
        "python-decouple",
        "python-dotenv"
    )
    
    $allPresent = $true
    foreach ($package in $requiredPackages) {
        if ($requirementsContent -match $package) {
            Write-Host "   ✅ $package encontrado" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $package NO encontrado" -ForegroundColor Red
            $allPresent = $false
        }
    }
    
    if ($allPresent) {
        Write-Host "   ✅ Todas las dependencias necesarias están presentes" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Faltan algunas dependencias" -ForegroundColor Red
    }
} else {
    Write-Host "   ❌ requirements.txt no existe" -ForegroundColor Red
}

Write-Host ""

# 3. Verificar que existe .env localmente
Write-Host "🔐 3. Verificando archivo .env local..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✅ .env encontrado localmente" -ForegroundColor Green
    Write-Host "   ⚠️  Recuerda crear .env manualmente en PythonAnywhere" -ForegroundColor Yellow
} else {
    Write-Host "   ❌ .env NO encontrado" -ForegroundColor Red
    Write-Host "   Asegúrate de configurar .env en PythonAnywhere" -ForegroundColor Yellow
}

Write-Host ""

# 4. Verificar conexión a Supabase
Write-Host "🗄️  4. Verificando conexión a Supabase..." -ForegroundColor Yellow
try {
    $result = python test_supabase_connection.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Conexión a Supabase OK" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Problemas con la conexión a Supabase" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ⚠️  No se pudo verificar la conexión" -ForegroundColor Yellow
}

Write-Host ""

# 5. Estado de Git
Write-Host "📂 5. Estado de Git..." -ForegroundColor Yellow
git status --short
Write-Host ""

# 6. Resumen
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*59 -ForegroundColor Cyan
Write-Host "✅ CHECKLIST PARA PYTHONANYWHERE" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*59 -ForegroundColor Cyan
Write-Host ""
Write-Host "Antes de hacer deploy:" -ForegroundColor Yellow
Write-Host "  1. ✅ .env en .gitignore (no se subirá a GitHub)"
Write-Host "  2. ✅ requirements.txt completo"
Write-Host "  3. ⚠️  Crear .env en PythonAnywhere con tus credenciales"
Write-Host "  4. ⚠️  Actualizar ALLOWED_HOSTS en .env de PythonAnywhere"
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. git add ."
Write-Host "  2. git commit -m 'Listo para deploy'"
Write-Host "  3. git push origin main"
Write-Host "  4. Seguir DEPLOY_PYTHONANYWHERE.md o DEPLOY_QUICKSTART.md"
Write-Host ""
Write-Host "📚 Documentación:" -ForegroundColor Cyan
Write-Host "  - DEPLOY_PYTHONANYWHERE.md (guía completa)"
Write-Host "  - DEPLOY_QUICKSTART.md (resumen rápido)"
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "="*59 -ForegroundColor Cyan
