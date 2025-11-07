# 🚀 INICIO RÁPIDO - Supabase Auth

## ✅ Lo que ya está implementado

**¡El código está 100% completo!** Solo falta configurar el Dashboard de Supabase.

### Archivos creados/modificados:

1. **`inscripciones/supabase_client.py`** - Cliente de Supabase Auth
2. **`inscripciones/middleware.py`** - Middleware de sincronización
3. **`inscripciones/auth_views.py`** - Vistas de autenticación
4. **`inscripciones/urls.py`** - URLs actualizadas
5. **`sistema_practicas/settings.py`** - Middleware agregado
6. **`templates/inscripciones/login.html`** - Login con email
7. **`templates/inscripciones/reset_password_supabase.html`** - Reset con Supabase

---

## 🎯 Configuración en 3 pasos

### PASO 1: Configurar Dashboard de Supabase (5 minutos)

Ve a: https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd

#### 1.1 Activar Email Provider
- **Authentication** → **Providers** → **Email**
- ✅ Enable Email provider
- ✅ Confirm email
- ✅ Save

#### 1.2 Configurar Redirect URLs
- **Authentication** → **URL Configuration**
- **Site URL**: `http://localhost:8000`
- **Redirect URLs**:
  ```
  http://localhost:8000/auth/callback
  http://localhost:8000/auth/reset-password
  ```
- ✅ Save

#### 1.3 Personalizar Email Templates (Opcional)
- **Authentication** → **Email Templates**
- Editar "Confirm signup" y "Reset Password"
- Ver: `PASO_1_CONFIGURAR_SUPABASE_AUTH.md` para templates completos

---

### PASO 2: Probar el sistema (2 minutos)

```powershell
# 1. Verificar configuración
python manage.py check

# 2. Ejecutar script de prueba
python test_supabase_auth_integration.py

# 3. Iniciar servidor
python manage.py runserver
```

---

### PASO 3: Probar en el navegador (3 minutos)

1. **Registro**: http://localhost:8000/registro/
   - Registra un nuevo estudiante
   - Verás: "📧 Hemos enviado un correo de confirmación"

2. **Confirmar Email**:
   - Abre tu bandeja de entrada
   - Haz clic en "Confirmar mi correo"
   - Serás redirigido a `/auth/callback`

3. **Login**: http://localhost:8000/login/
   - Email: tu_email@ejemplo.com
   - Contraseña: la que usaste
   - ✅ Deberías iniciar sesión correctamente

4. **Recuperar Contraseña**: http://localhost:8000/recuperar-contrasena/
   - Ingresa tu email
   - Revisa tu correo
   - Haz clic en el link
   - Establece nueva contraseña

---

## 🔍 Verificar que funciona

### ✅ Señales de éxito:

1. **Al registrarse**:
   ```
   ¡Registro exitoso! 📧 Hemos enviado un correo de confirmación a tu email.
   ```

2. **En el email**:
   - Asunto: "Confirm your signup"
   - Botón: "Confirmar mi correo"

3. **Al confirmar**:
   ```
   ✅ ¡Tu email ha sido confirmado exitosamente!
   Ahora puedes iniciar sesión con tus credenciales.
   ```

4. **Al hacer login**:
   - Redirige a la página principal
   - Muestra tu nombre en el navbar
   - Puedes acceder a tu perfil

### ❌ Posibles errores:

#### Error: "Supabase Auth no está configurado"
**Solución**: Verifica `.env`:
```env
SUPABASE_URL=https://owrgthzfdlnhkiwzdgbd.supabase.co
SUPABASE_KEY=tu_anon_key
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key
```

#### Error: "Email not confirmed"
**Solución**: 
- Es NORMAL antes de confirmar el email
- Revisa tu bandeja de entrada
- Confirma el email y vuelve a intentar

#### Error: "Invalid login credentials"
**Solución**:
- Verifica email y contraseña
- Asegúrate de haber confirmado el email
- La contraseña debe tener mínimo 6 caracteres

---

## 📧 Configuración de Email para Producción

### Opción 1: SMTP de Supabase (Por defecto)
- ✅ Ya está configurado
- ⚠️ Limitado a 3 emails/hora en plan gratuito
- 📧 Funciona para desarrollo

### Opción 2: SendGrid (Recomendado para producción)

1. **Crear cuenta en SendGrid**: https://signup.sendgrid.com/

2. **Obtener API Key**:
   - Dashboard → Settings → API Keys
   - Create API Key → Full Access

3. **Configurar en Supabase**:
   - Project Settings → Auth → SMTP Settings
   - Host: `smtp.sendgrid.net`
   - Port: `587`
   - User: `apikey`
   - Pass: `tu_api_key_de_sendgrid`
   - Sender: `noreply@tudominio.com`

4. **Verificar dominio**:
   - SendGrid → Settings → Sender Authentication
   - Verificar dominio o email

---

## 🎨 Personalización

### Cambiar colores en emails
Edita los templates en:
**Authentication** → **Email Templates**

### Cambiar tiempo de expiración
- **Confirmación de email**: 24 horas (por defecto)
- **Reset de contraseña**: 1 hora (por defecto)
- No configurable desde el código, se maneja en Supabase

### Agregar más campos al registro
Modifica `auth_views.py`:
```python
user_metadata = {
    'nombre': form.cleaned_data['first_name'],
    'apellido': form.cleaned_data['last_name'],
    'rol': 'estudiante',
    'nuevo_campo': form.cleaned_data['nuevo_campo'],  # ← Agregar aquí
}
```

---

## 📚 Documentación Completa

- **`SUPABASE_AUTH_COMPLETO.md`** - Documentación completa del sistema
- **`PASO_1_CONFIGURAR_SUPABASE_AUTH.md`** - Guía detallada del dashboard
- **`test_supabase_auth_integration.py`** - Script de prueba

---

## 🆘 Soporte

### Logs del sistema
Ver en la consola del servidor:
```
✅ Usuario registrado: email@ejemplo.com
📧 Email de confirmación enviado automáticamente por Supabase
```

### Django Admin
Para gestión manual de usuarios:
http://localhost:8000/admin/

### Supabase Dashboard
Ver usuarios registrados:
https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/auth/users

---

## ✨ Características

- ✅ Registro con confirmación de email
- ✅ Login solo con email confirmado
- ✅ Recuperación de contraseña por email
- ✅ Tokens JWT seguros
- ✅ Refresh automático de tokens
- ✅ Sincronización Django ↔ Supabase
- ✅ Metadata personalizada por usuario
- ✅ Emails HTML personalizables
- ✅ Validación de fortaleza de contraseña
- ✅ Mensajes de error claros

---

**¡Listo para usar! 🎉**

¿Necesitas ayuda? Revisa `SUPABASE_AUTH_COMPLETO.md` para más detalles.
