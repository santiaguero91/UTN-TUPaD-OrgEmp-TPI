import os

import telebot
from dotenv import load_dotenv

from auxiliares import clientes
from consultar import _consultar_saldo
from problemas import _problemas, esperando_problema
from tickets import _ver_tickets

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Guarda que cliente esta identificado en cada chat
sesiones = {}

# Inicio de aplicacion cuando el bot recibe el comando /start
# Solicita el numero de cliente


@bot.message_handler(commands=['start'])
def start(message):

    # Reiniciamos el estado del chat para empezar de nuevo
    sesiones.pop(message.chat.id, None)
    esperando_problema.discard(message.chat.id)

    bot.send_message(message.chat.id, "Ingrese numero de cliente: ")

# Cuando recibe un comando distinto:


@bot.message_handler(func=lambda m: True)
def menu(message):
    MENU = (
        "=== SOPORTE TECNICO - INTERNETX ===\n\n"
        "1. Reportar problema\n"
        "2. Consultar saldo\n"
        "3. Ver mis tickets\n\n"
        "Escriba MENU en cualquier momento para volver aqui."
    )

    # Si todavia no se identifico, el mensaje debe ser su numero de cliente
    if message.chat.id not in sesiones:
        if message.text in clientes:
            sesiones[message.chat.id] = message.text
            bot.send_message(message.chat.id, MENU)
        else:
            bot.send_message(message.chat.id, "Cliente no encontrado")
        return
    # Si escribe MENU, limmpia esperando_problema y volvemos al inicio
    if message.text.upper() == "MENU":
        esperando_problema.discard(message.chat.id)
        bot.send_message(message.chat.id, MENU)
        return

    # Esto es necesario para que los ingresos no trigereen el menu nuevamente
    # sino  la funcion _problemas
    if message.chat.id in esperando_problema:
        _problemas(message, sesiones[message.chat.id], bot, MENU)
        return

    # Si ya esta identificado, el mensaje debe ser una opcion del menu
    if message.text == "1":
        _problemas(message, sesiones[message.chat.id], bot, MENU)
    elif message.text == "2":
        cliente_id = sesiones[message.chat.id]
        bot.send_message(message.chat.id, _consultar_saldo(cliente_id))
    elif message.text == "3":
        cliente_id = sesiones[message.chat.id]
        bot.send_message(message.chat.id, _ver_tickets(cliente_id))
    else:
        bot.send_message(message.chat.id, "Opcion invalida.")


print("Bot corriendo... Presiona Ctrl+C para detener.")
bot.infinity_polling()
