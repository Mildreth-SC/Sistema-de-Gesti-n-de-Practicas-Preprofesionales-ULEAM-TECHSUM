"""
Guía interactiva para configurar SMTP de Supabase
Te ayuda a obtener las credenciales necesarias
"""

print("""
╔═══════════════════════════════════════════════════════════════╗
║  📧 CONFIGURACIÓN DE SMTP CON SUPABASE - GUÍA PASO A PASO    ║
╚═══════════════════════════════════════════════════════════════╝

Voy a ayudarte a configurar el envío de emails usando Supabase.

═══════════════════════════════════════════════════════════════

🎯 PASO 1: Obtener Service Role Key de Supabase
═══════════════════════════════════════════════════════════════

1. Abre tu navegador y ve a:
   
   🌐 https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/settings/api

2. En la sección "Project API keys", verás dos keys:
   
   ✅ anon / public (ya lo tienes configurado)
   🔑 service_role (este es el que necesitas)

3. Haz clic en el ícono del ojo 👁️ en "service_role" para revelarlo

4. Haz clic en el ícono de copiar 📋 para copiarlo

⚠️  IMPORTANTE: Este key es SECRETO. NUNCA lo compartas ni lo subas a GitHub.

═══════════════════════════════════════════════════════════════
""")

service_key = input("📋 Pega aquí tu SUPABASE_SERVICE_ROLE_KEY (o presiona Enter para configurar después): ").strip()

print("""
═══════════════════════════════════════════════════════════════

🎯 PASO 2: Elegir método de envío de emails
═══════════════════════════════════════════════════════════════

Tienes 2 opciones:

OPCIÓN A: SMTP Interno de Supabase (Más fácil - 5 min)
   ✅ No requiere configuración adicional
   ✅ Usa el service role key que acabas de copiar
   ⚠️  Tiene límites de rate (no ideal para producción)
   
OPCIÓN B: SMTP Personalizado via Supabase (Recomendado - 10 min)
   ✅ Puedes usar SendGrid, Gmail, etc.
   ✅ Sin límites (según tu proveedor)
   ✅ Profesional para producción
   ⚠️  Requiere configurar en el dashboard de Supabase

═══════════════════════════════════════════════════════════════
""")

opcion = input("¿Qué opción prefieres? (A/B): ").strip().upper()

if opcion == 'A':
    print("""
═══════════════════════════════════════════════════════════════

✅ OPCIÓN A SELECCIONADA: SMTP Interno de Supabase
═══════════════════════════════════════════════════════════════

🎯 PASO 3: Configurar .env
═══════════════════════════════════════════════════════════════

Voy a generar la configuración para tu archivo .env:
""")
    
    if service_key:
        print(f"""
# ====================================
# EMAIL CONFIGURATION - SUPABASE SMTP INTERNO
# ====================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.supabase.io
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD={service_key}
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <noreply@owrgthzfdlnhkiwzdgbd.supabase.co>
SITE_URL=http://localhost:8000

# Supabase Service Role Key
SUPABASE_SERVICE_ROLE_KEY={service_key}
""")
    else:
        print("""
# ====================================
# EMAIL CONFIGURATION - SUPABASE SMTP INTERNO
# ====================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.supabase.io
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu_supabase_service_role_key_aqui
DEFAULT_FROM_EMAIL=Sistema de Prácticas ULEAM <noreply@owrgthzfdlnhkiwzdgbd.supabase.co>
SITE_URL=http://localhost:8000

# Supabase Service Role Key
SUPABASE_SERVICE_ROLE_KEY=tu_supabase_service_role_key_aqui
""")
    
    print("""
═══════════════════════════════════════════════════════════════

📝 INSTRUCCIONES:

1. Abre el archivo .env en la raíz del proyecto
2. COMENTA estas líneas (agrega # al inicio):
   #EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   #SITE_URL=http://localhost:8000

3. AGREGA las líneas de arriba en tu .env

4. GUARDA el archivo

═══════════════════════════════════════════════════════════════
""")

elif opcion == 'B':
    print("""
═══════════════════════════════════════════════════════════════

✅ OPCIÓN B SELECCIONADA: SMTP Personalizado
═══════════════════════════════════════════════════════════════

🎯 PASO 3: Configurar SMTP en Supabase Dashboard
═══════════════════════════════════════════════════════════════

1. Ve a tu Dashboard de Supabase:
   
   🌐 https://supabase.com/dashboard/project/owrgthzfdlnhkiwzdgbd/auth/templates

2. Haz clic en la pestaña "SMTP Settings"

3. Haz clic en el botón verde "Set up SMTP"

4. Completa el formulario según tu proveedor:

   ┌─────────────────────────────────────────────────────────┐
   │ PARA SENDGRID (Recomendado):                            │
   ├─────────────────────────────────────────────────────────┤
   │ Host: smtp.sendgrid.net                                 │
   │ Port: 587                                               │
   │ Username: apikey                                        │
   │ Password: [Tu API Key de SendGrid]                     │
   │ From Email: practicas@uleam.edu.ec                     │
   └─────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────┐
   │ PARA GMAIL:                                             │
   ├─────────────────────────────────────────────────────────┤
   │ Host: smtp.gmail.com                                    │
   │ Port: 587                                               │
   │ Username: guanoluisamildreth@gmail.com                  │
   │ Password: [Contraseña de aplicación de 16 caracteres]  │
   │ From Email: guanoluisamildreth@gmail.com                │
   └─────────────────────────────────────────────────────────┘

5. Haz clic en "Save" o "Update"

═══════════════════════════════════════════════════════════════

🎯 PASO 4: Usar Supabase Auth para enviar emails
═══════════════════════════════════════════════════════════════

Con esta opción, Supabase se encargará de enviar los emails.
NO necesitas configurar SMTP en Django.

Pero NECESITAMOS actualizar el código para usar Supabase Auth.

═══════════════════════════════════════════════════════════════
""")
    
    print("\n⚠️  Esta opción requiere modificar el código de Django.")
    print("¿Quieres que te ayude a configurarlo? (s/n): ", end='')
    
else:
    print("""
⚠️  Opción inválida. Por favor ejecuta el script nuevamente.
""")

print("""
═══════════════════════════════════════════════════════════════

🎯 PASO 4: Probar la configuración
═══════════════════════════════════════════════════════════════

Una vez que hayas actualizado el archivo .env:

1. Guarda el archivo .env

2. Ejecuta el script de prueba:
   
   python test_envio_email.py

3. Ingresa tu email para recibir un correo de prueba

═══════════════════════════════════════════════════════════════

📚 DOCUMENTACIÓN ADICIONAL:
═══════════════════════════════════════════════════════════════

• SUPABASE_SMTP_CONFIG.md - Guía completa de Supabase SMTP
• CONFIGURAR_EMAIL_PRODUCCION.md - Guía de SendGrid/Gmail
• INICIO_RAPIDO_EMAIL.md - Inicio rápido

═══════════════════════════════════════════════════════════════

✅ ¡Configuración lista!

Si tienes problemas, consulta SUPABASE_SMTP_CONFIG.md

═══════════════════════════════════════════════════════════════
""")
