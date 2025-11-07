from django.http import JsonResponse
from django.urls import reverse
from inscripciones.models import Practica, Empresa, PracticaInterna, Facultad
from django.db.models import Count
import json
import re

def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'response': '¿En qué puedo ayudarte hoy?',
                'options': [
                    {'icon': 'bi-person-plus', 'text': 'Registrarme', 'message': '¿Cómo me registro?'},
                    {'icon': 'bi-briefcase', 'text': 'Ver Prácticas', 'message': 'Ver prácticas disponibles'},
                    {'icon': 'bi-question-circle', 'text': 'Ayuda', 'message': 'Necesito ayuda'}
                ]
            })
        
        # Procesar mensaje y obtener respuesta con opciones
        response_data = process_message(message)
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def process_message(message):
    """Procesa el mensaje del usuario y retorna la respuesta apropiada con opciones"""
    msg = normalize_text(message)
    
    # Base de conocimientos - Orden de prioridad
    responses = [
        # ============ SALUDOS Y DESPEDIDAS ============
        {
            'patterns': [
                r'\b(hola|buenos dias|buenas tardes|buenas noches|saludos|hey|que tal)\b',
            ],
            'response': lambda: f"¡Hola! 😊 ¡Qué gusto saludarte! Soy tu asistente virtual del Sistema de Prácticas de ULEAM.\n\n{get_estadisticas_sistema()}\n\nEstoy aquí para ayudarte. Selecciona una opción del menú abajo o escribe tu pregunta directamente. 👇"
        },
        {
            'patterns': [
                r'\b(menu|menu principal|inicio|volver|opciones|mostrar opciones|otra pregunta|otro tema)\b',
            ],
            'response': lambda: f"📋 **Menú Principal**\n\n{get_estadisticas_sistema()}\n\n¿En qué puedo ayudarte? Selecciona una opción:"
        },
        {
            'patterns': [r'\b(adios|chao|hasta luego|bye|nos vemos)\b'],
            'response': "¡Fue un placer ayudarte! � Espero haber resuelto tus dudas.\n\nRecuerda que siempre estaré aquí cuando me necesites. ¡Mucho éxito en tu búsqueda de prácticas! 🚀\n\n¡Hasta pronto! 👋"
        },
        {
            'patterns': [r'\b(gracias|muchas gracias|te agradezco|esta claro|entendido)\b'],
            'response': "¡No hay de qué! 😊 Me alegra mucho haber podido ayudarte.\n\nSi en algún momento tienes más preguntas o necesitas aclarar algo, aquí estaré. ¡Cuenta conmigo! 💪"
        },
        {
            'patterns': [
                r'\b(necesito mas|quiero saber mas|mas informacion|mas info|mas detalles)\b',
                r'\b(explicame mas|cuentame mas)\b',
            ],
            'response': "¡Claro! 😊 ¿Sobre qué tema te gustaría saber más?\n\nPuedo darte más detalles sobre:\n• Prácticas disponibles\n• Proceso de inscripción\n• Evaluaciones y calificaciones\n• Documentos requeridos\n• Empresas colaboradoras\n• Duración y horarios\n\n¿Qué te interesa?"
        },
        
        # ============ REGISTRO Y CUENTAS ============
        {
            'patterns': [
                r'\b(como|donde|quiero).*(registr|crear cuenta|inscribir|darme de alta)\b',
                r'\b(registro|registrarme|crear usuario)\b',
            ],
            'response': "¡Perfecto! Te ayudo a registrarte en el sistema 😊\n\nPrimero, cuéntame, ¿quién eres?\n\n👨‍🎓 **¿Eres estudiante?**\nNecesitarás tu código de estudiante, datos de tu carrera y tu CV actualizado.\n\n🏢 **¿Representas a una empresa?**\nTe pediré el RUC, información de contacto y datos de tu organización.\n\n🎓 **¿Eres de una facultad?**\nRequerirás el código de facultad y datos del decano.\n\nCada registro es súper sencillo y te tomará solo unos minutos. ¿Cuál es tu caso?"
        },
        {
            'patterns': [r'\b(estudiante|alumno|como estudiante)\b.*\b(registr)\b'],
            'response': "¡Genial! Vamos a registrarte como estudiante 👨‍🎓\n\nEs muy fácil, te guío paso a paso:\n\n1️⃣ Ve al botón 'Registrarse' arriba a la derecha y selecciona 'Estudiante'\n\n2️⃣ Completa el formulario (tranquilo, no es largo):\n   • Tu nombre completo\n   • Email (preferible el institucional @uleam.edu.ec)\n   • Tu código de estudiante\n   • Carrera y ciclo actual\n   • Teléfono y dirección\n   • Sube tu CV en PDF (importante tenerlo actualizado)\n\n3️⃣ Crea una contraseña que recuerdes bien (combina letras y números)\n\n4️⃣ Dale click a 'Registrar' y ¡listo! 🎉\n\nEn segundos tendrás tu cuenta activa y podrás empezar a buscar prácticas. ¿Alguna duda con algún campo?"
        },
        {
            'patterns': [r'\b(empresa|negocio|compañia)\b.*\b(registr)\b'],
            'response': "¡Excelente que quieran sumarse como empresa! 🏢\n\nRegistrar su empresa es muy valioso para nuestros estudiantes. Déjame contarte qué necesitas:\n\n📋 **Información básica:**\n• RUC de la empresa\n• Nombre comercial\n• Sector al que pertenecen\n• Datos del responsable de RRHH\n• Email corporativo\n• Teléfono y dirección\n• Logo (opcional, pero queda bonito 😉)\n\n🎁 **Lo que ganan:**\n✓ Acceso a talento joven y preparado\n✓ Pueden publicar todas las prácticas que quieran\n✓ Sistema fácil para revisar postulantes\n✓ Herramientas de evaluación incluidas\n✓ Reportes automáticos\n\n¿Te ayudo con algún dato específico o tienes todo listo?"
        },
        {
            'patterns': [
                r'\b(olvide|recuperar|resetear|cambiar|perdi).*(contraseña|password|clave)\b',
            ],
            'response': "¡No te preocupes! � Nos pasa a todos, es súper normal.\n\nTe explico cómo recuperar tu contraseña en un ratito:\n\n1️⃣ Ve a la página de login (donde inicias sesión)\n\n2️⃣ Verás un link que dice '¿Olvidaste tu contraseña?' - dale click\n\n3️⃣ Escribe el email con el que te registraste\n\n4️⃣ Revisa tu bandeja de entrada (dale 1-2 minutitos)\n\n5️⃣ Abre el correo y haz click en el enlace que te enviamos\n\n6️⃣ Crea tu nueva contraseña (esta vez anótala en algún lugar seguro 😉)\n\n💡 **Pro tip:** Si no ves el correo, chequea en spam/correo no deseado. Y asegúrate de escribir bien tu email.\n\n¿No te llega nada? Avísame y te doy más opciones."
        },
        
        # ============ PRÁCTICAS - INFORMACIÓN GENERAL ============
        {
            'patterns': [
                r'\b(cuantas|cuantos|estadistica|numero).*(practica|empresa|disponible)\b',
                r'\b(estado|situacion).*(sistema)\b',
            ],
            'response': lambda: get_estadisticas_sistema()
        },
        {
            'patterns': [
                r'\b(que son|que es|info|informacion sobre).*(practica|pasantia)\b',
                r'\b(practica|pasantia).*(que es|info)\b',
            ],
            'response': lambda: f"¡Buena pregunta! 😊 Te explico de manera sencilla:\n\nLas prácticas pre-profesionales son como tu primer contacto con el mundo laboral real. Es donde pones en práctica todo lo que has aprendido en la universidad.\n\n**¿Qué tipos hay?**\n🏢 **Externas:** Trabajas en empresas privadas - ¡la experiencia real del mercado!\n🎓 **Internas:** Apoyas dentro de ULEAM - ideal si tienes horarios complicados\n\n**Lo importante:**\n⏱️ Entre 240-480 horas (depende de tu carrera)\n📊 Te evalúan por quimestres, igual que tus materias\n📚 Necesitas tener aprobado al menos el 60% de tus créditos\n\nEs obligatorio para graduarte, pero créeme, ¡es una experiencia que vale oro! 💎\n\n{get_estadisticas_sistema()}"
        },
        {
            'patterns': [
                r'\b(como|donde|ver|buscar|encontrar).*(practica|practicas disponible|oferta)\b',
                r'\b(lista|listado).*(practica)\b',
                r'\b(ver practica)\b',
                r'\b(muestra|dame).*(practica)\b',
            ],
            'response': lambda: get_practicas_disponibles()
        },
        {
            'patterns': [
                r'\b(como|quiero|proceso).*(inscribir|aplicar|postular).*(practica)\b',
                r'\b(inscripcion|postulacion).*(practica)\b',
            ],
            'response': "¡Genial que quieras inscribirte! 🎉 Es muy sencillo, te explico:\n\n**El proceso es así de simple:**\n\n1️⃣ Inicia sesión con tu cuenta de estudiante\n\n2️⃣ Ve a 'Prácticas Disponibles' en el menú\n\n3️⃣ Explora y encuentra la que te gusta (léela bien 👀)\n\n4️⃣ Haz click en 'Ver detalles' para ver todo\n\n5️⃣ Si te convence, dale a 'Inscribirse'\n\n6️⃣ Confirma y ¡listo! Tu postulación está enviada 📨\n\n**⚠️ Cosas importantes que debes saber:**\n• Solo puedes inscribirte UNA vez en cada práctica\n• Una vez enviada, no se puede cancelar fácilmente\n• La empresa revisará tu perfil y decidirá\n\n**Tu postulación puede estar:**\n⏳ Pendiente - La empresa está revisando tu perfil\n✅ Aprobada - ¡Felicitaciones, lo lograste!\n❌ Rechazada - No pasa nada, hay más oportunidades\n\n¿Tienes dudas sobre algún paso?"
        },
        {
            'patterns': [
                r'\b(requisito|necesito|documento|debo).*(practica|inscribir)\b',
                r'\b(que necesito|que debo).*(practica)\b',
            ],
            'response': "📋 **Requisitos para Prácticas**\n\n**Académicos:**\n✓ 60% de créditos aprobados\n✓ Estar matriculado\n✓ Promedio mínimo según carrera\n\n**Documentación:**\n✓ CV actualizado (PDF)\n✓ Certificado de matrícula\n✓ Récord académico\n✓ Carta de compromiso (algunos casos)\n\n**Personales:**\n✓ Disponibilidad de tiempo\n✓ Compromiso y responsabilidad\n✓ Habilidades según la práctica\n\n¿Necesitas información sobre documentos específicos?"
        },
        {
            'patterns': [
                r'\b(practica interna|practica dentro|dentro de uleam)\b',
                r'\b(ver|muestra|dame).*(practica interna)\b',
                r'\b(mostrar practica interna)\b',
            ],
            'response': lambda: get_practicas_internas_disponibles()
        },
        {
            'patterns': [
                r'\b(todas las practica|ver todas|mostrar todas).*(practica|disponible)\b',
                r'\b(practica externa).*(interna)\b',
            ],
            'response': lambda: f"{get_practicas_disponibles()}\n\n---\n\n{get_practicas_internas_disponibles()}"
        },
        {
            'patterns': [
                r'\b(diferencia|diferente).*(externa|interna)\b',
                r'\b(tipo|clase).*(practica)\b',
            ],
            'response': lambda: f"🏢 **Tipos de Prácticas**\n\n**EXTERNAS (en empresas):**\n• Mayor exposición laboral\n• Networking profesional\n• Experiencia del mercado\n• Posible vinculación laboral\n\n**INTERNAS (en ULEAM):**\n• Servicio a la comunidad\n• Apoyo a facultades\n• Proyectos académicos\n• Horarios más flexibles\n\n**Ambas valen igual académicamente** ✓\n\n{get_estadisticas_sistema()}"
        },
        
        # ============ EVALUACIÓN Y CALIFICACIONES ============
        {
            'patterns': [
                r'\b(como|quien|cuando).*(evalua|califica|nota)\b',
                r'\b(evaluacion|calificacion|nota).*(practica)\b',
            ],
            'response': "Te cuento cómo funciona la evaluación 😊 Es importante que lo sepas desde el inicio:\n\n**¿Quién te evalúa?**\n🏢 Si estás en una empresa → Ellos te califican\n🎓 Si estás en la universidad → Tu facultad te evalúa\n\n**¿Qué evalúan?**\n\nTe califican en 2 cosas diferentes:\n\n1️⃣ **Tu COMPORTAMIENTO** (cómo te portas, tu actitud)\nLas notas van de la A a la E:\n• **A** = Eres excelente (9-10) 🌟\n• **B** = Muy bien (7-8) 👍\n• **C** = Vas bien pero puedes mejorar (4-6)\n• **D** = Necesitas esforzarte más (1-3)\n• **E** = Hay problemas serios (<1) 😟\n\n2️⃣ **Tus PROYECTOS** (el trabajo que haces)\nAquí las notas son:\n• **EX** = Excelente trabajo (10.00) 🏆\n• **MB** = Muy bueno (9.00-9.99) 💪\n• **B** = Buen trabajo (7.00-8.99) ✓\n• **R** = Regular, a mejorar (<7.00)\n\n**¿Cada cuánto?**\nTe evalúan cada período (3 por quimestre), así sabes cómo vas y puedes mejorar.\n\nTransquilo, si te esfuerzas, ¡te irá súper bien! 💯"
        },
        {
            'patterns': [
                r'\b(quimestre|periodo|cuando evaluan|cuando me evaluan)\b',
                r'\b(cada cuanto|frecuencia).*(evaluacion)\b',
            ],
            'response': "📅 **Períodos de Evaluación**\n\n**Estructura:**\n• 2 Quimestres al año\n• 3 Períodos por quimestre\n\n**QUIMESTRE 1:**\n📍 Período 1 (P1)\n📍 Período 2 (P2)\n📍 Período 3 (P3)\n\n**QUIMESTRE 2:**\n📍 Período 1 (P1)\n📍 Período 2 (P2)\n📍 Período 3 (P3)\n\n**Evaluación continua:**\n• Comportamiento en cada período\n• Proyectos por período\n• Retroalimentación constante\n\n✅ Nota final: Promedio de todos los períodos"
        },
        {
            'patterns': [
                r'\b(ver|donde|consultar|como veo).*(calificacion|nota|evaluacion)\b',
                r'\b(mis nota|mis calificacion|como veo mis nota)\b',
            ],
            'response': "📈 **Consultar Calificaciones**\n\nPasos:\n1. Inicia sesión como estudiante\n2. Ve a 'Mi Perfil'\n3. Selecciona 'Mis Inscripciones'\n4. Haz clic en la práctica activa\n5. Ve la pestaña 'Calificaciones'\n\n**Verás:**\n• Comportamiento por período (A, B, C, D, E)\n• Proyectos por período (EX, MB, B, R)\n• Observaciones del evaluador\n• Promedio parcial y final\n\n🔔 Recibirás notificación cuando haya nuevas calificaciones"
        },
        {
            'patterns': [
                r'\b(mas sobre evaluacion|mas informacion evaluacion|mas info evaluacion)\b',
                r'\b(detalles|explicame).*(evaluacion)\b',
            ],
            'response': "⭐ **Más Información sobre Evaluaciones**\n\n**¿Qué se evalúa?**\n\n1️⃣ **COMPORTAMIENTO (A-E):**\n• Puntualidad y asistencia\n• Actitud y compromiso\n• Trabajo en equipo\n• Proactividad\n• Responsabilidad\n\n2️⃣ **PROYECTOS (EX-R):**\n• Calidad del trabajo\n• Cumplimiento de objetivos\n• Creatividad e innovación\n• Aplicación de conocimientos\n• Resultados obtenidos\n\n**Escala de Comportamiento:**\n• A = Excelente (9-10)\n• B = Muy Bueno (7-8)\n• C = Bueno (4-6)\n• D = Regular (1-3)\n• E = Deficiente (<1)\n\n**Escala de Proyectos:**\n• EX = Excelente (10.00)\n• MB = Muy Bueno (9.00-9.99)\n• B = Bueno (7.00-8.99)\n• R = Regular (<7.00)\n\n**¿Quién evalúa?**\n👔 Supervisor de la empresa/facultad\n📊 Basado en rúbricas oficiales\n📝 Con observaciones detalladas\n\n✅ La nota mínima para aprobar es 7.0/10"
        },
        
        # ============ EMPRESAS ============
        {
            'patterns': [
                r'\b(lista|ver|buscar|conocer|muestra|dame).*(empresa|empleador)\b',
                r'\b(empresa|compañia).*(colabora|asociada|disponible)\b',
                r'\b(todas las empresa)\b',
            ],
            'response': lambda: get_empresas_colaboradoras()
        },
        {
            'patterns': [
                r'\b(empresa).*(tecnologia|tech|software|sistemas)\b',
            ],
            'response': lambda: get_empresas_colaboradoras('tecnologia')
        },
        {
            'patterns': [
                r'\b(empresa).*(salud|medica|hospital|clinica)\b',
            ],
            'response': lambda: get_empresas_colaboradoras('salud')
        },
        {
            'patterns': [
                r'\b(empresa).*(educacion|educativa|colegio|escuela)\b',
            ],
            'response': lambda: get_empresas_colaboradoras('educacion')
        },
        {
            'patterns': [
                r'\b(cuentame|informacion|info|que tal).*(practica externa)\b',
                r'\b(sobre|acerca).*(practica externa)\b',
            ],
            'response': lambda: f"🏢 **Prácticas Externas**\n\nSon prácticas que realizas en empresas privadas. ¡La mejor forma de conocer el mundo laboral real!\n\n**Ventajas:**\n✓ Experiencia profesional directa\n✓ Networking con empresas\n✓ Posibilidad de contratación\n✓ Conoces el mercado laboral\n✓ Referencias profesionales\n\n{get_practicas_disponibles()}"
        },
        {
            'patterns': [
                r'\b(cuentame|informacion|info|que tal).*(practica interna)\b',
                r'\b(sobre|acerca).*(practica interna)\b',
            ],
            'response': lambda: f"🎓 **Prácticas Internas**\n\nSon prácticas que realizas dentro de ULEAM, apoyando a las diferentes facultades y áreas.\n\n**Ventajas:**\n✓ Horarios más flexibles\n✓ Cerca del campus\n✓ Ambiente conocido\n✓ Servicio a la comunidad\n✓ Proyectos académicos\n\n{get_practicas_internas_disponibles()}"
        },
        {
            'patterns': [
                r'\b(empresa).*(ofrece|publica|crea).*(practica)\b',
                r'\b(como empresa|siendo empresa).*(publicar|ofrecer)\b',
            ],
            'response': "📝 **Publicar Prácticas (Empresas)**\n\nPasos:\n1. Inicia sesión como empresa\n2. Ve a 'Panel de Control'\n3. Clic en 'Nueva Práctica'\n4. Completa:\n   • Título atractivo\n   • Descripción detallada\n   • Requisitos específicos\n   • Duración (horas)\n   • Horario\n   • Cupos disponibles\n   • Fecha límite de inscripción\n5. Publicar\n\n✅ Automáticamente visible para estudiantes\n📊 Recibirás postulaciones en tu panel"
        },
        {
            'patterns': [
                r'\b(empresa).*(evalua|califica|revisa).*(estudiante|postulante)\b',
                r'\b(como evaluar|evaluacion de estudiante)\b',
            ],
            'response': "⭐ **Evaluar Estudiantes (Empresas)**\n\nProceso:\n1. Panel de Empresa → 'Postulantes'\n2. Selecciona la práctica\n3. Lista de estudiantes inscritos\n4. Clic en 'Evaluar'\n\n**Secciones:**\n\n📊 **Calificaciones por Quimestre:**\n• Comportamiento (A-E) x 3 períodos\n• Proyectos (EX-R) x 3 períodos\n• Guardar calificaciones\n\n✅ **Decisión Final:**\n• Aprobar postulante\n• Rechazar (con observaciones)\n• Observaciones generales\n\n🔔 El estudiante recibe notificación inmediata"
        },
        
        # ============ DOCUMENTOS ============
        {
            'patterns': [
                r'\b(documento|archivo|subir|cargar).*(necesito|debo|requiere)\b',
                r'\b(documento requerido|documento necesario)\b',
            ],
            'response': "📄 **Documentos Requeridos**\n\n**Para Inscripción:**\n1. CV actualizado (PDF, máx 2MB)\n2. Certificado de matrícula\n3. Récord académico\n\n**Durante la Práctica:**\n4. Informes mensuales\n5. Bitácora de actividades\n6. Evidencias de proyectos\n\n**Al Finalizar:**\n7. Informe final\n8. Certificado de la empresa\n9. Evaluación de supervisor\n\n**Formatos aceptados:**\n• PDF (preferido)\n• DOCX\n• JPG/PNG (solo imágenes)\n\n⚠️ Tamaño máximo: 5MB por archivo"
        },
        {
            'patterns': [
                r'\b(informacion|info|sobre|acerca).*(cv|curriculum)\b',
                r'\b(como hacer|que poner|que incluir).*(cv)\b',
            ],
            'response': "📄 **Sobre el CV (Currículum Vitae)**\n\n**Debe incluir:**\n✓ Datos personales (nombre, email, teléfono)\n✓ Objetivo profesional\n✓ Formación académica (carrera, universidad, ciclo)\n✓ Experiencia laboral (si tienes)\n✓ Habilidades técnicas\n✓ Idiomas\n✓ Referencias (opcionales)\n\n**Formato:**\n• PDF (preferido)\n• Máximo 2MB\n• Máximo 2 páginas\n• Fuente legible (Arial, Calibri)\n\n**Tips:**\n💡 Sé honesto y claro\n💡 Sin faltas de ortografía\n💡 Organizado y profesional\n💡 Actualízalo regularmente\n\n¿Necesitas ayuda con otro documento?"
        },
        {
            'patterns': [
                r'\b(que certificado|certificado necesario|que certificado necesito)\b',
                r'\b(sobre|acerca).*(certificado)\b',
            ],
            'response': "✅ **Certificados Necesarios**\n\n**Al inicio:**\n📋 Certificado de matrícula (actual)\n📋 Récord académico (desde secretaría)\n📋 Certificado de aprobación del 60% de créditos\n\n**Durante la práctica:**\n📋 Certificados de asistencia a talleres (si hay)\n📋 Certificados de capacitaciones\n\n**Al finalizar:**\n📋 Certificado de la empresa/facultad\n📋 Certificado de culminación (lo da ULEAM)\n\n**¿Dónde conseguirlos?**\n🏢 Secretaría de tu facultad\n🏢 Coordinación de prácticas\n🏢 Portal estudiantil ULEAM\n\n¿Algún certificado específico?"
        },
        {
            'patterns': [
                r'\b(lista completa|todos los documento|que documento)\b',
            ],
            'response': "📁 **Lista Completa de Documentos**\n\n**ETAPA 1 - INSCRIPCIÓN:**\n1️⃣ CV actualizado (PDF)\n2️⃣ Certificado de matrícula\n3️⃣ Récord académico\n4️⃣ Foto tamaño carnet\n5️⃣ Copia de cédula\n\n**ETAPA 2 - DURANTE LA PRÁCTICA:**\n6️⃣ Informes mensuales de actividades\n7️⃣ Bitácora diaria\n8️⃣ Evidencias fotográficas\n9️⃣ Reportes de proyectos\n\n**ETAPA 3 - FINALIZACIÓN:**\n🔟 Informe final completo\n1️⃣1️⃣ Certificado de la empresa\n1️⃣2️⃣ Encuesta de satisfacción\n1️⃣3️⃣ Carta de recomendación (opcional)\n\n💡 No te preocupes, te avisaremos qué necesitas en cada momento."
        },
        {
            'patterns': [
                r'\b(gestionar|administrar|ver).*(documento)\b',
                r'\b(donde subo|como subo).*(archivo|documento)\b',
            ],
            'response': "📁 **Gestión de Documentos**\n\n**Subir Documentos:**\n1. Perfil → 'Mis Inscripciones'\n2. Selecciona práctica activa\n3. Pestaña 'Documentos'\n4. Clic en 'Subir Documento'\n5. Selecciona tipo de documento\n6. Elige el archivo\n7. Guardar\n\n**Tipos:**\n• CV\n• Certificados\n• Informes\n• Evidencias\n• Otros\n\n✅ El evaluador verá tus documentos\n📥 Puedes descargarlos cuando quieras"
        },
        
        # ============ PROBLEMAS TÉCNICOS ============
        {
            'patterns': [
                r'\b(no puedo|error|problema|falla|bug).*(entrar|acceder|login|ingresar)\b',
                r'\b(no funciona|no carga).*(pagina|sistema)\b',
            ],
            'response': "¡Uy! Veo que tienes problemas para entrar 😕 No te preocupes, vamos a solucionarlo juntos:\n\n**Primero lo básico (funciona el 80% de las veces):**\n\n✅ Revisa que tu email esté bien escrito (sin espacios extras)\n✅ La contraseña es sensible a mayúsculas/minúsculas\n✅ ¿Quizás Caps Lock está activado? 🔠\n\n**Si eso no funciona, prueba esto:**\n\n🧹 Limpia la caché del navegador:\n• Presiona Ctrl + Shift + Delete\n• Marca 'Cookies' y 'Caché'\n• Borra y cierra el navegador\n• Ábrelo de nuevo\n\n🌐 Intenta con otro navegador:\n• Chrome funciona mejor (te lo recomiendo)\n• Firefox también va bien\n• Edge si estás en Windows\n\n📶 Verifica tu internet:\n• ¿Está estable tu conexión?\n• ¿Tienes un VPN activo? A veces causan problemas\n\n**¿Nada de esto funcionó?** 🤔\nNo te frustres, contacta al soporte técnico:\n📧 soporte@uleam.edu.ec\n📞 (+593) 5-262-3740 Ext. 123\n\nEllos te ayudarán personalmente. ¡Ánimo!"
        },
        {
            'patterns': [
                r'\b(no recibo|no llega).*(correo|email|notificacion)\b',
                r'\b(notificacion|alerta).*(no funciona)\b',
            ],
            'response': "📧 **Problemas con Correos**\n\n**Verificaciones:**\n1. ✉️ Revisa carpeta SPAM/Correo no deseado\n2. 📧 Confirma email registrado en perfil\n3. 🔍 Busca remitente: noreply@uleam.edu.ec\n4. 📬 Espera 5-10 minutos\n\n**Agregar a contactos seguros:**\n• noreply@uleam.edu.ec\n• notificaciones@uleam.edu.ec\n\n**Cambiar email:**\n• Ve a 'Mi Perfil'\n• Editar información\n• Actualizar email\n• Verificar nuevo correo\n\n⚠️ Los correos institucionales (@uleam.edu.ec) tienen prioridad"
        },
        
        # ============ CONTACTO Y SOPORTE ============
        {
            'patterns': [
                r'\b(contacto|comunicar|hablar|llamar).*(soporte|ayuda|admin)\b',
                r'\b(telefono|email|correo).*(soporte|contacto)\b',
            ],
            'response': "¡Claro! Te paso todos los contactos 📞\n\n**¿Problemas técnicos con el sistema?**\n📧 Escribe a: soporte.practicas@uleam.edu.ec\n📱 O llama: (+593) 5-262-3740 Ext. 123\n🕒 Te atienden: Lunes a Viernes, 8am-5pm\n\n**¿Dudas sobre tu práctica o inscripción?**\n📧 Contacta a: practicas@uleam.edu.ec\n📱 Teléfono: (+593) 5-262-3740 Ext. 456\n🏢 O pásate por: Edificio Administrativo, 2do piso\n\n**¿Prefieres redes sociales?**\n📘 Facebook: /ULEAMPracticas\n📸 Instagram: @uleam_practicas\n\n💡 **Mi consejo:** El email es más rápido y te responden en menos de 24 horas. Por teléfono a veces están ocupados.\n\n¿Necesitas que te explique algo más antes de contactarlos?"
        },
        {
            'patterns': [
                r'\b(horario|cuando|atencion).*(oficina|soporte)\b',
            ],
            'response': "🕒 **Horarios de Atención**\n\n**Oficina de Prácticas:**\n📅 Lunes a Viernes\n⏰ 8:00 AM - 5:00 PM\n🏢 Edificio Administrativo, Piso 2\n\n**Soporte Técnico:**\n📧 Email: 24/7 (respuesta en 24h)\n📞 Teléfono: Lun-Vie 8:00-17:00\n💬 Chat: Lun-Vie 9:00-16:00\n\n**Atención Presencial:**\n• Con cita previa (recomendado)\n• O por orden de llegada\n• Máximo 30 min por consulta\n\n🎯 Reserva tu cita en línea para evitar esperas"
        },
        
        # ============ PREGUNTAS FRECUENTES ============
        {
            'patterns': [
                r'\b(cuanto|duracion|tiempo).*(practica|pasantia)\b',
                r'\b(hora|cuantas hora)\b',
            ],
            'response': "Buena pregunta, así sabes cómo organizarte ⏱️\n\n**Depende del tipo de práctica:**\n\n🏢 **En empresas (externas):**\nEntre 240 y 480 horas\nLa mayoría son de 320-360 horas\n\n🎓 **En la universidad (internas):**\nEntre 240 y 400 horas\nGeneralmente 280-320 horas\n\n**¿Cómo se distribuye?**\nNormalmente en 3 a 6 meses, trabajando:\n📅 Entre 4 y 8 horas al día\n📆 Unas 20-40 horas por semana\n\n**Lo importante:**\n✅ Se ajusta a tu horario de clases (¡no te preocupes!)\n✅ No debe interferir con tus materias obligatorias\n✅ Tú y la empresa/facultad acuerdan los horarios\n\nPiensa que es como un trabajo de medio tiempo que combinas con la U. ¡Es totalmente manejable! 💪\n\n¿Te preocupa el tiempo? Hablemos de eso."
        },
        {
            'patterns': [
                r'\b(paga|remunera|sueldo|salario|dinero).*(practica)\b',
                r'\b(practica).*(paga|cobra|sueldo)\b',
            ],
            'response': "Sé que es una pregunta importante 💰 Te doy la verdad completa:\n\n**La realidad es:**\n❌ Las prácticas pre-profesionales oficialmente NO son pagadas\n\n¿Por qué? Porque son parte de tu formación académica, como una materia más.\n\n**PERO... aquí viene lo bueno: 😊**\n\n🎁 Muchas empresas sí dan beneficios:\n• Algunas ofrecen un estipendio (ayuda económica)\n• Otras pagan transporte\n• Algunas dan almuerzo\n• Depende de cada empresa y su generosidad\n\n**El verdadero valor está en:**\n✨ La experiencia que ganas (¡no tiene precio!)\n✨ Los contactos que haces (networking)\n✨ Tu CV se pone súper interesante\n✨ Referencias laborales reales\n✨ Muchas veces te contratan después\n\nPiénsalo así: estás invirtiendo en tu futuro. Conozco muchos casos donde terminaron con trabajo fijo después de las prácticas.\n\n💼 Nota: Las pasantías pagadas son otra cosa diferente.\n\n¿Quieres que te cuente más sobre los beneficios reales?"
        },
        {
            'patterns': [
                r'\b(cuanto|cuantas|numero).*(practica|inscribir|tomar)\b',
                r'\b(varias|multiple).*(practica)\b',
            ],
            'response': "🎯 **Número de Prácticas**\n\n**Límites:**\n• 1️⃣ UNA inscripción activa por vez\n• ❌ NO puedes inscribirte en múltiples simultáneamente\n• ✅ Puedes aplicar a otra después de completar una\n\n**Razones:**\n• Garantiza tu compromiso\n• Evita sobrecarga académica\n• Respeta a empresas y otros estudiantes\n• Asegura calidad del aprendizaje\n\n**Si necesitas más experiencia:**\n• Completa una práctica\n• Luego aplica a prácticas complementarias\n• O busca voluntariados paralelos\n\n⚠️ Intentar registrarse dos veces en la misma práctica está bloqueado"
        },
        {
            'patterns': [
                r'\b(cancelar|retirar|salir).*(practica|inscripcion)\b',
                r'\b(ya no quiero|desistir)\b',
            ],
            'response': "⚠️ **Cancelar Inscripción**\n\n**Si está PENDIENTE:**\n✅ Puedes cancelar desde tu perfil\n• Mi Perfil → Mis Inscripciones\n• Clic en 'Cancelar Inscripción'\n• Confirmar acción\n\n**Si está APROBADA:**\n❌ NO puedes cancelar por tu cuenta\n📧 Debes contactar a:\n• Coordinación de Prácticas\n• Justificar motivo válido\n• Puede afectar tu récord\n\n**Consecuencias:**\n• Puede retrasar tu graduación\n• Posible penalización\n• Afecta disponibilidad de cupos\n\n💡 Piensa bien antes de inscribirte"
        },
        {
            'patterns': [
                r'\b(certificado|constancia|diploma).*(practica)\b',
                r'\b(como obtengo|cuando recibo).*(certificado)\b',
            ],
            'response': "¡El famoso certificado! 🎓 Ese papelito importante para tu carpeta.\n\nTe cuento cómo lo consigues:\n\n**¿Qué necesitas para que te lo den?**\n✅ Completar todas las horas (sin excepción)\n✅ Que tus evaluaciones estén aprobadas\n✅ Haber entregado toda la documentación y el informe final\n\n**¿Qué trae el certificado?**\n• Tu nombre completo\n• Cuánto tiempo hiciste de práctica\n• En qué empresa o facultad\n• Tus calificaciones finales\n• Firmas oficiales y sellos (lo importante 😉)\n\n**El proceso:**\n1️⃣ Terminas tus horas completas\n2️⃣ Apruebas tu evaluación final\n3️⃣ Entregas tu informe final (bien hecho)\n4️⃣ Esperas unos 15 días hábiles (sé paciente)\n5️⃣ ¡Vas a Secretaría y lo recoges!\n\n📥 **Bonus:** También te lo pueden dar en formato digital para que lo tengas en tu compu.\n\nEse certificado vale oro para tu CV y futuras entrevistas. ¡Cuídalo bien!"
        },
        
        # ============ FACULTADES (INTERNAS) ============
        {
            'patterns': [
                r'\b(facultad|universidad).*(practica|ofrece)\b',
                r'\b(practica interna|dentro de uleam)\b',
            ],
            'response': "🏫 **Prácticas Internas ULEAM**\n\n**Áreas disponibles:**\n• Secretarías académicas\n• Laboratorios\n• Biblioteca\n• Extensión universitaria\n• Vinculación con la sociedad\n• Investigación\n• Comunicación institucional\n\n**Ventajas:**\n✓ Cerca del campus\n✓ Horarios flexibles\n✓ Contacto con docentes\n✓ Acceso a recursos ULEAM\n✓ Ambiente conocido\n\n**Proceso:**\nIgual que prácticas externas:\n• Revisar oferta\n• Inscribirse\n• Evaluación por facultad\n• Sistema de calificaciones\n\n¿Te interesa alguna facultad específica?"
        },
        {
            'patterns': [r'\b(empresa.*tecnologia|tecnologia|sector tecnologico)\b'],
            'response': lambda: get_empresas_colaboradoras('tecnología')
        },
        {
            'patterns': [r'\b(empresa.*salud|salud|sector salud|sector sanitario)\b'],
            'response': lambda: get_empresas_colaboradoras('salud')
        },
        {
            'patterns': [r'\b(empresa.*educacion|educacion|sector educativo)\b'],
            'response': lambda: get_empresas_colaboradoras('educación')
        },
        {
            'patterns': [r'\b(horario.*atencion|cuando atienden|horario oficina)\b'],
            'response': """🕐 **Horarios de Atención**

📍 **Oficina de Prácticas Pre-profesionales**

🗓️ **Lunes a Viernes**:
- **Mañana**: 08:00 - 12:30
- **Tarde**: 14:00 - 17:30

🚫 **Cerrado**: Sábados, domingos y feriados

📧 **Atención en línea**: 24/7 a través del sistema

💡 **Tip**: Para trámites rápidos, te recomiendo venir en horario de la mañana. Las tardes suelen estar más tranquilas si prefieres una atención más personalizada. 😊"""
        },
        {
            'patterns': [r'\b(email|correo|contacto|escribir)\b', r'\b(contacto de soporte|contactar soporte|necesito contactar soporte)\b'],
            'response': """📧 **Información de Contacto**

📬 **Email oficial**:
practicas@uleam.edu.ec

📍 **Ubicación**:
Universidad Laica Eloy Alfaro de Manabí
Ciudadela Universitaria, Edificio Administrativo
Manta - Ecuador

📞 **Teléfono** (próximamente):
En este momento, el canal principal es el correo electrónico.

💬 **Asistente Virtual**:
Estoy aquí 24/7 para ayudarte con dudas generales, consultas sobre prácticas y más. 😊

⚡ **Tiempo de respuesta**: Generalmente respondemos correos en 24-48 horas hábiles.

💡 **Tip**: Para consultas urgentes, menciona "URGENTE" en el asunto del email."""
        },
        {
            'patterns': [r'\b(como son los horarios|horarios de las practicas)\b'],
            'response': """⏰ **Horarios de las Prácticas**

Los horarios dependen del tipo de práctica y se coordinan entre tú y la empresa/facultad:

🏢 **Prácticas Externas:**
• Generalmente 4-8 horas diarias
• Pueden ser corridos o divididos
• Horario a negociar con la empresa
• ¡Importante! No debe interferir con tus clases obligatorias

🎓 **Prácticas Internas:**
• Horarios más flexibles
• Se adaptan a tu carga académica
• Coordinación directa con tu facultad
• Pueden ser por la mañana o tarde

📋 **Requisito:**
Debes cumplir las horas totales (240-480 horas según tu práctica) distribuidas en el periodo acordado.

💡 **Tip**: Durante la inscripción, especifica tu disponibilidad horaria para que las empresas lo consideren."""
        },
        {
            'patterns': [r'\b(no me llegan notificaciones|no recibo correos|no llegan emails)\b'],
            'response': """📧 **No recibes notificaciones?**

No te preocupes, vamos a solucionarlo 😊

**Primero revisa:**

1️⃣ **Carpeta de Spam/Correo no deseado**
   • Los emails pueden estar ahí
   • Marca como "No es spam"
   • Agrega practicas@uleam.edu.ec a contactos

2️⃣ **Email correcto en tu perfil**
   • Inicia sesión → Mi Perfil
   • Verifica que tu email esté bien escrito
   • Actualiza si es necesario

3️⃣ **Configuración de notificaciones**
   • Mi Perfil → Configuración
   • Activa las notificaciones por email
   • Guarda cambios

**Si ya revisaste todo eso:**
📞 Contacta a soporte técnico:
📧 practicas@uleam.edu.ec
Con tu nombre completo y email registrado.

🔄 Te reenviarán las notificaciones pendientes."""
        },
        {
            'patterns': [r'\b(tengo otra pregunta|otra pregunta|otra consulta)\b'],
            'response': """¡Por supuesto! 😊 Estoy aquí para ayudarte con todo lo que necesites.

¿Qué más te gustaría saber? Puedo ayudarte con:

📝 **Registro e inscripciones**
💼 **Prácticas disponibles**
📄 **Documentos necesarios**
⭐ **Evaluaciones y calificaciones**
🏢 **Empresas colaboradoras**
🔧 **Problemas técnicos**
📞 **Contacto y horarios**

Solo pregúntame lo que necesites. ¡No hay límite de preguntas! 💬"""
        },
        
        # ============ NAVEGACIÓN DEL SISTEMA ============
        {
            'patterns': [
                r'\b(como usar|como funciona|tutorial|guia).*(sistema|plataforma|pagina)\b',
                r'\b(navegar|usar|manejar).*(sistema)\b',
            ],
            'response': "🧭 **Guía de Navegación del Sistema**\n\n**MENÚ PRINCIPAL:**\n🏠 Inicio: Información general\n📋 Prácticas: Ofertas disponibles\n🏢 Empresas: Directorio completo\n👤 Perfil: Tu información\n📧 Notificaciones: Alertas\n\n**ESTUDIANTES:**\n• Ver prácticas disponibles\n• Inscribirse\n• Seguimiento de postulaciones\n• Consultar calificaciones\n• Gestionar documentos\n\n**EMPRESAS:**\n• Publicar prácticas\n• Revisar postulantes\n• Evaluar estudiantes\n• Ver reportes\n\n**FACULTADES:**\n• Gestionar prácticas internas\n• Evaluar estudiantes\n• Generar reportes\n\n💡 Todo es intuitivo con iconos claros"
        },
        
        # ============ AYUDA GENERAL ============
        {
            'patterns': [
                r'\b(ayuda|help|auxilio|no se|no entiendo|necesito ayuda)\b',
            ],
            'response': "¡Tranquilo! Estoy aquí para ayudarte 😊 Cuéntame, ¿con qué necesitas una mano?\n\n**Cosas con las que puedo ayudarte:**\n\n�‍🎓 **Si eres estudiante:**\n• Cómo registrarte en el sistema\n• Buscar prácticas perfectas para ti\n• Inscribirte paso a paso\n• Ver tus calificaciones\n• Subir tus documentos\n\n🏢 **Si representas una empresa:**\n• Crear cuenta de empresa\n• Publicar ofertas de prácticas\n• Revisar y evaluar estudiantes\n• Usar el sistema de calificaciones\n\n🤔 **Dudas generales:**\n• Qué documentos necesitas\n• Los diferentes tipos de prácticas\n• Cuánto tiempo toma\n• Cómo conseguir tu certificado\n• Problemas técnicos\n\n💬 **Háblame con confianza**, pregúntame lo que sea. No hay preguntas tontas, ¡todas son válidas!\n\n¿Qué te tiene con dudas?"
        },
        
        # ============ RESPUESTA POR DEFECTO ============
        {
            'patterns': [r'.*'],  # Catch-all
            'response': "Mmm... 🤔 Creo que no capté bien lo que necesitas.\n\nNo te preocupes, es que a veces no entiendo todo (todavía estoy aprendiendo 😅).\n\n**Estos son los temas donde soy experto:**\n\n📝 Cómo registrarte y crear tu cuenta\n📚 Todo sobre las prácticas (externas e internas)\n🏢 Empresas que ofrecen prácticas\n📊 Sistema de calificaciones\n📄 Qué documentos necesitas\n🔧 Solucionar problemas técnicos\n📞 Contactos de ayuda\n\n**Prueba preguntándome algo como:**\n• \"¿Cómo me inscribo en una práctica?\"\n• \"¿Qué documentos debo tener?\"\n• \"¿Cómo veo mis notas?\"\n• \"Muéstrame empresas\"\n• \"Olvidé mi contraseña\"\n\n💬 Intenta reformular tu pregunta de otra manera, ¡seguro así te entiendo! O si prefieres, pregúntame lo más específico que puedas.\n\n¿En qué estabas pensando exactamente?"
        }
    ]
    
    # Buscar coincidencia
    for response_data in responses:
        for pattern in response_data['patterns']:
            if re.search(pattern, msg, re.IGNORECASE):
                # Si la respuesta es una función, ejecutarla
                response_text = response_data['response']
                if callable(response_text):
                    response_text = response_text()
                options = get_contextual_options(response_text, msg)
                return {'response': response_text, 'options': options}
    
    # Fallback (no debería llegar aquí por el catch-all)
    return {
        'response': "No pude procesar tu mensaje. ¿Puedes intentar de nuevo?",
        'options': [
            {'icon': 'bi-person-plus', 'text': 'Registro', 'message': '¿Cómo me registro?'},
            {'icon': 'bi-briefcase', 'text': 'Prácticas', 'message': 'Ver prácticas disponibles'},
            {'icon': 'bi-headset', 'text': 'Ayuda', 'message': 'Necesito ayuda'}
        ]
    }


