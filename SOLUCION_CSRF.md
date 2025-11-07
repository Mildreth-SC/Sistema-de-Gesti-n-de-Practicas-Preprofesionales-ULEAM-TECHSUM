# 🔧 Solución al Error CSRF (403 Forbidden)

## El Problema
El error CSRF aparece porque las cookies del navegador están desactualizadas o corruptas después de cambios en el servidor.

---

## ✅ SOLUCIÓN RÁPIDA (Recomendada)

### Opción 1: Modo Incógnito/Privado
1. Cierra todas las ventanas del navegador
2. Abre una **ventana de incógnito/privado**:
   - **Chrome/Edge:** `Ctrl + Shift + N`
   - **Firefox:** `Ctrl + Shift + P`
3. Ve a: `http://localhost:8000/`
4. Intenta registrarte o iniciar sesión nuevamente

### Opción 2: Limpiar Cookies (Solución Permanente)

#### En Chrome/Edge:
1. Presiona `F12` para abrir las herramientas de desarrollador
2. Ve a la pestaña **"Application"** (Aplicación)
3. En el menú lateral izquierdo, expande **"Cookies"**
4. Haz clic en `http://localhost:8000`
5. Selecciona todas las cookies (Ctrl+A)
6. Presiona la tecla `Delete` o clic derecho → **"Delete Selected"**
7. Cierra las herramientas de desarrollador (`F12`)
8. Recarga la página (`F5`)

#### En Firefox:
1. Presiona `F12` para abrir las herramientas de desarrollador
2. Ve a la pestaña **"Storage"** (Almacenamiento)
3. Expande **"Cookies"** en el menú lateral
4. Haz clic en `http://localhost:8000`
5. Selecciona todas las cookies y elimínalas
6. Recarga la página (`F5`)

---

## 🔄 Si el problema persiste

### 1. Reiniciar el servidor Django

En la terminal donde está corriendo el servidor:
1. Presiona `Ctrl + C` para detenerlo
2. Ejecuta nuevamente:
```powershell
python manage.py runserver
```

### 2. Limpiar sesiones de Django

Ejecuta este comando para limpiar sesiones viejas:
```powershell
python manage.py clearsessions
```

### 3. Usar un navegador diferente

Si estás usando Chrome, prueba con:
- Microsoft Edge
- Firefox
- Brave

---

## 📝 Notas Importantes

✅ **El servidor debe estar corriendo** en `http://localhost:8000` o `http://127.0.0.1:8000`

✅ **Las configuraciones CSRF ya están correctas** en el sistema:
- `CSRF_TRUSTED_ORIGINS` incluye localhost
- `CSRF_COOKIE_SECURE = False` en desarrollo
- `SESSION_COOKIE_SECURE = False` en desarrollo
- Middleware configurado correctamente

✅ **El problema es siempre del lado del navegador** (cookies viejas/corruptas)

---

## 🎯 Verificación

Después de limpiar las cookies, deberías poder:
1. ✅ Ver el formulario de login sin errores
2. ✅ Enviar el formulario sin error 403
3. ✅ Ver los mensajes de éxito/error correctamente

---

## 💡 Prevención

Para evitar este problema en el futuro:
- Usa **modo incógnito** cuando estés probando cambios
- Limpia las cookies después de cambios importantes en el servidor
- Reinicia el navegador completamente cuando hagas cambios en settings.py
