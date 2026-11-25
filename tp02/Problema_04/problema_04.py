import csv
import os
import sys
import time

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_TP02 = os.path.normpath(os.path.join(DIR_ACTUAL, ".."))
DIR_P1 = os.path.join(DIR_TP02, "Problema_01")
DIR_P2 = os.path.join(DIR_TP02, "Problema_02")
for ruta in (DIR_TP02, DIR_P1, DIR_P2):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

from Problema_01.cotas import calcular_cota_martello_toth, calcular_cota_relajacion_lineal  # noqa: E402
from Problema_01.items import crear_y_ordenar_items  # noqa: E402
from Problema_01.sahni import algoritmo_sahni  # noqa: E402
from Problema_02.datos import DIR_MOCHILAS, leer_mochila  # noqa: E402
from Problema_02.fptas import mochila_fptas  # noqa: E402
from mochila_tradicional import mochila_tradicional
from Problema_03.greedy import resolver_mochila_greedy  # noqa: E402
from Problema_03.randomizado import mochila_randomizada  # noqa: E402
from Problema_04.algoritmos_tp1 import (  # noqa: E402
    resolver_backtracking,
    resolver_fuerza_bruta,
    resolver_programacion_lineal,
)

DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")

TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 1000]
EPSILON_FPTAS = 0.5
K_SAHNI = 1
RAND_ITERACIONES = 50
RAND_VENTANA = 3
RAND_SEMILLA = 42

COLUMNAS_TIEMPOS = [
    "n",
    "capacidad",
    "fuerza_bruta_s",
    "backtracking_s",
    "greedy_s",
    "pd_tradicional_s",
    "programacion_lineal_s",
    "sahni_k1_s",
    "fptas_eps05_s",
    "randomizado_s",
]

COLUMNAS_APROX = [
    "n",
    "capacidad",
    "optimo_pd",
    "greedy",
    "sahni_k1",
    "fptas_eps05",
    "randomizado",
    "cota_mt_u2",
    "cota_rl_u1",
    "rl_continua",
]


def medir_promedio(funcion, *args, repeticiones=1):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        tiempos.append(time.perf_counter() - inicio)
    return resultado, sum(tiempos) / repeticiones


def medir_sahni_completo(beneficios, pesos, capacidad, k, repeticiones=3):
    tiempos = []
    benef = 0
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        items_ord = crear_y_ordenar_items(beneficios, pesos)
        benef, _ = algoritmo_sahni(items_ord, capacidad, k)
        tiempos.append(time.perf_counter() - inicio)
    return benef, sum(tiempos) / repeticiones


