#!/usr/bin/env python3
"""
Script de diagnóstico para Render
"""

import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, PHONE_NUMBER

# Leer sesión string
SESSION_STRING = os.getenv('SESSION_STRING')

async def test_connection():
    """Prueba la conexión a Telegram"""
    print("🔍 DIAGNÓSTICO DE CONEXIÓN")
    print("=" * 50)
    
    # Verificar variables
    print("📋 Variables de entorno:")
    print(f"API_ID: {'✅ Configurado' if API_ID else '❌ Faltante'}")
    print(f"API_HASH: {'✅ Configurado' if API_HASH else '❌ Faltante'}")
    print(f"PHONE_NUMBER: {'✅ Configurado' if PHONE_NUMBER else '❌ Faltante'}")
    print(f"SESSION_STRING: {'✅ Configurado' if SESSION_STRING else '❌ Faltante'}")
    
    if not all([API_ID, API_HASH, PHONE_NUMBER, SESSION_STRING]):
        print("\n❌ ERROR: Faltan variables de entorno")
        return False
    
    # Probar conexión
    print("\n📡 Probando conexión a Telegram...")
    try:
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Conexión exitosa!")
            print(f"👤 Usuario: {me.first_name} {me.last_name or ''}")
            print(f"📱 Teléfono: {me.phone}")
            print(f"🆔 ID: {me.id}")
            await client.disconnect()
            return True
        else:
            print("❌ Sesión no autorizada")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection()) 