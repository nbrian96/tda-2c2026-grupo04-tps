import csv
import os
import sys
import time

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_TP02 = os.path.normpath(os.path.join(DIR_ACTUAL, ".."))
if DIR_TP02 not in sys.path:
    sys.path.insert(0, DIR_TP02)

from Problema_02.datos import DIR_MOCHILAS, leer_mochila  # noqa: E402
from mochila_tradicional import mochila_tradicional  # noqa: E402
from Problema_03.greedy import resolver_mochila_greedy  # noqa: E402
from Problema_03.randomizado import mochila_randomizada  # noqa: E402

DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")

TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 1000]
ITERACIONES = 50
VENTANA = 3
SEMILLA = 42
REPETICIONES_RAPIDOS = 5

COLUMNAS = [
    "n",
    "capacidad",
    "beneficio_rand",
    "peso_rand",
    "beneficio_greedy",
    "peso_greedy",
    "optimo_pd",
    "pct_optimo_rand",
    "pct_optimo_greedy",
    "gap_rand",
    "gap_greedy",
    "mejora_vs_greedy",
    "tiempo_rand_s",
    "tiempo_greedy_s",
    "tiempo_pd_s",
]


def medir_promedio(funcion, *args, repeticiones=5):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        tiempos.append(time.perf_counter() - inicio)
    return resultado, sum(tiempos) / repeticiones


def main():
    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    filas = []

    print(
        f"{'n':<5} | {'W':<6} | {'Rand':<7} | {'Greedy':<7} | {'Opt PD':<7} | "
        f"{'%Rand':<7} | {'%Grdy':<7} | {'t_rand(s)':<10} | {'t_grdy(s)':<10} | {'t_pd(s)':<10}"
    )
    print("-" * 98)

    for n in TAMANIOS:
        ruta = os.path.join(DIR_MOCHILAS, f"mochila{n}.txt")
        capacidad, elementos = leer_mochila(ruta)

        (benef_rand, peso_rand, _), t_rand = medir_promedio(
            mochila_randomizada,
            elementos,
            capacidad,
            ITERACIONES,
            VENTANA,
            SEMILLA,
            repeticiones=REPETICIONES_RAPIDOS,
        )
        (benef_greedy, peso_greedy), t_greedy = medir_promedio(
            resolver_mochila_greedy,
            elementos,
            capacidad,
            repeticiones=REPETICIONES_RAPIDOS,
        )

        reps_pd = 3 if n <= 100 else 1
        optimo_pd, t_pd = medir_promedio(
            mochila_tradicional,
            elementos,
            capacidad,
            repeticiones=reps_pd,
        )

        assert peso_rand <= capacidad, f"Peso randomizado excedido en n={n}"
        assert benef_rand <= optimo_pd, f"Beneficio randomizado mayor al óptimo en n={n}"
        assert peso_greedy <= capacidad, f"Peso greedy excedido en n={n}"
        assert benef_greedy <= optimo_pd, f"Beneficio greedy mayor al óptimo en n={n}"

        pct_rand = (benef_rand / optimo_pd * 100.0) if optimo_pd > 0 else 100.0
        pct_greedy = (benef_greedy / optimo_pd * 100.0) if optimo_pd > 0 else 100.0
        gap_rand = (optimo_pd - benef_rand) / optimo_pd if optimo_pd > 0 else 0.0
        gap_greedy = (optimo_pd - benef_greedy) / optimo_pd if optimo_pd > 0 else 0.0
        mejora = benef_rand - benef_greedy

        filas.append(
            {
                "n": n,
                "capacidad": capacidad,
                "beneficio_rand": benef_rand,
                "peso_rand": peso_rand,
                "beneficio_greedy": benef_greedy,
                "peso_greedy": peso_greedy,
                "optimo_pd": optimo_pd,
                "pct_optimo_rand": round(pct_rand, 4),
                "pct_optimo_greedy": round(pct_greedy, 4),
                "gap_rand": round(gap_rand, 6),
                "gap_greedy": round(gap_greedy, 6),
                "mejora_vs_greedy": mejora,
                "tiempo_rand_s": round(t_rand, 6),
                "tiempo_greedy_s": round(t_greedy, 6),
                "tiempo_pd_s": round(t_pd, 6),
            }
        )

        print(
            f"{n:<5} | {capacidad:<6} | {benef_rand:<7} | {benef_greedy:<7} | {optimo_pd:<7} | "
            f"{pct_rand:<7.2f} | {pct_greedy:<7.2f} | {t_rand:<10.6f} | {t_greedy:<10.6f} | {t_pd:<10.6f}"
        )

    ruta_csv = os.path.join(DIR_RESULTADOS, "resultados_problema_03.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(filas)

    print("\nResultados guardados en:", ruta_csv)


if __name__ == "__main__":
    main()
