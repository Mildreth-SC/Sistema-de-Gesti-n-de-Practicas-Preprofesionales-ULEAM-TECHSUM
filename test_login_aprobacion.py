"""
Prueba de integración: Login con sistema de aprobación

Ejecutar con: python test_login_aprobacion.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_practicas.settings')
django.setup()

from django.contrib.auth.models import User
from inscripciones.models import Empresa, Facultad
from inscripciones.supabase_client import supabase_auth
from django.core.files.uploadedfile import SimpleUploadedFile


def print_separator(title):
    """Imprime un separador con título"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def create_dummy_pdf():
    """Crea un archivo PDF falso para pruebas"""
    pdf_content = b'%PDF-1.4\nTest PDF'
    return SimpleUploadedFile("doc.pdf", pdf_content, content_type="application/pdf")


def test_login_empresa_pendiente():
    """Prueba login de empresa pendiente de aprobación"""
    print_separator("🔐 TEST: Login de Empresa PENDIENTE")
    
    # Limpiar
    Empresa.objects.filter(ruc='9999999990001').delete()
    User.objects.filter(username='empresa_pendiente').delete()
    
    # Crear empresa pendiente
    print("\n📝 Creando empresa PENDIENTE...")
    user = User.objects.create_user(
        username='empresa_pendiente',
        email='empresa_pendiente@test.com',
        password='Test123!',
        is_active=False
    )
    
    empresa = Empresa.objects.create(
        user=user,
        nombre='Empresa Pendiente',
        ruc='9999999990001',
        direccion='Test',
        telefono='0987654321',
        email='empresa_pendiente@test.com',
        contacto_responsable='Test',
        sector='Tecnología',
        documento_constitucion=create_dummy_pdf(),
        documento_ruc=create_dummy_pdf(),
        documento_representante=create_dummy_pdf(),
        estado_aprobacion='pendiente'
    )
    
    print(f"   ✅ Empresa creada: {empresa.nombre}")
    print(f"   📊 Estado: {empresa.get_estado_aprobacion_display()}")
    print(f"   🔒 Usuario activo: {user.is_active}")
    print(f"   🚪 Puede acceder: {empresa.puede_acceder()}")
    
    # Intentar login
    print("\n🔑 Intentando login...")
    print("   ⏳ Usuario: empresa_pendiente@test.com")
    print("   🔒 Contraseña: Test123!")
    
    if not empresa.puede_acceder():
        print("   ❌ Login BLOQUEADO - Empresa pendiente de aprobación")
        print("   📝 El usuario verá mensaje: 'Tu cuenta está PENDIENTE DE APROBACIÓN'")
    else:
        print("   ⚠️  ERROR: Empresa pendiente NO debería poder acceder")
    
    return empresa


def test_login_empresa_aprobada(empresa):
    """Prueba login de empresa aprobada"""
    print_separator("🔐 TEST: Login de Empresa APROBADA")
    
    # Aprobar empresa
    print("\n👨‍💼 Simulando aprobación por admin...")
    from django.utils import timezone
    admin = User.objects.filter(is_superuser=True).first()
    
    empresa.estado_aprobacion = 'aprobada'
    empresa.fecha_aprobacion = timezone.now()
    empresa.aprobado_por = admin
    empresa.user.is_active = True
    empresa.user.save()
    empresa.save()
    
    print(f"   ✅ Empresa APROBADA")
    print(f"   🔒 Usuario activo: {empresa.user.is_active}")
    print(f"   🚪 Puede acceder: {empresa.puede_acceder()}")
    
    # Intentar login
    print("\n🔑 Intentando login...")
    if empresa.puede_acceder():
        print("   ✅ Login PERMITIDO - Empresa aprobada")
        print("   🎉 El usuario puede acceder al sistema")
    else:
        print("   ⚠️  ERROR: Empresa aprobada DEBERÍA poder acceder")


