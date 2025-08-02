#!/usr/bin/env python3
"""
Script para debuggear variables de entorno en Railway
"""

import os
from dotenv import load_dotenv

def debug_environment():
    """Debuggear las variables de entorno"""
    print("🔍 DEBUG: Variables de entorno")
    print("=" * 40)
    
    # Cargar archivo .env si existe
    if os.path.exists('.env'):
        print("✅ Archivo .env encontrado")
        load_dotenv()
    else:
        print("❌ Archivo .env NO encontrado")
    
    # Variables requeridas
    required_vars = ['API_ID', 'API_HASH', 'PHONE_NUMBER']
    
    print("\n📋 Variables de entorno:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mostrar solo los primeros caracteres por seguridad
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NO CONFIGURADA")
    
    # Mostrar todas las variables de entorno (solo nombres)
    print("\n📋 Todas las variables disponibles:")
    for key, value in os.environ.items():
        if any(required in key.upper() for required in ['API', 'PHONE', 'TELEGRAM']):
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"🔍 {key}: {display_value}")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    debug_environment() 