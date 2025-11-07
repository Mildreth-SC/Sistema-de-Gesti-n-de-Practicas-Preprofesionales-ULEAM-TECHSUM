# -*- coding: utf-8 -*-
"""
Script para crear usuarios para empresas y facultades existentes
"""
from django.contrib.auth.models import User
from inscripciones.models import Empresa, Facultad
from django.db import transaction

def crear_usuarios_empresas():
    """Crea usuarios para empresas que no tienen uno"""
    empresas_sin_user = Empresa.objects.filter(user__isnull=True)
    
    print(f"\n{'='*60}")
    print(f"CREANDO USUARIOS PARA EMPRESAS")
    print(f"{'='*60}\n")
    
    for empresa in empresas_sin_user:
        # Crear username basado en RUC (sin guiones ni espacios)
        username = f"empresa_{empresa.ruc}"
        
        # Verificar si ya existe el username
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Usuario {username} ya existe, saltando...")
            continue
        
        with transaction.atomic():
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=empresa.email,
                password='empresa123',  # Contraseña por defecto
                first_name=empresa.contacto_responsable.split()[0] if empresa.contacto_responsable else 'Admin',
                last_name=' '.join(empresa.contacto_responsable.split()[1:]) if len(empresa.contacto_responsable.split()) > 1 else empresa.nombre[:20]
            )
            
            # Asociar usuario con empresa
            empresa.user = user
            empresa.save()
            
            print(f"✅ Creado usuario para: {empresa.nombre}")
            print(f"   Username: {username}")
            print(f"   Password: empresa123")
            print(f"   Email: {empresa.email}")
            print()

def crear_usuarios_facultades():
    """Crea usuarios para facultades que no tienen uno"""
    facultades_sin_user = Facultad.objects.filter(user__isnull=True)
    
    print(f"\n{'='*60}")
    print(f"CREANDO USUARIOS PARA FACULTADES")
    print(f"{'='*60}\n")
    
    for facultad in facultades_sin_user:
        # Crear username basado en código
        username = f"facultad_{facultad.codigo.lower()}"
        
        # Verificar si ya existe el username
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Usuario {username} ya existe, saltando...")
            continue
        
        with transaction.atomic():
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=facultad.email,
                password='facultad123',  # Contraseña por defecto
                first_name=facultad.contacto_responsable.split()[0] if facultad.contacto_responsable else 'Admin',
                last_name=' '.join(facultad.contacto_responsable.split()[1:]) if len(facultad.contacto_responsable.split()) > 1 else facultad.nombre[:20]
            )
            
            # Asociar usuario con facultad
            facultad.user = user
            facultad.save()
            
            print(f"✅ Creado usuario para: {facultad.nombre}")
            print(f"   Username: {username}")
            print(f"   Password: facultad123")
            print(f"   Email: {facultad.email}")
            print()

# Ejecutar funciones
crear_usuarios_empresas()
crear_usuarios_facultades()

print(f"\n{'='*60}")
print(f"RESUMEN")
print(f"{'='*60}")
print(f"\nEmpresas con usuario: {Empresa.objects.filter(user__isnull=False).count()}/{Empresa.objects.count()}")
print(f"Facultades con usuario: {Facultad.objects.filter(user__isnull=False).count()}/{Facultad.objects.count()}")
print(f"\n✨ ¡Proceso completado!")
print(f"\n📋 CREDENCIALES DE ACCESO:")
print(f"\nEMPRESAS: Username: empresa_[RUC] | Password: empresa123")
print(f"FACULTADES: Username: facultad_[codigo] | Password: facultad123")
print(f"\nEjemplos:")
print(f"  - empresa_1790123456001 / empresa123")
print(f"  - facultad_fci / facultad123")
print(f"{'='*60}\n")
