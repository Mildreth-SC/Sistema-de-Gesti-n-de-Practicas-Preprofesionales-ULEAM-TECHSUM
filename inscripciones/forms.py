from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Estudiante, Empresa, Practica, Inscripcion, DocumentoInscripcion, Carrera, Facultad, PracticaInterna, InscripcionInterna, Calificacion


class EmpresaRegistrationForm(UserCreationForm):
    SECTOR_CHOICES = [
        ('', 'Seleccione un sector'),
        ('tecnologia', 'Tecnología e Informática'),
        ('salud', 'Salud y Medicina'),
        ('educacion', 'Educación'),
        ('construccion', 'Construcción e Ingeniería'),
        ('manufactura', 'Manufactura e Industria'),
        ('comercio', 'Comercio y Retail'),
        ('servicios', 'Servicios Profesionales'),
        ('finanzas', 'Finanzas y Banca'),
        ('turismo', 'Turismo y Hospitalidad'),
        ('agricultura', 'Agricultura y Ganadería'),
        ('transporte', 'Transporte y Logística'),
        ('comunicacion', 'Comunicación y Medios'),
        ('energia', 'Energía y Recursos Naturales'),
        ('inmobiliaria', 'Sector Inmobiliario'),
        ('alimentos', 'Alimentos y Bebidas'),
        ('otro', 'Otro'),
    ]
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre del Contacto")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido del Contacto")
    
    # Campos específicos de la empresa
    nombre = forms.CharField(max_length=200, required=True, label="Nombre de la Empresa")
    ruc = forms.CharField(
        max_length=13, 
        required=True, 
        label="RUC",
        help_text="El RUC debe tener 13 dígitos numéricos y terminar en 001"
    )
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label="Dirección")
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono")
    contacto_responsable = forms.CharField(max_length=100, required=True, label="Nombre del Responsable")
    sector = forms.ChoiceField(
        choices=SECTOR_CHOICES,
        required=True,
        label="Sector",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label="Descripción")
    logo = forms.ImageField(required=False, label="Logo de la Empresa")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels
        self.fields['username'].label = "Usuario"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        # Validar que solo contenga dígitos
        if not ruc.isdigit():
            raise forms.ValidationError("El RUC debe contener solo números.")
        # Validar que tenga exactamente 13 dígitos
        if len(ruc) != 13:
            raise forms.ValidationError("El RUC debe tener exactamente 13 dígitos.")
        # Validar que termine en 001
        if not ruc.endswith('001'):
            raise forms.ValidationError("El RUC de una empresa debe terminar en 001.")
        # Validar que no exista
        if Empresa.objects.filter(ruc=ruc).exists():
            raise forms.ValidationError("Ya existe una empresa registrada con este RUC.")
        return ruc

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Empresa.objects.create(
                user=user,
                nombre=self.cleaned_data['nombre'],
                ruc=self.cleaned_data['ruc'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                email=self.cleaned_data['email'],
                contacto_responsable=self.cleaned_data['contacto_responsable'],
                sector=self.cleaned_data['sector'],
                descripcion=self.cleaned_data['descripcion'],
                logo=self.cleaned_data.get('logo'),
                # Estado inicial: pendiente de aprobación por el administrador
                estado_aprobacion='pendiente'
            )
        return user


class FacultadRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre del Contacto")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido del Contacto")
    
    # Campos específicos de la facultad
    nombre = forms.CharField(max_length=200, required=True, label="Nombre de la Facultad")
    codigo = forms.CharField(max_length=10, required=True, label="Código de la Facultad")
    decano = forms.CharField(max_length=100, required=True, label="Nombre del Decano")
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label="Dirección")
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono")
    contacto_responsable = forms.CharField(max_length=100, required=True, label="Nombre del Responsable")
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label="Descripción")
    logo = forms.ImageField(required=False, label="Logo de la Facultad")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels
        self.fields['username'].label = "Usuario"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Facultad.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("Ya existe una facultad registrada con este código.")
        return codigo

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Facultad.objects.create(
                user=user,
                nombre=self.cleaned_data['nombre'],
                codigo=self.cleaned_data['codigo'],
                decano=self.cleaned_data['decano'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                email=self.cleaned_data['email'],
                contacto_responsable=self.cleaned_data['contacto_responsable'],
                descripcion=self.cleaned_data['descripcion'],
                logo=self.cleaned_data.get('logo'),
                # Estado inicial: pendiente de aprobación por el administrador
                estado_aprobacion='pendiente'
            )
        return user


class EstudianteRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo Electrónico')
    first_name = forms.CharField(max_length=30, required=True, label='Nombres')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    
    tipo_usuario = forms.ChoiceField(
        choices=[
            ('estudiante', 'Estudiante Activo'),
            ('egresado', 'Egresado')
        ],
        required=True,
        label='¿Eres estudiante o egresado?',
        widget=forms.RadioSelect,
        initial='estudiante'
    )
    
    codigo_estudiante = forms.CharField(
        max_length=20, 
        required=True,
        label='Código de Estudiante',
        help_text='Tu código único de estudiante'
    )
    
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activa=True), 
        required=True,
        label='Carrera'
    )
    
    ciclo_actual = forms.IntegerField(
        min_value=1, 
        max_value=12, 
        required=False,
        label='Ciclo Actual',
        help_text='Solo para estudiantes activos'
    )
    
    tipo_titulo = forms.ChoiceField(
        choices=[
            ('', 'Seleccione...'),
            ('licenciatura', 'Licenciatura'),
            ('ingenieria', 'Ingeniería')
        ],
        required=False,
        label='Tipo de Título',
        help_text='Solo para egresados'
    )
    
    telefono = forms.CharField(max_length=15, required=False, label='Teléfono')
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Dirección')
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False,
        label='Fecha de Nacimiento'
    )
    foto = forms.ImageField(required=False, label='Foto de Perfil')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        tipo_usuario = cleaned_data.get('tipo_usuario')
        ciclo_actual = cleaned_data.get('ciclo_actual')
        tipo_titulo = cleaned_data.get('tipo_titulo')
        
        # Validar que estudiantes tengan ciclo actual
        if tipo_usuario == 'estudiante' and not ciclo_actual:
            self.add_error('ciclo_actual', 'Los estudiantes activos deben indicar su ciclo actual.')
        
        # Validar que egresados tengan tipo de título
        if tipo_usuario == 'egresado' and not tipo_titulo:
            self.add_error('tipo_titulo', 'Los egresados deben indicar su tipo de título.')
        
        return cleaned_data
    
    def clean_codigo_estudiante(self):
        codigo = self.cleaned_data.get('codigo_estudiante')
        # Verificar si ya existe un estudiante con este código
        if Estudiante.objects.filter(codigo_estudiante=codigo).exists():
            raise forms.ValidationError(
                f'Ya existe un estudiante registrado con el código {codigo}. '
                'Por favor, verifica tu código o contacta al administrador.'
            )
        return codigo

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Estudiante.objects.create(
                user=user,
                tipo_usuario=self.cleaned_data.get('tipo_usuario'),
                codigo_estudiante=self.cleaned_data.get('codigo_estudiante'),
                carrera=self.cleaned_data.get('carrera'),
                ciclo_actual=self.cleaned_data.get('ciclo_actual') if self.cleaned_data.get('tipo_usuario') == 'estudiante' else None,
                tipo_titulo=self.cleaned_data.get('tipo_titulo') if self.cleaned_data.get('tipo_usuario') == 'egresado' else None,
                telefono=self.cleaned_data.get('telefono', ''),
                direccion=self.cleaned_data.get('direccion', ''),
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
                foto=self.cleaned_data.get('foto')
            )
        return user


class EstudianteProfileForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo_estudiante', 'carrera', 'ciclo_actual', 'telefono', 'direccion', 'fecha_nacimiento', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EstudianteUpdateForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo_estudiante', 'carrera', 'ciclo_actual', 'tipo_titulo', 'telefono', 'direccion', 'fecha_nacimiento', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)
        
        # Hacer los campos opcionales según el tipo de usuario
        instance = kwargs.get('instance')
        if instance:
            if instance.tipo_usuario == 'estudiante':
                self.fields['ciclo_actual'].required = True
                self.fields['tipo_titulo'].required = False
                self.fields['tipo_titulo'].widget = forms.HiddenInput()
            elif instance.tipo_usuario == 'egresado':
                self.fields['ciclo_actual'].required = False
                self.fields['ciclo_actual'].widget = forms.HiddenInput()
                self.fields['tipo_titulo'].required = True


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'ruc', 'direccion', 'telefono', 'email', 'contacto_responsable', 'sector', 'descripcion', 'logo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class PracticaForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = ['titulo', 'area', 'modalidad', 'dirigido_a', 'descripcion', 'requisitos', 'duracion_semanas', 'horas_semana', 
                 'fecha_inicio', 'fecha_fin', 'cupos_totales', 'fecha_limite_inscripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite_inscripcion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'dirigido_a': forms.Select(attrs={'class': 'form-control'}),
        }


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['observaciones']


