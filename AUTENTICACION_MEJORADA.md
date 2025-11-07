# 🔐 SISTEMA DE AUTENTICACIÓN MEJORADO CON SUPABASE

## ✨ Características Implementadas

### 1. **Verificación de Email**
- ✅ Al registrarse, el usuario recibe un email con un enlace de verificación
- ✅ La cuenta permanece inactiva hasta verificar el email
- ✅ Enlaces de verificación con token seguro que expira en 24 horas

### 2. **Recuperación de Contraseña**
- ✅ Los usuarios pueden solicitar un enlace para restablecer su contraseña
- ✅ Email con instrucciones y enlace seguro con token
- ✅ Validación de contraseñas (mínimo 8 caracteres)

### 3. **Integración con Supabase Auth** (Opcional)
- ✅ Servicio `SupabaseAuthService` para gestión de autenticación
- ✅ Registro y login sincronizado con Supabase Auth
- ✅ Fallback a Django Auth si Supabase no está configurado

---

## 🚀 Configuración

### 1. Configurar Variables de Entorno

Agrega estas variables a tu archivo `.env`:

```env
# Configuración de Email (REQUERIDO para verificación y recuperación)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
DEFAULT_FROM_EMAIL=noreply@sistema-practicas.com

# URL del sitio (para generar enlaces en emails)
SITE_URL=http://localhost:8000

# Supabase (opcional - ya configurado)
SUPABASE_URL=https://owrgthzfdlnhkiwzdgbd.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
```

### 2. Configurar Gmail para enviar emails

#### Opción A: Usar Gmail (Recomendado para desarrollo)

1. **Habilitar autenticación de dos factores** en tu cuenta de Gmail
2. **Generar una contraseña de aplicación**:
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Escribe "Sistema Prácticas ULEAM"
   - Copia la contraseña generada (16 caracteres)
   - Úsala en `EMAIL_HOST_PASSWORD`

**Ejemplo de configuración Gmail:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=mildreth@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Sistema Prácticas ULEAM <noreply@uleam.edu.ec>
```

#### Opción B: Usar Supabase Email (Producción)

Supabase incluye envío de emails. Para usarlo:

1. Ve a tu proyecto en https://supabase.com/dashboard
2. Settings → Project Settings → Auth
3. Configura el SMTP provider o usa el de Supabase
4. Personaliza las plantillas de email (opcional)

#### Opción C: Consola (Solo para pruebas - Default)

Si no configuras EMAIL, los emails se mostrarán en la consola/terminal:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 📋 Nuevas URLs Disponibles

```python
# Registro (ahora con verificación de email)
/registro/                    # Registro estudiante
/registro-empresa/            # Registro empresa
/registro-facultad/           # Registro facultad

# Autenticación
/login/                       # Login (ahora con enlace "¿Olvidaste tu contraseña?")
/logout/                      # Logout

# Verificación de email
/verificar-email/<uid>/<token>/

# Recuperación de contraseña
/recuperar-contrasena/                      # Solicitar enlace
/restablecer-contrasena/<uid>/<token>/      # Establecer nueva contraseña
```

---

## 🎯 Flujo de Registro

### ANTES:
```
Usuario se registra → Cuenta activa → Puede iniciar sesión
```

### AHORA:
```
Usuario se registra 
  ↓
Email de verificación enviado
  ↓
Usuario hace clic en enlace del email
  ↓
Cuenta activada
  ↓
Usuario puede iniciar sesión
```

---

## 🔑 Flujo de Recuperación de Contraseña

```
Usuario hace clic en "¿Olvidaste tu contraseña?"
  ↓
Ingresa su email
  ↓
Recibe email con enlace de restablecimiento
  ↓
Hace clic en el enlace
  ↓
Ingresa nueva contraseña
  ↓
Contraseña actualizada
  ↓
Puede iniciar sesión
```

---

## 📁 Archivos Creados/Modificados

### Nuevos Archivos:

```
inscripciones/
  └── supabase_auth.py                    # Servicio de autenticación

templates/inscripciones/
  ├── solicitar_reset_password.html       # Formulario para solicitar reset
  ├── reset_password.html                 # Formulario para nueva contraseña
  └── emails/
      ├── verificacion_email.html         # Email de verificación
      └── reset_password.html             # Email de recuperación
```

### Archivos Modificados:

```
sistema_practicas/
  └── settings.py                         # Configuración de EMAIL

inscripciones/
  ├── views.py                            # Vistas actualizadas + nuevas vistas
  ├── urls.py                             # Nuevas rutas
  └── templates/
      └── inscripciones/
          └── login.html                  # Agregado enlace "¿Olvidaste tu contraseña?"

requirements.txt                          # Agregado gotrue==2.10.0
```

---

## 🧪 Cómo Probar

### 1. Configurar Email (Desarrollo Local)

```bash
# En .env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 2. Registrar un nuevo usuario

