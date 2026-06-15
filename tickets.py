import json
import os
from datetime import datetime

from auxiliares import BASE_DIR, enviar
from contantes import MENU, PROBLEMAS

TICKETS_FILE = os.path.join(BASE_DIR, "tickets.json")
if os.path.exists(TICKETS_FILE):
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        tickets = json.load(f)
else:
    tickets = []


def _elegir_problema(chat_id, texto, s):
    if texto not in PROBLEMAS: enviar(chat_id, "Opcion invalida (1-4)."); return

    cliente_id = s["cliente_id"]

    # Gateway 3 — evita ticket duplicado abierto
    duplicado = next(
        (t for t in tickets if t["cliente_id"] == cliente_id
         and t["problema"] == PROBLEMAS[texto] and t["estado"] == "abierto"), None
    )
    if duplicado:
        enviar(chat_id, f"Ya tiene un ticket abierto N°{duplicado['id']} para ese problema.")
    else:
        nuevo = {
            "id":         len(tickets) + 1,
            "cliente_id": cliente_id,
            "problema":   PROBLEMAS[texto],
            "estado":     "abierto",
            "fecha":      datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        tickets.append(nuevo)
        with open(TICKETS_FILE, "w", encoding="utf-8") as f:
            json.dump(tickets, f, ensure_ascii=False, indent=2)
        enviar(chat_id, f"Ticket N°{nuevo['id']} generado.\n{nuevo['problema']} - {nuevo['fecha']}")

    s["estado"] = "menu"
    enviar(chat_id, MENU)


def _ver_tickets(chat_id, s):
    mis = [t for t in tickets if t["cliente_id"] == s["cliente_id"]]

    # Gateway 5 — ¿tiene tickets registrados?
    if not mis:
        enviar(chat_id, "No tiene tickets registrados.")
    else:
        enviar(chat_id, "\n".join(
            f"N°{t['id']} | {t['problema']} | {t['estado']} | {t['fecha']}" for t in mis
        ))

    enviar(chat_id, MENU)