def get_contextual_options(response_text, original_message):
    """Genera opciones contextuales basadas en la respuesta"""
    options = []
    
    # Menú principal
    if 'menú principal' in response_text.lower() or 'volver' in original_message.lower() or 'selecciona una opción' in response_text.lower():
        options = [
            {'icon': 'bi-person-plus-fill', 'text': '📝 ¿Cómo me registro?', 'message': '¿Cómo me registro?'},
            {'icon': 'bi-briefcase-fill', 'text': '💼 Ver prácticas disponibles', 'message': 'Ver prácticas disponibles'},
            {'icon': 'bi-clipboard-check-fill', 'text': '✅ ¿Cómo inscribirme?', 'message': '¿Cómo me inscribo en una práctica?'},
            {'icon': 'bi-file-earmark-text-fill', 'text': '📄 ¿Qué documentos necesito?', 'message': '¿Qué documentos necesito?'},
            {'icon': 'bi-star-fill', 'text': '⭐ ¿Cómo son las evaluaciones?', 'message': '¿Cómo funciona la evaluación?'},
            {'icon': 'bi-clock-fill', 'text': '⏱️ Duración y horarios', 'message': '¿Cuánto dura una práctica?'},
            {'icon': 'bi-building-fill', 'text': '🏢 Empresas colaboradoras', 'message': 'Lista de empresas'},
            {'icon': 'bi-key-fill', 'text': '🔑 Olvidé mi contraseña', 'message': 'Olvidé mi contraseña'},
            {'icon': 'bi-headset', 'text': '📞 Contactar soporte', 'message': 'Contacto de soporte'}
        ]
        return options
    
    # Opciones para registro
    if '¿quién eres?' in response_text.lower() or 'tipo de registro' in response_text.lower() or '¿cuál es tu caso?' in response_text.lower():
        options = [
            {'icon': 'bi-mortarboard-fill', 'text': '👨‍🎓 Soy Estudiante', 'message': 'Quiero registrarme como estudiante'},
            {'icon': 'bi-building-fill', 'text': '🏢 Soy Empresa', 'message': 'Quiero registrar mi empresa'},
            {'icon': 'bi-bank-fill', 'text': '🎓 Soy Facultad', 'message': 'Registro de facultad'},
            {'icon': 'bi-arrow-left-circle', 'text': '↩️ Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones para tipos de prácticas o cuando se muestran prácticas
    elif 'tipo específico' in response_text.lower() or 'tipos de prácticas' in response_text.lower() or 'ambas' in response_text.lower() or 'prácticas externas disponibles' in response_text.lower() or 'cupos:' in response_text.lower():
        options = [
            {'icon': 'bi-briefcase-fill', 'text': '🏢 Ver Prácticas Externas', 'message': 'Ver prácticas disponibles'},
            {'icon': 'bi-bank-fill', 'text': '🎓 Ver Prácticas Internas', 'message': 'Ver prácticas internas'},
            {'icon': 'bi-building-fill', 'text': '🏢 Ver Empresas', 'message': 'Lista de empresas'},
            {'icon': 'bi-arrow-left-circle', 'text': '↩️ Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones para empresas y sectores
    elif 'empresas colaboradoras' in response_text.lower() or 'empresas del sector' in response_text.lower() or 'sector:' in response_text.lower():
        options = [
            {'icon': 'bi-laptop-fill', 'text': '💻 Empresas de Tecnología', 'message': 'Empresas de tecnología'},
            {'icon': 'bi-heart-pulse-fill', 'text': '🏥 Empresas de Salud', 'message': 'Empresas de salud'},
            {'icon': 'bi-book-fill', 'text': '📚 Empresas de Educación', 'message': 'Empresas de educación'},
            {'icon': 'bi-briefcase-fill', 'text': '💼 Ver sus prácticas', 'message': 'Ver prácticas disponibles'},
            {'icon': 'bi-arrow-left-circle', 'text': '↩️ Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones para documentos
    elif 'documentos requeridos' in response_text.lower() or 'sobre el cv' in response_text.lower() or 'certificados necesarios' in response_text.lower() or 'lista completa de documentos' in response_text.lower():
        options = [
            {'icon': 'bi-file-earmark-pdf-fill', 'text': '📄 Sobre el CV', 'message': 'Información sobre CV'},
            {'icon': 'bi-file-earmark-check-fill', 'text': '✅ Certificados necesarios', 'message': 'Qué certificados necesito'},
            {'icon': 'bi-folder-fill', 'text': '📁 Lista completa de documentos', 'message': 'Lista completa de documentos'},
            {'icon': 'bi-arrow-left-circle', 'text': '↩️ Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones para evaluación
    elif 'evaluación' in response_text.lower() or 'califica' in response_text.lower() or 'comportamiento' in response_text.lower() or 'proyectos' in response_text.lower():
        options = [
            {'icon': 'bi-calendar-check-fill', 'text': '📅 ¿Cuándo me evalúan?', 'message': 'Cuándo me evalúan'},
            {'icon': 'bi-graph-up-arrow', 'text': '📊 ¿Cómo veo mis notas?', 'message': 'Cómo veo mis calificaciones'},
            {'icon': 'bi-info-circle-fill', 'text': 'ℹ️ Más sobre evaluaciones', 'message': 'Más información sobre evaluaciones'},
            {'icon': 'bi-arrow-left-circle', 'text': '↩️ Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones para problemas técnicos
    elif 'problemas' in response_text.lower() or 'error' in original_message.lower():
        options = [
            {'icon': 'bi-key', 'text': 'Contraseña', 'message': 'Olvidé mi contraseña'},
            {'icon': 'bi-envelope', 'text': 'No recibo correos', 'message': 'No me llegan notificaciones'},
            {'icon': 'bi-headset', 'text': 'Contactar Soporte', 'message': 'Necesito contactar soporte técnico'}
        ]
    
    # Opciones para ayuda general
    elif 'ayuda' in response_text.lower() or '¿en qué' in response_text.lower():
        options = [
            {'icon': 'bi-person-plus-fill', 'text': '📝 Registro', 'message': '¿Cómo me registro?'},
            {'icon': 'bi-briefcase-fill', 'text': '💼 Prácticas', 'message': 'Ver prácticas disponibles'},
            {'icon': 'bi-clipboard-check', 'text': '✅ Inscripción', 'message': '¿Cómo me inscribo en una práctica?'},
            {'icon': 'bi-star-fill', 'text': '⭐ Evaluación', 'message': '¿Cómo funciona la evaluación?'}
        ]
    
    # Opciones para preguntas frecuentes sobre práctica
    elif 'cuánto' in original_message.lower() or 'duración' in original_message.lower():
        options = [
            {'icon': 'bi-cash', 'text': '¿Pagan?', 'message': 'Las prácticas son pagadas'},
            {'icon': 'bi-calendar-event', 'text': 'Horarios', 'message': 'Cómo son los horarios'},
            {'icon': 'bi-award', 'text': 'Certificado', 'message': 'Cómo obtengo el certificado'}
        ]
    
    # Opciones después de respuestas de contacto
    elif 'contacto' in response_text.lower() or 'soporte' in response_text.lower():
        options = [
            {'icon': 'bi-clock', 'text': 'Horarios', 'message': 'Horarios de atención'},
            {'icon': 'bi-envelope-at', 'text': 'Escribir Email', 'message': 'Dame el email de soporte'},
            {'icon': 'bi-question-circle', 'text': 'Otra Consulta', 'message': 'Tengo otra pregunta'}
        ]
    
    # Opciones de seguimiento general
    elif '¿te ayudo' in response_text.lower() or 'algún campo' in response_text.lower() or 'alguna duda' in response_text.lower():
        options = [
            {'icon': 'bi-check-circle-fill', 'text': '✅ Entendido, gracias', 'message': 'Gracias, está claro'},
            {'icon': 'bi-question-circle-fill', 'text': '❓ Necesito más información', 'message': 'Necesito más información'},
            {'icon': 'bi-arrow-left-circle', 'text': '↩️ Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones después de respuestas de agradecimiento
    elif 'de nada' in response_text.lower() or 'placer ayudarte' in response_text.lower():
        options = [
            {'icon': 'bi-question-circle-fill', 'text': '❓ Otra pregunta', 'message': 'Tengo otra pregunta'},
            {'icon': 'bi-arrow-left-circle', 'text': '📋 Ver menú principal', 'message': 'Volver al menú principal'}
        ]
    
    # Opciones por defecto si no hay contexto específico
    elif not options:
        options = [
            {'icon': 'bi-question-circle-fill', 'text': '❓ Tengo otra pregunta', 'message': 'Tengo otra pregunta'},
            {'icon': 'bi-arrow-left-circle', 'text': '📋 Volver al menú', 'message': 'Volver al menú principal'}
        ]
    
    return options


def normalize_text(text):
    """Normaliza el texto para mejor coincidencia"""
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar tildes
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def get_practicas_disponibles():
    """Obtiene la lista de prácticas externas disponibles"""
    practicas = Practica.objects.filter(activa=True, estado='abierta').select_related('empresa')[:5]
    
    if not practicas:
        return "Actualmente no hay prácticas externas disponibles. Te recomiendo revisar la página regularmente, ya que se publican nuevas ofertas constantemente."
    
    response = "🎯 **Prácticas Externas Disponibles:**\n\n"
    for i, practica in enumerate(practicas, 1):
        response += f"{i}. **{practica.titulo}**\n"
        response += f"   🏢 Empresa: {practica.empresa.nombre}\n"
        response += f"   📍 Sector: {practica.empresa.sector}\n"
        response += f"   👥 Cupos: {practica.cupos_disponibles}\n"
        response += f"   📅 Inicio: {practica.fecha_inicio.strftime('%d/%m/%Y')}\n"
        response += f"   ⏰ Límite inscripción: {practica.fecha_limite_inscripcion.strftime('%d/%m/%Y')}\n\n"
    
    total = Practica.objects.filter(activa=True, estado='abierta').count()
    if total > 5:
        response += f"📋 Y {total - 5} prácticas más disponibles en el sistema.\n\n"
    
    response += "💡 Para ver todas las prácticas y más detalles, visita la sección 'Prácticas' en el menú principal."
    return response


def get_practicas_internas_disponibles():
    """Obtiene la lista de prácticas internas disponibles"""
    practicas = PracticaInterna.objects.filter(activa=True, estado='abierta').select_related('facultad')[:5]
    
    if not practicas:
        return "Actualmente no hay prácticas internas disponibles. Las prácticas internas se publican cada semestre."
    
    response = "🎓 **Prácticas Internas (ULEAM) Disponibles:**\n\n"
    for i, practica in enumerate(practicas, 1):
        response += f"{i}. **{practica.titulo}**\n"
        response += f"   🏛️ Facultad: {practica.facultad.nombre}\n"
        response += f"   📋 Tipo: {practica.get_tipo_servicio_display()}\n"
        response += f"   👥 Cupos: {practica.cupos_disponibles}\n"
        response += f"   📅 Inicio: {practica.fecha_inicio.strftime('%d/%m/%Y')}\n"
        response += f"   ⏰ Límite inscripción: {practica.fecha_limite_inscripcion.strftime('%d/%m/%Y')}\n\n"
    
    total = PracticaInterna.objects.filter(activa=True, estado='abierta').count()
    if total > 5:
        response += f"📋 Y {total - 5} prácticas internas más disponibles.\n\n"
    
    response += "💡 Para ver todas las prácticas internas, visita la sección 'Prácticas' en el menú principal."
    return response


def get_empresas_colaboradoras(sector=None):
    """Obtiene la lista de empresas colaboradoras"""
    if sector:
        empresas = Empresa.objects.filter(activa=True, sector__icontains=sector)[:5]
    else:
        empresas = Empresa.objects.filter(activa=True).annotate(
            num_practicas=Count('practica')
        ).order_by('-num_practicas')[:8]
    
    if not empresas:
        if sector:
            return f"No encontré empresas del sector '{sector}'. Intenta con otro sector como Tecnología, Salud, Educación, etc."
        return "Actualmente no hay empresas registradas en el sistema."
    
    if sector:
        response = f"🏢 **Empresas del Sector {sector.title()}:**\n\n"
    else:
        response = "🏢 **Empresas Colaboradoras Principales:**\n\n"
    
    for i, empresa in enumerate(empresas, 1):
        num_practicas = empresa.practica_set.filter(activa=True).count()
        response += f"{i}. **{empresa.nombre}**\n"
        response += f"   📋 Sector: {empresa.sector}\n"
        response += f"   📍 Ubicación: {empresa.direccion or 'No especificada'}\n"
        response += f"   💼 Prácticas activas: {num_practicas}\n"
        if empresa.email:
            response += f"   📧 Contacto: {empresa.email}\n"
        response += "\n"
    
    total = Empresa.objects.filter(activa=True).count()
    if total > len(empresas):
        response += f"📊 Total de empresas colaboradoras: {total}\n\n"
    
    response += "💡 Para ver el perfil completo de cada empresa y sus prácticas, visita la sección 'Empresas'."
    return response


def get_estadisticas_sistema():
    """Obtiene estadísticas generales del sistema"""
    total_practicas = Practica.objects.filter(activa=True, estado='abierta').count()
    total_internas = PracticaInterna.objects.filter(activa=True, estado='abierta').count()
    total_empresas = Empresa.objects.filter(activa=True).count()
    total_facultades = Facultad.objects.filter(activa=True).count()
    
    response = "📊 **Estado Actual del Sistema:**\n\n"
    response += f"💼 Prácticas externas disponibles: {total_practicas}\n"
    response += f"🎓 Prácticas internas disponibles: {total_internas}\n"
    response += f"🏢 Empresas colaboradoras: {total_empresas}\n"
    response += f"🏛️ Facultades participantes: {total_facultades}\n\n"
    response += "¡Hay muchas oportunidades esperándote! 🚀"
    
    return response
