import os
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from codigo import Mochila, backtracking, fuerzaBruta, leerArchivo

REPETICIONES = 3

def medirTiempo(algoritmo, pesoMochila, elementos):
    mejorTiempo = float("inf")
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        algoritmo(Mochila(pesoMochila), list(elementos), Mochila(pesoMochila))
        mejorTiempo = min(mejorTiempo, time.perf_counter() - inicio)
    return mejorTiempo

def modelo_teorico(n, c):
    return c * n * (2.0 ** n)

def graficarAjuste(eje, tamanios, tiempos, color, titulo, limitarAlMedido=False):
    if not tamanios:
        return
        
    x_data = np.array(tamanios, dtype=float)
    y_data = np.array(tiempos, dtype=float)
    
    popt, _ = curve_fit(modelo_teorico, x_data, y_data)
    c_opt = popt[0]
    
    x_plot = np.linspace(min(tamanios), max(tamanios), 100)
    y_teorico = modelo_teorico(x_plot, c_opt)

    eje.plot(x_plot, y_teorico, color="#6b6a63", linewidth=2, linestyle="--", label=r"Ajuste $c \cdot n 2^n$")
    eje.plot(tamanios, tiempos, color=color, linewidth=2, marker="o", markersize=7, label="Medido")
    
    if limitarAlMedido:
        eje.set_ylim(-max(tiempos) * 0.04, max(tiempos) * 1.15)
        
    eje.set_title(titulo)
    eje.set_xlabel("Cantidad de elementos (n)")
    eje.set_ylabel("Tiempo (s)")
    eje.legend(loc="upper left")

if __name__ == "__main__":
    directorio = os.path.dirname(os.path.abspath(__file__))
    dir_mochilas = os.path.join(os.path.dirname(directorio), "Mochilas")
    
    tamanios_fb_reales = []
    tiemposFuerzaBruta = []
    
    tamanios_bt_reales = []
    tiemposBacktracking = []

    for n in [10, 15, 20, 25, 30, 40]: 
        ruta = os.path.join(dir_mochilas, f"mochila{n}.txt")
        if not os.path.exists(ruta):
            continue
            
        pesoMochila, elementos = leerArchivo(ruta)
        
        if n <= 26:
            t_fb = medirTiempo(fuerzaBruta, pesoMochila, elementos)
            tiemposFuerzaBruta.append(t_fb)
            tamanios_fb_reales.append(n)
            print(f"Fuerza bruta  | n = {n:2d} | {t_fb:.6f} s", flush=True)
            
        if n <= 40:
            t_bt = medirTiempo(backtracking, pesoMochila, elementos)
            tiemposBacktracking.append(t_bt)
            tamanios_bt_reales.append(n)
            print(f"Backtracking  | n = {n:2d} | {t_bt:.6f} s", flush=True)

    figura, (ejeFuerzaBruta, ejeBacktracking) = plt.subplots(1, 2, figsize=(12, 5.5))
    graficarAjuste(ejeFuerzaBruta, tamanios_fb_reales, tiemposFuerzaBruta, "#2a78d6", "Fuerza bruta")
    graficarAjuste(ejeBacktracking, tamanios_bt_reales, tiemposBacktracking, "#eb6834", "Backtracking", limitarAlMedido=True)
    
    figura.tight_layout()
    figura.savefig(os.path.join(directorio, "grafico_problema01.png"), dpi=150)
    plt.show()