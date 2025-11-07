# 🔐 CONFIGURACIÓN DE SUPABASE AUTH - PASO A PASO

## 📧 Paso 1: Configurar Email Templates en Supabase

### 1.1 Accede a Authentication Settings

Ve a tu dashboard de Supabase:
```
https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/auth/templates
```

### 1.2 Configurar Template de "Confirm signup"

1. Haz clic en **"Confirm signup"**
2. Pega este HTML personalizado para ULEAM:

```html
<h2>🎓 Confirma tu registro - Sistema de Prácticas ULEAM</h2>

<p>¡Hola!</p>

<p>Gracias por registrarte en el <strong>Sistema de Gestión de Prácticas Preprofesionales de la ULEAM</strong>.</p>

<p>Para activar tu cuenta y acceder al sistema, por favor confirma tu correo electrónico haciendo clic en el siguiente enlace:</p>

<p style="text-align: center; margin: 30px 0;">
  <a href="{{ .ConfirmationURL }}" 
     style="background-color: #0d6efd; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
    ✅ Confirmar mi correo electrónico
  </a>
</p>

<p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
<p style="word-break: break-all; background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
  {{ .ConfirmationURL }}
</p>

<p><strong>Importante:</strong></p>
<ul>
  <li>Este enlace expirará en 24 horas</li>
  <li>Si no solicitaste este registro, puedes ignorar este correo</li>
  <li>Tu cuenta no se activará hasta que confirmes tu correo</li>
</ul>

<p>¡Bienvenido a nuestra plataforma!</p>

<p>Saludos,<br>
<strong>Equipo de Prácticas Preprofesionales - ULEAM</strong></p>

<hr>
<p style="font-size: 12px; color: #666;">
  Este es un correo automático, por favor no respondas a este mensaje.<br>
  © 2025 ULEAM - Universidad Laica Eloy Alfaro de Manabí
</p>
```

3. Haz clic en **"Save"**

### 1.3 Configurar Template de "Reset password"

1. Haz clic en **"Reset password"** (o "Magic Link")
2. Pega este HTML:

```html
<h2>🔐 Recuperación de Contraseña - Sistema de Prácticas ULEAM</h2>

<p>¡Hola!</p>

<p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en el Sistema de Gestión de Prácticas Preprofesionales.</p>

<p>Para crear una nueva contraseña, haz clic en el siguiente enlace:</p>

<p style="text-align: center; margin: 30px 0;">
  <a href="{{ .ConfirmationURL }}" 
     style="background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
    🔑 Restablecer mi contraseña
  </a>
</p>

<p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
<p style="word-break: break-all; background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
  {{ .ConfirmationURL }}
</p>

<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 20px 0;">
  <p><strong>⚠️ Importante:</strong></p>
  <ul>
    <li>Este enlace expirará en 24 horas</li>
    <li>Si no solicitaste este cambio, ignora este correo</li>
    <li>Tu contraseña actual seguirá siendo válida hasta que establezcas una nueva</li>
    <li>Nadie de ULEAM te pedirá tu contraseña por correo o teléfono</li>
  </ul>
</div>

<p>Si necesitas ayuda, contacta al administrador del sistema.</p>

<p>Saludos,<br>
<strong>Equipo de Prácticas Preprofesionales - ULEAM</strong></p>

<hr>
<p style="font-size: 12px; color: #666;">
  Este es un correo automático, por favor no respondas a este mensaje.<br>
  © 2025 ULEAM - Universidad Laica Eloy Alfaro de Manabí
</p>
```

3. Haz clic en **"Save"**

---

## ⚙️ Paso 2: Configurar SMTP en Supabase

### 2.1 Ir a SMTP Settings

En el mismo dashboard, ve a la pestaña **"SMTP Settings"**

### 2.2 Hacer clic en "Set up SMTP"

Elige una de estas opciones:

#### Opción A: Gmail (Rápido - 5 min)

```
Sender name: Sistema de Prácticas ULEAM
Sender email: guanoluisamildreth@gmail.com
Host: smtp.gmail.com
Port number: 587
Username: guanoluisamildreth@gmail.com
Password: [Contraseña de aplicación de 16 caracteres]
```

**Para obtener la contraseña:**
1. Ve a https://myaccount.google.com/apppasswords
2. Genera una contraseña de aplicación
3. Cópiala y pégala

#### Opción B: SendGrid (Profesional - 10 min)

```
Sender name: Sistema de Prácticas ULEAM
Sender email: practicas@uleam.edu.ec
Host: smtp.sendgrid.net
Port number: 587
Username: apikey
Password: [Tu API Key de SendGrid]
```

**Para obtener el API Key:**
1. Regístrate en https://signup.sendgrid.com/
2. Ve a Settings → API Keys
3. Create API Key → Full Access
4. Copia el API Key

### 2.3 Guardar y probar

1. Haz clic en **"Save"**
2. Haz clic en **"Send test email"**
3. Ingresa tu email y verifica que llegue

---

## 🔗 Paso 3: Configurar URLs de redirección

### 3.1 URL Settings

Ve a **Authentication → URL Configuration**

### 3.2 Site URL

```
Para desarrollo: http://localhost:8000
Para producción: https://tu-dominio.onrender.com
```

### 3.3 Redirect URLs

Agrega estas URLs permitidas:
```
http://localhost:8000/**
https://tu-dominio.onrender.com/**
```

---

## ✅ Paso 4: Verificar configuración

### 4.1 En Authentication → Providers

Verifica que esté activo:
- ✅ Enable email signup
- ✅ Confirm email
- ✅ Enable email provider

### 4.2 Probar registro manual

1. Ve a Authentication → Users
2. Haz clic en "Add user"
3. Ingresa un email de prueba
4. Verifica que llegue el email de confirmación

---

## 📝 Notas importantes

1. **Templates personalizados**: Los que agregamos arriba tienen el diseño de ULEAM
2. **SMTP configurado**: Ahora Supabase enviará emails reales
3. **URL de redirección**: Importante para que los enlaces funcionen
4. **Confirmación obligatoria**: Los usuarios DEBEN confirmar su email antes de acceder

---

## 🚀 Siguiente paso

Una vez configurado todo en Supabase Dashboard, continuaremos con:
1. Actualizar el código de Django
2. Integrar Supabase Auth en las vistas
3. Probar el flujo completo

¿Ya configuraste los templates y SMTP en Supabase?