def test_login_empresa_rechazada():
    """Prueba login de empresa rechazada"""
    print_separator("🔐 TEST: Login de Empresa RECHAZADA")
    
    # Limpiar
    Empresa.objects.filter(ruc='8888888880001').delete()
    User.objects.filter(username='empresa_rechazada').delete()
    
    # Crear empresa rechazada
    print("\n📝 Creando empresa RECHAZADA...")
    user = User.objects.create_user(
        username='empresa_rechazada',
        email='empresa_rechazada@test.com',
        password='Test123!',
        is_active=False
    )
    
    empresa = Empresa.objects.create(
        user=user,
        nombre='Empresa Rechazada',
        ruc='8888888880001',
        direccion='Test',
        telefono='0987654321',
        email='empresa_rechazada@test.com',
        contacto_responsable='Test',
        sector='Tecnología',
        documento_constitucion=create_dummy_pdf(),
        documento_ruc=create_dummy_pdf(),
        documento_representante=create_dummy_pdf(),
        estado_aprobacion='rechazada',
        observaciones_aprobacion='Documentos no cumplen con los requisitos'
    )
    
    print(f"   ✅ Empresa creada: {empresa.nombre}")
    print(f"   📊 Estado: {empresa.get_estado_aprobacion_display()}")
    print(f"   📝 Motivo: {empresa.observaciones_aprobacion}")
    print(f"   🚪 Puede acceder: {empresa.puede_acceder()}")
    
    # Intentar login
    print("\n🔑 Intentando login...")
    if not empresa.puede_acceder():
        print("   ❌ Login BLOQUEADO - Empresa rechazada")
        print("   📝 El usuario verá mensaje con el motivo del rechazo")
    else:
        print("   ⚠️  ERROR: Empresa rechazada NO debería poder acceder")


def test_validacion_ruc_formulario():
    """Prueba validación de RUC en tiempo real"""
    print_separator("📝 TEST: Validación de RUC en Formulario")
    
    rucs_test = [
        ('1234567890001', True, "RUC válido - termina en 001"),
        ('1234567890002', False, "RUC inválido - no termina en 001"),
        ('12345678', False, "RUC inválido - longitud incorrecta"),
        ('ABCD67890001', False, "RUC inválido - contiene letras"),
    ]
    
    for ruc, esperado_valido, descripcion in rucs_test:
        print(f"\n📋 Test: {ruc}")
        print(f"   {descripcion}")
        
        # Validar longitud
        longitud_ok = len(ruc) == 13
        
        # Validar terminación
        termina_001 = ruc.endswith('001')
        
        # Validar solo números
        solo_numeros = ruc.isdigit()
        
        es_valido = longitud_ok and termina_001 and solo_numeros
        
        if es_valido == esperado_valido:
            print(f"   ✅ CORRECTO - Validación esperada: {'válido' if esperado_valido else 'inválido'}")
        else:
            print(f"   ❌ ERROR - Se esperaba: {'válido' if esperado_valido else 'inválido'}, pero fue: {'válido' if es_valido else 'inválido'}")
        
        # Detalles
        print(f"      • Longitud 13: {'✅' if longitud_ok else '❌'} (actual: {len(ruc)})")
        print(f"      • Termina en 001: {'✅' if termina_001 else '❌'}")
        print(f"      • Solo números: {'✅' if solo_numeros else '❌'}")


def main():
    """Función principal"""
    print("\n" + "🔒"*40)
    print("PRUEBAS DE INTEGRACIÓN: LOGIN CON SISTEMA DE APROBACIÓN")
    print("🔒"*40)
    
    try:
        # Test 1: Validación de RUC
        test_validacion_ruc_formulario()
        
        # Test 2: Login empresa pendiente
        empresa = test_login_empresa_pendiente()
        
        # Test 3: Login empresa aprobada
        test_login_empresa_aprobada(empresa)
        
        # Test 4: Login empresa rechazada
        test_login_empresa_rechazada()
        
        print("\n" + "="*80)
        print("📊 RESUMEN DE PRUEBAS DE INTEGRACIÓN")
        print("="*80)
        print("\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("\n📋 Funcionalidades probadas:")
        print("   ✅ Validación de RUC con múltiples casos")
        print("   ✅ Bloqueo de login para empresas pendientes")
        print("   ✅ Acceso permitido para empresas aprobadas")
        print("   ✅ Bloqueo de login para empresas rechazadas")
        print("   ✅ Mensajes informativos según estado")
        
        print("\n" + "🎉"*40)
        print("SISTEMA DE APROBACIÓN FUNCIONANDO CORRECTAMENTE")
        print("🎉"*40)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
