# 🚀 Configuración de Render con Supabase

Esta guía te ayudará a configurar correctamente tu aplicación Django con Supabase en Render.

## 📋 Prerequisitos

✅ Cuenta en [Render.com](https://render.com)  
✅ Cuenta en [Supabase](https://supabase.com)  
✅ Código en GitHub  
✅ Base de datos PostgreSQL en Supabase

---

## 🔧 Paso 1: Obtener Credenciales de Supabase

### 1.1 Ir a tu Proyecto Supabase

1. Entra a [supabase.com](https://supabase.com)
2. Selecciona tu proyecto: **owrgthzfdlnhkiwzdgbd**
3. Ve a **Settings** ⚙️ (menú izquierdo)

### 1.2 Copiar Credenciales de Base de Datos

Ve a **Settings** → **Database**:

```
Host: aws-0-us-east-1.pooler.supabase.com
Database: postgres
Port: 6543
User: postgres.owrgthzfdlnhkiwzdgbd
Password: Milxi26.
```

⚠️ **IMPORTANTE:** Usa el **Connection Pooler** (puerto 6543) en lugar del puerto directo (5432)

### 1.3 Copiar API Keys

Ve a **Settings** → **API**:

```
Project URL: https://owrgthzfdlnhkiwzdgbd.supabase.co
anon/public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🌐 Paso 2: Crear Web Service en Render

### 2.1 Nuevo Proyecto

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub: **Mildreth-SC/nuevo-prueba**
4. Click en **"Connect"**

### 2.2 Configuración Básica

```
Name: sistema-practicas
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Build Command: bash build.sh
Start Command: gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT
Instance Type: Free
```

---

## 🔐 Paso 3: Variables de Entorno

En la sección **Environment Variables**, agrega estas 10 variables:

| Key | Value | Descripción |
|-----|-------|-------------|
| `SECRET_KEY` | (auto-generada) | Render puede generarla automáticamente |
| `DEBUG` | `False` | Siempre False en producción |
| `ALLOWED_HOSTS` | `.onrender.com,localhost` | Hosts permitidos |
| `DB_NAME` | `postgres` | Nombre de la base de datos |
| `DB_USER` | `postgres.owrgthzfdlnhkiwzdgbd` | Usuario de Supabase (con prefijo postgres.) |
| `DB_PASSWORD` | `Milxi26.` | Tu contraseña de Supabase |
| `DB_HOST` | `aws-0-us-east-1.pooler.supabase.com` | Host del Connection Pooler |
| `DB_PORT` | `6543` | Puerto del Connection Pooler |
| `SUPABASE_URL` | `https://owrgthzfdlnhkiwzdgbd.supabase.co` | URL de tu proyecto |
| `SUPABASE_KEY` | `eyJhbG...` | Tu clave anon/public |

### Cómo Agregar Variables:

1. Haz clic en **"Add Environment Variable"**
2. Ingresa **Key** y **Value**
3. Repite para cada variable
4. Click en **"Save Changes"**

---

## 🚀 Paso 4: Desplegar

1. Click en **"Create Web Service"**
2. Render comenzará a construir tu aplicación
3. Espera 5-10 minutos
4. ✅ Tu app estará disponible en: `https://sistema-practicas.onrender.com`

---

## 🔍 Verificar el Despliegue

### Ver Logs en Tiempo Real:

1. En tu servicio de Render, ve a la pestaña **"Logs"**
2. Verás el proceso de build y deploy
3. Busca mensajes como:
   ```
   ✓ Installing dependencies
   ✓ Running collectstatic
   ✓ Running migrations
   ✓ Starting server
   ```

### Probar la Aplicación:

1. Visita tu URL: `https://sistema-practicas.onrender.com`
2. Intenta hacer login
3. Verifica que puedes ver las prácticas disponibles

---

## 🐛 Solución de Problemas

### Error: "Network is unreachable"

**Causa:** No estás usando el Connection Pooler de Supabase

**Solución:**
- Asegúrate que `DB_HOST` sea: `aws-0-us-east-1.pooler.supabase.com`
- Asegúrate que `DB_PORT` sea: `6543`
- Asegúrate que `DB_USER` tenga el prefijo: `postgres.owrgthzfdlnhkiwzdgbd`

### Error: "relation does not exist"

**Causa:** Las migraciones no se ejecutaron

**Solución:**
1. Ve a tu servicio en Render
2. Click en **"Shell"** (terminal)
3. Ejecuta:
   ```bash
   python manage.py migrate
   ```

### Error: "Server Error (500)"

**Causa:** Variables de entorno mal configuradas

**Solución:**
1. Ve a **Environment** en Render
2. Verifica que todas las 10 variables estén correctas
3. Click en **"Manual Deploy"** → **"Deploy latest commit"**

### Error: "Application failed to respond"

**Causa:** Puerto incorrecto en el comando de inicio

**Solución:**
Verifica que el Start Command sea:
```
gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🔄 Actualizaciones Automáticas

Una vez configurado, cada vez que hagas `git push` a `main`:

1. ✅ Render detecta el cambio automáticamente
2. ✅ Ejecuta el build.sh
3. ✅ Despliega la nueva versión
4. ✅ Tu aplicación se actualiza sin intervención manual

---

## 📊 Limitaciones del Plan Gratuito de Render

- ⏱️ El servicio "duerme" después de 15 minutos de inactividad
- 🔄 Primera petición después de dormir tarda ~30 segundos
- 💾 750 horas/mes de uso (suficiente para proyectos personales)
- 🌐 100GB de bandwidth/mes

---

## ✅ Checklist Final

Antes de dar por terminado el despliegue, verifica:

- [ ] Las 10 variables de entorno están configuradas
- [ ] El build terminó sin errores
- [ ] La aplicación responde en la URL de Render
- [ ] Puedes hacer login correctamente
- [ ] Las prácticas se muestran correctamente
- [ ] Los archivos estáticos (CSS, JS, imágenes) cargan bien

---

## 🆘 Soporte Adicional

Si tienes problemas:

1. **Logs de Render:** Ve a la pestaña "Logs" para ver errores en tiempo real
2. **Shell de Render:** Usa el terminal para ejecutar comandos de Django
3. **Documentación:** [docs.render.com](https://docs.render.com)

---

**¡Tu aplicación ahora está lista para producción!** 🎉

Última actualización: Noviembre 2025
