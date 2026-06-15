import csv

# Cargo los clientes del csv en un diccionario, usando el id como clave
clientes = {}
with open("clientes.csv", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        clientes[fila["id"]] = fila
