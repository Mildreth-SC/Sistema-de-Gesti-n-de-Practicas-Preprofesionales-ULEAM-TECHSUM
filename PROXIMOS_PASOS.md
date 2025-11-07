# 🚀 PRÓXIMOS PASOS - Deploy a Render

## ⚡ Resumen Rápido

El proyecto ha sido **limpiado y optimizado** para deployment en **Render + Supabase**.

---

## 📝 Checklist de Deployment

### ✅ Ya Completado
- [x] Eliminados archivos de Vercel
- [x] Limpiado código obsoleto
- [x] Actualizado `settings.py`
- [x] Preparado `render.yaml`
- [x] Actualizado `.env.example`
- [x] Documentación completa creada

### 🔲 Por Hacer (En este orden)

#### 1. Configurar Supabase (10 minutos)
```
□ Ir a https://app.supabase.com/
□ Crear nuevo proyecto
□ Anotar:
  - Project URL: https://xxxxx.supabase.co
  - Database Password: [tu-password]
  - Connection String (Transaction pooling)
  - Anon/Public Key
```

#### 2. Actualizar render.yaml (5 minutos)
```
□ Abrir: render.yaml
□ Reemplazar en línea 17-22:
  - DATABASE_URL con tu connection string de Supabase
  - SUPABASE_URL con tu Project URL
  - SUPABASE_KEY con tu Anon Key
□ Guardar cambios
```

#### 3. Commit y Push (2 minutos)
```bash
□ git add .
□ git commit -m "Limpieza de código y configuración para Render + Supabase"
□ git push origin main
```

#### 4. Configurar Render (10 minutos)
```
□ Ir a https://dashboard.render.com/
□ New + > Web Service
□ Conectar repositorio GitHub
□ Configurar:
  - Name: sistema-practicas-uleam
  - Region: Oregon (misma que Supabase)
  - Branch: main
  - Build Command: bash build.sh
  - Start Command: gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
□ Environment Variables (copiar de render.yaml)
□ Create Web Service
```

#### 5. Post-Deploy (10 minutos)
```
□ Esperar a que termine el build (5-10 min)
□ Abrir Shell en Render
□ Crear superusuario:
  python manage.py createsuperuser
□ (Opcional) Poblar datos:
  python manage.py poblar_datos
□ Probar la aplicación
```

---

## 📚 Documentación Disponible

| Archivo | Propósito |
|---------|-----------|
| `GUIA_DEPLOY_RENDER_SUPABASE.md` | 📖 Guía completa paso a paso |
| `LIMPIEZA_CODIGO.md` | 📋 Resumen de cambios realizados |
| `README.md` | 📘 Documentación general del proyecto |
| `.env.example` | 🔑 Ejemplo de variables de entorno |

---

## 🆘 Solución Rápida de Problemas

### Error de conexión a BD
```bash
# Verificar en Render > Environment:
DATABASE_URL=postgresql://postgres.[REF]:[PASS]@aws-0-[REGION].pooler.supabase.com:6543/postgres?pgbouncer=true
```

### Error 500
```bash
# Ver logs en Render Dashboard > Logs
# Verificar DEBUG=False
# Verificar todas las env vars
```

### Static files no cargan
```bash
# En Shell de Render:
python manage.py collectstatic --no-input --clear
```

### Migraciones no aplicadas
```bash
# En Shell de Render:
python manage.py migrate --run-syncdb
```

---

## 🎯 URLs Importantes

- **Supabase Dashboard**: https://app.supabase.com/
- **Render Dashboard**: https://dashboard.render.com/
- **Repositorio GitHub**: https://github.com/JuanMoranULEAM/Sistema-de-Gesti-n-de-Practicas-Preprofesionales-ULEAM---TEHCSUM

---

## 💡 Comandos Útiles

### Local (Desarrollo)
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Ejecutar servidor local
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar datos de prueba
python poblar_datos_prueba.py
```

### Render (Shell)
```bash
# Ver migraciones
python manage.py showmigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Colectar archivos estáticos
python manage.py collectstatic --no-input

# Poblar datos
python manage.py poblar_datos
```

---

## ⏱️ Tiempo Estimado Total

- **Configuración Supabase**: ~10 minutos
- **Actualizar configuración**: ~5 minutos
- **Deploy en Render**: ~10 minutos
- **Build inicial**: ~5-10 minutos
- **Post-deploy**: ~10 minutos

**TOTAL: ~40-45 minutos**

---

## ✅ Al Finalizar Tendrás

- ✨ Aplicación desplegada en Render
- 🗄️ Base de datos PostgreSQL en Supabase
- 🔐 Configuración segura
- 📱 URL pública funcional
- 🔄 Auto-deploy configurado
- 📊 Panel admin accesible

---

## 🚀 ¡EMPECEMOS!

**Siguiente paso**: Ir a [GUIA_DEPLOY_RENDER_SUPABASE.md](GUIA_DEPLOY_RENDER_SUPABASE.md) y seguir la sección "1️⃣ Configurar Base de Datos en Supabase"

---

**Nota**: Guarda este archivo para referencia rápida durante el proceso de deployment.

**Última actualización**: 6 de Noviembre de 2025
