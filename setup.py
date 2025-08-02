#!/usr/bin/env python3
"""
Script de instalación automática para el UserBot de Telegram
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Imprime el banner del proyecto"""
    print("""
🤖 ======================================== 🤖
    USERBOT DE TELEGRAM - ENVÍO MASIVO
🤖 ======================================== 🤖
    """)

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crea el archivo .env si no existe"""
    print("\n⚙️ Configurando archivo de variables de entorno...")
    
    if os.path.exists(".env"):
        print("✅ Archivo .env ya existe")
        return True
    
    print("📝 Creando archivo .env...")
    print("💡 Necesitarás configurar las siguientes variables:")
    print("   - API_ID: Tu API ID de Telegram")
    print("   - API_HASH: Tu API Hash de Telegram")
    print("   - PHONE_NUMBER: Tu número de teléfono (+34612345678)")
    
    env_content = """# Configuración de Telegram API
# Obtén estos valores en https://my.telegram.org/apps
API_ID=tu_api_id_aqui
API_HASH=tu_api_hash_aqui
PHONE_NUMBER=+34612345678
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        print("⚠️  Recuerda configurar las variables con tus datos reales")
        return True
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def show_next_steps():
    """Muestra los siguientes pasos a seguir"""
    print("""
🎉 ¡Instalación completada!

📋 Próximos pasos:

1. 🔧 Configurar variables de entorno:
   - Edita el archivo .env
   - Reemplaza los valores con tus datos reales
   - Obtén API_ID y API_HASH en: https://my.telegram.org/apps

2. 🔐 Generar archivo de sesión:
   python generate_session.py

3. 🚀 Ejecutar el userbot:
   python userbot.py

📖 Para más información, consulta el README.md

⚠️  IMPORTANTE: Usa el userbot de forma responsable
    """)

def main():
    """Función principal del script de instalación"""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Crear archivo .env
    if not create_env_file():
        sys.exit(1)
    
    # Mostrar próximos pasos
    show_next_steps()

if __name__ == "__main__":
    main() 