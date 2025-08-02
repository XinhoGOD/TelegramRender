# 🤖 TelegramRender - UserBot de Envío Masivo

Un userbot avanzado de Telegram que permite enviar mensajes a todos los grupos donde estés unido de forma masiva, con estadísticas detalladas y manejo inteligente de errores.

## ✨ Características Principales

- 🚀 **Envío masivo inteligente** a todos los grupos
- 📊 **Estadísticas detalladas** de éxitos y fallos
- 🔄 **Actualizaciones en tiempo real** del progreso
- 🛡️ **Manejo automático de errores** y limitaciones
- 📱 **Interfaz intuitiva** con comandos simples
- 💾 **Sesión persistente** (sin verificaciones repetidas)
- 🔒 **Seguridad garantizada** - solo envía tu mensaje específico

## 🎯 Funcionalidades

### Comandos Disponibles
- `/start` - Inicia el bot y muestra comandos
- `/enviar` - Inicia el proceso de envío masivo
- `/confirmar` - Confirma el envío del mensaje
- `/cancelar` - Cancela la operación actual

### Flujo de Uso
1. **Iniciar**: Envía `/start` al userbot
2. **Enviar**: Usa `/enviar` para iniciar el proceso
3. **Escribir**: Envía el mensaje que quieres distribuir
4. **Confirmar**: Revisa la vista previa y usa `/confirmar`
5. **Esperar**: El bot enviará el mensaje a todos los grupos
6. **Revisar**: Recibirás estadísticas finales

## 📋 Requisitos

- Python 3.7 o superior
- Cuenta de Telegram
- API ID y API Hash de Telegram

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/XinhoGOD/TelegramRender.git
cd TelegramRender
```

### 2. Instalación automática
```bash
python setup.py
```

### 3. Configurar credenciales
Edita el archivo `.env` con tus datos:
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

### 5. Generar sesión
```bash
python generate_session.py
```

### 6. Ejecutar userbot
```bash
python userbot.py
```

## 📁 Estructura del Proyecto

```
TelegramRender/
├── userbot.py              # Script principal del userbot
├── generate_session.py     # Generador de sesión
├── config.py              # Configuración
├── setup.py               # Instalador automático
├── upload_to_github.py    # Script para subir a GitHub
├── requirements.txt        # Dependencias
├── README.md              # Documentación completa
├── README_GITHUB.md       # Este archivo
├── .gitignore             # Archivos a ignorar
└── .env                   # Variables de entorno (crear tú)
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
# Configuración de Telegram API
API_ID=tu_api_id_aqui
API_HASH=tu_api_hash_aqui
PHONE_NUMBER=+34612345678
```

### Personalización
Puedes modificar `config.py` para cambiar:
- Nombre de la sesión
- Configuración de logging
- Parámetros de envío

## 📊 Características del Envío

- **Filtrado inteligente**: Solo envía a grupos donde tengas permisos
- **Manejo de errores**: Detecta grupos donde no puedes escribir
- **Protección anti-flood**: Respeta las limitaciones de Telegram
- **Progreso en tiempo real**: Actualizaciones cada 5 grupos
- **Reporte detallado**: Estadísticas completas al finalizar

## 🛡️ Seguridad

- ✅ **Solo tu mensaje**: El bot solo envía el mensaje que tú le diste
- ✅ **Control por usuario**: Cada usuario tiene su propio mensaje guardado
- ✅ **Confirmación requerida**: Necesitas `/confirmar` para enviar
- ✅ **Cancelación disponible**: Puedes `/cancelar` en cualquier momento
- ✅ **Archivos protegidos**: `.session` y `.env` están en `.gitignore`

## ⚠️ Advertencias Importantes

- **Uso responsable**: No abuses del envío masivo
- **Respeto a grupos**: Solo envía contenido apropiado
- **Limitaciones de Telegram**: Respeta las políticas de la plataforma
- **Permisos**: Solo funciona en grupos donde tengas permisos de escritura

## 🛠️ Solución de Problemas

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
**Solución**: Ejecuta `python generate_session.py` nuevamente.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es para uso educativo y personal. Úsalo de forma responsable y respeta las políticas de Telegram.

## 👨‍💻 Autor

**XinhoGOD** - [GitHub](https://github.com/XinhoGOD)

## 🙏 Agradecimientos

- [Telethon](https://github.com/LonamiWebs/Telethon) - Librería de Telegram
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Manejo de variables de entorno

## 📞 Soporte

Si tienes problemas:
1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Confirma que tu configuración sea correcta
4. Abre un issue en GitHub

---

⭐ **Si te gusta este proyecto, dale una estrella en GitHub!** 