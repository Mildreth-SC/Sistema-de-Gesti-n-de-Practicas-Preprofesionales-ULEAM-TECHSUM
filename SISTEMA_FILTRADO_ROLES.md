# 🎯 SISTEMA DE FILTRADO POR ROLES (Estudiante vs Egresado)

## ✅ IMPLEMENTACIÓN COMPLETADA

### 📋 Resumen
Se ha implementado un sistema completo de filtrado de prácticas según el tipo de usuario (estudiante activo o egresado), que permite a las empresas y facultades dirigir sus ofertas a audiencias específicas.

---

## 🔧 COMPONENTES MODIFICADOS

### 1. **Modelos de Datos** (`inscripciones/models.py`)

#### Modelo `Estudiante`
```python
class Estudiante(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('estudiante', 'Estudiante Activo'),
        ('egresado', 'Egresado'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='estudiante',
        verbose_name='Tipo de usuario'
    )
    # ... otros campos
```

#### Modelo `Practica` y `PracticaInterna`
```python
class Practica(models.Model):
    DIRIGIDO_A_CHOICES = [
        ('estudiantes', 'Solo Estudiantes Activos'),
        ('egresados', 'Solo Egresados'),
        ('ambos', 'Estudiantes y Egresados'),
    ]
    
    dirigido_a = models.CharField(
        max_length=20,
        choices=DIRIGIDO_A_CHOICES,
        default='ambos',
        verbose_name='Dirigido a'
    )
    # ... otros campos
```

---

### 2. **Vistas con Filtrado** (`inscripciones/views.py`)

#### ✅ Vista `home` (Líneas 208-242)
**Filtrado de prácticas destacadas:**
```python
def home(request):
    # ... código anterior
    
    # Filtrar prácticas según tipo de usuario
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        estudiante = request.user.estudiante
        if estudiante.tipo_usuario == 'estudiante':
            practicas_destacadas = practicas_destacadas.filter(
                dirigido_a__in=['estudiantes', 'ambos']
            )
        elif estudiante.tipo_usuario == 'egresado':
            practicas_destacadas = practicas_destacadas.filter(
                dirigido_a__in=['egresados', 'ambos']
            )
```

#### ✅ Vista `lista_practicas` (Líneas 234-280)
**Filtrado de listado de prácticas externas:**
```python
def lista_practicas(request):
    practicas = Practica.objects.filter(activa=True, estado='disponible')
    
    # Filtrar por tipo de usuario
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        estudiante = request.user.estudiante
        if estudiante.tipo_usuario == 'estudiante':
            practicas = practicas.filter(dirigido_a__in=['estudiantes', 'ambos'])
        elif estudiante.tipo_usuario == 'egresado':
            practicas = practicas.filter(dirigido_a__in=['egresados', 'ambos'])
```

#### ✅ Vista `lista_practicas_internas` (Líneas 282-324)
**Filtrado de listado de prácticas internas:**
```python
def lista_practicas_internas(request):
    practicas_internas = PracticaInterna.objects.filter(activa=True, estado='disponible')
    
    # Filtrar por tipo de usuario
    if request.user.is_authenticated and hasattr(request.user, 'estudiante'):
        estudiante = request.user.estudiante
        if estudiante.tipo_usuario == 'estudiante':
            practicas_internas = practicas_internas.filter(
                dirigido_a__in=['estudiantes', 'ambos']
            )
        elif estudiante.tipo_usuario == 'egresado':
            practicas_internas = practicas_internas.filter(
                dirigido_a__in=['egresados', 'ambos']
            )
```

#### ✅ Vista `inscribirse_practica` (Líneas 387-490)
**Validación antes de inscripción:**
```python
def inscribirse_practica(request, pk):
    # ... código anterior
    
    # Validar dirigido_a
    if practica.dirigido_a == 'estudiantes' and estudiante.tipo_usuario == 'egresado':
        messages.error(
            request, 
            'Esta práctica está dirigida únicamente a estudiantes activos.'
        )
        return redirect('detalle_practica', pk=pk)
    
    if practica.dirigido_a == 'egresados' and estudiante.tipo_usuario == 'estudiante':
        messages.error(
            request, 
            'Esta práctica está dirigida únicamente a profesionales egresados.'
        )
        return redirect('detalle_practica', pk=pk)
```

#### ✅ Vista `inscribirse_practica_interna` (Líneas 548-650)
**Validación idéntica para prácticas internas**

---

## 🧪 PRÁCTICAS DE PRUEBA CREADAS

Se crearon **5 prácticas de prueba** para validar el sistema:

### Prácticas Externas (Empresa)
1. **"Práctica de Desarrollo Web (Solo Estudiantes)"**
   - `dirigido_a = 'estudiantes'`
   - Solo visible para estudiantes activos

2. **"Práctica Profesional Senior (Solo Egresados)"**
   - `dirigido_a = 'egresados'`
   - Solo visible para egresados

3. **"Práctica de Soporte Técnico (Estudiantes y Egresados)"**
   - `dirigido_a = 'ambos'`
   - Visible para ambos tipos

