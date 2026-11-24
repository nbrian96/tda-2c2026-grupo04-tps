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

RUTA_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados_problema1_k1.txt")
DIR_GRAFICOS = os.path.join(DIR_ACTUAL, "graficos")


def leer_resultados_p1():
    ns = []
    tiempos = []
    with open(RUTA_RESULTADOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or not linea[0].isdigit():
                continue
            partes = linea.split()
            ns.append(int(partes[0]))
            tiempos.append(float(partes[7]))
    return ns, tiempos


def main():
    os.makedirs(DIR_GRAFICOS, exist_ok=True)
    ns, tiempos = leer_resultados_p1()
    teoricos = [n * n for n in ns]
    c, ajustados, r2 = ajustar_curva(teoricos, tiempos)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, tiempos, marker="o", color="#1f77b4", linewidth=2, label="Tiempo real (Sahni k=1)")
    ax.plot(
        ns,
        ajustados,
        linestyle="--",
        color="#d62728",
        linewidth=2,
        label=f"Ajuste teórico O(n²) (R²={r2:.4f})",
    )
    ax.set_xlabel("Cantidad de ítems (n)")
    ax.set_ylabel("Tiempo promedio de ejecución (s)")
    ax.set_title("Algoritmo de Sahni (k=1) – Tiempo real vs. ajuste teórico O(n²)")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()

    ruta_salida = os.path.join(DIR_GRAFICOS, "tiempos_sahni_ajuste_O_n2.png")
    fig.savefig(ruta_salida, dpi=150)
    plt.close(fig)

    print(f"Ajuste O(n²): c = {c:.6e}, R² = {r2:.6f}")
    print("Gráfico guardado en:", ruta_salida)


if __name__ == "__main__":
    main()
