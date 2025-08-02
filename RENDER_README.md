# ⚠️ IMPORTANTE: Este proyecto NO es para Render

## 🤖 **¿Qué es este proyecto?**

Este es un **UserBot de Telegram** que debe ejecutarse **localmente** en tu computadora. **NO es una aplicación web** que se pueda desplegar en Render.

## 🚀 **Cómo usar este proyecto:**

### **Instalación local:**
```bash
# 1. Clonar el repositorio
git clone https://github.com/XinhoGOD/TelegramRender.git
cd TelegramRender

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar credenciales
# Edita el archivo .env con tus datos de Telegram

# 4. Generar sesión
python generate_session.py

# 5. Ejecutar userbot
python userbot.py
```

## ❌ **¿Por qué no funciona en Render?**

- **UserBots de Telegram** necesitan acceso directo a tu cuenta
- Requieren **verificación manual** con códigos SMS
- Necesitan **archivos de sesión** locales
- **No son aplicaciones web**

## 🎯 **Plataformas compatibles:**

✅ **Local** - Tu computadora  
✅ **VPS** - Servidor privado  
✅ **Heroku** - Con configuración especial  
❌ **Render** - No compatible  

## 📋 **Para usar en Render (NO RECOMENDADO):**

Si insistes en usar Render, necesitarías:
1. Convertir el userbot en un bot web
2. Usar webhooks de Telegram
3. Configurar autenticación diferente
4. Modificar completamente la arquitectura

## 🔧 **Alternativas recomendadas:**

### **1. Ejecutar localmente:**
```bash
python userbot.py
```

### **2. Usar un VPS:**
- DigitalOcean
- AWS EC2
- Google Cloud
- Azure

### **3. Heroku (con configuración especial):**
- Requiere buildpacks personalizados
- Configuración compleja

## 📞 **Soporte:**

Si necesitas ayuda para ejecutar el userbot localmente, consulta el `README.md` principal.

---

**Este repositorio está en GitHub solo para compartir el código, NO para desplegar en Render.** 