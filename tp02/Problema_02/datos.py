import os
import random

SEMILLA = 42
TAMANIOS_INTERMEDIOS = [60, 80, 120, 150, 180]

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_MOCHILAS = os.path.normpath(os.path.join(DIR_ACTUAL, "..", "Mochilas"))
DIR_INTERMEDIOS = os.path.join(DIR_ACTUAL, "sets_datos", "intermedios")


def leer_mochila(ruta):
    elementos = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().strip()
        if not primera_linea:
            raise ValueError("El archivo de instancia esta vacio.")
        capacidad = int(primera_linea)
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            peso, beneficio = linea.split(",")
            elementos.append((int(peso), int(beneficio)))
    return capacidad, elementos


def obtener_ruta_instancia(n):
    if n in TAMANIOS_INTERMEDIOS:
        return os.path.join(DIR_INTERMEDIOS, f"mochila{n}.txt")
    return os.path.join(DIR_MOCHILAS, f"mochila{n}.txt")


def generar_intermedios():
    os.makedirs(DIR_INTERMEDIOS, exist_ok=True)
    for n in TAMANIOS_INTERMEDIOS:
        random.seed(SEMILLA + n)
        capacidad = n * 50
        ruta = os.path.join(DIR_INTERMEDIOS, f"mochila{n}.txt")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(f"{capacidad}\n")
            for _ in range(n):
                peso = random.randint(1, 200)
                beneficio = random.randint(1, 1000)
                archivo.write(f"{peso},{beneficio}\n")


if __name__ == "__main__":
    generar_intermedios()
    print("Sets intermedios generados en:", DIR_INTERMEDIOS)
