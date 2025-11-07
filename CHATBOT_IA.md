# 🤖 Chatbot Inteligente con OpenAI

## Descripción

El chatbot del Sistema de Gestión de Prácticas ha sido mejorado con inteligencia artificial usando **OpenAI GPT-4o-mini** para proporcionar respuestas más naturales, contextuales e inteligentes.

---

## ✨ Características Principales

### 🎯 Respuestas Inteligentes
- **IA Conversacional**: Usa GPT-4o-mini para entender y responder naturalmente
- **Contexto del Sistema**: Conoce el estado actual de prácticas, empresas y facultades
- **Búsqueda Inteligente**: Puede buscar y recomendar prácticas específicas
- **Asistencia Personalizada**: Adapta respuestas según el tipo de usuario

### 📊 Información en Tiempo Real
- Estadísticas actualizadas del sistema
- Prácticas disponibles actualmente
- Empresas colaboradoras
- Prácticas internas de facultades

### 🔄 Sistema de Fallback
- Si la API de OpenAI falla, usa el sistema de respuestas predefinidas
- Garantiza disponibilidad 24/7
- No interrumpe la experiencia del usuario

---

## 🚀 Cómo Funciona

### 1. Usuario Envía Mensaje
El usuario escribe una pregunta o solicitud en el chatbot.

### 2. Procesamiento con IA
```python
# El sistema:
1. Obtiene contexto actualizado del sistema
2. Envía pregunta + contexto a OpenAI GPT-4o-mini
3. Recibe respuesta inteligente y natural
4. Genera opciones de seguimiento contextualmente relevantes
```

### 3. Respuesta Inteligente
El chatbot responde con:
- **Texto natural y conversacional**
- **Información específica del sistema**
- **URLs relevantes** (cuando aplica)
- **Opciones de seguimiento** adaptadas al contexto

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Buscar Prácticas
```
Usuario: "¿Qué prácticas de programación hay disponibles?"

Chatbot: "¡Claro! 😊 Actualmente tenemos 3 prácticas relacionadas con programación:

1. **Desarrollador Web Junior** en TechSolutions
   - Duración: 6 meses
   - Ubicación: Manta
   
2. **Programador Python** en DataCorp
   - Duración: 4 meses
   - Ubicación: Portoviejo
   
3. **Full Stack Developer** en InnovaCode
   - Duración: 6 meses
   - Ubicación: Remoto

¿Te gustaría más detalles de alguna? 🚀"

Opciones:
[Ver Todas] [Filtrar por Ubicación] [Cómo Inscribirme]
```

### Ejemplo 2: Registro
```
Usuario: "Quiero registrarme pero no sé cómo"

Chatbot: "¡Perfecto! Te ayudo con el registro 😊

Primero, ¿quién eres?

👨‍🎓 **Estudiante**: Regístrate aquí → /registro/
Necesitarás: código de estudiante, datos de carrera y CV

🏢 **Empresa**: Regístrate aquí → /registro-empresa/
Necesitarás: RUC, datos de contacto y logo (opcional)

El proceso es súper rápido, ¡solo 2-3 minutos! ¿Cuál es tu caso?"

Opciones:
[Soy Estudiante] [Soy Empresa] [Más Info]
```

### Ejemplo 3: Ayuda Específica
```
Usuario: "¿Qué documentos necesito para inscribirme?"

Chatbot: "¡Buena pregunta! 📄 Para inscribirte a una práctica necesitas:

✅ **Obligatorios:**
- CV actualizado (PDF)
- Carta de presentación
- Certificado de estudios

📋 **Opcionales (pero recomendados):**
- Certificados de cursos
- Portafolio de proyectos
- Cartas de recomendación

💡 Tip: Puedes subir múltiples documentos en tu perfil y el sistema los guardará para futuras postulaciones.

¿Necesitas ayuda con algún documento específico?"

Opciones:
[Formato CV] [Cómo Subir Docs] [Ver Perfil]
```

---

## ⚙️ Configuración Técnica

### Variables de Entorno Requeridas

