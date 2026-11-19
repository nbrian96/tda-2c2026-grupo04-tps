import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from problema04 import leer_mochila, resolver_mochila

TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
REPETICIONES = 10
ARCHIVO_TXT = "resultados_PL.txt"
ARCHIVO_PNG = "tiempos_PL.png"

def medir_tiempos():
    capacidades = []
    tiempos_promedio = []
    tamanios_reales = []

    print("Midiendo tiempos del solver PuLP...\n")
    resolver_mochila([1], [1], 1) # Calentamiento

    dir_mochilas = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Mochilas")

    for n in TAMANIOS:
        ruta = os.path.join(dir_mochilas, f"mochila{n}.txt")
        if not os.path.exists(ruta):
            continue
            
        capacidad, pesos, valores = leer_mochila(ruta)

        tiempos = []
        for _ in range(REPETICIONES):
            _, _, _, t = resolver_mochila(valores, pesos, capacidad)
            tiempos.append(t)

        promedio = sum(tiempos) / REPETICIONES
        capacidades.append(capacidad)
        tiempos_promedio.append(promedio)
        tamanios_reales.append(n)
        print(f"n={n:4d} | tiempo promedio solver: {promedio:.6f}s")

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
    print(f"\nResultados guardados en {ARCHIVO_TXT}")

def modelo_exponencial(n, c):
    return c * np.exp(n * np.log(2))

def graficar(tamanios, tiempos_promedio):
    if not tamanios:
        return
        
    figura, (eje_izq, eje_der) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel Izquierdo: Zoom para la curva exponencial
    n_limite_izq = 40
    tamanios_izq = [n for n in tamanios if n <= n_limite_izq]
    tiempos_izq = [tiempos_promedio[i] for i, n in enumerate(tamanios) if n <= n_limite_izq]
    
    if tamanios_izq:
        n_exp_max = 30
        tamanios_ajuste = [n for n in tamanios if n <= n_exp_max]
        tiempos_ajuste = [tiempos_promedio[i] for i, n in enumerate(tamanios) if n <= n_exp_max]
        
        popt, _ = curve_fit(modelo_exponencial, np.array(tamanios_ajuste, dtype=float), np.array(tiempos_ajuste, dtype=float))
        c_opt = popt[0]
        
        n_teorico = np.linspace(min(tamanios), n_exp_max, 100)
        t_teorico = modelo_exponencial(n_teorico, c_opt)
        
        eje_izq.plot(n_teorico, t_teorico, color="orange", linewidth=2, linestyle="--", label="Curva teórica $O(2^n)$")
        eje_izq.plot(tamanios_izq, tiempos_izq, marker="o", color="steelblue", linewidth=2, label="Tiempo real")
        
        eje_izq.set_ylim(-0.005, max(tiempos_izq) * 1.5)
        eje_izq.set_title(f"Ajuste Teórico (n <= {n_limite_izq})")
        eje_izq.set_xlabel("n (cantidad de elementos)")
        eje_izq.set_ylabel("Tiempo (s)")
        eje_izq.grid(True, linestyle=":", alpha=0.7)
        eje_izq.legend()

    # Panel Derecho: Escalabilidad completa
    eje_der.plot(tamanios, tiempos_promedio, marker="o", color="steelblue", linewidth=2, label="Tiempo real (solver)")
    eje_der.set_title("Escalabilidad del Solver (todos los tamaños)")
    eje_der.set_xlabel("n (cantidad de elementos)")
    eje_der.set_ylabel("Tiempo (s)")
    eje_der.grid(True, linestyle=":", alpha=0.7)
    eje_der.legend()

    figura.suptitle("Problema 4 - Programación Lineal: Tiempo del solver vs n")
    figura.tight_layout()
    plt.savefig(ARCHIVO_PNG, dpi=150)
    plt.show()
    print(f"Gráfico guardado en {ARCHIVO_PNG}")

if __name__ == "__main__":
    tamanios, capacidades, tiempos_promedio = medir_tiempos()
    guardar_resultados(tamanios, capacidades, tiempos_promedio)
    graficar(tamanios, tiempos_promedio)