class DocumentoInscripcionForm(forms.ModelForm):
    class Meta:
        model = DocumentoInscripcion
        fields = ['tipo', 'nombre', 'archivo']
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar extensión de archivo
            extensiones_validas = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
            nombre_archivo = archivo.name.lower()
            if not any(nombre_archivo.endswith(ext) for ext in extensiones_validas):
                raise forms.ValidationError(
                    f'Tipo de archivo no permitido. Extensiones válidas: {", ".join(extensiones_validas)}'
                )
            
            # Validar tamaño (máximo 5MB)
            if archivo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede superar los 5MB.')
        
        return archivo


class BusquedaPracticasForm(forms.Form):
    titulo = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar por título'}))
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.filter(activa=True), required=False, empty_label="Todas las empresas")
    sector = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar por sector'}))
    fecha_inicio_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_inicio_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(activa=True)


class PracticaInternaForm(forms.ModelForm):
    class Meta:
        model = PracticaInterna
        fields = ['titulo', 'descripcion', 'tipo_servicio', 'modalidad', 'dirigido_a', 'requisitos', 'duracion_semanas', 'horas_semana', 
                 'fecha_inicio', 'fecha_fin', 'cupos_totales', 'fecha_limite_inscripcion', 'beneficios']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite_inscripcion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
            'beneficios': forms.Textarea(attrs={'rows': 3}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'dirigido_a': forms.Select(attrs={'class': 'form-control'}),
        }


class InscripcionInternaForm(forms.ModelForm):
    class Meta:
        model = InscripcionInterna
        fields = ['observaciones']


class BusquedaPracticasInternasForm(forms.Form):
    titulo = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar por título'}))
    facultad = forms.ModelChoiceField(queryset=Facultad.objects.filter(activa=True), required=False, empty_label="Todas las facultades")
    tipo_servicio = forms.ChoiceField(choices=[('', 'Todos los tipos')] + list(PracticaInterna.TIPO_SERVICIO_CHOICES), required=False)
    fecha_inicio_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_inicio_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facultad'].queryset = Facultad.objects.filter(activa=True)


class CalificacionForm(forms.Form):
    """Formulario para ingresar múltiples calificaciones por quimestre"""
    
    def __init__(self, *args, **kwargs):
        quimestres = kwargs.pop('quimestres', ['Q1'])
        periodos = kwargs.pop('periodos', ['P1', 'P2', 'P3'])
        super().__init__(*args, **kwargs)
        
        # Crear campos dinámicamente para cada combinación
        for quimestre in quimestres:
            for periodo in periodos:
                # Campo para Comportamiento
                field_name_comp = f'comportamiento_{quimestre}_{periodo}'
                self.fields[field_name_comp] = forms.ChoiceField(
                    choices=[('', '---------')] + [
                        ('A', 'A - Muy Satisfactorio (9-10)'),
                        ('B', 'B - Satisfactorio (7-8)'),
                        ('C', 'C - Poco Satisfactorio (4-6)'),
                        ('D', 'D - Mejorable (1-3)'),
                        ('E', 'E - Insatisfactorio (<1)'),
                    ],
                    required=False,
                    label=f'Comportamiento {quimestre} {periodo}'
                )
                
                # Campo para Proyecto
                field_name_proy = f'proyecto_{quimestre}_{periodo}'
                self.fields[field_name_proy] = forms.ChoiceField(
                    choices=[('', '---------')] + [
                        ('EX', 'EX - Excelente (10.00)'),
                        ('MB', 'MB - Muy Bueno (9.00-9.99)'),
                        ('B', 'B - Bueno (7.00-8.99)'),
                        ('R', 'R - Regular (<7.00)'),
                    ],
                    required=False,
                    label=f'Proyecto {quimestre} {periodo}'
                )
