import time
import os

from mochila_tradicional import leer_mochila, mochila_tradicional
from mochila_alternativo import mochila_alternativo

TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 1000]
REPETICIONES = 3

ARCHIVO_TRADICIONAL = "res_tradicional.txt"
ARCHIVO_ALTERNATIVO = "res_alternativo.txt"

def medir_tiempo(algoritmo, elementos, capacidad):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        algoritmo(elementos, capacidad)
        tiempos.append(time.perf_counter() - inicio)
    return sum(tiempos) / REPETICIONES

def guardar_resultados(nombre_archivo, nombre_algoritmo, resultados):
    with open(nombre_archivo, "w") as archivo:
        archivo.write("Resultados - Problema 3: Programación Dinámica\n")
        archivo.write("Algoritmo: " + nombre_algoritmo + "\n")
        archivo.write("Repeticiones por instancia: " + str(REPETICIONES) + "\n")
        archivo.write("Tiempo medido: solamente ejecución del algoritmo\n")
        archivo.write("-" * 75 + "\n")
        archivo.write("{:<10} {:<15} {:<20} {:<20}\n".format(
            "n", "Capacidad", "Beneficio Total", "Tiempo Promedio (s)"
        ))
        archivo.write("-" * 75 + "\n")
        for n, capacidad, beneficio_total, tiempo in resultados:
            archivo.write("{:<10} {:<15} {:<20} {:<20.6f}\n".format(
                n, capacidad, beneficio_total, tiempo
            ))

def main():
    resultados_tradicional = []
    resultados_alternativo = []
    
    dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_mochilas = os.path.join(dir_base, "Mochilas")

    print("Midiendo tiempos de Programación Dinámica...")
    for n in TAMANIOS:
        ruta = os.path.join(dir_mochilas, f"mochila{n}.txt")
        if not os.path.exists(ruta):
            print(f"Aviso: No se encontró {ruta}. Saltando...")
            continue

        capacidad, elementos = leer_mochila(ruta)
        beneficio_total = sum(beneficio for peso, beneficio in elementos)
        
        tiempo_tradicional = medir_tiempo(mochila_tradicional, elementos, capacidad)
        tiempo_alternativo = medir_tiempo(mochila_alternativo, elementos, capacidad)

        resultados_tradicional.append((n, capacidad, beneficio_total, tiempo_tradicional))
        resultados_alternativo.append((n, capacidad, beneficio_total, tiempo_alternativo))
        print(f"n = {n:4d} medido.")

    guardar_resultados(ARCHIVO_TRADICIONAL, "Mochila tradicional", resultados_tradicional)
    guardar_resultados(ARCHIVO_ALTERNATIVO, "Mochila alternativo", resultados_alternativo)
    print("Resultados y tiempos guardados exitosamente.")

if __name__ == "__main__":
    main()