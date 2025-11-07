# 🔐 Sistema de Autenticación con Supabase Auth - IMPLEMENTADO

## ✅ Lo que ya está hecho

### 1. **Cliente de Supabase Auth** (`inscripciones/supabase_client.py`)
Cliente completo para gestionar autenticación usando Supabase Auth:

#### Métodos disponibles:
- **`signup(email, password, user_metadata)`** - Registra nuevo usuario
- **`signin(email, password)`** - Inicia sesión
- **`signout()`** - Cierra sesión
- **`send_password_reset_email(email)`** - Envía email de recuperación
- **`update_password(new_password, access_token)`** - Actualiza contraseña
- **`get_user(access_token)`** - Obtiene información del usuario
- **`refresh_session(refresh_token)`** - Refresca la sesión

### 2. **Middleware de sincronización** (`inscripciones/middleware.py`)
Middleware que conecta Supabase Auth con Django:

#### Funcionalidades:
- ✅ Lee `access_token` y `refresh_token` de la sesión de Django
- ✅ Verifica validez del token en cada request
- ✅ Sincroniza usuario de Supabase con Django User
- ✅ Refresca tokens expirados automáticamente
- ✅ Cierra sesión si los tokens son inválidos

### 3. **Vistas de autenticación actualizadas** (`inscripciones/auth_views.py`)
Nuevas vistas que usan Supabase Auth:

#### Vistas implementadas:
- **`login_view`** - Login con email y contraseña usando Supabase
- **`logout_view`** - Logout de Supabase y Django
- **`registro_estudiante`** - Registro de estudiantes con Supabase
- **`registro_empresa`** - Registro de empresas con Supabase
- **`registro_facultad`** - Registro de facultades con Supabase
- **`solicitar_reset_password`** - Solicitar recuperación de contraseña
- **`reset_password_callback`** - Callback para establecer nueva contraseña
- **`auth_callback`** - Callback para confirmación de email

### 4. **Templates actualizados**
#### `login.html`
- ✅ Cambiado de "username" a "email"
- ✅ Validación de email en el frontend
- ✅ Mensaje informativo sobre confirmación de email

#### `reset_password_supabase.html` (NUEVO)
- ✅ Extrae `access_token` del fragmento de URL con JavaScript
- ✅ Validación de fortaleza de contraseña
- ✅ Verificación de coincidencia de contraseñas
- ✅ Indicador visual de fortaleza (débil/media/fuerte)

### 5. **URLs actualizadas** (`inscripciones/urls.py`)
```python
# Autenticación con Supabase Auth
path('registro/', supabase_auth_views.registro_estudiante, name='registro_estudiante'),
path('registro-empresa/', supabase_auth_views.registro_empresa, name='registro_empresa'),
path('registro-facultad/', supabase_auth_views.registro_facultad, name='registro_facultad'),
path('login/', supabase_auth_views.login_view, name='login'),
path('logout/', supabase_auth_views.logout_view, name='logout'),

# Recuperación de contraseña
path('recuperar-contrasena/', supabase_auth_views.solicitar_reset_password, name='solicitar_restablecimiento_contrasena'),
path('auth/reset-password/', supabase_auth_views.reset_password_callback, name='reset_password_callback'),
path('auth/callback/', supabase_auth_views.auth_callback, name='auth_callback'),
```

### 6. **Settings actualizados** (`sistema_practicas/settings.py`)
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'inscripciones.middleware.SupabaseAuthMiddleware',  # ← Nuevo middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## 📋 LO QUE FALTA: Configurar el Dashboard de Supabase

### Paso 1: Acceder al Dashboard de Supabase

1. Ve a: https://supabase.com/dashboard
2. Inicia sesión con tu cuenta
3. Selecciona tu proyecto: **owrgthzfdlnhkiwzdgbd**

### Paso 2: Activar Email Provider

1. Ve a **Authentication** → **Providers**
2. Busca **Email** en la lista
3. Activa la opción **Enable Email provider**
4. Configura:
   - ✅ **Enable sign up**: Sí (permite nuevos registros)
   - ✅ **Confirm email**: Sí (requiere confirmación de email)
   - ✅ **Secure email change**: Sí (requiere confirmación para cambiar email)

### Paso 3: Configurar Redirect URLs

1. Ve a **Authentication** → **URL Configuration**
2. En **Site URL**, ingresa:
   ```
   http://localhost:8000
   ```
   (Cambiar a tu dominio en producción)

3. En **Redirect URLs**, agrega:
   ```
   http://localhost:8000/auth/callback
   http://localhost:8000/auth/reset-password
   ```

4. Haz clic en **Save**

### Paso 4: Personalizar Templates de Email

1. Ve a **Authentication** → **Email Templates**

#### Template: "Confirm signup"

```html
<h2>¡Bienvenido al Sistema de Prácticas ULEAM!</h2>

<p>Gracias por registrarte. Por favor, confirma tu correo electrónico haciendo clic en el botón de abajo:</p>

<a href="{{ .ConfirmationURL }}" style="display: inline-block; padding: 12px 24px; background-color: #0066CC; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">
  ✅ Confirmar mi correo
</a>

<p>O copia y pega este enlace en tu navegador:</p>
<p>{{ .ConfirmationURL }}</p>

<p>Este enlace expira en 24 horas.</p>

<hr>
<p style="font-size: 0.9em; color: #666;">
  Si no creaste esta cuenta, puedes ignorar este correo.
</p>
```

#### Template: "Reset Password"

