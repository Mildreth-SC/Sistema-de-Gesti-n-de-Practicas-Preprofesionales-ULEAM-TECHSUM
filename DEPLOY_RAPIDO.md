# 🚀 COMANDOS RÁPIDOS PARA DESPLEGAR EN RENDER

## ✅ PASO 1: VERIFICACIÓN PRE-DESPLIEGUE (YA HECHO)

```bash
python verificar_pre_deploy.py
```

**Resultado:** ✅ Sistema listo para producción

---

## 📤 PASO 2: SUBIR A GITHUB

### Opción A: Si ya tienes repositorio configurado

```bash
# Ver estado actual
git status

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "✅ Sistema preparado para producción en Render - Versión 2.0 con 43 carreras ULEAM"

# Subir a GitHub
git push origin main
```

### Opción B: Si es primera vez con Git

```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Primer commit
git commit -m "Sistema de Prácticas Preprofesionales ULEAM - Versión 2.0"

# Conectar con GitHub (reemplaza con tu URL)
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git

# Subir
git branch -M main
git push -u origin main
```

---

## 🌐 PASO 3: CREAR WEB SERVICE EN RENDER

### 3.1 Ir a Render

1. Abre: https://dashboard.render.com
2. Click en **"New +"** → **"Web Service"**
3. Conecta con GitHub y autoriza Render
4. Selecciona tu repositorio

### 3.2 Configuración del Servicio

Usa estos valores EXACTOS:

| Campo | Valor |
|-------|-------|
| **Name** | `sistema-practicas-uleam` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | (dejar vacío) |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120` |
| **Instance Type** | `Free` |

### 3.3 Variables de Entorno

Click en **"Advanced"** y agrega estas variables:

#### OBLIGATORIAS (copiar exactamente):

```
SECRET_KEY
[Auto-generado por Render - dejar que Render lo cree]

DEBUG
False

ALLOWED_HOSTS
.onrender.com,localhost,127.0.0.1

CSRF_TRUSTED_ORIGINS
https://*.onrender.com

DATABASE_URL
postgresql://postgres.owrgthzfdlnhkiwzdgbd:Milxi26.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true

SUPABASE_URL
https://owrgthzfdlnhkiwzdgbd.supabase.co
```

#### IMPORTANTE - SUPABASE_KEY:

1. Ve a: https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/settings/api
2. Copia la **"anon/public"** key
3. Agrégala como variable:
   ```
   SUPABASE_KEY
   [TU_CLAVE_AQUÍ]
   ```

#### OPCIONAL - OPENAI_API_KEY (para chatbot):

1. Ve a: https://platform.openai.com/api-keys
2. Crea una nueva key
3. Agrégala:
   ```
   OPENAI_API_KEY
   [TU_CLAVE_AQUÍ]
   ```

### 3.4 Iniciar Deploy

1. Click en **"Create Web Service"**
2. Espera 5-8 minutos

---

## ✅ PASO 4: CONFIGURACIÓN POST-DESPLIEGUE

### 4.1 Acceder al Shell de Render

1. En Render Dashboard, ve a tu servicio
2. Click en **"Shell"** (icono de terminal en la parte superior)
3. Se abrirá una terminal

### 4.2 Crear Superusuario (IMPORTANTE)

En el Shell de Render, ejecuta:

```bash
python manage.py createsuperuser
```

**Datos sugeridos:**
- Username: `admin`
- Email: `admin@uleam.edu.ec`
- Password: `[ELIGE UNA CONTRASEÑA SEGURA]`

### 4.3 Verificar Carreras (Opcional)

```bash
python manage.py shell
```

Luego dentro de shell:
```python
from inscripciones.models import Carrera
print(f"Carreras: {Carrera.objects.count()}")
# Debe mostrar: Carreras: 43
exit()
```

---

## 🧪 PASO 5: PROBAR LA APLICACIÓN

### 5.1 URL de tu App

Render te dará una URL como:
```
https://sistema-practicas-uleam.onrender.com
```

### 5.2 Tests Básicos

Verifica lo siguiente:

#### ✅ Página Principal
- Ir a: `https://tu-app.onrender.com/`
- Debe cargar con CSS correcto
- Logo de ULEAM visible
- Menú funcional

#### ✅ Login
- Ir a: `https://tu-app.onrender.com/login/`
- Probar login con superusuario creado
- Debe redirigir al home

#### ✅ Admin Panel
- Ir a: `https://tu-app.onrender.com/admin/`
- Login con superusuario
- Verificar que se vean todos los modelos

