import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import Chat, Channel, User
from telethon.errors import FloodWaitError, ChatWriteForbiddenError, UserNotParticipantError
from config import API_ID, API_HASH, PHONE_NUMBER, SESSION_NAME

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales para el estado del userbot
user_states = {}
pending_messages = {}

class TelegramUserBot:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.setup_handlers()
    
    def setup_handlers(self):
        # Handler para comandos específicos (debe ir primero)
        @self.client.on(events.NewMessage(pattern=r'^/(start|enviar|cancelar|confirmar)'))
        async def command_handler(event):
            command = event.message.text.split()[0].lower()
            
            if command == '/start':
                await self.handle_start(event)
            elif command == '/enviar':
                await self.handle_enviar(event)
            elif command == '/cancelar':
                await self.handle_cancelar(event)
            elif command == '/confirmar':
                await self.handle_confirmar(event)
        
        # Handler para mensajes normales (debe ir después)
        @self.client.on(events.NewMessage())
        async def message_handler(event):
            # Verificar que no sea un comando
            if event.message.text.startswith('/'):
                return
            
            await self.handle_message(event)
    
    async def handle_start(self, event):
        """Maneja el comando /start"""
        user_id = event.sender_id
        user_states[user_id] = 'idle'
        
        welcome_message = """
🤖 **Bienvenido al UserBot de Envío Masivo**

Este bot te permite enviar mensajes a todos los grupos donde estés unido.

**Comandos disponibles:**
• `/enviar` - Iniciar proceso de envío de mensaje
• `/cancelar` - Cancelar operación actual
• `/start` - Mostrar este mensaje

⚠️ **Importante:** Solo envía mensajes a grupos donde tengas permisos de escritura.
        """
        
        await event.respond(welcome_message, parse_mode='markdown')
    
    async def handle_enviar(self, event):
        """Maneja el comando /enviar"""
        user_id = event.sender_id
        user_states[user_id] = 'waiting_message'
        
        await event.respond("📝 **Por favor, envía el mensaje que quieres distribuir a todos los grupos.**\n\nPuedes usar `/cancelar` para cancelar la operación.")
    
    async def handle_cancelar(self, event):
        """Maneja el comando /cancelar"""
        user_id = event.sender_id
        
        if user_id in user_states:
            user_states[user_id] = 'idle'
            if user_id in pending_messages:
                del pending_messages[user_id]
        
        await event.respond("❌ **Operación cancelada.**\n\nUsa `/enviar` para iniciar una nueva operación.")
    
    async def handle_confirmar(self, event):
        """Maneja el comando /confirmar"""
        user_id = event.sender_id
        
        if user_id not in pending_messages:
            await event.respond("❌ **No hay mensaje pendiente para confirmar.**\n\nUsa `/enviar` para iniciar una nueva operación.")
            return
        
        await self.send_mass_message(event, user_id)
    
    async def handle_message(self, event):
        """Maneja mensajes normales para capturar el mensaje a enviar"""
        user_id = event.sender_id
        
        if user_id not in user_states or user_states[user_id] != 'waiting_message':
            return
        
        # Capturar el mensaje
        message_text = event.message.text
        pending_messages[user_id] = message_text
        user_states[user_id] = 'waiting_confirmation'
        
        # Mostrar preview del mensaje
        preview_message = f"""
📋 **Vista previa del mensaje:**

```
{message_text}
```

**¿Confirmas el envío de este mensaje a todos los grupos donde estés unido?**

• `/confirmar` - Confirmar y enviar
• `/cancelar` - Cancelar operación
        """
        
        await event.respond(preview_message, parse_mode='markdown')
    
    async def send_mass_message(self, event, user_id):
        """Envía el mensaje a todos los grupos"""
        message_text = pending_messages[user_id]
        
        await event.respond("🚀 **Iniciando envío masivo...**\n\nObteniendo lista de grupos...")
        
        # Obtener todos los chats
        dialogs = await self.client.get_dialogs()
        groups = []
        
        for dialog in dialogs:
            entity = dialog.entity
            try:
                # Verificar si es un grupo válido para enviar mensajes
                if isinstance(entity, Chat):
                    # Es un grupo normal
                    groups.append(entity)
                elif isinstance(entity, Channel):
                    # Verificar si es un supergrupo (no canal de broadcast)
                    if hasattr(entity, 'megagroup') and entity.megagroup:
                        groups.append(entity)
                    elif hasattr(entity, 'broadcast') and not entity.broadcast:
                        # Canal que no es de broadcast (puede ser un grupo)
                        groups.append(entity)
                        
            except Exception as e:
                logger.warning(f"Error procesando entidad {getattr(entity, 'title', 'Unknown')}: {str(e)}")
                continue
        
        await event.respond(f"📊 **Encontrados {len(groups)} grupos.**\n\nIniciando envío...")
        
        # Estadísticas
        success_count = 0
        failed_count = 0
        failed_groups = []
        
        for i, group in enumerate(groups, 1):
            try:
                # Intentar enviar el mensaje
                await self.client.send_message(group, message_text)
                success_count += 1
                
                # Actualizar progreso cada 5 grupos
                if i % 5 == 0 or i == len(groups):
                    progress = f"📤 **Progreso:** {i}/{len(groups)} grupos procesados\n✅ Exitosos: {success_count}\n❌ Fallidos: {failed_count}"
                    await event.respond(progress)
                
                # Pequeña pausa para evitar flood
                await asyncio.sleep(1)
                
            except FloodWaitError as e:
                # Esperar si hay flood wait
                wait_time = e.seconds
                await event.respond(f"⏳ **Esperando {wait_time} segundos debido a limitaciones de Telegram...**")
                await asyncio.sleep(wait_time)
                continue
                
            except (ChatWriteForbiddenError, UserNotParticipantError) as e:
                failed_count += 1
                group_title = getattr(group, 'title', 'Grupo desconocido')
                failed_groups.append(group_title)
                logger.warning(f"No se pudo enviar a {group_title}: {str(e)}")
                
            except Exception as e:
                failed_count += 1
                group_title = getattr(group, 'title', 'Grupo desconocido')
                failed_groups.append(group_title)
                logger.error(f"Error enviando a {group_title}: {str(e)}")
        
        # Generar reporte final
        report = f"""
📊 **REPORTE FINAL DE ENVÍO**

✅ **Enviados con éxito:** {success_count}
❌ **Fallidos:** {failed_count}
📈 **Total de grupos:** {len(groups)}

"""
        
        if failed_groups:
            report += f"❌ **Grupos donde falló el envío:**\n"
            for group in failed_groups[:10]:  # Mostrar solo los primeros 10
                report += f"• {group}\n"
            if len(failed_groups) > 10:
                report += f"... y {len(failed_groups) - 10} más\n"
        
        report += "\n🎉 **¡Envío masivo completado!**"
        
        await event.respond(report, parse_mode='markdown')
        
        # Limpiar estado
        user_states[user_id] = 'idle'
        if user_id in pending_messages:
            del pending_messages[user_id]
    
    async def start(self):
        """Inicia el userbot"""
        logger.info("Iniciando UserBot...")
        await self.client.start(phone=PHONE_NUMBER)
        logger.info("UserBot iniciado correctamente!")
        
        # Mantener el bot corriendo
        await self.client.run_until_disconnected()

async def main():
    """Función principal"""
    bot = TelegramUserBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main()) 