import csv
import os
from datetime import datetime

TICKETS_FILE = "tickets.csv"


# Agrega un ticket nuevo al csv y lo devuelve
def _generar_ticket(cliente_id, problema):
    existe = os.path.exists(TICKETS_FILE)

    cantidad = 0
    if existe:
        with open(TICKETS_FILE, encoding="utf-8") as archivo:
            cantidad = sum(1 for _ in csv.DictReader(archivo))

    ticket = {
        "id": str(cantidad + 1),
        "cliente_id": cliente_id,
        "problema": problema,
        "estado": "abierto",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    with open(TICKETS_FILE, "a", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=ticket.keys())
        if not existe:
            escritor.writeheader()
        escritor.writerow(ticket)

    return ticket


# Busca en el csv los tickets de un cliente y los devuelve como texto
def _ver_tickets(cliente_id):
    if not os.path.exists(TICKETS_FILE):
        return "No tiene tickets registrados."

    with open(TICKETS_FILE, encoding="utf-8") as archivo:
        tickets = list(csv.DictReader(archivo))

    mios = [t for t in tickets if t["cliente_id"] == cliente_id]

    if not mios:
        return "No tiene tickets registrados."

    return "\n".join(
        f"N°{t['id']} | {t['problema']} | {t['estado']} | {t['fecha']}" for t in mios
    )
