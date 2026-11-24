import csv
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_TP02 = os.path.normpath(os.path.join(DIR_ACTUAL, ".."))
if DIR_TP02 not in sys.path:
    sys.path.insert(0, DIR_TP02)

from Problema_02.graficar_problema_02 import ajustar_curva  # noqa: E402

DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")
DIR_GRAFICOS = os.path.join(DIR_ACTUAL, "graficos")
ITERACIONES = 50


def leer_resultados():
    ruta = os.path.join(DIR_RESULTADOS, "resultados_problema_03.csv")
    filas = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        for row in csv.DictReader(archivo):
            filas.append(
                {
                    "n": int(row["n"]),
                    "pct_rand": float(row["pct_optimo_rand"]),
                    "pct_greedy": float(row["pct_optimo_greedy"]),
                    "t_rand": float(row["tiempo_rand_s"]),
                    "t_greedy": float(row["tiempo_greedy_s"]),
                    "t_pd": float(row["tiempo_pd_s"]),
                }
            )
    return filas


def graficar_ajuste_randomizado(filas):
    ns = [f["n"] for f in filas]
    tiempos = [f["t_rand"] for f in filas]
    teoricos = [n * math.log2(n) + ITERACIONES * n for n in ns]
    c, ajustados, r2 = ajustar_curva(teoricos, tiempos)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, tiempos, marker="o", color="#1f77b4", linewidth=2, label="Tiempo real (Randomizado)")
    ax.plot(
        ns,
        ajustados,
        linestyle="--",
        color="#d62728",
        linewidth=2,
        label=f"Ajuste teórico O(n log n + T·n) (R²={r2:.4f})",
    )
    ax.set_xlabel("Cantidad de ítems (n)")
    ax.set_ylabel("Tiempo promedio de ejecución (s)")
    ax.set_title(f"Algoritmo Randomizado (T={ITERACIONES}) – Tiempo real vs. ajuste teórico")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "tiempos_randomizado_ajuste.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return c, r2


def graficar_comparacion_tiempos(filas):
    ns = [f["n"] for f in filas]
    t_rand = [f["t_rand"] for f in filas]
    t_greedy = [f["t_greedy"] for f in filas]
    t_pd = [f["t_pd"] for f in filas]

    fig, (ax_lin, ax_log) = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, escala_log, titulo in [
        (ax_lin, False, "Escala lineal"),
        (ax_log, True, "Escala logarítmica"),
    ]:
        ax.plot(ns, t_rand, marker="o", color="#1f77b4", linewidth=2, label="Randomizado (T=50, k=3)")
        ax.plot(ns, t_greedy, marker="s", color="#2ca02c", linewidth=2, label="Greedy (TP1)")
        ax.plot(ns, t_pd, marker="^", color="#d62728", linewidth=2, label="Prog. Dinámica (TP1)")
        if escala_log:
            ax.set_yscale("log")
        ax.set_xlabel("Cantidad de ítems (n)")
        ax.set_ylabel("Tiempo promedio de ejecución (s)")
        ax.set_title(titulo)
        ax.legend()
        ax.grid(True, linestyle=":", alpha=0.6)

    fig.suptitle("Comparación de tiempos: Randomizado vs. Greedy vs. Programación Dinámica")
    fig.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "comparacion_tiempos.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_comparacion_calidad(filas):
    ns = [f["n"] for f in filas]
    pct_rand = [f["pct_rand"] for f in filas]
    pct_greedy = [f["pct_greedy"] for f in filas]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, pct_rand, marker="o", color="#1f77b4", linewidth=2, label="Randomizado (T=50, k=3)")
    ax.plot(ns, pct_greedy, marker="s", color="#2ca02c", linewidth=2, label="Greedy (TP1)")
    ax.axhline(100.0, linestyle="--", color="#555555", alpha=0.7, label="Óptimo PD (100%)")
    ax.set_xlabel("Cantidad de ítems (n)")
    ax.set_ylabel("Porcentaje del óptimo alcanzado (%)")
    ax.set_title("Calidad de solución respecto del óptimo: Randomizado vs. Greedy")
    ax.set_ylim(min(min(pct_rand), min(pct_greedy)) - 1.0, 100.5)
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "comparacion_calidad.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def main():
    os.makedirs(DIR_GRAFICOS, exist_ok=True)
    filas = leer_resultados()
    c, r2 = graficar_ajuste_randomizado(filas)
    graficar_comparacion_tiempos(filas)
    graficar_comparacion_calidad(filas)
    print(f"Ajuste O(n log n + T·n): c = {c:.6e}, R² = {r2:.6f}")
    print("Gráficos guardados en:", DIR_GRAFICOS)


if __name__ == "__main__":
    main()
