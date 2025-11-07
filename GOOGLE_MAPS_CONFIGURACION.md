# Integración de Google Maps - Guía de Configuración

## 📍 Resumen de Implementación

Se ha integrado Google Maps para mostrar la ubicación de empresas y facultades, permitiendo a los estudiantes ver fácilmente dónde están ubicadas las organizaciones que ofrecen prácticas.

---

## ✨ Características Implementadas

### 1. **Autocompletado de Direcciones al Registrarse**
- Campo de dirección con autocompletado de Google Places
- Búsqueda restringida a Ecuador
- Selección de lugar en el mapa
- Guarda automáticamente latitud y longitud

### 2. **Visualización de Ubicación**
- Mapa interactivo en detalle de empresa/facultad
- Marcador con información de contacto
- Botón "Cómo llegar" que abre Google Maps
- Botón "Ver en Google Maps" en la sección de dirección

### 3. **Campos en Base de Datos**
- **Empresa**: `latitud` y `longitud` (DecimalField)
- **Facultad**: `latitud` y `longitud` (DecimalField)
- Ambos campos son opcionales (null=True, blank=True)

---

## 🔑 Configuración de Google Maps API

### Paso 1: Obtener una API Key de Google

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a **APIs & Services** > **Library**
4. Habilita las siguientes APIs:
   - **Maps JavaScript API**
   - **Places API**
   - **Geocoding API** (opcional, para conversión de direcciones)

5. Ve a **APIs & Services** > **Credentials**
6. Haz clic en **Create Credentials** > **API Key**
7. Copia la API Key generada

### Paso 2: Configurar Restricciones (Importante para Seguridad)

1. En **Credentials**, haz clic en tu API Key
2. En **Application restrictions**:
   - Selecciona **HTTP referrers (websites)**
   - Agrega tus dominios autorizados:
     ```
     http://localhost:8000/*
     https://tu-dominio.com/*
     ```

3. En **API restrictions**:
   - Selecciona **Restrict key**
   - Marca:
     - Maps JavaScript API
     - Places API
     - (Opcional) Geocoding API

4. Guarda los cambios

### Paso 3: Reemplazar la API Key en el Código

Busca `YOUR_API_KEY` en los siguientes archivos y reemplázalo con tu API Key:

**Archivo 1:** `templates/inscripciones/registro_empresa.html`
```javascript
script.src = 'https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&libraries=places&callback=initMap';
```

**Archivo 2:** `templates/inscripciones/registro_facultad.html`
```javascript
script.src = 'https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&libraries=places&callback=initMapFacultad';
```

**Archivo 3:** `templates/inscripciones/detalle_empresa.html`
```javascript
script.src = 'https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&callback=initMapEmpresa';
```

### Paso 4 (Recomendado): Usar Variable de Entorno

En lugar de poner la API Key directamente en el código, usa una variable de entorno:

**1. Agregar a `.env`:**
```
GOOGLE_MAPS_API_KEY=tu_api_key_aqui
```

**2. Actualizar `settings.py`:**
```python
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')
```

**3. Pasar a los templates:**

En tus vistas, agrega al contexto:
```python
def detalle_empresa(request, pk):
    # ... código existente ...
    context = {
        'empresa': empresa,
        'practicas': practicas,
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,  # Agregar esto
    }
    return render(request, 'inscripciones/detalle_empresa.html', context)
```

**4. Usar en el template:**
```javascript
script.src = 'https://maps.googleapis.com/maps/api/js?key={{ google_maps_key }}&libraries=places&callback=initMap';
```

---

## 📊 Archivos Modificados

### Modelos (`inscripciones/models.py`)
```python
class Empresa(models.Model):
    # ... campos existentes ...
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

class Facultad(models.Model):
    # ... campos existentes ...
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
```

### Vistas (`inscripciones/auth_views.py`)
- `registro_empresa`: Guarda latitud/longitud desde request.POST
- `registro_facultad`: Guarda latitud/longitud desde request.POST

### Templates
1. **`registro_empresa.html`**:
   - Campo de dirección con autocompletado
   - Mapa interactivo que aparece al seleccionar lugar
   - Campos ocultos para latitud/longitud

2. **`registro_facultad.html`**:
   - Mismo sistema de autocompletado
   - Prefijo `_facultad` para evitar conflictos

3. **`detalle_empresa.html`**:
   - Mapa embedido que muestra ubicación
   - Info window con datos de contacto
   - Botones para abrir en Google Maps y obtener direcciones

---

## 🎯 Cómo Funciona

### Flujo de Registro

1. **Usuario ingresa dirección**
   - Empieza a escribir en el campo "Dirección"
   - Google Places sugiere direcciones en Ecuador

2. **Usuario selecciona una sugerencia**
   - El mapa aparece automáticamente
   - Se coloca un marcador en la ubicación
   - Se guardan latitud y longitud en campos ocultos

3. **Usuario puede ajustar la ubicación**
   - Puede arrastrar el marcador
   - Las coordenadas se actualizan automáticamente

4. **Al enviar el formulario**
   - La vista guarda latitud y longitud en la base de datos
   - Junto con la dirección en texto

### Flujo de Visualización

1. **Estudiante ve detalle de empresa**
   - Si la empresa tiene coordenadas, se muestra el mapa
   - El mapa carga la ubicación exacta
   - Se muestra un marcador con info window

