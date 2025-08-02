import asyncio
import os
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME

async def generate_session():
    """Genera el archivo .session para evitar verificaciones futuras"""
    print("🔐 Generando archivo de sesión...")
    print(f"📱 Número de teléfono: {PHONE_NUMBER}")
    print(f"🆔 API ID: {API_ID}")
    print(f"🔑 API Hash: {API_HASH[:10]}...")
    print()
    
    # Crear cliente
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    try:
        # Iniciar sesión
        print("📡 Conectando a Telegram...")
        await client.start(phone=PHONE_NUMBER)
        
        # Verificar que la sesión se creó correctamente
        if await client.is_user_authorized():
            print("✅ Sesión creada exitosamente!")
            print(f"💾 Archivo de sesión guardado como: {SESSION_NAME}.session")
            print()
            print("🎉 ¡El userbot está listo para usar!")
            print("📝 Ahora puedes ejecutar: python userbot.py")
            
            # Obtener información del usuario
            me = await client.get_me()
            print(f"👤 Usuario: {me.first_name} {me.last_name or ''}")
            print(f"📱 Teléfono: {me.phone}")
            print(f"🆔 ID de usuario: {me.id}")
            
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
    
    await generate_session()

if __name__ == "__main__":
    asyncio.run(main()) 