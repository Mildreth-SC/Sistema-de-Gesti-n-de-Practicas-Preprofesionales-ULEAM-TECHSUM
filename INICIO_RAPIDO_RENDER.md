# 🚀 GUÍA RÁPIDA - Deploy en Render con Supabase

## ✅ Archivos Preparados

1. ✅ `render.yaml` - Configuración automática
2. ✅ `build.sh` - Script de construcción
3. ✅ `requirements.txt` - Dependencias Python
4. ✅ `.env.example` - Plantilla de variables de entorno
5. ✅ `CONFIGURACION_RENDER.md` - Guía detallada paso a paso

---

## 🎯 Paso a Paso RÁPIDO

### 1️⃣ Ir a Render (2 minutos)

1. Ve a [https://dashboard.render.com](https://dashboard.render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repo: **Mildreth-SC/nuevo-prueba**
4. Click en **"Connect"**

### 2️⃣ Configuración Automática

Render detectará `render.yaml` y pre-llenará casi todo:

```
✅ Name: sistema-practicas
✅ Build Command: bash build.sh
✅ Start Command: gunicorn sistema_practicas.wsgi:application --bind 0.0.0.0:$PORT
✅ Plan: Free
```

### 3️⃣ Agregar SOLO 3 Variables de Entorno ⚠️

Estas son las ÚNICAS que debes agregar manualmente (las demás ya están en render.yaml):

| Key | Value |
|-----|-------|
| `DB_PASSWORD` | `Milxi26.` |
| `SUPABASE_URL` | `https://owrgthzfdlnhkiwzdgbd.supabase.co` |
| `SUPABASE_KEY` | (tu clave anon/public de Supabase) |

**Cómo obtener SUPABASE_KEY:**
1. Ve a [supabase.com](https://supabase.com) → Tu proyecto
2. **Settings** → **API**
3. Copia la clave **"anon public"**

### 4️⃣ Desplegar

1. Click en **"Create Web Service"**
2. ☕ Espera 5-10 minutos
3. ✅ Tu app estará en: `https://sistema-practicas.onrender.com`

---

## 🔍 Verificar que Funcionó

1. Abre la URL de tu app
2. Intenta hacer login
3. Si ves la página principal → **¡Éxito!** 🎉

---

## 🐛 Si Algo Falla

### Error 500 o "Application Error"

1. Ve a tu servicio en Render
2. Click en pestaña **"Logs"**
3. Busca líneas rojas con errores
4. Verifica que las 3 variables estén bien escritas

### La base de datos no conecta

Verifica estas variables (están en render.yaml, pero revisa):
- `DB_HOST`: `aws-0-us-east-1.pooler.supabase.com`
- `DB_PORT`: `6543`
- `DB_USER`: `postgres.owrgthzfdlnhkiwzdgbd`

---

## 📖 Documentación Completa

Para una guía más detallada con capturas de pantalla:
👉 Abre `CONFIGURACION_RENDER.md`

---

## 💡 Tip Pro

Después del primer despliegue exitoso, cada `git push` actualizará automáticamente tu app en Render.

---

¡Buena suerte! 🚀
