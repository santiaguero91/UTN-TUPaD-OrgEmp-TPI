from auxiliares import clientes

# Checkear el csv por el id y muestra sus datos
def _consultar_saldo(cliente_id):
    c = clientes[cliente_id]

    respuesta = (
        f"{c['nombre']} | Plan: {c['plan']}\n"
        f"Saldo: ${float(c['saldo']):.2f} | Deuda: ${float(c['deuda']):.2f}\n"
        f"Estado: {c['estado_cuenta'].upper()}"
    )

    if c["estado_cuenta"] == "suspendido":
        respuesta += "\n\nServicio suspendido. Llame al 0800-555-INET."
    elif c["estado_cuenta"] == "moroso":
        respuesta += "\n\nRegularice su deuda para evitar la suspension."

    return respuesta
