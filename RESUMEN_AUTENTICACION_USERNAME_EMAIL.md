# Sistema de Autenticación con Username y Email

## 📋 Resumen de Implementación

Se ha mejorado el sistema de autenticación para permitir que los usuarios inicien sesión usando **username** O **correo electrónico** indistintamente.

---

## ✨ Características Implementadas

### 1. **Backend de Autenticación Personalizado**

**Archivo:** `inscripciones/backends.py`

Se creó un backend personalizado que extiende `ModelBackend` de Django:

```python
class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend personalizado que permite autenticación con email o username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Busca usuario por username O email (case-insensitive)
        user = User.objects.get(
            Q(username__iexact=username) | Q(email__iexact=username)
        )
        
        # Verifica la contraseña
        if user.check_password(password):
            return user
```

**Características:**
- ✅ Acepta username o email en el campo de login
- ✅ Case-insensitive (no distingue mayúsculas/minúsculas)
- ✅ Verifica contraseña con hash seguro de Django
- ✅ Retorna None si no encuentra el usuario

---

### 2. **Configuración en Settings**

**Archivo:** `sistema_practicas/settings.py`

Se agregó la configuración de backends de autenticación:

```python
AUTHENTICATION_BACKENDS = [
    'inscripciones.backends.EmailOrUsernameModelBackend',  # Backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # Backend por defecto (fallback)
]
```

**Orden de ejecución:**
1. Primero intenta con el backend personalizado (username o email)
2. Si falla, intenta con el backend por defecto de Django

---

### 3. **Vista de Login Actualizada**

**Archivo:** `inscripciones/auth_views.py`

La vista `login_view` ahora:

```python
def login_view(request):
    # Obtiene username o email del formulario
    username_or_email = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    
    # Si no parece email, busca el username y obtiene el email
    email = username_or_email
    if '@' not in username_or_email:
        user_obj = User.objects.get(username__iexact=username_or_email)
        email = user_obj.email
    
    # Login con Supabase Auth usando el email
    result = supabase_auth.signin(email, password)
```

**Flujo:**
1. Usuario ingresa username o email
2. Si ingresó username, busca el email asociado
3. Autentica con Supabase usando el email
4. Verifica aprobación (empresas/facultades)
5. Guarda tokens en sesión
6. Redirige según tipo de usuario

---

### 4. **Template de Login Actualizado**

**Archivo:** `templates/inscripciones/login.html`

Cambios en el formulario:

**ANTES:**
```html
<label>Correo Electrónico</label>
<input type="email" name="email" placeholder="tucorreo@ejemplo.com">
<small>Usa el mismo correo con el que te registraste</small>
```

**AHORA:**
```html
<label>Usuario o Correo Electrónico</label>
<input type="text" name="username" placeholder="usuario o tucorreo@ejemplo.com">
<small>Puedes usar tu usuario o tu correo electrónico</small>
```

**Mejoras:**
- ✅ Icono cambiado a `bi-person-circle` (más genérico)
- ✅ Campo `type="text"` (no limita a email)
- ✅ Placeholder informativo
- ✅ Mensaje claro para el usuario

---

## 🎯 Casos de Uso

### Caso 1: Login con Username
```
Usuario ingresa: "juanperez"
Password: "micontraseña123"
✓ Sistema busca usuario con username="juanperez"
✓ Encuentra email asociado: juan.perez@example.com
✓ Autentica con Supabase usando el email
✓ Login exitoso
```

### Caso 2: Login con Email
```
Usuario ingresa: "juan.perez@example.com"
Password: "micontraseña123"
✓ Sistema detecta que es un email (contiene @)
✓ Autentica directamente con Supabase
✓ Login exitoso
```

### Caso 3: Case-Insensitive
```
Usuario ingresa: "JUANPEREZ" (mayúsculas)
✓ Sistema busca case-insensitive (juanperez)
✓ Encuentra el usuario
✓ Login exitoso

Usuario ingresa: "JUAN.PEREZ@EXAMPLE.COM"
✓ Sistema busca case-insensitive
✓ Login exitoso
```

