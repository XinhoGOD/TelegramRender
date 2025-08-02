# 🚀 Guía para desplegar en Render

## 📋 **Cómo funciona el "truco":**

Render requiere que los Web Services respondan a peticiones HTTP para mantenerse activos. Nuestro userbot ahora:

1. **Ejecuta el userbot** en segundo plano
2. **Sirve una API web** para health checks
3. **Mantiene el servicio activo** en el plan gratuito

## 🔧 **Configuración en Render:**

### **1. Crear nuevo Web Service:**
- Ve a [render.com](https://render.com)
- Crea un nuevo **Web Service**
- Conecta tu repositorio de GitHub

### **2. Configurar variables de entorno:**
En Render, agrega estas variables:
```
API_ID=22252541
API_HASH=91c195d7de...
PHONE_NUMBER=+525667766556
SESSION_STRING=1AZWarzkBu5IqmqM7a6l2qEVb3SfXTXTaZ0oN3EdBvsAP_AQW5dD2wq0-LFkLaEr3dtzyK5kaUhKz45XbGQhUlGpHoVadTsucPuJDiBfw...
```

### **3. Configurar el servicio:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python render_web_service.py`
- **Plan**: Free

## 🌐 **Endpoints disponibles:**

### **Página principal:**
- `https://tu-app.onrender.com/` - Estado del servicio

### **Health check:**
- `https://tu-app.onrender.com/health` - Para Render

### **Estado del userbot:**
- `https://tu-app.onrender.com/status` - Verificar configuración

### **Control manual:**
- `https://tu-app.onrender.com/start` - Iniciar userbot
- `https://tu-app.onrender.com/stop` - Detener userbot

## ✅ **Ventajas de Render:**

- ✅ **Plan gratuito** disponible
- ✅ **Sin problemas** de permisos
- ✅ **Health checks** automáticos
- ✅ **Logs detallados**
- ✅ **Reinicio automático** si falla

## ⚠️ **Importante:**

- **Render puede dormir** el servicio si no recibe tráfico
- **El userbot se reinicia** automáticamente
- **Los logs** están disponibles en Render
- **El servicio** responde a peticiones HTTP

## 🎯 **Después del despliegue:**

1. **Verifica** que el servicio esté "Live"
2. **Revisa los logs** para confirmar conexión
3. **Prueba los endpoints** para verificar funcionamiento
4. **Envía mensajes** al userbot para probar

¡Render es mucho más confiable que Railway para este tipo de proyectos! 🚀 