# 📧 GUÍA RÁPIDA - CONFIGURACIÓN DE EMAIL PARA AUTENTICACIÓN

## 🚀 Configuración Rápida (5 minutos)

### Opción 1: Modo Consola (Para pruebas inmediatas - SIN configurar nada)

**Ya está configurado por defecto.** Los emails se mostrarán en la terminal.

```bash
# En .env (o déjalo sin configurar)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

✅ **Ventaja:** No requiere configuración  
❌ **Desventaja:** No envía emails reales

---

### Opción 2: Gmail (Para desarrollo - 5 minutos)

#### Paso 1: Habilitar autenticación de 2 pasos

1. Ve a: https://myaccount.google.com/security
2. Busca "Verificación en dos pasos"
3. Actívala

#### Paso 2: Generar contraseña de aplicación

1. Ve a: https://myaccount.google.com/apppasswords
2. En "Seleccionar app" → Elige "Correo"
3. En "Seleccionar dispositivo" → Elige "Otro" y escribe "Sistema Prácticas ULEAM"
4. Haz clic en "Generar"
5. **Copia la contraseña de 16 caracteres** (ejemplo: `abcd efgh ijkl mnop`)

#### Paso 3: Configurar .env

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Sistema Prácticas ULEAM <noreply@uleam.edu.ec>
SITE_URL=http://localhost:8000
```

✅ **Ventaja:** Fácil de configurar  
⚠️ **Limitación:** 500 emails/día

---

### Opción 3: SendGrid (Para producción - 10 minutos)

#### Paso 1: Crear cuenta

1. Ve a: https://signup.sendgrid.com/
2. Regístrate (gratis hasta 100 emails/día)

#### Paso 2: Verificar email y crear API Key

1. Verifica tu email
2. Ve a: Settings → API Keys
3. Haz clic en "Create API Key"
4. Nombre: "Sistema Prácticas ULEAM"
5. Permisos: "Full Access"
6. **Copia el API Key** (solo se muestra una vez)

#### Paso 3: Configurar .env

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.tu_api_key_aqui
DEFAULT_FROM_EMAIL=Sistema Prácticas ULEAM <noreply@uleam.edu.ec>
SITE_URL=https://tu-dominio.onrender.com
```

✅ **Ventaja:** Profesional, 100 emails/día gratis  
✅ **Ideal para:** Producción

---

## 🧪 Probar el Sistema

### 1. Verificar configuración

```bash
python test_autenticacion.py
```

### 2. Iniciar servidor

```bash
python manage.py runserver
```

### 3. Probar registro

1. Ve a: http://localhost:8000/registro/
2. Completa el formulario
3. Haz clic en "Registrarse"
4. **IMPORTANTE:** 
   - Si usas **consola**: Busca el enlace en la terminal
   - Si usas **Gmail/SendGrid**: Revisa tu bandeja de entrada

### 4. Verificar email

- Copia el enlace de verificación
- Pégalo en tu navegador
- Tu cuenta se activará

### 5. Probar recuperación de contraseña

1. Ve a: http://localhost:8000/login/
2. Haz clic en "¿Olvidaste tu contraseña?"
3. Ingresa tu email
4. Busca el enlace (terminal o email)
5. Crea tu nueva contraseña

---

## 🐛 Solución de Problemas Comunes

### Error: "SMTPAuthenticationError"

**Causa:** Contraseña incorrecta o autenticación de 2 pasos no habilitada

**Solución:**
1. Verifica que hayas habilitado la autenticación de 2 pasos
2. Genera una nueva contraseña de aplicación
3. Copia y pega exactamente (con espacios)

### Error: "Connection refused"

**Causa:** Firewall bloqueando puerto 587

**Solución:**
1. Prueba con `EMAIL_PORT=465` y `EMAIL_USE_SSL=True`
2. O desactiva temporalmente el firewall

### Los emails no llegan (Gmail)

**Causa:** Gmail puede bloquear inicialmente

**Solución:**
1. Revisa la carpeta de spam
2. Ve a: https://accounts.google.com/DisplayUnlockCaptcha
3. Intenta enviar otro email

### El enlace de verificación no funciona

**Causa:** `SITE_URL` no está configurado correctamente

**Solución:**
```env
# Desarrollo local:
SITE_URL=http://localhost:8000

# Producción:
SITE_URL=https://tu-dominio.onrender.com
```

---

## 📊 Comparación de Opciones

| Característica | Consola | Gmail | SendGrid |
|---------------|---------|-------|----------|
| Configuración | ✅ 0 min | ⚠️ 5 min | ⚠️ 10 min |
| Emails reales | ❌ No | ✅ Sí | ✅ Sí |
| Límite diario | ∞ | 500 | 100 (gratis) |
| Para desarrollo | ✅ Ideal | ✅ Bueno | ⚠️ Excesivo |
| Para producción | ❌ No | ⚠️ Limitado | ✅ Ideal |
| Costo | Gratis | Gratis | Gratis/Pago |

---

## ✅ Checklist Final

Antes de pasar a producción:

- [ ] Configurar email (Gmail o SendGrid)
- [ ] Probar registro completo
- [ ] Probar verificación de email
- [ ] Probar recuperación de contraseña
- [ ] Actualizar `SITE_URL` en producción
- [ ] Verificar que `SECRET_KEY` es segura
- [ ] Configurar `ALLOWED_HOSTS` correctamente
- [ ] Establecer `DEBUG=False` en producción

---

## 📞 Soporte

Si tienes problemas:

1. Lee `AUTENTICACION_MEJORADA.md`
2. Revisa `.env.example`
3. Ejecuta `python test_autenticacion.py`
4. Verifica la consola/terminal para errores

---

**Creado:** 7 de Noviembre de 2025  
**Versión:** 3.0 - Autenticación con Verificación de Email
