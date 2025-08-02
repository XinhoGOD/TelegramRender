#!/usr/bin/env python3
"""
Servidor web para Render que ejecuta el userbot en segundo plano
"""

import os
import threading
import asyncio
import time
from flask import Flask, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, PHONE_NUMBER

# Configurar Flask
app = Flask(__name__)

# Variables globales para el userbot
userbot_thread = None
userbot_running = False
connection_status = "Desconectado"
user_info = None

# Leer sesión string desde variables de entorno
SESSION_STRING = os.getenv('SESSION_STRING')

class RenderUserBot:
    def __init__(self):
        self.client = None
        self.running = True
        self.connection_attempts = 0
        
    async def connect_telegram(self):
        """Conecta a Telegram"""
        global connection_status, user_info
        self.connection_attempts += 1
        print(f"📡 Intento {self.connection_attempts}: Conectando a Telegram...")
        connection_status = "Conectando..."
        
        try:
            if SESSION_STRING:
                print("✅ Usando sesión string pre-generada")
                self.client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
            else:
                print("⚠️ No hay sesión string configurada")
                connection_status = "Error: No hay sesión string"
                return False
            
            print("📡 Estableciendo conexión...")
            await self.client.connect()
            
            print("🔐 Verificando autorización...")
            if await self.client.is_user_authorized():
                me = await self.client.get_me()
                print(f"✅ Sesión autorizada")
                print(f"👤 Conectado como: {me.first_name} ({me.phone})")
                connection_status = f"Conectado como {me.first_name}"
                user_info = {
                    "name": me.first_name,
                    "phone": me.phone,
                    "id": me.id
                }
                return True
            else:
                print("❌ Sesión no autorizada")
                connection_status = "Error: Sesión no autorizada"
                return False
                    
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            connection_status = f"Error: {str(e)}"
            return False
    
    async def run_userbot(self):
        """Ejecuta el userbot principal"""
        try:
            print("🚀 Importando TelegramUserBot...")
            from userbot import TelegramUserBot
            print("✅ TelegramUserBot importado correctamente")
            
            print("🚀 Creando instancia del userbot...")
            bot = TelegramUserBot()
            print("✅ Instancia creada")
            
            print("🚀 Iniciando userbot...")
            await bot.start()
            print("✅ Userbot iniciado correctamente")
            
        except Exception as e:
            print(f"❌ Error ejecutando userbot: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def main_loop(self):
        """Bucle principal del userbot"""
        print("🚀 Iniciando UserBot en Render...")
        print("=" * 50)
        
        while self.running:
            try:
                # Conectar a Telegram
                if not await self.connect_telegram():
                    print("❌ No se pudo conectar a Telegram")
                    print("💡 Esperando 60 segundos antes de reintentar...")
                    await asyncio.sleep(60)
                    continue
                
                # Ejecutar userbot
                print("🚀 Iniciando UserBot...")
                await self.run_userbot()
                
            except Exception as e:
                print(f"❌ Error en bucle principal: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(10)
            
            finally:
                if self.client:
                    await self.client.disconnect()
    
    def stop(self):
        """Detiene el userbot"""
        print("🛑 Deteniendo UserBot...")
        self.running = False

def run_userbot_async():
    """Ejecuta el userbot en un bucle asíncrono"""
    try:
        # Crear nuevo event loop para el hilo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot = RenderUserBot()
        loop.run_until_complete(bot.main_loop())
    except Exception as e:
        print(f"❌ Error en hilo asíncrono: {e}")
        import traceback
        traceback.print_exc()

def start_userbot():
    """Inicia el userbot en un hilo separado"""
    global userbot_thread, userbot_running
    
    if not userbot_running:
        print("🚀 Iniciando UserBot en hilo separado...")
        userbot_thread = threading.Thread(target=run_userbot_async, daemon=True)
        userbot_thread.start()
        userbot_running = True
        print("✅ UserBot iniciado en segundo plano")

# Rutas de Flask
@app.route('/')
def home():
    """Página principal - Render la usa para health checks"""
    return jsonify({
        "status": "online",
        "service": "Telegram UserBot",
        "userbot_running": userbot_running,
        "connection_status": connection_status,
        "user_info": user_info,
        "message": "UserBot está funcionando en segundo plano"
    })

@app.route('/health')
def health():
    """Endpoint de health check para Render"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "userbot_running": userbot_running,
        "connection_status": connection_status
    })

@app.route('/status')
def status():
    """Endpoint para verificar el estado del userbot"""
    return jsonify({
        "userbot_running": userbot_running,
        "connection_status": connection_status,
        "user_info": user_info,
        "session_configured": bool(SESSION_STRING),
        "variables_configured": bool(API_ID and API_HASH and PHONE_NUMBER),
        "api_id_configured": bool(API_ID),
        "api_hash_configured": bool(API_HASH),
        "phone_configured": bool(PHONE_NUMBER),
        "session_string_configured": bool(SESSION_STRING)
    })

@app.route('/debug')
def debug():
    """Endpoint para diagnóstico detallado"""
    return jsonify({
        "userbot_running": userbot_running,
        "connection_status": connection_status,
        "user_info": user_info,
        "session_configured": bool(SESSION_STRING),
        "variables_configured": bool(API_ID and API_HASH and PHONE_NUMBER),
        "api_id": API_ID[:10] + "..." if API_ID else None,
        "api_hash": API_HASH[:10] + "..." if API_HASH else None,
        "phone_number": PHONE_NUMBER,
        "session_string_length": len(SESSION_STRING) if SESSION_STRING else 0
    })

@app.route('/start')
def start_bot():
    """Endpoint para iniciar el userbot manualmente"""
    start_userbot()
    return jsonify({"message": "UserBot iniciado"})

@app.route('/stop')
def stop_bot():
    """Endpoint para detener el userbot manualmente"""
    global userbot_running
    userbot_running = False
    return jsonify({"message": "UserBot detenido"})

if __name__ == '__main__':
    # Mostrar información de diagnóstico al inicio
    print("🔍 DIAGNÓSTICO INICIAL")
    print("=" * 50)
    print(f"API_ID: {'✅ Configurado' if API_ID else '❌ Faltante'}")
    print(f"API_HASH: {'✅ Configurado' if API_HASH else '❌ Faltante'}")
    print(f"PHONE_NUMBER: {'✅ Configurado' if PHONE_NUMBER else '❌ Faltante'}")
    print(f"SESSION_STRING: {'✅ Configurado' if SESSION_STRING else '❌ Faltante'}")
    print("=" * 50)
    
    # Iniciar el userbot en segundo plano
    start_userbot()
    
    # Iniciar el servidor web
    print("🌐 Iniciando servidor web en puerto 10000...")
    app.run(host='0.0.0.0', port=10000, debug=False) 