```html
<h2>Restablecer tu Contraseña</h2>

<p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>

<p>Haz clic en el botón de abajo para crear una nueva contraseña:</p>

<a href="{{ .ConfirmationURL }}" style="display: inline-block; padding: 12px 24px; background-color: #CC0000; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">
  🔑 Restablecer Contraseña
</a>

<p>O copia y pega este enlace en tu navegador:</p>
<p>{{ .ConfirmationURL }}</p>

<p>Este enlace expira en 1 hora.</p>

<hr>
<p style="font-size: 0.9em; color: #666;">
  Si no solicitaste restablecer tu contraseña, puedes ignorar este correo.
</p>
```

### Paso 5: Configurar SMTP (Opcional - Producción)

Por defecto, Supabase usa su propio servidor SMTP (limitado). Para producción:

1. Ve a **Project Settings** → **Auth**
2. En **SMTP Settings**, configura:
   - **SMTP Host**: smtp.sendgrid.net (o tu proveedor)
   - **SMTP Port**: 587
   - **SMTP User**: apikey
   - **SMTP Pass**: [Tu API Key de SendGrid]
   - **SMTP Sender Name**: Sistema de Prácticas ULEAM
   - **SMTP Sender Email**: noreply@tudominio.com

---

## 🧪 Cómo probar el sistema

### 1. Verificar que todo está configurado

```powershell
# En tu terminal de VS Code
python manage.py check
```

Debería mostrar: **System check identified no issues**

### 2. Probar el flujo de registro

1. **Iniciar servidor**:
   ```powershell
   python manage.py runserver
   ```

2. **Abrir en navegador**: http://localhost:8000/registro/

3. **Registrar un nuevo estudiante**:
   - Nombre: Test
   - Apellido: Usuario
   - Email: test@ejemplo.com
   - Contraseña: Test1234
   - Carrera: (seleccionar una)

4. **Verificar que aparece el mensaje**:
   ```
   ¡Registro exitoso! 📧 Hemos enviado un correo de confirmación a tu email.
   Por favor, revisa tu bandeja de entrada y confirma tu cuenta para poder iniciar sesión.
   ```

5. **Revisar email**:
   - Ve a tu bandeja de entrada (test@ejemplo.com)
   - Abre el email de "Confirm signup"
   - Haz clic en "✅ Confirmar mi correo"
   - Deberías ser redirigido a `/auth/callback` con mensaje de éxito

6. **Intentar login**:
   - Ve a: http://localhost:8000/login/
   - Email: test@ejemplo.com
   - Contraseña: Test1234
   - Deberías iniciar sesión correctamente

### 3. Probar recuperación de contraseña

1. **Ir a recuperar contraseña**: http://localhost:8000/recuperar-contrasena/

2. **Ingresar email**: test@ejemplo.com

3. **Revisar email de recuperación**

4. **Hacer clic en el link del email**

5. **Ingresar nueva contraseña** (mínimo 6 caracteres)

6. **Iniciar sesión con nueva contraseña**

---

## 🔍 Debugging

### Ver logs de Supabase Auth

En el código ya hay logs configurados:

```python
import logging
logger = logging.getLogger(__name__)

# Los logs se mostrarán en la consola del servidor
logger.info("✅ Usuario registrado: {email}")
logger.error("❌ Error en signup: {e}")
```

### Revisar tokens en la sesión

```python
# En la vista, puedes ver:
access_token = request.session.get('supabase_access_token')
refresh_token = request.session.get('supabase_refresh_token')
user_metadata = request.session.get('supabase_user_metadata')
```

### Probar cliente de Supabase directamente

```python
# En Django shell
python manage.py shell

from inscripciones.supabase_client import supabase_auth

# Probar registro
result = supabase_auth.signup(
    email="test@ejemplo.com",
    password="Test1234",
    user_metadata={"nombre": "Test", "rol": "estudiante"}
)
print(result)

# Probar login
result = supabase_auth.signin(
    email="test@ejemplo.com",
    password="Test1234"
)
print(result)
```

---

## ✨ Características Implementadas

### Registro
- ✅ Registro con Supabase Auth
- ✅ Email de confirmación automático
- ✅ Metadata del usuario guardada en Supabase
- ✅ Usuario de Django creado (inactivo hasta confirmar)
- ✅ Perfil creado (Estudiante/Empresa/Facultad)

### Login
- ✅ Login solo con email confirmado
- ✅ Tokens guardados en sesión de Django
- ✅ Middleware sincroniza con Django User
- ✅ Redirección según tipo de usuario

### Recuperación de Contraseña
- ✅ Email automático con link de recuperación
- ✅ Link expira en 1 hora
- ✅ Nueva contraseña con validación de fortaleza
- ✅ Mensaje de seguridad (siempre igual, no revela si el email existe)

### Seguridad
- ✅ Tokens JWT de Supabase
- ✅ Refresh automático de tokens
- ✅ Logout limpia sesiones de Supabase y Django
- ✅ Email debe ser confirmado antes de login
- ✅ CSRF protection de Django

---

## 📚 Referencias

- **Supabase Auth Docs**: https://supabase.com/docs/guides/auth
- **Supabase Python Client**: https://supabase.com/docs/reference/python/introduction
- **Email Templates**: https://supabase.com/docs/guides/auth/auth-email-templates

---

## 🚀 Próximos Pasos

1. ⏳ **Configurar Dashboard de Supabase** (sigue Paso 1-5 arriba)
2. ⏳ **Probar flujo completo de registro y login**
3. ⏳ **Probar recuperación de contraseña**
4. ⏳ **Configurar SMTP en producción** (SendGrid recomendado)
5. ⏳ **Actualizar SITE_URL en settings.py para producción**

---

**¡El sistema está CASI LISTO! Solo falta configurar el dashboard de Supabase y probarlo. 🎉**