```env
# .env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

### Modelo Usado
- **GPT-4o-mini**: Rápido, económico y eficiente
- **Max Tokens**: 500 (respuestas concisas)
- **Temperature**: 0.7 (balance entre creatividad y precisión)

### Contexto del Sistema
El chatbot tiene acceso a:
```python
- Número de prácticas activas
- Lista de empresas colaboradoras
- Prácticas internas disponibles
- Información de las últimas 5 prácticas publicadas
- URLs importantes del sistema
```

---

## 🔧 Arquitectura

```
Usuario → Frontend (Chat UI)
          ↓
    POST /chatbot/chat/
          ↓
    chatbot/views.py
          ↓
    ┌─────────────────────┐
    │ Hay API Key?        │
    └─────────────────────┘
           ↓          ↓
         SÍ          NO
           ↓          ↓
    OpenAI GPT    Fallback
           ↓          ↓
    Respuesta IA   Respuestas
           ↓       Predefinidas
           ↓          ↓
    ┌─────────────────────┐
    │ Generar Opciones    │
    │ Contextuales        │
    └─────────────────────┘
           ↓
    JSON Response
           ↓
    Frontend (Mostrar)
```

---

## 📊 Ventajas sobre el Sistema Anterior

| Característica | Sistema Anterior | Sistema con IA |
|----------------|------------------|----------------|
| **Comprensión** | Solo palabras clave | Lenguaje natural |
| **Respuestas** | Predefinidas | Contextuales |
| **Búsqueda** | No disponible | Búsqueda inteligente |
| **Personalización** | Limitada | Alta |
| **Idioma** | Rígido | Natural y conversacional |
| **Aprendizaje** | No | Sí (mejora con uso) |
| **Contexto** | Limitado | Completo del sistema |

---

## 🎯 Casos de Uso

### Para Estudiantes
- ✅ Buscar prácticas por área/carrera
- ✅ Entender proceso de inscripción
- ✅ Resolver dudas sobre documentos
- ✅ Obtener información de empresas
- ✅ Ayuda con el perfil

### Para Empresas
- ✅ Proceso de registro
- ✅ Cómo publicar prácticas
- ✅ Gestión de postulantes
- ✅ Información sobre evaluaciones

### Para Facultades
- ✅ Publicar prácticas internas
- ✅ Gestionar estudiantes
- ✅ Proceso de evaluación

---

## 🔒 Seguridad

- ✅ API Key almacenada en variables de entorno
- ✅ No se expone en el código fuente
- ✅ Validación de entrada
- ✅ Rate limiting (por OpenAI)
- ✅ Logs de errores sin exponer datos sensibles

---

## 💰 Costos

**GPT-4o-mini** es muy económico:
- ~$0.00015 por 1K tokens de entrada
- ~$0.0006 por 1K tokens de salida

**Estimación**: Con 500 tokens por conversación:
- ~1000 conversaciones por $1 USD
- Muy escalable para el uso esperado

---

## 🚀 Mejoras Futuras

### Corto Plazo
- [ ] Integrar con base de conocimientos vectorial
- [ ] Historial de conversaciones
- [ ] Análisis de sentiment

### Mediano Plazo
- [ ] Múltiples idiomas (inglés, quichua)
- [ ] Voice input/output
- [ ] Integración con calendario para recordatorios

### Largo Plazo
- [ ] Fine-tuning del modelo con datos específicos de ULEAM
- [ ] Integración con sistema de notificaciones
- [ ] Dashboard de analytics del chatbot

---

## 📝 Testing

### Probar Localmente
```bash
# 1. Asegúrate de tener la API key en .env
OPENAI_API_KEY=sk-proj-xxxxx

# 2. Inicia el servidor
python manage.py runserver

# 3. Ve a http://127.0.0.1:8000
# 4. Abre el chatbot (botón flotante abajo derecha)
# 5. Prueba conversaciones naturales
```

### Casos de Prueba Recomendados
```
✅ "¿Qué prácticas hay disponibles?"
✅ "Necesito ayuda para registrarme"
✅ "Busco prácticas de ingeniería en Manta"
✅ "¿Qué documentos necesito?"
✅ "Cómo funciona el proceso de evaluación"
✅ "Información sobre empresas colaboradoras"
```

---

## 🐛 Troubleshooting

### Error: "OpenAI API key not found"
**Solución**: Verifica que `OPENAI_API_KEY` esté en `.env`

### Error: Rate limit exceeded
**Solución**: Espera unos minutos o actualiza plan de OpenAI

### Respuestas lentas
**Solución**: Normal la primera vez, luego es instantáneo

### Fallback activado
**Solución**: Verifica conexión a internet y API key válida

---

## 📚 Recursos

- [Documentación OpenAI](https://platform.openai.com/docs)
- [OpenAI Python Library](https://github.com/openai/openai-python)
- [GPT-4o-mini Pricing](https://openai.com/pricing)

---

**Desarrollado con ❤️ para ULEAM**
**Versión**: 2.0 con IA
**Última actualización**: Noviembre 2025
