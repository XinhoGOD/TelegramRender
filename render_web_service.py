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

# Leer sesión string desde variables de entorno
SESSION_STRING = os.getenv('SESSION_STRING')

class RenderUserBot:
    def __init__(self):
        self.client = None
        self.running = True
        
    async def connect_telegram(self):
        """Conecta a Telegram"""
        print("📡 Conectando a Telegram...")
        
        try:
            if SESSION_STRING:
                print("✅ Usando sesión string pre-generada")
                self.client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
            else:
                print("⚠️ No hay sesión string configurada")
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
        """Bucle principal del userbot"""
        print("🚀 Iniciando UserBot en Render...")
        print("=" * 50)
        
        while self.running:
            try:
                # Conectar a Telegram
                if not await self.connect_telegram():
                    print("❌ No se pudo conectar a Telegram")
                    await asyncio.sleep(60)
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
    
    def stop(self):
        """Detiene el userbot"""
        print("🛑 Deteniendo UserBot...")
        self.running = False

def run_userbot_async():
    """Ejecuta el userbot en un bucle asíncrono"""
    bot = RenderUserBot()
    asyncio.run(bot.main_loop())

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
        "message": "UserBot está funcionando en segundo plano"
    })

@app.route('/health')
def health():
    """Endpoint de health check para Render"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })

@app.route('/status')
def status():
    """Endpoint para verificar el estado del userbot"""
    return jsonify({
        "userbot_running": userbot_running,
        "session_configured": bool(SESSION_STRING),
        "variables_configured": bool(API_ID and API_HASH and PHONE_NUMBER)
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
    # Iniciar el userbot en segundo plano
    start_userbot()
    
    # Iniciar el servidor web
    print("🌐 Iniciando servidor web en puerto 10000...")
    app.run(host='0.0.0.0', port=10000, debug=False) 