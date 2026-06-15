from auxiliares import clientes, enviar
from contantes import MENU


def _consultar_saldo(chat_id, s):
    c = clientes[s["cliente_id"]]
    respuesta = (
        f"{c['nombre']} | Plan: {c['plan']}\n"
        f"Saldo: ${c['saldo']:.2f} | Deuda: ${c['deuda']:.2f}\n"
        f"Estado: {c['estado_cuenta'].upper()}"
    )

    # Gateway 4 — advertencia segun estado de cuenta
    if   c["estado_cuenta"] == "suspendido": respuesta += "\n\nServicio suspendido. Llame al 0800-555-INET."
    elif c["estado_cuenta"] == "moroso":      respuesta += "\n\nRegularice su deuda para evitar la suspension."

    enviar(chat_id, respuesta)
    enviar(chat_id, MENU)
