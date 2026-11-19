import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from problema04 import leer_mochila, resolver_mochila

# Usamos los tamaños unificados que se generaron en la raíz
TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 1000]
REPETICIONES = 3
ARCHIVO_TXT = "resultados_PL.txt"
ARCHIVO_PNG = "tiempos_PL.png"

N_EXP_MAX = 30
N_COTA_MAX = 60

def medir_tiempos():
    capacidades = []
    tiempos_promedio = []
    tamanios_reales = []

    print("Midiendo tiempos del solver PuLP...\n")

    # Corrida de calentamiento
    resolver_mochila([1], [1], 1)

    dir_mochilas = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Mochilas")

    for n in TAMANIOS:
        ruta = os.path.join(dir_mochilas, f"mochila{n}.txt")
        if not os.path.exists(ruta):
            continue
            
        capacidad, pesos, valores = leer_mochila(ruta)

        tiempos = []
        for _ in range(REPETICIONES):
            # Guardamos la solución de la última iteración
            seleccionados, valor_total, peso_total, t = resolver_mochila(valores, pesos, capacidad)
            tiempos.append(t)

        promedio = sum(tiempos) / repeticiones
        capacidades.append(capacidad)
        tiempos_promedio.append(promedio)
        tamanios_reales.append(n)
        print(f"n={n:4d} | tiempo promedio solver: {promedio:.6f}s")

        # Guardar la solución obtenida (requerimiento de la cátedra)
        ruta_solucion = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"solucion_PL_n{n}.txt")
        with open(ruta_solucion, "w") as f_sol:
            f_sol.write(f"Valor total: {valor_total}\n")
            f_sol.write(f"Peso utilizado: {peso_total}\n")
            f_sol.write(f"IDs seleccionados: {seleccionados}\n")

    return tamanios_reales, capacidades, tiempos_promedio

def guardar_resultados(tamanios, capacidades, tiempos_promedio, repeticiones=REPETICIONES):
    with open(ARCHIVO_TXT, "w") as f:
        f.write("Resultados - Problema 4: Programacion Lineal\n")
        f.write("Tiempo medido: solo resolucion del solver\n")
        f.write("Repeticiones por instancia: " + str(repeticiones) + "\n")
        f.write("-" * 45 + "\n")
        f.write("{:<10} {:<15} {:<15}\n".format("n", "Capacidad W", "Tiempo (s)"))
        f.write("-" * 45 + "\n")
        for i in range(len(tamanios)):
            f.write("{:<10} {:<15} {:<15}\n".format(
                tamanios[i], capacidades[i], round(tiempos_promedio[i], 6)
            ))
    print("\nResultados guardados en " + ARCHIVO_TXT)

# Función para el ajuste exponencial puro (O(2^n))
def modelo_exponencial(n, c):
    # n * log(2) para evitar overflow antes del exp
    return c * np.exp(n * np.log(2))

def graficar(tamanios, tiempos_promedio):
    if not tamanios:
        return
        
    figura, (ejeLineal, ejeLog) = plt.subplots(1, 2, figsize=(15, 6))

    # Filtramos para el ajuste teórico solo los n <= N_EXP_MAX
    tamanios_ajuste = [n for n in tamanios if n <= N_EXP_MAX]
    tiempos_ajuste = [tiempos_promedio[i] for i, n in enumerate(tamanios) if n <= N_EXP_MAX]
    
    if tamanios_ajuste:
        # Ajuste por mínimos cuadrados de la curva teórica exponencial
        popt, _ = curve_fit(modelo_exponencial, np.array(tamanios_ajuste, dtype=float), np.array(tiempos_ajuste, dtype=float))
        c_opt = popt[0]
        
        n_exp = list(range(tamanios[0], N_EXP_MAX + 1))
        t_exp = modelo_exponencial(np.array(n_exp, dtype=float), c_opt)
        
        ejeLineal.plot(n_exp, t_exp, color="orange", linewidth=2, linestyle="--",
                       label="Curva teórica $O(2^n)$ (ajustada)")
        ejeLineal.plot(tamanios_ajuste, tiempos_ajuste, marker="o",
                       color="steelblue", linewidth=2, label="Tiempo real (solver)")
        ejeLineal.set_ylim(-0.03 * t_exp[-1], t_exp[-1])
        
        n_cota = list(range(tamanios[0], N_COTA_MAX + 1))
        t_cota = modelo_exponencial(np.array(n_cota, dtype=float), c_opt)
        ejeLog.plot(n_cota, t_cota, color="orange", linewidth=2, linestyle="--",
                    label="Cota teórica $O(2^n)$ (ajustada)")
    
    ejeLineal.set_title(f"Escala lineal, n <= {N_EXP_MAX}")
    ejeLineal.set_xlabel("n (cantidad de elementos)")
    ejeLineal.set_ylabel("Tiempo (s)")

    # Panel derecho: todos los tamaños en escala log-log, con ajuste empírico t = a * n^b
    b, log_a = np.polyfit(np.log10(tamanios), np.log10(tiempos_promedio), 1)
    n_ajuste = np.logspace(np.log10(tamanios[0]), np.log10(tamanios[-1]), 100)
    t_ajuste = (10 ** log_a) * n_ajuste ** b

    ejeLog.plot(tamanios, tiempos_promedio, marker="o", color="steelblue", linewidth=2,
                label="Tiempo real (solver)")
    ejeLog.plot(n_ajuste, t_ajuste, color="green", linewidth=2, linestyle=":",
                label=f"Ajuste empírico ~ n^{b:.2f}")
    
    ejeLog.set_xscale("log")
    ejeLog.set_yscale("log")
    ejeLog.set_ylim(min(tiempos_promedio) / 2, max(tiempos_promedio) * 10)
    ejeLog.set_title("Escala logarítmica, todos los tamaños")
    ejeLog.set_xlabel("n (cantidad de elementos, escala log)")
    ejeLog.set_ylabel("Tiempo (s, escala log)")

    for eje in (ejeLineal, ejeLog):
        eje.legend()
        eje.grid(True, which="both")

    figura.suptitle("Problema 4 - Programación Lineal: Tiempo del solver vs n")
    figura.tight_layout()
    figura.savefig(ARCHIVO_PNG, dpi=150)
    plt.show()

    print("Gráfico guardado en " + ARCHIVO_PNG)

if __name__ == "__main__":
    tamanios, capacidades, tiempos_promedio = medir_tiempos()
    guardar_resultados(tamanios, capacidades, tiempos_promedio)
    graficar(tamanios, tiempos_promedio)