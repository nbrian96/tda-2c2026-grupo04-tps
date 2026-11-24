import os
import random
import sys

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_TP02 = os.path.normpath(os.path.join(DIR_ACTUAL, ".."))
if DIR_TP02 not in sys.path:
    sys.path.insert(0, DIR_TP02)

from Problema_02.datos import leer_mochila  # noqa: E402


def mochila_randomizada(elementos, capacidad, iteraciones=50, ventana=3, semilla=42):
    """Resuelve Mochila 0-1 mediante Greedy aleatorizado con ventana y multi-arranque (Monte Carlo)."""
    if capacidad < 0:
        raise ValueError("La capacidad debe ser mayor o igual a 0.")
    if iteraciones < 1:
        raise ValueError("La cantidad de iteraciones debe ser al menos 1.")
    if ventana < 1:
        raise ValueError("El tamaño de ventana debe ser al menos 1.")

    if capacidad == 0 or not elementos:
        return 0, 0, []

    candidatos = [(w, v) for w, v in elementos if 0 < w <= capacidad and v > 0]
    if not candidatos:
        return 0, 0, []

    candidatos.sort(key=lambda item: (item[1] / item[0], item[1]), reverse=True)
    n = len(candidatos)

    rng = random.Random(semilla)
    mejor_beneficio = 0
    mejor_peso = 0
    mejor_seleccion = []

    for _ in range(iteraciones):
        copia = candidatos[:]
        peso = 0
        beneficio = 0
        seleccion = []

        for i in range(n):
            limite = min(i + ventana - 1, n - 1)
            j = rng.randint(i, limite)
            copia[i], copia[j] = copia[j], copia[i]

            w, v = copia[i]
            if peso + w <= capacidad:
                seleccion.append((w, v))
                peso += w
                beneficio += v

        if beneficio > mejor_beneficio:
            mejor_beneficio = beneficio
            mejor_peso = peso
            mejor_seleccion = seleccion

    return mejor_beneficio, mejor_peso, mejor_seleccion


def main():
    if len(sys.argv) < 2:
        print("Uso: python randomizado.py <ruta_instancia> [iteraciones] [ventana] [semilla]")
        sys.exit(1)

    ruta = sys.argv[1]
    iteraciones = int(sys.argv[2]) if len(sys.argv) >= 3 else 50
    ventana = int(sys.argv[3]) if len(sys.argv) >= 4 else 3
    semilla = int(sys.argv[4]) if len(sys.argv) >= 5 else 42

    capacidad, elementos = leer_mochila(ruta)
    beneficio, peso, seleccion = mochila_randomizada(
        elementos, capacidad, iteraciones=iteraciones, ventana=ventana, semilla=semilla
    )

    print(f"Instancia:   {ruta}")
    print(f"Capacidad:   {capacidad}")
    print(f"Ítems total: {len(elementos)}")
    print(f"Parámetros:  T={iteraciones}, ventana={ventana}, semilla={semilla}")
    print(f"Beneficio:   {beneficio}")
    print(f"Peso usado:  {peso}")
    print(f"Elegidos:    {len(seleccion)}")


if __name__ == "__main__":
    main()