2. **Interacción con el mapa**
   - Click en marcador muestra información de contacto
   - Botón "Cómo llegar" abre Google Maps con direcciones
   - Botón "Ver en Google Maps" abre la ubicación en nueva pestaña

---

## 🔍 Ejemplos de Código

### JavaScript para Autocompletado

```javascript
// Crear autocompletado
const input = document.getElementById('id_direccion');
autocomplete = new google.maps.places.Autocomplete(input, {
    componentRestrictions: { country: 'ec' }, // Solo Ecuador
    fields: ['formatted_address', 'geometry', 'name'],
});

// Cuando se selecciona un lugar
autocomplete.addListener('place_changed', function() {
    const place = autocomplete.getPlace();
    
    // Actualizar mapa
    map.setCenter(place.geometry.location);
    marker.setPosition(place.geometry.location);
    
    // Guardar coordenadas
    document.getElementById('id_latitud').value = place.geometry.location.lat();
    document.getElementById('id_longitud').value = place.geometry.location.lng();
});
```

### Python para Guardar Coordenadas

```python
# En la vista de registro
if request.POST.get('latitud') and request.POST.get('longitud'):
    empresa = user.empresa
    empresa.latitud = request.POST.get('latitud')
    empresa.longitud = request.POST.get('longitud')
    empresa.save()
```

### Template para Mostrar Mapa

```html
{% if empresa.latitud and empresa.longitud %}
<div id="mapa_empresa" style="height: 400px;"></div>
<script>
function initMapEmpresa() {
    const location = { 
        lat: {{ empresa.latitud }}, 
        lng: {{ empresa.longitud }} 
    };
    
    const map = new google.maps.Map(document.getElementById('mapa_empresa'), {
        center: location,
        zoom: 15,
    });
    
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        title: '{{ empresa.nombre }}',
    });
}
</script>
{% endif %}
```

---

## 💰 Costos de Google Maps API

### Precios (2024)
- **Maps JavaScript API**: $7 por 1,000 cargas de mapa
- **Places API (Autocomplete)**: $2.83 por 1,000 sesiones
- **Crédito gratuito mensual**: $200

### Cálculo Estimado
Con el crédito gratuito de $200/mes:
- ~28,571 cargas de mapa GRATIS
- ~70,000 autocompletados GRATIS

**Para la mayoría de aplicaciones educativas, esto es suficiente y NO generará costos.**

### Recomendaciones para Ahorrar
1. ✅ Configurar restricciones de dominio
2. ✅ Solo cargar el mapa cuando sea necesario
3. ✅ Usar `libraries=places` solo donde se necesita
4. ✅ Habilitar facturación para monitorear uso

---

## ✅ Checklist de Implementación

- [x] Campos latitud/longitud agregados a modelos
- [x] Migración creada y aplicada
- [x] Autocompletado en registro de empresa
- [x] Autocompletado en registro de facultad
- [x] Guardado de coordenadas en vistas
- [x] Mapa en detalle de empresa
- [x] Botones "Ver en Google Maps" y "Cómo llegar"
- [ ] **Configurar API Key de Google Maps** (⚠️ PENDIENTE)
- [ ] Agregar mapa a detalle de facultad
- [ ] Configurar variables de entorno (recomendado)
- [ ] Probar en producción

---

## 🚀 Próximos Pasos

1. **Obtener API Key** (instrucciones arriba)
2. **Reemplazar `YOUR_API_KEY`** en los templates
3. **Probar el registro** de empresa/facultad
4. **Verificar** que el mapa aparece en el detalle
5. **Configurar restricciones** de seguridad
6. **(Opcional)** Agregar mapa a detalle de facultad
7. **(Opcional)** Usar variable de entorno para la API Key

---

## 📝 Notas Importantes

- La API Key debe tener permisos para **Maps JavaScript API** y **Places API**
- Las coordenadas se guardan con 7 decimales de precisión (~1.1 cm)
- El autocompletado está restringido a Ecuador (`componentRestrictions: { country: 'ec' }`)
- Si no hay coordenadas, el mapa simplemente no se muestra
- Los mapas cargan de forma asíncrona para no bloquear la página

---

## 🎨 Personalización

### Cambiar el Zoom Inicial
```javascript
map.setZoom(17); // 17 = muy cerca, 10 = lejos
```

### Cambiar el Centro por Defecto (si no hay dirección)
```javascript
const defaultLocation = { 
    lat: -0.9537,  // Manta, Manabí
    lng: -80.7089 
};
```

### Personalizar el Info Window
```javascript
const infoWindow = new google.maps.InfoWindow({
    content: `
        <div style="padding: 10px;">
            <h6>${empresa.nombre}</h6>
            <p>${empresa.direccion}</p>
            <!-- Agregar más información aquí -->
        </div>
    `
});
```

---

## 🎉 Sistema Listo

Una vez configurada la API Key, el sistema estará completamente funcional:

- ✅ Empresas y facultades pueden registrar su ubicación exacta
- ✅ Estudiantes pueden ver dónde están ubicadas las organizaciones
- ✅ Botones para obtener direcciones desde Google Maps
- ✅ Experiencia de usuario profesional y moderna

**¡Configuración completada!** 🗺️
