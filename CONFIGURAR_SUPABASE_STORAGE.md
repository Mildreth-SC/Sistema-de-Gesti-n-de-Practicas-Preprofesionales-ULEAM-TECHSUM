# 🖼️ CONFIGURAR IMÁGENES EN SUPABASE STORAGE

## ❓ ¿Por qué las imágenes no se ven en Render?

**El plan gratuito de Render NO guarda archivos subidos.** Cada vez que se reinicia o hace deploy, se pierden las imágenes de la carpeta `/media`.

**Solución:** Usar **Supabase Storage** para guardar las imágenes en la nube.

---

## 🎯 YA ESTÁ CONFIGURADO EN TU CÓDIGO

He configurado automáticamente tu proyecto para usar Supabase Storage. Solo necesitas hacer 3 pasos:

---

## 📋 PASO 1: Configurar el Bucket en Supabase

1. Ve a tu proyecto en **Supabase Dashboard**: https://supabase.com/dashboard
2. En el menú lateral, click en **Storage**
3. Click en **"Create a new bucket"**
4. Configuración del bucket:
   - **Name**: `media`
   - **Public bucket**: ✅ **ACTIVAR** (debe estar marcado)
   - **File size limit**: `50 MB`
   - Click **"Create bucket"**

5. **Configurar permisos públicos** (IMPORTANTE):
   - Click en el bucket `media` que acabas de crear
   - Click en **"Policies"** (arriba a la derecha)
   - Click en **"New Policy"**
   - Selecciona **"For full customization"**
   - Policy name: `Public Access`
   - Allowed operation: **SELECT** ✅
   - En el editor SQL, pega esto:
   
   ```sql
   CREATE POLICY "Public Access" ON storage.objects
   FOR SELECT
   USING ( bucket_id = 'media' );
   ```
   
   - Click **"Review"** → **"Save policy"**

6. **Agregar política de inserción**:
   - Click en **"New Policy"** nuevamente
   - Policy name: `Allow authenticated uploads`
   - Allowed operation: **INSERT** ✅
   - En el editor SQL:
   
   ```sql
   CREATE POLICY "Allow authenticated uploads" ON storage.objects
   FOR INSERT
   WITH CHECK ( bucket_id = 'media' );
   ```
   
   - Click **"Review"** → **"Save policy"**

---

## 📋 PASO 2: Agregar Variables de Entorno en Render

1. Ve a tu **Web Service** en Render Dashboard
2. Click en **"Environment"** (menú lateral izquierdo)
3. Agrega estas **2 variables nuevas**:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://avgxyvihvlijvammzizt.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | `[Ver abajo]` |

**Para obtener el `SUPABASE_SERVICE_ROLE_KEY`:**
1. Ve a Supabase Dashboard → **Settings** → **API**
2. En la sección **Project API keys**
3. Copia la clave **`service_role`** (la que dice "secret")
4. ⚠️ **NUNCA compartas esta clave, es secreta**

Tu `SUPABASE_SERVICE_ROLE_KEY` es:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2Z3h5dmlodmxpanZhbW16aXp0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjUyMDA5NywiZXhwIjoyMDc4MDk2MDk3fQ.Re6o2O0o0KAYNk7uMCNshGrE0SfKnCbKgvGnkxycA1U
```

4. Click **"Save Changes"**
5. Render reiniciará automáticamente el servicio

---

## 📋 PASO 3: Subir los Cambios y Hacer Deploy

Ahora sube los cambios al repositorio:

```bash
git add .
git commit -m "Configurar Supabase Storage para imágenes"
git push origin main
```

Render detectará los cambios y hará deploy automáticamente.

---

## ✅ VERIFICAR QUE FUNCIONA

1. **Espera a que Render termine el deploy** (5-10 minutos)
2. **Sube una imagen de prueba**:
   - Entra al admin: `https://tu-app.onrender.com/admin/`
   - Edita una empresa o estudiante
   - Sube una nueva imagen
3. **Verifica la imagen**:
   - La URL de la imagen debe ser algo como: `https://avgxyvihvlijvammzizt.supabase.co/storage/v1/object/public/media/...`
   - Si ves esta URL, ¡funciona! ✅

---

## 🔄 ¿Qué Pasa con las Imágenes Antiguas?

Las imágenes que ya subiste **NO se migrarán automáticamente**. Tienes 2 opciones:

### Opción A: Re-subir manualmente (Recomendado)
1. Vuelve a subir las imágenes desde el admin de Django
2. Las nuevas imágenes se guardarán en Supabase

### Opción B: Migrar usando script
Puedo crear un script para migrar las imágenes existentes desde tu base de datos local a Supabase Storage si lo necesitas.

---

## 📊 CAPACIDAD DE SUPABASE STORAGE (Plan Gratuito)

- **Almacenamiento**: 1 GB gratis
- **Transferencia**: 2 GB/mes gratis
- **Archivos ilimitados**

Para un sistema de prácticas, esto es más que suficiente. 1 GB = aproximadamente 10,000 fotos de perfil.

---

## 🆘 PROBLEMAS COMUNES

### Error: "Could not create bucket"
**Solución**: El bucket ya existe, continúa con el Paso 2.

### Error: "403 Forbidden" al subir imágenes
**Solución**: Verifica que configuraste las políticas públicas en el Paso 1 (punto 5 y 6).

### Las imágenes no se ven
**Solución**: 
1. Verifica que `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` estén en Render
2. Verifica que el bucket `media` sea público
3. Revisa los logs de Render para ver errores

---

## 🎉 ¡LISTO!

Después de estos 3 pasos:
- ✅ Las nuevas imágenes se guardan en Supabase
- ✅ Las imágenes persisten después de reinicios
- ✅ Las imágenes son accesibles públicamente
- ✅ No hay límite de archivos en el plan gratuito de Render

---

## 📝 RESUMEN TÉCNICO

**Archivos modificados/creados:**
- `supabase_storage.py` - Backend de almacenamiento para Django
- `sistema_practicas/settings.py` - Configuración de Django Storage
- `requirements.txt` - Agregadas dependencias: `supabase-storage-py`, `django-storages`

**Cómo funciona:**
1. Cuando subes una imagen en Django, se ejecuta `SupabaseStorage._save()`
2. El archivo se sube a Supabase Storage bucket `media`
3. Django guarda la URL pública en la base de datos
4. Cuando se muestra la imagen, Django usa `SupabaseStorage.url()` para obtener la URL pública

**En desarrollo (DEBUG=True):**
- Usa el filesystem local (`/media`)

**En producción (DEBUG=False en Render):**
- Usa Supabase Storage automáticamente
