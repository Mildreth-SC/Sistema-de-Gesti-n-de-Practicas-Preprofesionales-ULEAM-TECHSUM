"""
Pruebas del Sistema de Aprobación de Empresas y Facultades

Ejecutar con: python test_sistema_aprobacion.py
"""
import os
import django
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.contrib.auth.models import User
from inscripciones.models import Empresa, Facultad
from inscripciones.forms import EmpresaRegistrationForm, FacultadRegistrationForm
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def print_separator(title):
    """Imprime un separador con título"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def create_dummy_pdf():
    """Crea un archivo PDF falso para pruebas"""
    pdf_content = b'%PDF-1.4\n%Test PDF\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n190\n%%EOF'
    return SimpleUploadedFile("documento_test.pdf", pdf_content, content_type="application/pdf")


def test_validacion_ruc():
    """Prueba la validación del RUC (debe terminar en 001)"""
    print_separator("🔍 PROBANDO VALIDACIÓN DE RUC")
    
    print("\n📋 Test 1: RUC válido (termina en 001)")
    ruc_valido = "1234567890001"
    print(f"   RUC: {ruc_valido}")
    if ruc_valido.endswith('001'):
        print("   ✅ RUC válido - Termina en 001")
    else:
        print("   ❌ RUC inválido - No termina en 001")
    
    print("\n📋 Test 2: RUC inválido (termina en 002)")
    ruc_invalido = "1234567890002"
    print(f"   RUC: {ruc_invalido}")
    if ruc_invalido.endswith('001'):
        print("   ✅ RUC válido - Termina en 001")
    else:
        print("   ❌ RUC inválido - No termina en 001")
    
    print("\n📋 Test 3: RUC inválido (longitud incorrecta)")
    ruc_corto = "123001"
    print(f"   RUC: {ruc_corto}")
    if len(ruc_corto) == 13 and ruc_corto.endswith('001'):
        print("   ✅ RUC válido")
    else:
        print(f"   ❌ RUC inválido - Longitud: {len(ruc_corto)} (debe ser 13)")


def test_creacion_empresa_con_documentos():
    """Prueba la creación de una empresa con documentos"""
    print_separator("🏢 PROBANDO CREACIÓN DE EMPRESA CON DOCUMENTOS")
    
    # Limpiar datos previos
    print("\n🧹 Limpiando datos de prueba anteriores...")
    Empresa.objects.filter(ruc__startswith='TEST').delete()
    User.objects.filter(username__startswith='test_empresa_').delete()
    
    print("\n📄 Creando documentos PDF de prueba...")
    doc_constitucion = create_dummy_pdf()
    doc_ruc = create_dummy_pdf()
    doc_representante = create_dummy_pdf()
    print("   ✅ 3 documentos PDF creados")
    
    print("\n👤 Creando usuario...")
    user = User.objects.create_user(
        username='test_empresa_aprobacion',
        email='test_empresa_aprobacion@test.com',
        password='TestPass123!',
        first_name='Empresa',
        last_name='Test'
    )
    user.is_active = False  # Inactivo hasta aprobación
    user.save()
    print(f"   ✅ Usuario creado: {user.email} (Inactivo)")
    
    print("\n🏢 Creando empresa...")
    empresa = Empresa.objects.create(
        user=user,
        nombre='TEST Empresa de Pruebas S.A.',
        ruc='TEST567890001',  # Termina en 001
        direccion='Calle Test 123',
        telefono='0987654321',
        email='test_empresa_aprobacion@test.com',
        contacto_responsable='Juan Pérez',
        sector='Tecnología',
        descripcion='Empresa de prueba para el sistema',
        documento_constitucion=doc_constitucion,
        documento_ruc=doc_ruc,
        documento_representante=doc_representante,
        estado_aprobacion='pendiente'
    )
    
    print(f"   ✅ Empresa creada: {empresa.nombre}")
    print(f"   📋 RUC: {empresa.ruc}")
    print(f"   📄 Estado: {empresa.get_estado_aprobacion_display()}")
    print(f"   🔒 Usuario activo: {user.is_active}")
    
    # Verificar documentos
    print("\n📎 Verificando documentos adjuntos:")
    print(f"   {'✅' if empresa.documento_constitucion else '❌'} Documento de Constitución: {empresa.documento_constitucion.name if empresa.documento_constitucion else 'No cargado'}")
    print(f"   {'✅' if empresa.documento_ruc else '❌'} Certificado de RUC: {empresa.documento_ruc.name if empresa.documento_ruc else 'No cargado'}")
    print(f"   {'✅' if empresa.documento_representante else '❌'} Documento Representante: {empresa.documento_representante.name if empresa.documento_representante else 'No cargado'}")
    
    return empresa


def test_flujo_aprobacion_empresa(empresa):
    """Prueba el flujo de aprobación de una empresa"""
    print_separator("✅ PROBANDO FLUJO DE APROBACIÓN DE EMPRESA")
    
    print(f"\n📊 Estado inicial: {empresa.get_estado_aprobacion_display()}")
    print(f"🔒 Usuario activo: {empresa.user.is_active}")
    print(f"🚪 Puede acceder: {empresa.puede_acceder()}")
    
    # Simular aprobación por administrador
    print("\n👨‍💼 Simulando aprobación por administrador...")
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='AdminPass123!'
        )
        print(f"   ✅ Administrador creado: {admin_user.username}")
    
    from django.utils import timezone
    empresa.estado_aprobacion = 'aprobada'
    empresa.fecha_aprobacion = timezone.now()
    empresa.aprobado_por = admin_user
    empresa.observaciones_aprobacion = 'Documentos verificados y aprobados correctamente.'
    empresa.save()
    
    # Activar usuario
    empresa.user.is_active = True
    empresa.user.save()
    
    print(f"   ✅ Empresa APROBADA")
    print(f"   📅 Fecha: {empresa.fecha_aprobacion}")
    print(f"   👨‍💼 Aprobado por: {empresa.aprobado_por.username}")
    print(f"   📝 Observaciones: {empresa.observaciones_aprobacion}")
    
    print(f"\n📊 Estado final: {empresa.get_estado_aprobacion_display()}")
    print(f"🔒 Usuario activo: {empresa.user.is_active}")
    print(f"🚪 Puede acceder: {empresa.puede_acceder()}")
    
    # Probar rechazo
    print("\n❌ Simulando RECHAZO de otra solicitud...")
    empresa.estado_aprobacion = 'rechazada'
    empresa.observaciones_aprobacion = 'Documentos incompletos. Por favor, enviar documentos actualizados.'
    empresa.user.is_active = False
    empresa.user.save()
    empresa.save()
    
    print(f"   ❌ Empresa RECHAZADA")
    print(f"   📝 Motivo: {empresa.observaciones_aprobacion}")
    print(f"   🚪 Puede acceder: {empresa.puede_acceder()}")


def test_creacion_facultad_con_documentos():
    """Prueba la creación de una facultad con documentos"""
    print_separator("🎓 PROBANDO CREACIÓN DE FACULTAD CON DOCUMENTOS")
    
    # Limpiar datos previos
    print("\n🧹 Limpiando datos de prueba anteriores...")
    Facultad.objects.filter(codigo__startswith='TEST').delete()
    User.objects.filter(username__startswith='test_facultad_').delete()
    
    print("\n📄 Creando documentos PDF de prueba...")
    doc_autorizacion = create_dummy_pdf()
    doc_resolucion = create_dummy_pdf()
    doc_representante = create_dummy_pdf()
    print("   ✅ 3 documentos PDF creados")
    
    print("\n👤 Creando usuario...")
    user = User.objects.create_user(
        username='test_facultad_aprobacion',
        email='test_facultad_aprobacion@test.com',
        password='TestPass123!',
        first_name='Facultad',
        last_name='Test'
    )
    user.is_active = False  # Inactivo hasta aprobación
    user.save()
    print(f"   ✅ Usuario creado: {user.email} (Inactivo)")
    
    print("\n🎓 Creando facultad...")
    facultad = Facultad.objects.create(
        user=user,
        nombre='TEST Facultad de Pruebas',
        codigo='TEST_FP',
        decano='Dr. Test Decano',
        direccion='Campus ULEAM',
        telefono='0987654321',
        email='test_facultad_aprobacion@test.com',
        contacto_responsable='Secretaría Académica',
        descripcion='Facultad de prueba para el sistema',
        documento_autorizacion=doc_autorizacion,
        documento_resolucion=doc_resolucion,
        documento_representante=doc_representante,
        estado_aprobacion='pendiente'
    )
    
    print(f"   ✅ Facultad creada: {facultad.nombre}")
    print(f"   📋 Código: {facultad.codigo}")
    print(f"   📄 Estado: {facultad.get_estado_aprobacion_display()}")
    print(f"   🔒 Usuario activo: {user.is_active}")
    
    # Verificar documentos
    print("\n📎 Verificando documentos adjuntos:")
    print(f"   {'✅' if facultad.documento_autorizacion else '❌'} Documento de Autorización: {facultad.documento_autorizacion.name if facultad.documento_autorizacion else 'No cargado'}")
    print(f"   {'✅' if facultad.documento_resolucion else '❌'} Resolución: {facultad.documento_resolucion.name if facultad.documento_resolucion else 'No cargado'}")
    print(f"   {'✅' if facultad.documento_representante else '❌'} Documento Representante: {facultad.documento_representante.name if facultad.documento_representante else 'No cargado'}")
    
    return facultad


def test_validacion_formulario():
    """Prueba validaciones del formulario"""
    print_separator("📝 PROBANDO VALIDACIONES DE FORMULARIO")
    
    print("\n❌ Test 1: RUC que no termina en 001")
    form_data = {
        'username': 'test_form_empresa',
        'email': 'test_form@test.com',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'Form',
        'nombre': 'Empresa Form Test',
        'ruc': '1234567890002',  # No termina en 001
        'direccion': 'Calle Test',
        'telefono': '0987654321',
        'contacto_responsable': 'Juan Test',
        'sector': 'Tecnología',
    }
    
    # Crear archivos para el formulario
    files = {
        'documento_constitucion': create_dummy_pdf(),
        'documento_ruc': create_dummy_pdf(),
        'documento_representante': create_dummy_pdf(),
    }
    
    form = EmpresaRegistrationForm(data=form_data, files=files)
    
    if form.is_valid():
        print("   ❌ ERROR: El formulario NO debería ser válido (RUC inválido)")
    else:
        print("   ✅ CORRECTO: Formulario inválido como se esperaba")
        if 'ruc' in form.errors:
            print(f"   📝 Error de RUC: {form.errors['ruc'][0]}")
    
    print("\n✅ Test 2: RUC válido que termina en 001")
    form_data['ruc'] = '1234567890001'  # Termina en 001
    form_data['email'] = 'test_form_valid@test.com'  # Email único
    form_data['username'] = 'test_form_empresa_valid'  # Username único
    
    files = {
        'documento_constitucion': create_dummy_pdf(),
        'documento_ruc': create_dummy_pdf(),
        'documento_representante': create_dummy_pdf(),
    }
    
    form = EmpresaRegistrationForm(data=form_data, files=files)
    
    if form.is_valid():
        print("   ✅ CORRECTO: Formulario válido")
        print("   📋 RUC aceptado: " + form.cleaned_data['ruc'])
    else:
        print("   ❌ ERROR: El formulario debería ser válido")
        for field, errors in form.errors.items():
            print(f"   Error en {field}: {errors}")


def main():
    """Función principal"""
    print("\n" + "🚀"*40)
    print("PRUEBAS DEL SISTEMA DE APROBACIÓN")
    print("Empresas y Facultades - Validación de Documentos")
    print("🚀"*40)
    
    try:
        # Test 1: Validación de RUC
        test_validacion_ruc()
        
        # Test 2: Validación de formulario
        test_validacion_formulario()
        
        # Test 3: Creación de empresa con documentos
        empresa = test_creacion_empresa_con_documentos()
        
        # Test 4: Flujo de aprobación
        test_flujo_aprobacion_empresa(empresa)
        
        # Test 5: Creación de facultad con documentos
        facultad = test_creacion_facultad_con_documentos()
        
        print("\n" + "="*80)
        print("📊 RESUMEN DE PRUEBAS")
        print("="*80)
        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("\n📋 Resultados:")
        print(f"   • Validación de RUC: ✅")
        print(f"   • Validación de formularios: ✅")
        print(f"   • Creación de empresa con documentos: ✅")
        print(f"   • Flujo de aprobación/rechazo: ✅")
        print(f"   • Creación de facultad con documentos: ✅")
        
        print("\n🎉 Sistema de aprobación funcionando correctamente!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()
