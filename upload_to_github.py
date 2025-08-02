#!/usr/bin/env python3
"""
Script para subir el proyecto UserBot a GitHub
"""

import os
import subprocess
import sys

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

def check_git():
    """Verifica si Git está disponible"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    """Función principal para subir a GitHub"""
    print("🚀 Iniciando proceso de subida a GitHub...")
    print()
    
    # Verificar Git
    if not check_git():
        print("❌ Git no está disponible. Por favor:")
        print("1. Reinicia tu terminal")
        print("2. Ejecuta: git --version")
        print("3. Si no funciona, instala Git desde: https://git-scm.com/")
        return
    
    print("✅ Git está disponible")
    
    # Comandos para subir a GitHub
    commands = [
        ("git init", "Inicializando repositorio Git"),
        ("git add .", "Agregando archivos al staging"),
        ("git commit -m \"Initial commit: UserBot de Telegram para envío masivo\"", "Creando commit inicial"),
        ("git branch -M main", "Configurando rama principal"),
        ("git remote add origin https://github.com/XinhoGOD/TelegramRender.git", "Agregando repositorio remoto"),
        ("git push -u origin main", "Subiendo código a GitHub")
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
    print("📋 Próximos pasos:")
    print("1. Ve a tu repositorio en GitHub")
    print("2. Verifica que todos los archivos estén subidos")
    print("3. Actualiza el README si es necesario")
    print("4. Comparte el enlace con otros desarrolladores")

if __name__ == "__main__":
    main() 