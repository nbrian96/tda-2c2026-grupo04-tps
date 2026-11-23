import csv
import os
import time

try:
    from tp02.Problema_02 import datos, fptas
    from tp02.Problema_02.mochila_tradicional import mochila_tradicional
except ImportError:
    import datos
    import fptas
    from mochila_tradicional import mochila_tradicional

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")

REPETICIONES = 3
TAMANIOS_EXP1 = [10, 15, 20, 25, 30, 40, 60, 80, 100, 120, 150, 180, 200]
EPSILONS_EXP1 = [1.0, 0.5]

TAMANIOS_EXP2 = [20, 40, 100]
EPSILONS_EXP2 = [1.0, 0.5, 0.25, 0.2, 0.1, 0.05]

COLUMNAS = [
    "n",
    "capacidad",
    "epsilon",
    "resultado_fptas",
    "optimo_tp1",
    "peso_fptas",
    "gap_relativo",
    "tiempo_fptas_s",
]


def medir_experimento(nombre_archivo, titulo, tamanios, epsilons, cache_optimos):
    print(f"\n=== {titulo} ===")
    print(f"{'n':<5} | {'eps':<5} | {'FPTAS':<8} | {'Optimo':<8} | {'Gap':<8} | {'Tiempo(s)':<10}")
    print("-" * 58)

    filas = []
    for n in tamanios:
        ruta = datos.obtener_ruta_instancia(n)
        capacidad, elementos = datos.leer_mochila(ruta)

        if n not in cache_optimos:
            cache_optimos[n] = mochila_tradicional(elementos, capacidad)
        optimo = cache_optimos[n]

        for eps in epsilons:
            tiempos = []
            beneficio = 0
            peso = 0
            for _ in range(REPETICIONES):
                inicio = time.perf_counter()
                beneficio, peso = fptas.mochila_fptas(elementos, capacidad, eps)
                tiempos.append(time.perf_counter() - inicio)

            tiempo_prom = sum(tiempos) / REPETICIONES
            assert peso <= capacidad, f"Peso excedido en n={n}, eps={eps}"
            assert beneficio <= optimo <= (1.0 + eps) * beneficio + 1e-9, (
                f"Cota incumplida en n={n}, eps={eps}: fptas={beneficio}, opt={optimo}"
            )

            gap = (optimo - beneficio) / beneficio if beneficio > 0 else 0.0
            filas.append(
                {
                    "n": n,
                    "capacidad": capacidad,
                    "epsilon": eps,
                    "resultado_fptas": beneficio,
                    "optimo_tp1": optimo,
                    "peso_fptas": peso,
                    "gap_relativo": round(gap, 6),
                    "tiempo_fptas_s": round(tiempo_prom, 6),
                }
            )
            print(f"{n:<5} | {eps:<5.2f} | {beneficio:<8} | {optimo:<8} | {gap:<8.5f} | {tiempo_prom:<10.6f}")

    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    ruta_csv = os.path.join(DIR_RESULTADOS, nombre_archivo)
    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(filas)
    print("Guardado:", ruta_csv)


def main():
    cache_optimos = {}
    medir_experimento(
        "exp1_variando_n.csv",
        "Experimento 1: Variando n con epsilon fijo",
        TAMANIOS_EXP1,
        EPSILONS_EXP1,
        cache_optimos,
    )
    medir_experimento(
        "exp2_variando_epsilon.csv",
        "Experimento 2: Variando epsilon con n fijo",
        TAMANIOS_EXP2,
        EPSILONS_EXP2,
        cache_optimos,
    )


if __name__ == "__main__":
    main()
