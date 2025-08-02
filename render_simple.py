#!/usr/bin/env python3
"""
Versión simplificada del userbot para Render
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

# Variables globales
userbot_running = False
connection_status = "Desconectado"
user_info = None

# Leer sesión string
SESSION_STRING = os.getenv('SESSION_STRING')

class SimpleUserBot:
    def __init__(self):
        self.client = None
        self.running = True
        
    async def test_connection(self):
        """Prueba la conexión a Telegram"""
        global connection_status, user_info
        
        try:
            print("📡 Probando conexión a Telegram...")
            connection_status = "Probando conexión..."
            
            if not SESSION_STRING:
                print("❌ No hay sesión string")
                connection_status = "Error: No hay sesión string"
                return False
            
            # Crear cliente con timeout
            self.client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
            
            # Conectar con timeout
            print("🔌 Conectando...")
            await asyncio.wait_for(self.client.connect(), timeout=15.0)
            
            # Verificar autorización
            print("🔐 Verificando autorización...")
            if await self.client.is_user_authorized():
                me = await self.client.get_me()
                print(f"✅ Conectado como: {me.first_name}")
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
                
        except asyncio.TimeoutError:
            print("⏰ Timeout de conexión")
            connection_status = "Error: Timeout"
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            connection_status = f"Error: {str(e)}"
            return False
    
    async def run_basic_userbot(self):
        """Ejecuta un userbot básico"""
        try:
            print("🚀 Iniciando userbot básico...")
            
            # Importar y crear userbot
            from userbot import TelegramUserBot
            bot = TelegramUserBot()
            
            # Iniciar con timeout
            await asyncio.wait_for(bot.start(), timeout=30.0)
            print("✅ Userbot iniciado")
            
            # Mantener activo
            while self.running:
                await asyncio.sleep(10)
                
        except asyncio.TimeoutError:
            print("⏰ Timeout al iniciar userbot")
        except Exception as e:
            print(f"❌ Error en userbot: {e}")
    
    async def main_loop(self):
        """Bucle principal simplificado"""
        print("🚀 Iniciando UserBot Simple...")
        
        while self.running:
            try:
                # Probar conexión
                if await self.test_connection():
                    print("✅ Conexión exitosa, iniciando userbot...")
                    await self.run_basic_userbot()
                else:
                    print("❌ No se pudo conectar, reintentando en 60s...")
                    await asyncio.sleep(60)
                    
            except Exception as e:
                print(f"❌ Error en bucle: {e}")
                await asyncio.sleep(30)
            
            finally:
                if self.client:
                    await self.client.disconnect()

def run_userbot_thread():
    """Ejecuta el userbot en un hilo"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot = SimpleUserBot()
        loop.run_until_complete(bot.main_loop())
    except Exception as e:
        print(f"❌ Error en hilo: {e}")

def start_userbot():
    """Inicia el userbot"""
    global userbot_running
    
    if not userbot_running:
        print("🚀 Iniciando UserBot...")
        thread = threading.Thread(target=run_userbot_thread, daemon=True)
        thread.start()
        userbot_running = True
        print("✅ UserBot iniciado")

# Rutas de Flask
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Telegram UserBot Simple",
        "userbot_running": userbot_running,
        "connection_status": connection_status,
        "user_info": user_info
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "userbot_running": userbot_running,
        "connection_status": connection_status
    })

@app.route('/status')
def status():
    return jsonify({
        "userbot_running": userbot_running,
        "connection_status": connection_status,
        "user_info": user_info,
        "session_configured": bool(SESSION_STRING),
        "variables_configured": bool(API_ID and API_HASH and PHONE_NUMBER)
    })

@app.route('/start')
def start_bot():
    start_userbot()
    return jsonify({"message": "UserBot iniciado"})

if __name__ == '__main__':
    print("🔍 DIAGNÓSTICO INICIAL")
    print("=" * 50)
    print(f"API_ID: {'✅ Configurado' if API_ID else '❌ Faltante'}")
    print(f"API_HASH: {'✅ Configurado' if API_HASH else '❌ Faltante'}")
    print(f"PHONE_NUMBER: {'✅ Configurado' if PHONE_NUMBER else '❌ Faltante'}")
    print(f"SESSION_STRING: {'✅ Configurado' if SESSION_STRING else '❌ Faltante'}")
    print("=" * 50)
    
    # Iniciar userbot
    start_userbot()
    
    # Iniciar servidor web
    print("🌐 Iniciando servidor web...")
    app.run(host='0.0.0.0', port=10000, debug=False) 