#### ✅ Carreras
- En admin, ir a **Carreras**
- Debe haber 43 carreras de ULEAM
- Verificar que tengan código y nombre

#### ✅ Registro
- Ir a: `https://tu-app.onrender.com/registro/`
- Probar registro de estudiante
- Verificar que aparezcan las 43 carreras en el selector

#### ✅ Crear Práctica
- Registrar una empresa (o aprobarla desde admin)
- Crear una práctica
- Verificar que campos "área", "modalidad" y "dirigido a" funcionen

---

## 🔧 CONFIGURACIÓN ADICIONAL OPCIONAL

### Poblar Datos de Prueba

Si quieres datos de ejemplo (empresas, estudiantes, prácticas):

```bash
# En Shell de Render
python poblar_datos_prueba.py
```

Esto creará:
- 3 Facultades
- 5 Estudiantes
- 3 Empresas
- 10 Prácticas

### Configurar Dominio Personalizado (Opcional)

1. En Render → Settings → Custom Domains
2. Agrega: `practicas.uleam.edu.ec`
3. Configura DNS en tu proveedor:
   - CNAME: `practicas` → `sistema-practicas-uleam.onrender.com`

---

## 📊 MONITOREO

### Ver Logs en Tiempo Real

En Render Dashboard:
1. Click en tu servicio
2. Click en **"Logs"**
3. Verás todos los requests y errores

### Comandos Útiles en Shell

```bash
# Ver versión de Python
python --version

# Ver migraciones aplicadas
python manage.py showmigrations

# Ver configuración actual
python manage.py check

# Crear datos de prueba
python manage.py shell
```

---

## 🚨 TROUBLESHOOTING RÁPIDO

### ❌ "Application failed to respond"

**Solución:**
1. Verifica logs en Render
2. Asegúrate de que `DATABASE_URL` sea correcto
3. Revisa que Supabase esté activo

### ❌ CSS no carga

**Solución:**
1. Verifica que `collectstatic` se ejecutó en el build
2. Revisa logs: debe aparecer "Copying static files..."

### ❌ Base de datos vacía

**Solución:**
1. Ejecuta en Shell de Render:
   ```bash
   python manage.py migrate
   python poblar_carreras_uleam.py
   ```

### ⏱️ App tarda en cargar (primera vez)

**Normal** - Plan Free se apaga después de 15 min.
Primera carga: ~50 segundos.

**Solución permanente:**
- Upgrade a plan Starter ($7/mes)
- O usar servicio de ping (cron-job.org)

---

## ✅ CHECKLIST FINAL

Antes de anunciar a usuarios:

- [ ] ✅ App accesible en URL de Render
- [ ] ✅ CSS funcionando correctamente
- [ ] ✅ Login/Registro funcionan
- [ ] ✅ Admin panel accesible con superusuario
- [ ] ✅ 43 Carreras de ULEAM verificadas
- [ ] ✅ Crear práctica funciona (empresa)
- [ ] ✅ Crear práctica interna funciona (facultad)
- [ ] ✅ Inscribirse a práctica funciona (estudiante)
- [ ] ✅ Evaluar postulante funciona (empresa/facultad)
- [ ] ✅ Chatbot responde (si OpenAI configurado)
- [ ] ✅ Documentos se suben correctamente
- [ ] ✅ Emails funcionan (o Console backend funciona)

---

## 🎉 ¡LISTO PARA PRODUCCIÓN!

Tu Sistema de Prácticas Preprofesionales de ULEAM está desplegado.

**URL:** `https://sistema-practicas-uleam.onrender.com`

**Credenciales Admin:**
- Usuario: `admin`
- Password: La que elegiste

**Compartir con:**
- ✅ Estudiantes y egresados → Pueden registrarse directamente
- ✅ Empresas → Requieren aprobación del admin
- ✅ Facultades → Requieren aprobación del admin
- ✅ Administradores → Acceso al panel `/admin/`

---

**¿Necesitas ayuda?**
- Revisa `DESPLIEGUE_RENDER.md` para guía detallada
- Revisa `CUMPLIMIENTO_RETO_1.md` para funcionalidades
- Contacta soporte de Render: https://render.com/docs

---

**Sistema Desarrollado por:** GitHub Copilot  
**Fecha:** 7 de Noviembre de 2025  
**Versión:** 2.0 - Producción Ready  
**Stack:** Django 5.2.7 + PostgreSQL (Supabase) + OpenAI + Render
