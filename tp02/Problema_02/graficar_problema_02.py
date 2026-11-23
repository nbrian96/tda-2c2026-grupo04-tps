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
    filas = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        for row in csv.DictReader(archivo):
            filas.append(
                {
                    "n": int(row["n"]),
                    "epsilon": float(row["epsilon"]),
                    "tiempo": float(row["tiempo_fptas_s"]),
                }
            )
    return filas


def ajustar_curva(xs, tiempos):
    if not tiempos:
        return 0.0, [], 1.0
    # Ajuste por minimos cuadrados t(x) = c * x
    numerador = sum(x * t for x, t in zip(xs, tiempos))
    denominador = sum(x * x for x in xs)
    c = numerador / denominador if denominador > 0 else 0.0
    ajustados = [c * x for x in xs]

    media = sum(tiempos) / len(tiempos)
    ss_res = sum((t - th) ** 2 for t, th in zip(tiempos, ajustados))
    ss_tot = sum((t - media) ** 2 for t in tiempos)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
    return c, ajustados, r2


def graficar_curva_con_ajuste(ax, eje_x, tiempos, teoricos, etiqueta_real, etiqueta_ajuste, color, marker):
    c, ajustados, r2 = ajustar_curva(teoricos, tiempos)
    ax.plot(eje_x, tiempos, marker=marker, color=color, linewidth=2, label=etiqueta_real)
    ax.plot(
        eje_x,
        ajustados,
        linestyle="--",
        color=color,
        alpha=0.75,
        label=f"{etiqueta_ajuste} (R²={r2:.4f})",
    )
    return c, r2


def graficar_variando_n(filas_exp1):
    fig, ax = plt.subplots(figsize=(10, 6))
    ajustes = []
    for eps, color, marker in [(0.5, "#1f77b4", "o"), (1.0, "#d62728", "s")]:
        sub = sorted([f for f in filas_exp1 if abs(f["epsilon"] - eps) < 1e-9], key=lambda f: f["n"])
        ns = [f["n"] for f in sub]
        tiempos = [f["tiempo"] for f in sub]
        c, r2 = graficar_curva_con_ajuste(
            ax, ns, tiempos, [n**3 for n in ns], f"Tiempo real (ε={eps})", f"Ajuste O(n³) ε={eps}", color, marker
        )
        ajustes.append((f"Exp1 eps={eps}", c, r2))

    ax.set_xlabel("Cantidad de ítems (n)")
    ax.set_ylabel("Tiempo promedio de ejecución (s)")
    ax.set_title("FPTAS – Tiempo de ejecución vs. n con ajuste O(n³)")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_GRAFICOS, "tiempos_vs_n_ajuste_O_n3.png"), dpi=150)
    plt.close(fig)
    return ajustes


def graficar_variando_epsilon(filas_exp2):
    fig, (ax_izq, ax_der) = plt.subplots(1, 2, figsize=(13, 5.5))
    ajustes = []
    for ax, lista_n in [(ax_izq, [(100, "#1f77b4", "o")]), (ax_der, [(40, "#2ca02c", "s"), (20, "#ff7f0e", "^")])]:
        for n_obj, color, marker in lista_n:
            sub = sorted([f for f in filas_exp2 if f["n"] == n_obj], key=lambda f: round(1.0 / f["epsilon"]))
            ks = [round(1.0 / f["epsilon"]) for f in sub]
            tiempos = [f["tiempo"] for f in sub]
            c, r2 = graficar_curva_con_ajuste(
                ax, ks, tiempos, ks, f"Tiempo real (n={n_obj})", f"Ajuste O(ε⁻¹) n={n_obj}", color, marker
            )
            ajustes.append((f"Exp2 n={n_obj}", c, r2))

        ax.set_xlabel("k = 1/ε  (ε ∈ {1.0, 0.5, 0.25, 0.2, 0.1, 0.05})")
        ax.set_ylabel("Tiempo promedio de ejecución (s)")
        ax.set_xticks([1, 2, 4, 5, 10, 20])
        ax.legend()
        ax.grid(True, linestyle=":", alpha=0.6)

    ax_izq.set_title("n = 100")
    ax_der.set_title("n = 40 y n = 20")
    fig.suptitle("FPTAS – Tiempo de ejecución vs. 1/ε con ajuste lineal O(ε⁻¹)")
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_GRAFICOS, "tiempos_vs_inv_epsilon_ajuste_lineal.png"), dpi=150)
    plt.close(fig)
    return ajustes


def main():
    os.makedirs(DIR_GRAFICOS, exist_ok=True)
    filas_exp1 = leer_csv("exp1_variando_n.csv")
    filas_exp2 = leer_csv("exp2_variando_epsilon.csv")

    ajustes = graficar_variando_n(filas_exp1) + graficar_variando_epsilon(filas_exp2)
    for nombre, c, r2 in ajustes:
        print(f"{nombre}: c = {c:.6e}, R^2 = {r2:.6f}")


if __name__ == "__main__":
    main()
