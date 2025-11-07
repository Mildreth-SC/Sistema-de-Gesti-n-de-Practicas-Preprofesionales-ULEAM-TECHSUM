# ✅ CHECKLIST PRE-DEPLOY

## 📋 **ANTES DE HACER DEPLOY, VERIFICA:**

### 1. Archivos de Configuración
- [x] `build.sh` existe y tiene permisos de ejecución
- [x] `requirements.txt` está actualizado
- [x] `runtime.txt` especifica Python 3.12
- [x] `.gitignore` excluye archivos sensibles (.env, db.sqlite3)

### 2. Settings.py
- [ ] `DEBUG = False` en producción
- [ ] `ALLOWED_HOSTS` incluye `.onrender.com`
- [ ] `DATABASES` usa `dj_database_url` para leer `DATABASE_URL`
- [ ] `MIDDLEWARE` incluye `WhiteNoiseMiddleware`
- [ ] `STATIC_ROOT` está configurado
- [ ] `CSRF_TRUSTED_ORIGINS` incluye tu dominio de Render

### 3. Variables de Entorno (.env)
Asegúrate de tener TODAS estas variables para configurarlas en Render:

```env
# SEGURIDAD (REQUERIDO)
SECRET_KEY=tu-clave-secreta-super-larga-y-unica
DEBUG=False

# HOSTS (REQUERIDO)
ALLOWED_HOSTS=.onrender.com,tu-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
SITE_URL=https://tu-app.onrender.com

# BASE DE DATOS (REQUERIDO)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# SUPABASE (opcional)
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key

# EMAIL (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com
```

### 4. Git y GitHub
- [ ] Código está en un repositorio local de Git
- [ ] Tienes un repositorio en GitHub
- [ ] Has hecho `git push` con todos los cambios

### 5. Cuenta de Render
- [ ] Tienes cuenta en https://render.com
- [ ] Tu cuenta de GitHub está conectada a Render

### 6. Base de Datos
- [ ] Tienes una base de datos PostgreSQL (Supabase o Render)
- [ ] Tienes la URL de conexión (`DATABASE_URL`)
- [ ] La base de datos es accesible desde internet

---

## 🚀 **COMANDOS ÚTILES PARA PROBAR LOCALMENTE**

Antes de hacer deploy, prueba que todo funcione localmente:

### 1. Probar con configuración de producción

```bash
# En tu .env temporal, cambia:
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Probar el servidor
python manage.py runserver
```

### 2. Verificar que las migraciones están al día

```bash
python manage.py makemigrations --check
python manage.py migrate --check
```

### 3. Verificar que no hay errores de sintaxis

```bash
python manage.py check
python manage.py check --deploy
```

---

## ⚠️ **PROBLEMAS COMUNES Y SOLUCIONES**

### Problema: CSS no se carga en producción
**Solución:**
```python
# En settings.py, asegúrate de tener:
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Problema: Error 500 al acceder
**Solución:**
- Verifica que `SECRET_KEY` esté configurada
- Verifica que `ALLOWED_HOSTS` incluya tu dominio
- Revisa los logs en Render

### Problema: Base de datos no conecta
**Solución:**
- Verifica que `DATABASE_URL` sea correcta
- Asegúrate que incluya `?sslmode=require` al final
- Verifica que la base de datos esté activa

### Problema: Build falla en Render
**Solución:**
- Verifica que `build.sh` tenga permisos: `chmod +x build.sh`
- Revisa los logs de build en Render
- Asegúrate que todas las dependencias estén en `requirements.txt`

---

## 📝 **NOTAS FINALES**

1. **NUNCA** subas tu archivo `.env` a GitHub
2. Cambia `SECRET_KEY` cada vez que hagas deploy a un nuevo servidor
3. Usa contraseñas seguras para tu base de datos
4. Activa autenticación de dos factores en GitHub y Render
5. Haz backups regulares de tu base de datos

---

## 🎯 **PRÓXIMOS PASOS**

Una vez que hagas deploy exitoso:

1. [ ] Crea un superusuario en el Shell de Render
2. [ ] Accede al admin y verifica que funcione
3. [ ] Registra una empresa y una facultad de prueba
4. [ ] Apruébalas desde el admin
5. [ ] Crea una práctica de prueba
6. [ ] Registra un estudiante y verifica que pueda inscribirse
7. [ ] Configura Cloudinary para archivos media (opcional)
8. [ ] Configura un dominio personalizado (opcional)

¡Todo listo para el deploy! 🚀