1. Ve a http://localhost:8000/registro/
2. Completa el formulario
3. Haz clic en "Registrarse"
4. **Busca el email en la consola/terminal**
5. Copia el enlace de verificación
6. Pégalo en tu navegador
7. Tu cuenta se activará

### 3. Recuperar Contraseña

1. Ve a http://localhost:8000/login/
2. Haz clic en "¿Olvidaste tu contraseña?"
3. Ingresa tu email
4. **Busca el email en la consola/terminal**
5. Copia el enlace
6. Pégalo en tu navegador
7. Ingresa tu nueva contraseña

---

## 🔒 Seguridad

### Características de Seguridad Implementadas:

✅ **Tokens temporales**: Los enlaces expiran en 24 horas  
✅ **Cuentas inactivas**: Los usuarios deben verificar email antes de acceder  
✅ **Validación de contraseñas**: Mínimo 8 caracteres  
✅ **Mensajes genéricos**: No revela si un email existe o no (seguridad)  
✅ **Tokens seguros**: Usa `default_token_generator` de Django  
✅ **CSRF Protection**: Todos los formularios protegidos  

---

## 📧 Plantillas de Email

Las plantillas de email son totalmente personalizables y están en:

```
templates/inscripciones/emails/
  ├── verificacion_email.html    # Email de bienvenida con verificación
  └── reset_password.html         # Email de recuperación de contraseña
```

**Características de las plantillas:**
- 📱 Responsive (se ven bien en móviles)
- 🎨 Diseño profesional con colores de ULEAM
- ✅ Botón grande para hacer clic fácilmente
- 📋 Enlace de texto alternativo si el botón no funciona
- ⚠️ Instrucciones claras y advertencias de seguridad

---

## 🌐 Configuración para Producción

### 1. Usar Gmail en Producción (No recomendado)

Gmail tiene límites de envío (500 emails/día). Para producción, usa:

### 2. Usar un servicio de Email profesional

Opciones recomendadas:
- **SendGrid**: https://sendgrid.com/ (100 emails/día gratis)
- **Mailgun**: https://www.mailgun.com/ (5,000 emails/mes gratis)
- **Amazon SES**: https://aws.amazon.com/ses/ (62,000 emails/mes gratis)
- **Supabase Email**: Ya incluido en Supabase

### 3. Configuración ejemplo con SendGrid:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=TU_API_KEY_DE_SENDGRID
DEFAULT_FROM_EMAIL=Sistema Prácticas ULEAM <noreply@uleam.edu.ec>
```

### 4. Actualizar SITE_URL en producción:

```env
SITE_URL=https://tu-dominio.onrender.com
```

---

## 🐛 Solución de Problemas

### El email no se envía

**Problema:** Los usuarios no reciben emails

**Soluciones:**
1. Verifica que `EMAIL_BACKEND` esté configurado
2. Revisa `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD`
3. Si usas Gmail, asegúrate de usar contraseña de aplicación
4. Revisa la consola/terminal para ver errores
5. Prueba con `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

### El enlace de verificación no funciona

**Problema:** Error al hacer clic en el enlace

**Soluciones:**
1. Verifica que `SITE_URL` esté configurado correctamente
2. El enlace expira en 24 horas - solicita uno nuevo
3. Asegúrate de copiar el enlace completo

### La cuenta no se activa

**Problema:** El usuario verificó el email pero no puede iniciar sesión

**Soluciones:**
1. Verifica en el admin: http://localhost:8000/admin/auth/user/
2. Asegúrate que `is_active` esté en True
3. Reactiva manualmente si es necesario

---

## ✅ Checklist de Implementación

- [x] Servicio de autenticación Supabase (`supabase_auth.py`)
- [x] Configuración de EMAIL en `settings.py`
- [x] Vistas de verificación de email
- [x] Vistas de recuperación de contraseña
- [x] Templates de email (HTML)
- [x] Templates de formularios (solicitar/resetear)
- [x] URLs configuradas
- [x] Login actualizado con enlace de recuperación
- [x] Registro actualizado para enviar email
- [ ] Configurar EMAIL_HOST_USER y EMAIL_HOST_PASSWORD en `.env`
- [ ] Probar flujo completo de registro
- [ ] Probar flujo completo de recuperación
- [ ] Configurar servicio de email para producción

---

## 📚 Referencias

- [Django Email Configuration](https://docs.djangoproject.com/en/5.2/topics/email/)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [SendGrid Django Integration](https://docs.sendgrid.com/for-developers/sending-email/django)

---

**Fecha de implementación:** 7 de Noviembre de 2025  
**Desarrollador:** GitHub Copilot  
**Versión:** 3.0 - Autenticación Completa con Verificación de Email
