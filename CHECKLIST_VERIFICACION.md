# ✅ CHECKLIST DE VERIFICACIÓN PRE-DEPLOYMENT

## Antes de hacer commit y desplegar en Render

### 🔐 Seguridad

- [ ] ✅ Archivo `.env` NO está en el repositorio (verificar `.gitignore`)
- [ ] ✅ No hay credenciales reales en `render.yaml` (solo comentarios)
- [ ] ✅ No hay credenciales en ningún archivo `.py`
- [ ] ✅ `SECRET_KEY` no está hardcodeado en `settings.py`
- [ ] ✅ Contraseñas guardadas en lugar seguro (fuera del repo)

### 🗑️ Limpieza

- [ ] ✅ Archivos de Vercel eliminados (`vercel.json`, `vercel_build.sh`)
- [ ] ✅ Scripts duplicados eliminados (`build_files.sh`)
- [ ] ✅ Documentación duplicada eliminada
- [ ] ✅ No hay archivos `__pycache__` en el repo
- [ ] ✅ No hay `db.sqlite3` en el repo

### 📝 Configuración

- [ ] ✅ `settings.py` actualizado (sin referencias a Vercel)
- [ ] ✅ `render.yaml` preparado (con placeholders)
- [ ] ✅ `.env.example` documentado
- [ ] ✅ `README.md` actualizado
- [ ] ✅ `requirements.txt` tiene todas las dependencias
- [ ] ✅ `runtime.txt` especifica Python 3.10.15

### 📚 Documentación

- [ ] ✅ `GUIA_DEPLOY_RENDER_SUPABASE.md` creado
- [ ] ✅ `LIMPIEZA_CODIGO.md` creado
- [ ] ✅ `PROXIMOS_PASOS.md` creado
- [ ] ✅ `README.md` refleja el estado actual

### 🔧 Funcionalidad Local

- [ ] 🔲 Servidor local funciona: `python manage.py runserver`
- [ ] 🔲 Migraciones aplicadas: `python manage.py migrate`
- [ ] 🔲 Admin accesible: `http://127.0.0.1:8000/admin`
- [ ] 🔲 Páginas principales funcionan correctamente

---

## ⚠️ IMPORTANTE ANTES DE COMMIT

### Verificar estos archivos NO estén en staging:

```bash
# Ejecutar en PowerShell:
git status

# NO deben aparecer:
# - .env
# - db.sqlite3
# - __pycache__/
# - *.pyc
# - /media/ (si tiene archivos subidos)
```

### Si aparecen archivos sensibles:

```bash
# Remover del staging:
git reset HEAD .env
git reset HEAD db.sqlite3

# Agregar a .gitignore si no está:
echo ".env" >> .gitignore
echo "db.sqlite3" >> .gitignore
```

---

## 📋 Archivos que DEBEN estar en el commit:

```
✅ sistema_practicas/settings.py (actualizado)
✅ render.yaml (sin credenciales reales)
✅ .env.example (documentado)
✅ README.md (actualizado)
✅ GUIA_DEPLOY_RENDER_SUPABASE.md (nuevo)
✅ LIMPIEZA_CODIGO.md (nuevo)
✅ PROXIMOS_PASOS.md (nuevo)
✅ CHECKLIST_VERIFICACION.md (este archivo)
✅ .gitignore (actualizado)
```

---

## 🚀 Cuando TODO esté verificado:

### 1. Hacer Commit

```bash
git add .
git commit -m "Limpieza de código y preparación para Render + Supabase

- Eliminados archivos de Vercel
- Limpiado código obsoleto
- Actualizado settings.py (solo Render)
- Preparado render.yaml para nuevas credenciales
- Creada documentación completa de deployment
- Actualizado README.md
"
```

### 2. Push a GitHub

```bash
git push origin main
```

### 3. Continuar con Deployment

Seguir la guía: `GUIA_DEPLOY_RENDER_SUPABASE.md`

---

## 🆘 Si algo sale mal:

### Deshacer último commit (si no has hecho push):
```bash
git reset --soft HEAD~1
```

### Ver qué archivos están en staging:
```bash
git status
```

### Ver diferencias:
```bash
git diff
git diff --staged
```

---

## ✅ ESTADO ACTUAL DEL PROYECTO

**Fecha de limpieza:** 6 de Noviembre de 2025

**Archivos eliminados:** 7
- vercel.json
- vercel_build.sh
- build_files.sh
- prepare_deploy.ps1
- INICIO_RAPIDO_RENDER.md
- DEPLOY_RENDER.md
- CONFIGURACION_RENDER.md

**Archivos actualizados:** 4
- sistema_practicas/settings.py
- render.yaml
- .env.example
- README.md

**Archivos nuevos:** 4
- GUIA_DEPLOY_RENDER_SUPABASE.md
- LIMPIEZA_CODIGO.md
- PROXIMOS_PASOS.md
- CHECKLIST_VERIFICACION.md

**Estado:** ✅ LISTO PARA DEPLOYMENT

---

**¡El proyecto está limpio y listo para ser desplegado en Render con Supabase!** 🎉
