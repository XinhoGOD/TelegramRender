#!/usr/bin/env python3
"""
Script de inicio robusto para Railway
"""

import os
import sys
import subprocess
import time

def install_dependencies():
    """Instala las dependencias"""
    print("📦 Instalando dependencias...")
    try:
        # Intentar con python -m pip primero
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError:
        try:
            # Intentar con pip directamente
            subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencias instaladas")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False

def check_environment():
    """Verifica las variables de entorno"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = ['API_ID', 'API_HASH', 'PHONE_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        print("💡 Configura estas variables en Railway:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ Variables de entorno configuradas")
    return True

def main():
    """Función principal"""
    print("🚂 Iniciando UserBot en Railway...")
    print("=" * 50)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error en la instalación")
        sys.exit(1)
    
    # Verificar entorno
    if not check_environment():
        print("❌ Error en la configuración")
        sys.exit(1)
    
    # Importar y ejecutar el userbot
    try:
        print("🚀 Iniciando UserBot...")
        from railway_start import main as userbot_main
        userbot_main()
    except Exception as e:
        print(f"❌ Error iniciando UserBot: {e}")
        print("💡 Verifica que las variables de entorno estén configuradas")
        sys.exit(1)

if __name__ == "__main__":
    main() 