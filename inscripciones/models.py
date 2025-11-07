from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Carrera(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo_estudiante = models.CharField(max_length=20, unique=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    ciclo_actual = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='estudiantes/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['codigo_estudiante']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.codigo_estudiante}"


class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    contacto_responsable = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    logo = models.ImageField(upload_to='empresas/', blank=True, null=True)
    activa = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Practica(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    requisitos = models.TextField()
    duracion_semanas = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    horas_semana = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(40)]
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cupos_disponibles = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    cupos_totales = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_limite_inscripcion = models.DateTimeField()
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Práctica"
        verbose_name_plural = "Prácticas"
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre}"
    
    @property
    def cupos_ocupados(self):
        return self.cupos_totales - self.cupos_disponibles
    
    @property
    def puede_inscribirse(self):
        return (
            self.activa and 
            self.estado == 'disponible' and 
            self.cupos_disponibles > 0 and
            timezone.now() <= self.fecha_limite_inscripcion
        )
    
    def clean(self):
        """Validar fechas y cupos lógicos"""
        super().clean()
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })
        if self.fecha_limite_inscripcion and self.fecha_inicio:
            if self.fecha_limite_inscripcion.date() > self.fecha_inicio:
                raise ValidationError({
                    'fecha_limite_inscripcion': 'La fecha límite de inscripción debe ser anterior o igual a la fecha de inicio.'
                })
        if self.cupos_disponibles is not None and self.cupos_totales is not None:
            if self.cupos_disponibles > self.cupos_totales:
                raise ValidationError({
                    'cupos_disponibles': 'Los cupos disponibles no pueden ser mayores que los cupos totales.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Inscripcion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)
    fecha_evaluacion = models.DateTimeField(null=True, blank=True)
    evaluado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='inscripciones_evaluadas'
    )
    
    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ['estudiante', 'practica']
        ordering = ['-fecha_inscripcion']
    
    def __str__(self):
        return f"{self.estudiante} - {self.practica.titulo}"


class DocumentoInscripcion(models.Model):
    TIPO_CHOICES = [
        ('cv', 'Curriculum Vitae'),
        ('carta_presentacion', 'Carta de Presentación'),
        ('certificado_notas', 'Certificado de Notas'),
        ('carta_recomendacion', 'Carta de Recomendación'),
        ('otro', 'Otro'),
    ]
    
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos_inscripcion/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Documento de Inscripción"
        verbose_name_plural = "Documentos de Inscripción"
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.inscripcion} - {self.nombre}"


