import json
import os
import telebot
from dotenv import load_dotenv

from contantes import P_DIGITOS, P_NO_CLIENTE

# ── Token del bot (obtenelo con @BotFather en Telegram) ──────────
load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

# ── Base de datos simulada ────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "clientes.json"), "r", encoding="utf-8") as f:
    clientes = json.load(f)

# ── Sesiones por usuario (maquina de estados) ─────────────────────
sesiones = {}

def sesion(chat_id):
    if chat_id not in sesiones:
        sesiones[chat_id] = {"estado": "pedir_cliente", "cliente_id": None}
    return sesiones[chat_id]

def enviar(chat_id, texto):
    bot.send_message(chat_id, texto)

def validar_cliente(chat_id, texto):
    """Retorna True y setea datos si es valido; False y envia error si no."""
    if not texto.isdigit():           enviar(chat_id, P_DIGITOS);    return False
    if texto not in clientes:         enviar(chat_id, P_NO_CLIENTE); return False
    return True