def main():
    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    filas_tiempos = []
    filas_aprox = []

    print(
        f"{'n':<5} | {'FB(s)':<9} | {'BT(s)':<9} | {'Greedy(s)':<9} | {'PD(s)':<9} | "
        f"{'PL(s)':<9} | {'Sahni(s)':<9} | {'FPTAS(s)':<9} | {'Rand(s)':<9}"
    )
    print("-" * 97)

    for n in TAMANIOS:
        ruta = os.path.join(DIR_MOCHILAS, f"mochila{n}.txt")
        capacidad, elementos = leer_mochila(ruta)
        pesos = [w for w, _ in elementos]
        beneficios = [v for _, v in elementos]

        # 1. Exactos: PD tradicional y Programación Lineal (todos los tamaños)
        reps_pd = 3 if n <= 100 else 1
        opt_pd, t_pd = medir_promedio(mochila_tradicional, elementos, capacidad, repeticiones=reps_pd)

        (opt_pl, peso_pl), t_pl = medir_promedio(
            resolver_programacion_lineal, elementos, capacidad, repeticiones=1
        )
        assert opt_pl == opt_pd and peso_pl <= capacidad, f"PL difiere de PD en n={n}"

        # 2. Exactos exponenciales: Fuerza Bruta (n <= 25) y Backtracking (n <= 40)
        t_fb_str = ""
        if n <= 25:
            reps_fb = 3 if n <= 15 else 1
            (opt_fb, peso_fb), t_fb = medir_promedio(
                resolver_fuerza_bruta, elementos, capacidad, repeticiones=reps_fb
            )
            assert opt_fb == opt_pd and peso_fb <= capacidad, f"FB difiere de PD en n={n}"
            t_fb_str = f"{t_fb:.6f}"

        t_bt_str = ""
        if n <= 40:
            reps_bt = 3 if n <= 25 else 1
            (opt_bt, peso_bt), t_bt = medir_promedio(
                resolver_backtracking, elementos, capacidad, repeticiones=reps_bt
            )
            assert opt_bt == opt_pd and peso_bt <= capacidad, f"BT difiere de PD en n={n}"
            t_bt_str = f"{t_bt:.6f}"

        # 3. Aproximados y Randomizado
        (val_greedy, peso_greedy), t_greedy = medir_promedio(
            resolver_mochila_greedy, elementos, capacidad, repeticiones=5
        )
        val_sahni, t_sahni = medir_sahni_completo(beneficios, pesos, capacidad, K_SAHNI, repeticiones=3)
        (val_rand, peso_rand, _), t_rand = medir_promedio(
            mochila_randomizada,
            elementos,
            capacidad,
            RAND_ITERACIONES,
            RAND_VENTANA,
            RAND_SEMILLA,
            repeticiones=5,
        )

        val_fptas_str = ""
        t_fptas_str = ""
        if n <= 200:
            reps_fptas = 3 if n <= 100 else 1
            (val_fptas, peso_fptas), t_fptas = medir_promedio(
                mochila_fptas, elementos, capacidad, EPSILON_FPTAS, repeticiones=reps_fptas
            )
            assert peso_fptas <= capacidad and val_fptas <= opt_pd, f"FPTAS inválido en n={n}"
            val_fptas_str = str(val_fptas)
            t_fptas_str = f"{t_fptas:.6f}"

        # 4. Cotas RL (U1) y Martello-Toth (U2)
        items_ord = crear_y_ordenar_items(beneficios, pesos)
        z_cont, u1 = calcular_cota_relajacion_lineal(items_ord, capacidad)
        u2 = calcular_cota_martello_toth(items_ord, capacidad)

        assert peso_greedy <= capacidad and val_greedy <= opt_pd <= u2 <= u1
        assert val_sahni <= opt_pd <= u2 <= u1
        assert peso_rand <= capacidad and val_rand <= opt_pd <= u2 <= u1

        filas_tiempos.append(
            {
                "n": n,
                "capacidad": capacidad,
                "fuerza_bruta_s": t_fb_str,
                "backtracking_s": t_bt_str,
                "greedy_s": f"{t_greedy:.6f}",
                "pd_tradicional_s": f"{t_pd:.6f}",
                "programacion_lineal_s": f"{t_pl:.6f}",
                "sahni_k1_s": f"{t_sahni:.6f}",
                "fptas_eps05_s": t_fptas_str,
                "randomizado_s": f"{t_rand:.6f}",
            }
        )

        filas_aprox.append(
            {
                "n": n,
                "capacidad": capacidad,
                "optimo_pd": opt_pd,
                "greedy": val_greedy,
                "sahni_k1": val_sahni,
                "fptas_eps05": val_fptas_str,
                "randomizado": val_rand,
                "cota_mt_u2": u2,
                "cota_rl_u1": u1,
                "rl_continua": f"{z_cont:.2f}",
            }
        )

        print(
            f"{n:<5} | {t_fb_str or '-':<9} | {t_bt_str or '-':<9} | {t_greedy:<9.6f} | {t_pd:<9.6f} | "
            f"{t_pl:<9.6f} | {t_sahni:<9.6f} | {t_fptas_str or '-':<9} | {t_rand:<9.6f}"
        )

    ruta_tiempos = os.path.join(DIR_RESULTADOS, "comparacion_tiempos.csv")
    with open(ruta_tiempos, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_TIEMPOS)
        writer.writeheader()
        writer.writerows(filas_tiempos)

    ruta_aprox = os.path.join(DIR_RESULTADOS, "comparacion_aproximados_cotas.csv")
    with open(ruta_aprox, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_APROX)
        writer.writeheader()
        writer.writerows(filas_aprox)

    print("\nArchivos guardados en:", DIR_RESULTADOS)


if __name__ == "__main__":
    main()
