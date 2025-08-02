#!/usr/bin/env python3
"""
Script de inicio para Railway
Maneja la configuración automática del userbot en Railway
"""

import os
import sys
import asyncio
import time
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER

# Usar un nombre de sesión único para Railway
SESSION_NAME = 'railway_userbot_session'

async def setup_railway():
    """Configura el userbot para Railway"""
    print("🚂 Configurando UserBot para Railway...")
    
    # Verificar variables de entorno
    if not API_ID or not API_HASH or not PHONE_NUMBER:
        print("❌ Error: Faltan variables de entorno")
        print("💡 Configura en Railway:")
        print("   - API_ID")
        print("   - API_HASH") 
        print("   - PHONE_NUMBER")
        return False
    
    print(f"✅ API_ID: {API_ID}")
    print(f"✅ API_HASH: {API_HASH[:10]}...")
    print(f"✅ PHONE_NUMBER: {PHONE_NUMBER}")
    
    # Crear cliente con nombre de sesión único
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        print("📡 Conectando a Telegram...")
        
        # Intentar conectar con manejo de errores
        try:
            await client.start(phone=PHONE_NUMBER)
        except Exception as e:
            if "database is locked" in str(e):
                print("⚠️ Error de base de datos bloqueada, intentando limpiar...")
                # Eliminar archivo de sesión si existe
                session_file = f"{SESSION_NAME}.session"
                if os.path.exists(session_file):
                    try:
                        os.remove(session_file)
                        print("✅ Archivo de sesión eliminado")
                    except:
                        pass
                
                # Intentar conectar nuevamente
                await client.start(phone=PHONE_NUMBER)
            else:
                raise e
        
        if await client.is_user_authorized():
            print("✅ Sesión autorizada")
            me = await client.get_me()
            print(f"👤 Usuario: {me.first_name}")
            print(f"📱 Teléfono: {me.phone}")
            
            # Importar y ejecutar el userbot
            from userbot import main
            print("🚀 Iniciando UserBot...")
            await main()
            
        else:
            print("❌ Error: No se pudo autorizar la sesión")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        await client.disconnect()
    
    return True

def main():
    """Función principal"""
    print("🤖 UserBot de Telegram para Railway")
    print("=" * 40)
    
    # Ejecutar configuración
    success = asyncio.run(setup_railway())
    
    if not success:
        print("\n❌ Error en la configuración")
        sys.exit(1)
    
    print("\n✅ UserBot configurado y ejecutándose en Railway")

if __name__ == "__main__":
    main() 