class Facultad(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10, unique=True)
    decano = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    contacto_responsable = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    logo = models.ImageField(upload_to='facultades/', blank=True, null=True)
    activa = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class PracticaInterna(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_SERVICIO_CHOICES = [
        ('investigacion', 'Investigación'),
        ('docencia', 'Docencia'),
        ('administrativo', 'Administrativo'),
        ('tecnico', 'Técnico'),
        ('social', 'Servicio Social'),
        ('otro', 'Otro'),
    ]
    
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_servicio = models.CharField(max_length=20, choices=TIPO_SERVICIO_CHOICES)
    requisitos = models.TextField()
    duracion_semanas = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    horas_semana = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(40)]
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cupos_disponibles = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    cupos_totales = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_limite_inscripcion = models.DateTimeField()
    activa = models.BooleanField(default=True)
    beneficios = models.TextField(blank=True, help_text="Beneficios para el estudiante")
    
    class Meta:
        verbose_name = "Práctica Interna"
        verbose_name_plural = "Prácticas Internas"
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.facultad.nombre}"
    
    @property
    def cupos_ocupados(self):
        return self.cupos_totales - self.cupos_disponibles
    
    @property
    def puede_inscribirse(self):
        return (
            self.activa and 
            self.estado == 'disponible' and 
            self.cupos_disponibles > 0 and
            timezone.now() <= self.fecha_limite_inscripcion
        )
    
    def clean(self):
        """Validar fechas y cupos lógicos"""
        super().clean()
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })
        if self.fecha_limite_inscripcion and self.fecha_inicio:
            if self.fecha_limite_inscripcion.date() > self.fecha_inicio:
                raise ValidationError({
                    'fecha_limite_inscripcion': 'La fecha límite de inscripción debe ser anterior o igual a la fecha de inicio.'
                })
        if self.cupos_disponibles is not None and self.cupos_totales is not None:
            if self.cupos_disponibles > self.cupos_totales:
                raise ValidationError({
                    'cupos_disponibles': 'Los cupos disponibles no pueden ser mayores que los cupos totales.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class InscripcionInterna(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    practica_interna = models.ForeignKey(PracticaInterna, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)
    fecha_evaluacion = models.DateTimeField(null=True, blank=True)
    evaluado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='inscripciones_internas_evaluadas'
    )
    
    class Meta:
        verbose_name = "Inscripción Interna"
        verbose_name_plural = "Inscripciones Internas"
        unique_together = ['estudiante', 'practica_interna']
        ordering = ['-fecha_inscripcion']
    
    def __str__(self):
        return f"{self.estudiante} - {self.practica_interna.titulo}"


class Calificacion(models.Model):
    """Modelo para almacenar calificaciones por quimestre"""
    TIPO_CALIFICACION_CHOICES = [
        ('comportamiento', 'Comportamiento'),
        ('proyecto', 'Proyecto'),
    ]
    
    QUIMESTRE_CHOICES = [
        ('Q1', 'Quimestre 1'),
        ('Q2', 'Quimestre 2'),
    ]
    
    PERIODO_CHOICES = [
        ('P1', 'Período 1'),
        ('P2', 'Período 2'),
        ('P3', 'Período 3'),
    ]
    
    # Valores de calificación según el sistema
    VALOR_COMPORTAMIENTO_CHOICES = [
        ('A', 'A - Muy Satisfactorio (9-10)'),
        ('B', 'B - Satisfactorio (7-8)'),
        ('C', 'C - Poco Satisfactorio (4-6)'),
        ('D', 'D - Mejorable (1-3)'),
        ('E', 'E - Insatisfactorio (<1)'),
    ]
    
    VALOR_PROYECTO_CHOICES = [
        ('EX', 'EX - Excelente (10.00)'),
        ('MB', 'MB - Muy Bueno (9.00-9.99)'),
        ('B', 'B - Bueno (7.00-8.99)'),
        ('R', 'R - Regular (<7.00)'),
    ]
    
    inscripcion = models.ForeignKey(
        Inscripcion, 
        on_delete=models.CASCADE, 
        related_name='calificaciones',
        null=True,
        blank=True
    )
    inscripcion_interna = models.ForeignKey(
        InscripcionInterna, 
        on_delete=models.CASCADE, 
        related_name='calificaciones',
        null=True,
        blank=True
    )
    tipo_calificacion = models.CharField(max_length=20, choices=TIPO_CALIFICACION_CHOICES)
    quimestre = models.CharField(max_length=2, choices=QUIMESTRE_CHOICES)
    periodo = models.CharField(max_length=2, choices=PERIODO_CHOICES)
    valor = models.CharField(max_length=2)  # Almacena A, B, C, D, E, EX, MB, B, R
    fecha_registro = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        unique_together = ['inscripcion', 'inscripcion_interna', 'tipo_calificacion', 'quimestre', 'periodo']
        ordering = ['quimestre', 'periodo', 'tipo_calificacion']
    
    def __str__(self):
        inscripcion_ref = self.inscripcion or self.inscripcion_interna
        return f"{inscripcion_ref} - {self.get_tipo_calificacion_display()} {self.quimestre} {self.periodo}: {self.valor}"
    
    def get_descripcion_valor(self):
        """Retorna la descripción completa del valor"""
        if self.tipo_calificacion == 'comportamiento':
            for valor, descripcion in self.VALOR_COMPORTAMIENTO_CHOICES:
                if valor == self.valor:
                    return descripcion
        elif self.tipo_calificacion == 'proyecto':
            for valor, descripcion in self.VALOR_PROYECTO_CHOICES:
                if valor == self.valor:
                    return descripcion
        return self.valor