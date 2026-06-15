from auxiliares import bot, clientes, enviar, sesion, sesiones, validar_cliente
from contantes import MENU, P_CLIENTE
from consultar import _consultar_saldo
from tickets import _elegir_problema, _ver_tickets


def _pedir_cliente(chat_id, texto, s):
    if not validar_cliente(chat_id, texto): return

    s["cliente_id"] = texto
    s["estado"] = "menu"
    cliente = clientes[texto]
    enviar(chat_id, f"Hola {cliente['nombre']}!\n\n{MENU}")


def _menu(chat_id, texto, s):
    if   texto == "1": _reportar_problema(chat_id, s)
    elif texto == "2": _consultar_saldo(chat_id, s)
    elif texto == "3": _ver_tickets(chat_id, s)
    else: enviar(chat_id, "Opcion invalida. Ingrese 1, 2 o 3.")


def _reportar_problema(chat_id, s):
    cliente = clientes[s["cliente_id"]]

    # Gateway 1 — cuenta suspendida: bloquea el ticket
    if cliente["estado_cuenta"] == "suspendido":
        enviar(chat_id, f"Cuenta SUSPENDIDA (deuda: ${cliente['deuda']:.2f}). Llame al 0800-555-INET.")
        return

    # Gateway 2 — cuenta morosa: aviso pero puede continuar
    if cliente["estado_cuenta"] == "moroso":
        enviar(chat_id, f"ATENCION: deuda pendiente de ${cliente['deuda']:.2f}.")

    s["estado"] = "elegir_problema"
    enviar(chat_id, "Tipo de problema:\n1. Sin internet\n2. Internet lento\n3. Router apagado\n4. Falla intermitente")


# ── Dispatcher ────────────────────────────────────────────────────
HANDLERS = {
    "pedir_cliente":  _pedir_cliente,
    "menu":           _menu,
    "elegir_problema": _elegir_problema,
}

# ── Comandos /start y /menu ───────────────────────────────────────
@bot.message_handler(commands=["start", "menu"])
def cmd_inicio(msg):
    sesiones[msg.chat.id] = {"estado": "pedir_cliente", "cliente_id": None}
    enviar(msg.chat.id, P_CLIENTE)

# ── Handler principal ─────────────────────────────────────────────
@bot.message_handler(func=lambda _: True)
def handle(msg):
    chat_id = msg.chat.id
    texto   = msg.text.strip()
    s       = sesion(chat_id)

    if texto.upper() in ("MENU", "/MENU") and s["cliente_id"] is not None:
        s["estado"] = "menu"
        enviar(chat_id, MENU)
        return

    handler = HANDLERS.get(s["estado"])
    if handler:
        handler(chat_id, texto, s)

# ── Iniciar bot ───────────────────────────────────────────────────
print("Bot corriendo... Presiona Ctrl+C para detener.")
bot.polling()
