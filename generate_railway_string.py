#!/usr/bin/env python3
"""
Script para generar sesión string localmente para Railway
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, PHONE_NUMBER

async def generate_railway_string():
    """Genera la sesión string para Railway"""
    print("🔐 Generando sesión string para Railway...")
    print(f"📱 Número de teléfono: {PHONE_NUMBER}")
    print(f"🆔 API ID: {API_ID}")
    print(f"🔑 API Hash: {API_HASH[:10]}...")
    print()
    
    # Crear cliente con sesión string
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    try:
        # Iniciar sesión
        print("📡 Conectando a Telegram...")
        await client.start(phone=PHONE_NUMBER)
        
        # Verificar que la sesión se creó correctamente
        if await client.is_user_authorized():
            # Obtener la sesión string
            session_string = client.session.save()
            
            print("✅ Sesión string generada exitosamente!")
            print()
            
            # Obtener información del usuario
            me = await client.get_me()
            print(f"👤 Usuario: {me.first_name} {me.last_name or ''}")
            print(f"📱 Teléfono: {me.phone}")
            print(f"🆔 ID de usuario: {me.id}")
            
            print("\n🎉 ¡Sesión string lista para Railway!")
            print("📋 Próximos pasos:")
            print("1. Copia la sesión string de abajo")
            print("2. Ve a Railway → Variables")
            print("3. Agrega: SESSION_STRING=tu_sesion_string")
            print()
            print("🔑 SESIÓN STRING:")
            print("=" * 50)
            print(session_string)
            print("=" * 50)
            print()
            print("⚠️ IMPORTANTE:")
            print("- No compartas esta sesión string con nadie")
            print("- Es específica para tu cuenta de Telegram")
            print("- Regenera si cambias de cuenta")
            
        else:
            print("❌ Error: No se pudo autorizar la sesión")
            
    except Exception as e:
        print(f"❌ Error durante la generación de sesión: {str(e)}")
        print()
        print("💡 Posibles soluciones:")
        print("1. Verifica que API_ID y API_HASH sean correctos")
        print("2. Asegúrate de que el número de teléfono esté en formato internacional")
        print("3. Revisa tu conexión a internet")
        
    finally:
        await client.disconnect()

async def main():
    """Función principal"""
    # Verificar configuración
    if not API_ID or not API_HASH or not PHONE_NUMBER:
        print("❌ Error: Faltan variables de configuración")
        print("📝 Asegúrate de crear un archivo .env con:")
        print("   API_ID=tu_api_id")
        print("   API_HASH=tu_api_hash")
        print("   PHONE_NUMBER=+34612345678")
        return
    
    await generate_railway_string()

if __name__ == "__main__":
    asyncio.run(main()) 