import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")
DIR_GRAFICOS = os.path.join(DIR_ACTUAL, "graficos")


def leer_csv(nombre_archivo):
    ruta = os.path.join(DIR_RESULTADOS, nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def graficar_tiempos(filas):
    fig, (ax_zoom, ax_full) = plt.subplots(1, 2, figsize=(14, 5.8))

    series = [
        ("fuerza_bruta_s", "Fuerza Bruta (TP1)", "#8c564b", "v", ":"),
        ("backtracking_s", "Backtracking (TP1)", "#e377c2", "^", ":"),
        ("greedy_s", "Greedy (TP1)", "#2ca02c", "s", "-"),
        ("pd_tradicional_s", "Prog. Dinámica (TP1)", "#d62728", "o", "-"),
        ("programacion_lineal_s", "Prog. Lineal (TP1)", "#9467bd", "D", "--"),
        ("sahni_k1_s", "Sahni k=1 (TP2 P1)", "#ff7f0e", "P", "-."),
        ("fptas_eps05_s", "FPTAS ε=0.5 (TP2 P2)", "#17becf", "X", "-."),
        ("randomizado_s", "Randomizado (TP2 P3)", "#1f77b4", "*", "-"),
    ]

    for col, label, color, marker, ls in series:
        pares = [(int(r["n"]), float(r[col])) for r in filas if r[col]]
        if not pares:
            continue
        ns = [p[0] for p in pares]
        ts = [max(p[1], 1e-6) for p in pares]
        ax_full.plot(ns, ts, label=label, color=color, marker=marker, linestyle=ls, linewidth=1.8)

        pares_zoom = [(n, t) for n, t in zip(ns, ts) if n <= 40]
        if pares_zoom:
            ax_zoom.plot(
                [p[0] for p in pares_zoom],
                [p[1] for p in pares_zoom],
                label=label,
                color=color,
                marker=marker,
                linestyle=ls,
                linewidth=1.8,
            )

    for ax, titulo in [
        (ax_zoom, "Rango n ≤ 40 (escala logarítmica)"),
        (ax_full, "Rango completo n ≤ 1000 (escala logarítmica)"),
    ]:
        ax.set_yscale("log")
        ax.set_xlabel("Cantidad de ítems (n)")
        ax.set_ylabel("Tiempo de ejecución (s)")
        ax.set_title(titulo)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=8, loc="best")

    fig.suptitle("Comparación de tiempos de ejecución – TP1 y TP2 (8 algoritmos)")
    fig.tight_layout()
    ruta = os.path.join(DIR_GRAFICOS, "comparacion_tiempos_todos.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_aproximados_cotas(filas):
    ns = [int(r["n"]) for r in filas]
    opt = [int(r["optimo_pd"]) for r in filas]

    fig, ax = plt.subplots(figsize=(11, 6))

    curvas = [
        ("cota_rl_u1", "Cota RL (U1)", "#7f7f7f", "^", "--"),
        ("cota_mt_u2", "Cota Martello-Toth (U2)", "#111111", "v", ":"),
        ("randomizado", "Randomizado (TP2 P3)", "#1f77b4", "*", "-"),
        ("sahni_k1", "Sahni k=1 (TP2 P1)", "#ff7f0e", "P", "-."),
        ("greedy", "Greedy (TP1)", "#2ca02c", "s", "-"),
    ]

    for col, label, color, marker, ls in curvas:
        pcts = [int(r[col]) / o * 100.0 for r, o in zip(filas, opt)]
        ax.plot(ns, pcts, label=label, color=color, marker=marker, linestyle=ls, linewidth=1.8)

    pares_fptas = [
        (int(r["n"]), int(r["fptas_eps05"]) / int(r["optimo_pd"]) * 100.0)
        for r in filas
        if r["fptas_eps05"]
    ]
    ax.plot(
        [p[0] for p in pares_fptas],
        [p[1] for p in pares_fptas],
        label="FPTAS ε=0.5 (TP2 P2, n ≤ 200)",
        color="#17becf",
        marker="X",
        linestyle="-.",
        linewidth=1.8,
    )

    ax.axhline(100.0, color="#d62728", linestyle="-", linewidth=1.2, alpha=0.7, label="Óptimo exacto (100%)")
    ax.set_xlabel("Cantidad de ítems (n)")
    ax.set_ylabel("Porcentaje respecto del óptimo (%)")
    ax.set_title("Algoritmos aproximados y cotas superiores (RL y Martello-Toth) respecto del óptimo")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(fontsize=9, loc="best")
    fig.tight_layout()

    ruta = os.path.join(DIR_GRAFICOS, "comparacion_aproximados_cotas.png")
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def main():
    os.makedirs(DIR_GRAFICOS, exist_ok=True)
    filas_tiempos = leer_csv("comparacion_tiempos.csv")
    filas_aprox = leer_csv("comparacion_aproximados_cotas.csv")
    graficar_tiempos(filas_tiempos)
    graficar_aproximados_cotas(filas_aprox)
    print("Gráficos del Problema 4 guardados en:", DIR_GRAFICOS)


if __name__ == "__main__":
    main()