### Prácticas Internas (Facultad)
4. **"Práctica de Investigación (Solo Estudiantes)"**
   - `dirigido_a = 'estudiantes'`
   - Solo visible para estudiantes activos

5. **"Programa de Docencia (Solo Egresados)"**
   - `dirigido_a = 'egresados'`
   - Solo visible para egresados

---

## 🔍 CÓMO PROBAR EL SISTEMA

### Servidor corriendo en: **http://127.0.0.1:8000/**

### Prueba 1: Iniciar sesión como ESTUDIANTE
```
Usuario: estudianteprueba
Contraseña: test123
```

**Resultado esperado:**
- ✅ Debe ver: Práctica de Desarrollo Web, Soporte Técnico, Investigación
- ❌ NO debe ver: Práctica Senior, Programa de Docencia

### Prueba 2: Registrar un EGRESADO nuevo
1. Ir a registro de estudiante
2. Completar formulario seleccionando **tipo_usuario = "Egresado"**
3. Iniciar sesión

**Resultado esperado:**
- ✅ Debe ver: Práctica Senior, Soporte Técnico, Programa de Docencia
- ❌ NO debe ver: Práctica de Desarrollo Web, Investigación

### Prueba 3: Intentar inscribirse en práctica no permitida
1. Como estudiante, intentar acceder directamente a URL de práctica para egresados
2. Intentar inscribirse

**Resultado esperado:**
- ❌ Mensaje de error: "Esta práctica está dirigida únicamente a profesionales egresados."
- ↩️ Redirección a página de detalle

---

## 📊 LÓGICA DE FILTRADO

### Tabla de Visibilidad

| Práctica dirigida a | Estudiante ve | Egresado ve |
|---------------------|---------------|-------------|
| **estudiantes**     | ✅ SÍ         | ❌ NO       |
| **egresados**       | ❌ NO         | ✅ SÍ       |
| **ambos**           | ✅ SÍ         | ✅ SÍ       |

### Código de Filtrado
```python
# Para estudiantes
practicas.filter(dirigido_a__in=['estudiantes', 'ambos'])

# Para egresados
practicas.filter(dirigido_a__in=['egresados', 'ambos'])
```

---

## ✅ VALIDACIONES IMPLEMENTADAS

### 1. **Validación en Vista de Inscripción**
- Verifica que `practica.dirigido_a` coincida con `estudiante.tipo_usuario`
- Muestra mensaje de error descriptivo
- Redirige a página de detalle

### 2. **Filtrado en QuerySets**
- Las prácticas no permitidas no aparecen en listados
- Reduce confusión del usuario
- Mejora experiencia de usuario

### 3. **Templates Actualizados**
- `detalle_practica.html` muestra campo "Dirigido a"
- Usa `{{ practica.get_dirigido_a_display }}` para mostrar texto legible

---

## 🎯 BENEFICIOS DEL SISTEMA

1. **Segmentación de Audiencia**: Empresas y facultades pueden dirigir ofertas específicas
2. **Mejor UX**: Usuarios solo ven prácticas relevantes para su perfil
3. **Validaciones Robustas**: Impide inscripciones no permitidas
4. **Flexibilidad**: Opción "ambos" permite ofertas universales
5. **Escalabilidad**: Fácil agregar nuevos tipos de usuario en el futuro

---

## 📝 ARCHIVOS MODIFICADOS

1. ✅ `inscripciones/models.py` - Modelos con campo `dirigido_a`
2. ✅ `inscripciones/views.py` - 5 vistas con filtrado y validación
3. ✅ `templates/inscripciones/detalle_practica.html` - Muestra campo dirigido_a
4. ✅ `crear_practicas_filtradas.py` - Script para crear datos de prueba

---

## 🚀 PRÓXIMOS PASOS RECOMENDADOS

1. **Probar el sistema** con los usuarios de prueba
2. **Verificar formularios** de creación de prácticas (PracticaForm)
3. **Crear más usuarios** de prueba (egresados)
4. **Documentar en README.md** el uso del campo dirigido_a
5. **Agregar filtros** en panel de empresa/facultad para ver sus prácticas por tipo

---

## 🐛 DEBUGGING

Si algo no funciona:

1. **Verificar que el usuario tiene objeto Estudiante:**
   ```python
   hasattr(request.user, 'estudiante')
   ```

2. **Verificar tipo de usuario:**
   ```python
   request.user.estudiante.tipo_usuario
   ```

3. **Verificar prácticas en BD:**
   ```python
   python manage.py shell
   >>> from inscripciones.models import Practica
   >>> Practica.objects.values('titulo', 'dirigido_a')
   ```

4. **Verificar logs del servidor** en la terminal

---

## 📞 SOPORTE

Si encuentras algún problema:
1. Revisa los logs del servidor
2. Verifica que las migraciones estén aplicadas
3. Confirma que los datos de prueba se crearon correctamente
4. Revisa la consola del navegador (F12) para errores JavaScript

---

**Implementado el:** 7 de noviembre de 2025  
**Sistema:** Django 5.2.7 + PostgreSQL 17.6
