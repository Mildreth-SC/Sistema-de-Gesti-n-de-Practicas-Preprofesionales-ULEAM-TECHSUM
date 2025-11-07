# 🎯 RESUMEN RÁPIDO: DEPLOY EN RENDER EN 9 PASOS

```
┌─────────────────────────────────────────────────────────────┐
│  PREPARACIÓN LOCAL → GITHUB → RENDER → ¡EN LÍNEA! 🚀       │
└─────────────────────────────────────────────────────────────┘
```

## 📋 **PASO A PASO ULTRA SIMPLIFICADO**

### ✅ **PASO 1: Verificar archivos**
Ya tienes todo listo:
- ✅ `build.sh` 
- ✅ `requirements.txt`
- ✅ `runtime.txt`
- ✅ `settings.py` configurado

### ✅ **PASO 2: Subir a GitHub**
```bash
# En tu terminal (PowerShell):
git init
git add .
git commit -m "Listo para deploy"

# Crea un repo en github.com, luego:
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git push -u origin main
```

### ✅ **PASO 3: Crear base de datos en Render**
1. Ve a https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Name: `sistema-practicas-db`
4. Region: **Oregon (US West)**
5. Plan: **Free**
6. Click **"Create Database"**
7. **COPIA LA "Internal Database URL"**

### ✅ **PASO 4: Crear Web Service**
1. En Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect tu repositorio de GitHub
3. Configuración:
   - **Name**: `sistema-practicas-uleam`
   - **Region**: **Oregon (US West)**
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn sistema_practicas.wsgi:application`
   - **Plan**: **Free**

### ✅ **PASO 5: Variables de entorno**
Click **"Advanced"** → **"Add Environment Variable"**

**Agregar una por una:**

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `tu-clave-super-secreta-larga-12345` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | `[La URL que copiaste del Paso 3]` |
| `CSRF_TRUSTED_ORIGINS` | `https://sistema-practicas-uleam.onrender.com` |
| `SITE_URL` | `https://sistema-practicas-uleam.onrender.com` |

### ✅ **PASO 6: Create Web Service**
1. Revisa que todo esté correcto
2. Click **"Create Web Service"**
3. **ESPERA 5-10 MINUTOS** (ve la pestaña "Logs")

### ✅ **PASO 7: Crear superusuario**
1. En Render, ve a tu Web Service
2. Click en **"Shell"** (arriba)
3. Ejecuta:
```bash
python manage.py createsuperuser
```
4. Username: `admin`
5. Email: `admin@uleam.edu.ec`
6. Password: (tu contraseña)

### ✅ **PASO 8: Acceder al admin**
Ve a: `https://sistema-practicas-uleam.onrender.com/admin/`

### ✅ **PASO 9: ¡Probar que funcione!**
- [ ] Página principal carga
- [ ] Puedes entrar al admin
- [ ] CSS se ve bien
- [ ] Puedes registrar una empresa
- [ ] Puedes registrar un estudiante

---

## 🎉 **¡LISTO! TU APP ESTÁ EN LÍNEA**

URL: `https://sistema-practicas-uleam.onrender.com`

---

## ⚠️ **IMPORTANTE: Plan Gratuito de Render**

**Limitaciones:**
- Se "duerme" después de 15 minutos sin uso
- Primera carga después de dormir: ~1 minuto
- No guarda archivos subidos (usa Cloudinary)

**Para mejorar:**
- Plan Starter ($7/mes): Sin "spin down", almacenamiento persistente

---

## 🆘 **SI ALGO SALE MAL**

### Error: Build fails
**Solución:** Revisa los Logs en Render

### Error: 500 Internal Server Error
**Solución:**
1. Verifica `SECRET_KEY` en Environment Variables
2. Verifica `DATABASE_URL` esté correcta
3. Revisa Logs

### Error: CSS no se carga
**Solución:**
1. Ve al Shell de Render
2. Ejecuta: `python manage.py collectstatic --no-input`

### Error: Base de datos no conecta
**Solución:**
- Verifica que `DATABASE_URL` sea la "Internal Database URL"
- Asegúrate que ambos (DB y Web Service) estén en la misma región

---

## 📚 **DOCUMENTACIÓN COMPLETA**

Para la guía detallada completa, lee:
- `DEPLOY_RENDER_COMPLETO.md` - Guía paso a paso con explicaciones
- `CHECKLIST_PRE_DEPLOY.md` - Lista de verificación antes del deploy
- `.env.example` - Ejemplo de variables de entorno

---

## 🔄 **ACTUALIZACIONES FUTURAS**

Cuando hagas cambios:
```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

Render detectará el cambio y **automáticamente** hará el deploy. ✨

---

```
╔═══════════════════════════════════════════════════════╗
║  ¡Tu Sistema de Prácticas está EN VIVO! 🌍🚀          ║
║                                                       ║
║  Comparte la URL con tus usuarios:                    ║
║  https://sistema-practicas-uleam.onrender.com        ║
╚═══════════════════════════════════════════════════════╝
```
