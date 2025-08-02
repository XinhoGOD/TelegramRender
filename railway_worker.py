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
from config import API_ID, API_HASH, PHONE_NUMBER

# Nombre de sesión único para Railway
SESSION_NAME = 'railway_userbot_session'

class RailwayUserBot:
    def __init__(self):
        self.client = None
        self.running = True
        
    async def cleanup_session(self):
        """Limpia archivos de sesión problemáticos"""
        session_file = f"{SESSION_NAME}.session"
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
                print("✅ Archivo de sesión eliminado")
                return True
            except Exception as e:
                print(f"⚠️ No se pudo eliminar archivo de sesión: {e}")
        return False
    
    async def connect_telegram(self):
        """Conecta a Telegram con manejo de errores"""
        print("📡 Conectando a Telegram...")
        
        try:
            self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
            
            # Verificar si ya existe una sesión válida
            if os.path.exists(f"{SESSION_NAME}.session"):
                print("✅ Archivo de sesión encontrado, intentando usar...")
                try:
                    await self.client.connect()
                    if await self.client.is_user_authorized():
                        print("✅ Sesión válida encontrada")
                        return True
                    else:
                        print("⚠️ Sesión inválida, eliminando...")
                        await self.cleanup_session()
                except Exception as e:
                    print(f"⚠️ Error con sesión existente: {e}")
                    await self.cleanup_session()
            
            # Si no hay sesión válida, intentar crear una nueva
            print("🔄 Creando nueva sesión...")
            
            # En Railway, no podemos leer stdin, así que usamos un método alternativo
            try:
                # Intentar conectar sin verificación manual
                await self.client.start(phone=PHONE_NUMBER, code_callback=self.code_callback)
                return True
            except Exception as e:
                if "EOF when reading a line" in str(e) or "code_callback" in str(e):
                    print("❌ Error: Railway no puede manejar verificación manual")
                    print("💡 Solución: Necesitas generar la sesión localmente primero")
                    return False
                else:
                    print(f"❌ Error de conexión: {e}")
                    return False
                    
        except Exception as e:
            if "database is locked" in str(e):
                print("⚠️ Error de base de datos bloqueada, limpiando...")
                await self.cleanup_session()
                # Intentar nuevamente
                try:
                    self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
                    await self.client.start(phone=PHONE_NUMBER, code_callback=self.code_callback)
                    return True
                except Exception as e2:
                    print(f"❌ Error en segundo intento: {e2}")
                    return False
            else:
                print(f"❌ Error de conexión: {e}")
                return False
    
    def code_callback(self):
        """Callback para código de verificación (no usado en Railway)"""
        print("❌ Error: Railway no puede manejar verificación manual")
        return None
    
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
                    print("1. Ejecuta localmente: python generate_session.py")
                    print("2. Copia el archivo .session a Railway")
                    print("3. O usa el método de sesión string")
                    await asyncio.sleep(60)  # Esperar 1 minuto
                    continue
                
                # Verificar autorización
                if not await self.client.is_user_authorized():
                    print("❌ No se pudo autorizar la sesión")
                    await asyncio.sleep(30)
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