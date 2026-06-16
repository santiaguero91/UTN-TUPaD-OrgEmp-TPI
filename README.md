# Trabajo Practico Integrador
## Organización Empresarial

**Alumnos:** Santiago Aguero y Liam Saez

Tecnicatura Universitaria en Programación - Universidad Tecnológica Nacional.

---

Bot de Telegram de soporte técnico que automatiza la gestión de atencion al cliente, consulta de saldo, gestion de ticklets y reporte de problemas técnicos.

---

Para poner en funcionamiento el bot se requiere tener instalado Python 3.x y las siguientes dependencias:
- pyTelegramBotAPI
- python-dotenv


Además, es necesario un archivo `.env` con la variable:

```
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

Este token es provisto por BotFather de Telegram al crear un bot. Una vez configurado el entorno, el bot se inicia ejecutando el comando `python index.py` en la carpeta raíz del proyecto.

Para inicializar el bot el primer mensaje a mandar al bot es `/start`
