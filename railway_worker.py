#!/usr/bin/env python3
"""
Worker script para Railway que maneja reinicios y errores
"""

import os
import sys
import asyncio
import time
import signal
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, PHONE_NUMBER

# Leer sesión string desde variables de entorno
SESSION_STRING = os.getenv('SESSION_STRING')

class RailwayUserBot:
    def __init__(self):
        self.client = None
        self.running = True
        
    async def connect_telegram(self):
        """Conecta a Telegram con manejo de errores"""
        print("📡 Conectando a Telegram...")
        
        try:
            # Usar sesión en memoria
            if SESSION_STRING:
                print("✅ Usando sesión string pre-generada")
                self.client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
            else:
                print("⚠️ No hay sesión string configurada")
                print("💡 Necesitas generar la sesión string localmente")
                print("💡 Ejecuta: python generate_railway_string.py")
                return False
            
            await self.client.connect()
            
            if await self.client.is_user_authorized():
                print("✅ Sesión autorizada")
                return True
            else:
                print("❌ Sesión no autorizada")
                return False
                    
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    async def run_userbot(self):
        """Ejecuta el userbot principal"""
        try:
            from userbot import TelegramUserBot
            bot = TelegramUserBot()
            await bot.start()
        except Exception as e:
            print(f"❌ Error ejecutando userbot: {e}")
            return False
    
    async def main_loop(self):
        """Bucle principal con manejo de errores"""
        print("🚂 Iniciando UserBot Worker en Railway...")
        print("=" * 50)
        
        while self.running:
            try:
                # Conectar a Telegram
                if not await self.connect_telegram():
                    print("❌ No se pudo conectar a Telegram")
                    print("💡 Instrucciones para solucionar:")
                    print("1. Ejecuta localmente: python generate_railway_string.py")
                    print("2. Copia la sesión string a Railway como variable de entorno")
                    print("3. Configura SESSION_STRING en Railway")
                    await asyncio.sleep(60)  # Esperar 1 minuto
                    continue
                
                # Obtener información del usuario
                me = await self.client.get_me()
                print(f"✅ Conectado como: {me.first_name} ({me.phone})")
                
                # Ejecutar userbot
                print("🚀 Iniciando UserBot...")
                await self.run_userbot()
                
            except Exception as e:
                print(f"❌ Error en bucle principal: {e}")
                await asyncio.sleep(10)
            
            finally:
                if self.client:
                    await self.client.disconnect()
    
    def signal_handler(self, signum, frame):
        """Maneja señales de terminación"""
        print("🛑 Recibida señal de terminación, cerrando...")
        self.running = False

async def main():
    """Función principal"""
    worker = RailwayUserBot()
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, worker.signal_handler)
    signal.signal(signal.SIGTERM, worker.signal_handler)
    
    # Ejecutar bucle principal
    await worker.main_loop()

if __name__ == "__main__":
    asyncio.run(main()) 