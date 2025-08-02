# 🤖 UserBot de Telegram - Envío Masivo

Un userbot de Telegram que permite enviar mensajes a todos los grupos donde estés unido de forma masiva.

## ✨ Características

- ✅ Envío masivo a todos los grupos
- 📊 Estadísticas detalladas de envío
- 🔄 Actualizaciones en tiempo real
- 🛡️ Manejo de errores y limitaciones
- 📱 Interfaz intuitiva con comandos
- 💾 Sesión persistente (sin verificaciones repetidas)

## 📋 Requisitos

- Python 3.7 o superior
- Cuenta de Telegram
- API ID y API Hash de Telegram

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
API_ID=tu_api_id_aqui
API_HASH=tu_api_hash_aqui
PHONE_NUMBER=+34612345678
```

### 4. Obtener API ID y API Hash

1. Ve a https://my.telegram.org/apps
2. Inicia sesión con tu número de teléfono
3. Crea una nueva aplicación
4. Copia el `api_id` y `api_hash`
5. Pégales en tu archivo `.env`

## 🔧 Configuración

### Generar archivo de sesión

Antes de usar el userbot, debes generar el archivo de sesión:

```bash
python generate_session.py
```

Este comando:
- Te pedirá el código de verificación de Telegram (solo la primera vez)
- Creará un archivo `userbot_session.session`
- Evitará verificaciones futuras

## 🎯 Uso

### Iniciar el userbot

```bash
python userbot.py
```

### Comandos disponibles

- `/start` - Inicia el bot y muestra comandos disponibles
- `/enviar` - Inicia el proceso de envío masivo
- `/confirmar` - Confirma el envío del mensaje
- `/cancelar` - Cancela la operación actual

### Flujo de uso

1. **Iniciar**: Envía `/start` al userbot
2. **Enviar**: Usa `/enviar` para iniciar el proceso
3. **Escribir**: Envía el mensaje que quieres distribuir
4. **Confirmar**: Revisa la vista previa y usa `/confirmar`
5. **Esperar**: El bot enviará el mensaje a todos los grupos
6. **Revisar**: Recibirás estadísticas finales

## 📊 Características del envío

- **Filtrado inteligente**: Solo envía a grupos donde tengas permisos
- **Manejo de errores**: Detecta grupos donde no puedes escribir
- **Protección anti-flood**: Respeta las limitaciones de Telegram
- **Progreso en tiempo real**: Actualizaciones cada 5 grupos
- **Reporte detallado**: Estadísticas completas al finalizar

## ⚠️ Advertencias importantes

- **Uso responsable**: No abuses del envío masivo
- **Respeto a grupos**: Solo envía contenido apropiado
- **Limitaciones de Telegram**: Respeta las políticas de la plataforma
- **Permisos**: Solo funciona en grupos donde tengas permisos de escritura

## 🛠️ Solución de problemas

### Error de configuración
```
❌ Error: Faltan variables de configuración
```
**Solución**: Verifica que tu archivo `.env` esté configurado correctamente.

### Error de conexión
```
❌ Error durante la generación de sesión
```
**Soluciones**:
1. Verifica tu conexión a internet
2. Confirma que API_ID y API_HASH sean correctos
3. Asegúrate de que el número de teléfono esté en formato internacional

### Error de autorización
```
❌ Error: No se pudo autorizar la sesión
```
**Solución**: Ejecuta `python generate_session.py` nuevamente y sigue las instrucciones.

## 📁 Estructura del proyecto

```
userbot-telegram/
├── userbot.py              # Script principal del userbot
├── generate_session.py     # Generador de sesión
├── config.py              # Configuración
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
└── .env                   # Variables de entorno (crear tú)
```

## 🔒 Seguridad

- El archivo `.session` contiene información sensible
- No compartas tu archivo `.session` con nadie
- Mantén seguras tus credenciales de API
- Usa el userbot de forma responsable

## 📞 Soporte

Si tienes problemas:
1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Confirma que tu configuración sea correcta

## 📄 Licencia

Este proyecto es para uso educativo y personal. Úsalo de forma responsable y respeta las políticas de Telegram. 