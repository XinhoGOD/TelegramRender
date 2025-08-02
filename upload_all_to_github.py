#!/usr/bin/env python3
"""
Script para subir TODOS los archivos del proyecto UserBot a GitHub
INCLUYENDO archivos protegidos (.env, .session)
"""

import os
import subprocess
import sys
import platform

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Error: {e.stderr}")
        return False

def get_git_path():
    """Obtiene la ruta de Git según el sistema operativo"""
    if platform.system() == "Windows":
        # Rutas comunes de Git en Windows
        git_paths = [
            r"C:\Program Files\Git\bin\git.exe",
            r"C:\Program Files (x86)\Git\bin\git.exe",
            "git.exe"  # Si está en PATH
        ]
        
        for path in git_paths:
            try:
                subprocess.run([path, "--version"], check=True, capture_output=True)
                return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return None
    else:
        return "git"

def check_git():
    """Verifica si Git está disponible"""
    git_path = get_git_path()
    if git_path:
        print(f"✅ Git encontrado en: {git_path}")
        return True
    else:
        print("❌ Git no encontrado")
        return False

def show_warning():
    """Muestra advertencia de seguridad"""
    print("""
⚠️  ADVERTENCIA DE SEGURIDAD ⚠️

Este script subirá TODOS los archivos, incluyendo:
- .env (contiene tus credenciales de Telegram)
- *.session (contiene tu sesión de Telegram)

Esto puede exponer información sensible públicamente.

¿Estás seguro de que quieres continuar? (s/n): """)
    
    response = input().lower().strip()
    return response in ['s', 'si', 'sí', 'y', 'yes']

def main():
    """Función principal para subir a GitHub"""
    print("🚀 Iniciando proceso de subida COMPLETA a GitHub...")
    print()
    
    # Mostrar advertencia
    if not show_warning():
        print("❌ Operación cancelada por el usuario")
        return
    
    # Verificar Git
    if not check_git():
        print("❌ Git no está disponible. Por favor:")
        print("1. Reinicia tu terminal")
        print("2. Ejecuta: git --version")
        print("3. Si no funciona, instala Git desde: https://git-scm.com/")
        return
    
    git_path = get_git_path()
    
    # Comandos para subir a GitHub usando la ruta completa
    commands = [
        (f'"{git_path}" init', "Inicializando repositorio Git"),
        (f'"{git_path}" add .', "Agregando TODOS los archivos al staging"),
        (f'"{git_path}" commit -m "Initial commit: UserBot de Telegram para envío masivo - INCLUYE ARCHIVOS PROTEGIDOS"', "Creando commit inicial"),
        (f'"{git_path}" branch -M main', "Configurando rama principal"),
        (f'"{git_path}" remote add origin https://github.com/XinhoGOD/TelegramRender.git', "Agregando repositorio remoto"),
        (f'"{git_path}" push -u origin main', "Subiendo código a GitHub")
    ]
    
    # Ejecutar comandos
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Error en: {description}")
            print("💡 Posibles soluciones:")
            print("1. Verifica tu conexión a internet")
            print("2. Asegúrate de tener permisos en el repositorio")
            print("3. Verifica que el repositorio existe en GitHub")
            return
    
    print("\n🎉 ¡Proyecto subido exitosamente a GitHub!")
    print("📁 Repositorio: https://github.com/XinhoGOD/TelegramRender")
    print()
    print("⚠️  IMPORTANTE:")
    print("- Tus credenciales de Telegram están ahora públicas")
    print("- Tu archivo de sesión está expuesto")
    print("- Considera regenerar tus credenciales de API")
    print()
    print("📋 Próximos pasos:")
    print("1. Ve a tu repositorio en GitHub")
    print("2. Verifica que todos los archivos estén subidos")
    print("3. Considera hacer el repositorio privado")
    print("4. Regenera tus credenciales de Telegram API")

if __name__ == "__main__":
    main() 