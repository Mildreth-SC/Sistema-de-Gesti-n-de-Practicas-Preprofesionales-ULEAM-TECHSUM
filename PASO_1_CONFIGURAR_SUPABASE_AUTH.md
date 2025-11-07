# 🔐 CONFIGURAR SUPABASE AUTH - PASO A PASO

## 📋 PASO 1: Activar Email Provider

1. **Ve a tu Dashboard de Supabase:**
   ```
   https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/auth/providers
   ```

2. **Busca "Email" en la lista de providers**

3. **Activa las siguientes opciones:**
   - ✅ **Enable email provider** (Habilitar proveedor de email)
   - ✅ **Enable email confirmations** (Confirmar email)
   - ✅ **Secure email change** (Cambio seguro de email)
   - ⚠️ **Desactiva** "Double confirm email changes" (para simplificar)

4. **Haz clic en "Save"**

---

## 📧 PASO 2: Configurar Template de Confirmación

1. **Ve a Email Templates:**
   ```
   https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/auth/templates
   ```

2. **Selecciona "Confirm signup"**

3. **Reemplaza el contenido con este template personalizado:**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #0d6efd;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .content {
            background-color: #f4f4f4;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background-color: #0d6efd;
            color: white !important;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Sistema de Prácticas ULEAM</h1>
    </div>
    <div class="content">
        <h2>¡Confirma tu registro!</h2>
        
        <p>Gracias por registrarte en el Sistema de Gestión de Prácticas Preprofesionales de la ULEAM.</p>
        
        <p>Para activar tu cuenta, por favor haz clic en el siguiente botón:</p>
        
        <div style="text-align: center;">
            <a href="{{ .ConfirmationURL }}" class="button">✅ Confirmar mi correo electrónico</a>
        </div>
        
        <p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
        <p style="word-break: break-all; background-color: white; padding: 10px; border-radius: 5px;">
            {{ .ConfirmationURL }}
        </p>
        
        <p><strong>Importante:</strong></p>
        <ul>
            <li>Este enlace expirará en 24 horas</li>
            <li>Si no solicitaste este registro, puedes ignorar este correo</li>
            <li>Tu cuenta no se activará hasta que verifiques tu correo</li>
        </ul>
        
        <p>¡Bienvenido a nuestra plataforma!</p>
        
        <p>Saludos,<br>
        <strong>Equipo de Prácticas Preprofesionales - ULEAM</strong></p>
    </div>
    <div class="footer">
        <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
        <p>&copy; 2025 ULEAM - Universidad Laica Eloy Alfaro de Manabí</p>
    </div>
</body>
</html>
```

4. **Haz clic en "Save"**

---

## 🔑 PASO 3: Configurar Template de Recuperación de Contraseña

1. **Selecciona "Magic Link" o "Reset Password"**

2. **Reemplaza con este template:**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #dc3545;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .content {
            background-color: #f4f4f4;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }
        .button {
            display: inline-block;
            padding: 12px 30px;
            background-color: #dc3545;
            color: white !important;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }
        .warning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔐 Recuperación de Contraseña</h1>
    </div>
    <div class="content">
        <h2>Restablece tu contraseña</h2>
        
        <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en el Sistema de Prácticas ULEAM.</p>
        
        <p>Para crear una nueva contraseña, haz clic en el siguiente botón:</p>
        
        <div style="text-align: center;">
            <a href="{{ .ConfirmationURL }}" class="button">🔑 Restablecer mi contraseña</a>
        </div>
        
        <p>Si el botón no funciona, copia y pega este enlace:</p>
        <p style="word-break: break-all; background-color: white; padding: 10px; border-radius: 5px;">
            {{ .ConfirmationURL }}
        </p>
        
        <div class="warning">
            <p><strong>⚠️ Importante:</strong></p>
            <ul>
                <li>Este enlace expirará en 1 hora</li>
                <li>Si no solicitaste este cambio, ignora este correo</li>
                <li>Tu contraseña actual seguirá siendo válida</li>
                <li>Nadie de ULEAM te pedirá tu contraseña por correo</li>
            </ul>
        </div>
        
        <p>Saludos,<br>
        <strong>Equipo de Prácticas ULEAM</strong></p>
    </div>
</body>
</html>
```

3. **Haz clic en "Save"**

---

## 🌐 PASO 4: Configurar URL de Redirección

1. **Ve a Authentication → URL Configuration:**
   ```
   https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/auth/url-configuration
   ```

2. **Agrega estas URLs:**

   **Site URL:**
   ```
   http://localhost:8000
   ```

   **Redirect URLs (una por línea):**
   ```
   http://localhost:8000/verificar-email/*
   http://localhost:8000/auth/callback
   http://localhost:8000/restablecer-contrasena/*
   http://127.0.0.1:8000/verificar-email/*
   http://127.0.0.1:8000/auth/callback
   http://127.0.0.1:8000/restablecer-contrasena/*
   ```

3. **Para producción, agrega también:**
   ```
   https://tu-dominio.onrender.com/verificar-email/*
   https://tu-dominio.onrender.com/auth/callback
   https://tu-dominio.onrender.com/restablecer-contrasena/*
   ```

---

## ✅ PASO 5: Verificar Configuración

1. **Ve a Settings → API:**
   ```
   https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/settings/api
   ```

2. **Copia estos valores (los necesitarás):**
   - ✅ Project URL
   - ✅ anon/public key
   - ✅ service_role key (¡manténlo secreto!)

---

## 🧪 PASO 6: Probar Email Provider

1. **Ve a Authentication → Users**

2. **Haz clic en "Invite user"**

3. **Ingresa un email de prueba**

4. **Verifica que el email llegue con el template correcto**

---

## 📋 Checklist de Configuración

- [ ] Email provider activado
- [ ] Email confirmations habilitada
- [ ] Template "Confirm signup" personalizado
- [ ] Template "Reset password" personalizado
- [ ] Site URL configurada
- [ ] Redirect URLs agregadas
- [ ] API keys copiadas
- [ ] Email de prueba enviado y recibido

---

**Siguiente paso:** Una vez completado esto, actualizaremos el código de Django para usar Supabase Auth.

**Fecha:** 7 de Noviembre de 2025  
**Sistema:** ULEAM Prácticas v3.0 con Supabase Auth
