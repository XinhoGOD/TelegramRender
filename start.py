#!/usr/bin/env python3
"""
Script de inicio robusto para Railway con Docker
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def load_environment():
    """Carga las variables de entorno"""
    print("🔧 Cargando variables de entorno...")
    
    # Cargar archivo .env si existe
    if os.path.exists('.env'):
        print("✅ Archivo .env encontrado, cargando...")
        load_dotenv()
    else:
        print("⚠️ Archivo .env no encontrado, usando variables del sistema")
    
    # Debuggear variables
    from debug_env import debug_environment
    debug_environment()

def check_environment():
    """Verifica las variables de entorno"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = ['API_ID', 'API_HASH', 'PHONE_NUMBER']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: Configurada")
    
    if missing_vars:
        print(f"❌ Variables faltantes: {', '.join(missing_vars)}")
        print("💡 Configura estas variables en Railway:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ Todas las variables de entorno configuradas")
    return True

def main():
    """Función principal"""
    print("🚂 Iniciando UserBot en Railway (Docker)...")
    print("=" * 50)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Cargar entorno
    load_environment()
    
    # Verificar entorno
    if not check_environment():
        print("❌ Error en la configuración")
        print("💡 Asegúrate de configurar las variables en Railway:")
        print("   - Ve a tu proyecto en Railway")
        print("   - Ve a la pestaña 'Variables'")
        print("   - Agrega: API_ID, API_HASH, PHONE_NUMBER")
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