from contantes import PROBLEMAS
from tickets import _generar_ticket


# Guarda los chats que estan elegiendo el tipo de problema
esperando_problema = set()

# Armamos el texto del menu a partir de PROBLEMAS, para no repetir la lista
MENU_PROBLEMAS = "Tipo de problema:\n" + "\n".join(
    f"{numero}. {nombre}" for numero, nombre in PROBLEMAS.items()
)


def _problemas(message, cliente_id, bot, MENU):
    chat_id = message.chat.id

    if chat_id not in esperando_problema:
        esperando_problema.add(chat_id)
        bot.send_message(chat_id, MENU_PROBLEMAS)
        return

    # Validamos la opcion
    if message.text in PROBLEMAS:
        ticket = _generar_ticket(cliente_id, PROBLEMAS[message.text])
        esperando_problema.discard(chat_id)
        bot.send_message(
            chat_id, f"Ticket N°{ticket['id']} generado.\n{ticket['problema']} - {ticket['fecha']}")
        bot.send_message(chat_id, MENU)
    else:
        bot.send_message(chat_id, "Opcion invalida.\n\n" + MENU_PROBLEMAS)