---

## 📊 Resultados de Pruebas

```bash
python test_autenticacion_username_email.py
```

**Resultados:**
```
=======================================
PRUEBA DE AUTENTICACIÓN CON USERNAME Y EMAIL
=======================================

✓ Usuario creado (username: testuser, email: test@example.com)
✓ Autenticación exitosa con USERNAME
✓ Autenticación exitosa con EMAIL
✓ Contraseñas incorrectas son rechazadas
✓ Usuarios inexistentes son rechazados
✓ Autenticación con username en MAYÚSCULAS
✓ Autenticación con email en MAYÚSCULAS

TODAS LAS PRUEBAS PASARON EXITOSAMENTE
```

---

## 🔒 Seguridad

### Ventajas del Sistema

1. **Hash de Contraseñas**
   - Django usa `PBKDF2` por defecto
   - Contraseñas nunca se almacenan en texto plano

2. **Case-Insensitive**
   - Evita problemas de mayúsculas/minúsculas
   - Mejor experiencia de usuario

3. **Doble Verificación**
   - Backend de Django verifica username/email
   - Supabase Auth verifica email/password

4. **Tokens Seguros**
   - Access token y refresh token almacenados en sesión
   - Tokens encriptados por Supabase

---

## 🚀 Integración con Supabase Auth

El sistema mantiene compatibilidad con Supabase Auth:

1. **Registro:** Sigue usando email como requerido por Supabase
2. **Login:** Convierte username a email si es necesario
3. **Tokens:** Almacena tokens de Supabase en sesión Django
4. **Middleware:** Sincroniza estado de autenticación

---

## 💡 Recomendaciones

### Para Usuarios

**Pueden iniciar sesión con:**
- ✅ Username: `juanperez`
- ✅ Email: `juan.perez@example.com`
- ✅ Ambos son válidos y funcionan igual

**Consejos:**
- El username se crea automáticamente del email al registrarse
- Ambos métodos son seguros
- No distingue mayúsculas/minúsculas

### Para Desarrolladores

**Al crear usuarios:**
```python
# El email se usa como username por defecto
user = User.objects.create_user(
    username=email,  # Username = email
    email=email,
    password=password
)
```

**Al autenticar:**
```python
# Funciona con ambos
user = authenticate(username='juanperez', password='pass123')
user = authenticate(username='juan@example.com', password='pass123')
```

---

## 📝 Archivos Modificados

### Nuevos Archivos
- ✅ `inscripciones/backends.py` - Backend personalizado
- ✅ `test_autenticacion_username_email.py` - Tests completos

### Archivos Modificados
- ✅ `sistema_practicas/settings.py` - AUTHENTICATION_BACKENDS
- ✅ `inscripciones/auth_views.py` - Vista login_view actualizada
- ✅ `templates/inscripciones/login.html` - Formulario de login

---

## ✅ Checklist de Funcionalidades

- [x] Backend personalizado EmailOrUsernameModelBackend
- [x] Autenticación con username
- [x] Autenticación con email
- [x] Case-insensitive (mayúsculas/minúsculas)
- [x] Verificación de contraseña con hash
- [x] Integración con Supabase Auth
- [x] Template de login actualizado
- [x] Mensajes de error descriptivos
- [x] Validación de usuarios inexistentes
- [x] Validación de contraseñas incorrectas
- [x] Pruebas completas pasando
- [x] Compatibilidad con sistema de aprobación
- [x] Compatibilidad con notificaciones

---

## 🎉 Sistema Listo

El sistema de autenticación ahora es más flexible y amigable:

- **Usuarios pueden elegir** cómo iniciar sesión
- **No hay confusión** sobre qué campo usar
- **Funciona con Supabase** sin problemas
- **Totalmente probado** y seguro

**¡Implementación exitosa!** 🎊
