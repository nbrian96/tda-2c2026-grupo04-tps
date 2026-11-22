import os
import time

from items import crear_y_ordenar_items
from cotas import calcular_cota_relajacion_lineal, calcular_cota_martello_toth
from sahni import algoritmo_sahni

from mochila_tradicional import mochila_tradicional

# Usamos los mismos tamaños que generaste en crear_mochila.py
TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 1000]
REPETICIONES = 3
K_SAHNI = 1  # Parámetro k de Sahni (con k=1 la complejidad es O(n^2) y garantía 1/2)


def leer_instancia_mochila(ruta_archivo):
    """
    Lee el formato de crear_mochila.py:
    Línea 1: capacidad
    Siguientes líneas: peso,beneficio
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        capacidad = int(archivo.readline().strip())
        pesos = []
        beneficios = []
        elementos_tuplas = []  # Para pasarle directo a mochila_tradicional del TP1

        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(",")
            w = int(partes[0])
            p = int(partes[1])

            pesos.append(w)
            beneficios.append(p)
            elementos_tuplas.append((w, p))

    return capacidad, pesos, beneficios, elementos_tuplas


def medir_sahni(items_ordenados, capacidad, k, repeticiones):
    """Ejecuta Sahni 'repeticiones' veces y devuelve el resultado y el tiempo promedio."""
    tiempos = []
    mejor_beneficio = 0
    ids_elegidos = []

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        mejor_beneficio, ids_elegidos = algoritmo_sahni(items_ordenados, capacidad, k)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    tiempo_promedio = sum(tiempos) / repeticiones
    return mejor_beneficio, ids_elegidos, tiempo_promedio


def main():
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    dir_mochilas = os.path.join(os.path.dirname(dir_actual), "Mochilas")
    ruta_salida = os.path.join(dir_actual, f"resultados_problema1_k{K_SAHNI}.txt")

    resultados = []

    print(f"Ejecutando Problema 1 (Sahni con k = {K_SAHNI})...\n")
    encabezado = (
        f"{'n':<6} | {'Cap.':<7} | {'Sahni':<10} | {'Óptimo (DP)':<12} | "
        f"{'Cota MT (U2)':<13} | {'Cota RL (U1)':<13} | {'Tiempo Sahni (s)':<16}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    for n in TAMANIOS:
        ruta_mochila = os.path.join(dir_mochilas, f"mochila{n}.txt")
        if not os.path.exists(ruta_mochila):
            print(f"Aviso: No se encontró {ruta_mochila}, se saltea.")
            continue

        capacidad, pesos, beneficios, elementos_tuplas = leer_instancia_mochila(ruta_mochila)

        # 1. Preparamos y ordenamos los ítems por p_j / w_j (incluido en el tiempo de Sahni)
        t_ord_ini = time.perf_counter()
        items_ord = crear_y_ordenar_items(beneficios, pesos)
        t_ord = time.perf_counter() - t_ord_ini

        # 2. Calculamos las dos cotas superiores
        z_continuo, u1 = calcular_cota_relajacion_lineal(items_ord, capacidad)
        u2 = calcular_cota_martello_toth(items_ord, capacidad)

        # 3. Calculamos Sahni y medimos su tiempo (ordenamiento + esquema S(k))
        val_sahni, _, t_sahni = medir_sahni(items_ord, capacidad, K_SAHNI, REPETICIONES)
        tiempo_total_sahni = t_ord + t_sahni

        # 4. Calculamos el óptimo exacto usando DP del TP1
        val_optimo = mochila_tradicional(elementos_tuplas, capacidad)

        resultados.append((n, capacidad, val_sahni, val_optimo, u2, u1, z_continuo, tiempo_total_sahni))

        print(
            f"{n:<6} | {capacidad:<7} | {val_sahni:<10} | {val_optimo:<12} | "
            f"{u2:<13} | {u1:<13} | {tiempo_total_sahni:<16.6f}"
        )

    # Guardamos los resultados en archivo para adjuntar en el ZIP de entrega
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(f"Resultados - Problema 1: Algoritmo de Sahni (k = {K_SAHNI})\n")
        f.write("-" * 95 + "\n")
        f.write(
            f"{'n':<6} {'Capacidad':<10} {'Sahni':<10} {'Optimo':<10} "
            f"{'Cota_MT_U2':<12} {'Cota_RL_U1':<12} {'RL_Continua':<13} {'Tiempo_s':<12}\n"
        )
        f.write("-" * 95 + "\n")
        for r in resultados:
            f.write(
                f"{r[0]:<6} {r[1]:<10} {r[2]:<10} {r[3]:<10} "
                f"{r[4]:<12} {r[5]:<12} {r[6]:<13.2f} {r[7]:<12.6f}\n"
            )

    print(f"\nTabla de resultados guardada en: {ruta_salida}")


if __name__ == "__main__":
    main()