"""Experimentación y mediciones empíricas para el Problema 2 (FPTAS).

Ejecuta tres experimentos sobre instancias de mochila 0-1:
1. Variando ``n`` con ``epsilon`` fijo (instancias TP1 + intermedias).
2. Variando ``epsilon`` con ``n`` fijo (instancias TP1).
3. Instancias con pesos, beneficios y capacidad grandes (comparadas con PL del TP1).

Exporta los resultados en formatos CSV y TXT dentro de ``tp02/Problema_02/resultados/``.
"""

from __future__ import annotations

import csv
import importlib.util
import os
import sys
import time
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_RAIZ = os.path.normpath(os.path.join(DIR_ACTUAL, "..", ".."))
DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")

if DIR_ACTUAL not in sys.path:
    sys.path.insert(0, DIR_ACTUAL)

import datos
import fptas


def _cargar_modulo(nombre: str, ruta_archivo: str) -> Any:
    """Carga un módulo Python desde una ruta arbitraria sin duplicar código del TP1."""
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el módulo requerido: {ruta_archivo}")
    spec = importlib.util.spec_from_file_location(nombre, ruta_archivo)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar {nombre} desde {ruta_archivo}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_mod_dp = _cargar_modulo(
    "tp01_mochila_tradicional",
    os.path.join(DIR_RAIZ, "tp01", "problema03", "mochila_tradicional.py"),
)

mochila_tradicional_tp1 = _mod_dp.mochila_tradicional

REPETICIONES = 3

TAMANIOS_EXP1 = [10, 15, 20, 25, 30, 40, 60, 80, 100, 120, 150, 180, 200]
EPSILONS_EXP1 = [1.0, 0.5]

TAMANIOS_EXP2 = [20, 40, 100]
EPSILONS_EXP2 = [1.0, 0.5, 0.25, 0.2, 0.1, 0.05]

TAMANIOS_EXP3 = [20, 40, 60, 80, 100]
EPSILONS_EXP3 = [1.0, 0.5, 0.25, 0.1]

COLUMNAS_CSV = [
    "n",
    "capacidad",
    "epsilon",
    "k_inv_epsilon",
    "resultado_fptas",
    "optimo_tp1",
    "metodo_optimo",
    "peso_fptas",
    "gap_relativo",
    "factor_escala_b",
    "v_esc_max",
    "tiempo_fptas_s",
    "tiempo_optimo_s",
]


def _ruta_instancia_estandar(n: int) -> str:
    """Devuelve la ruta de instancia estándar desde TP1 o sets intermedios."""
    if n in datos.TAMANIOS_INTERMEDIOS:
        return datos.obtener_ruta_instancia_intermedia(n)
    return datos.obtener_ruta_instancia_tp1(n)


def _calcular_optimo(
    ruta_archivo: str,
    elementos: list[tuple[int, int]],
    capacidad: int,
    metodo: str,
    cache_optimos: dict[tuple[str, str], tuple[int, float]],
) -> tuple[int, float]:
    """Calcula y cachea el óptimo exacto usando el algoritmo indicado del TP1."""
    clave = (ruta_archivo, metodo)
    if clave in cache_optimos:
        return cache_optimos[clave]

    if metodo == "DP_tradicional_TP1":
        t0 = time.perf_counter()
        optimo = int(mochila_tradicional_tp1(elementos, capacidad))
        dt = time.perf_counter() - t0
    elif metodo == "PLE_SciPy_HiGHS":
        n_items = len(elementos)
        c = -np.array([v for _, v in elementos], dtype=float)
        pesos = np.array([w for w, _ in elementos], dtype=float)
        integrality = np.ones(n_items, dtype=int)
        bounds = Bounds(lb=np.zeros(n_items), ub=np.ones(n_items))
        constraints = LinearConstraint(
            A=pesos.reshape(1, -1), lb=-np.inf, ub=float(capacidad)
        )
        t0 = time.perf_counter()
        res_milp = milp(
            c=c,
            integrality=integrality,
            bounds=bounds,
            constraints=constraints,
        )
        dt = time.perf_counter() - t0
        if not res_milp.success:
            raise RuntimeError(
                f"SciPy MILP no convergió en {ruta_archivo}: {res_milp.message}"
            )
        x = np.rint(res_milp.x).astype(int)
        peso_total = sum(w for (w, _), sel in zip(elementos, x) if sel == 1)
        assert peso_total <= capacidad, (
            f"Solución PLE infactible en {ruta_archivo}: peso={peso_total} > cap={capacidad}"
        )
        optimo = sum(v for (_, v), sel in zip(elementos, x) if sel == 1)
    else:
        raise ValueError(f"Método óptimo desconocido: {metodo}")

    cache_optimos[clave] = (optimo, dt)
    return optimo, dt


def _medir_instancia(
    n: int,
    ruta_archivo: str,
    epsilon: float,
    metodo_optimo: str,
    cache_optimos: dict[tuple[str, str], tuple[int, float]],
) -> dict[str, Any]:
    """Ejecuta FPTAS ``REPETICIONES`` veces sobre una instancia y valida invariantes."""
    capacidad, elementos = datos.leer_instancia(ruta_archivo)
    optimo, tiempo_optimo_s = _calcular_optimo(
        ruta_archivo, elementos, capacidad, metodo_optimo, cache_optimos
    )

    tiempos: list[float] = []
    resultado = None
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        resultado = fptas.mochila_fptas(elementos, capacidad, epsilon)
        tiempos.append(time.perf_counter() - t0)

    assert resultado is not None
    tiempo_fptas_s = sum(tiempos) / REPETICIONES

    assert resultado.peso_total <= capacidad, (
        f"Infáctible en n={n}, eps={epsilon}: peso={resultado.peso_total} > cap={capacidad}"
    )
    assert resultado.beneficio_total <= optimo, (
        f"FPTAS superó al óptimo en n={n}, eps={epsilon}: "
        f"{resultado.beneficio_total} > {optimo}"
    )
    assert optimo <= (1.0 + epsilon) * resultado.beneficio_total + 1e-9, (
        f"Violación de cota (1+eps) en n={n}, eps={epsilon}: "
        f"opt={optimo}, fptas={resultado.beneficio_total}"
    )

    gap_relativo = (
        (optimo - resultado.beneficio_total) / resultado.beneficio_total
        if resultado.beneficio_total > 0
        else 0.0
    )

    return {
        "n": n,
        "capacidad": capacidad,
        "epsilon": resultado.epsilon,
        "k_inv_epsilon": resultado.k_inv_epsilon,
        "resultado_fptas": resultado.beneficio_total,
        "optimo_tp1": optimo,
        "metodo_optimo": metodo_optimo,
        "peso_fptas": resultado.peso_total,
        "gap_relativo": gap_relativo,
        "factor_escala_b": resultado.factor_escala_b,
        "v_esc_max": resultado.beneficio_escalado_maximo,
        "tiempo_fptas_s": tiempo_fptas_s,
        "tiempo_optimo_s": tiempo_optimo_s,
    }


def _exportar_csv(ruta_csv: str, filas: list[dict[str, Any]]) -> None:
    """Guarda las filas del experimento en formato CSV."""
    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=COLUMNAS_CSV)
        writer.writeheader()
        for fila in filas:
            writer.writerow(fila)


def _exportar_txt(ruta_txt: str, titulo: str, filas: list[dict[str, Any]]) -> None:
    """Guarda una tabla alineada legible en texto plano."""
    encabezado = (
        f"{'n':<5} {'Capacidad':<11} {'eps':<6} {'FPTAS':<11} {'Optimo':<11} "
        f"{'Metodo_Opt':<18} {'Gap_Rel':<10} {'b':<12} {'V_esc_max':<10} "
        f"{'T_FPTAS(s)':<12} {'T_Opt(s)':<12}"
    )
    separador = "-" * len(encabezado)
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        archivo.write(f"{titulo}\n")
        archivo.write(f"Repeticiones por instancia: {REPETICIONES}\n")
        archivo.write("Tiempo medido: solamente ejecución del algoritmo\n")
        archivo.write(f"{separador}\n")
        archivo.write(f"{encabezado}\n")
        archivo.write(f"{separador}\n")
        for f in filas:
            archivo.write(
                f"{f['n']:<5} {f['capacidad']:<11} {f['epsilon']:<6.2f} "
                f"{f['resultado_fptas']:<11} {f['optimo_tp1']:<11} "
                f"{f['metodo_optimo']:<18} {f['gap_relativo']:<10.6f} "
                f"{f['factor_escala_b']:<12.4f} {f['v_esc_max']:<10} "
                f"{f['tiempo_fptas_s']:<12.6f} {f['tiempo_optimo_s']:<12.6f}\n"
            )


def _ejecutar_experimento(
    nombre_base: str,
    titulo: str,
    tamanios: list[int],
    epsilons: list[float],
    obtener_ruta_fn,
    metodo_optimo: str,
    cache_optimos: dict[tuple[str, str], tuple[int, float]],
) -> list[dict[str, Any]]:
    """Corre un experimento completo, imprime progreso y exporta CSV y TXT."""
    print(f"\n=== {titulo} ===")
    print(
        f"{'n':<5} | {'eps':<5} | {'FPTAS':<10} | {'Optimo':<10} | "
        f"{'Gap':<8} | {'V_esc_max':<10} | {'T_FPTAS(s)':<10}"
    )
    print("-" * 76)

    filas: list[dict[str, Any]] = []
    for n in tamanios:
        ruta = obtener_ruta_fn(n)
        for eps in epsilons:
            fila = _medir_instancia(n, ruta, eps, metodo_optimo, cache_optimos)
            filas.append(fila)
            print(
                f"{fila['n']:<5} | {fila['epsilon']:<5.2f} | "
                f"{fila['resultado_fptas']:<10} | {fila['optimo_tp1']:<10} | "
                f"{fila['gap_relativo']:<8.5f} | {fila['v_esc_max']:<10} | "
                f"{fila['tiempo_fptas_s']:<10.6f}"
            )

    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    ruta_csv = os.path.join(DIR_RESULTADOS, f"{nombre_base}.csv")
    ruta_txt = os.path.join(DIR_RESULTADOS, f"{nombre_base}.txt")
    _exportar_csv(ruta_csv, filas)
    _exportar_txt(ruta_txt, titulo, filas)
    print(f"Exportado: {ruta_csv}")
    print(f"Exportado: {ruta_txt}")
    return filas


def main() -> None:
    cache_optimos: dict[tuple[str, str], tuple[int, float]] = {}

    _ejecutar_experimento(
        nombre_base="exp1_variando_n",
        titulo="Problema 2 (FPTAS) - Experimento 1: Variando n con epsilon fijo",
        tamanios=TAMANIOS_EXP1,
        epsilons=EPSILONS_EXP1,
        obtener_ruta_fn=_ruta_instancia_estandar,
        metodo_optimo="DP_tradicional_TP1",
        cache_optimos=cache_optimos,
    )

    _ejecutar_experimento(
        nombre_base="exp2_variando_epsilon",
        titulo="Problema 2 (FPTAS) - Experimento 2: Variando epsilon con n fijo",
        tamanios=TAMANIOS_EXP2,
        epsilons=EPSILONS_EXP2,
        obtener_ruta_fn=datos.obtener_ruta_instancia_tp1,
        metodo_optimo="DP_tradicional_TP1",
        cache_optimos=cache_optimos,
    )

    _ejecutar_experimento(
        nombre_base="exp3_valores_grandes",
        titulo="Problema 2 (FPTAS) - Experimento 3: Instancias con valores grandes",
        tamanios=TAMANIOS_EXP3,
        epsilons=EPSILONS_EXP3,
        obtener_ruta_fn=datos.obtener_ruta_instancia_grande,
        metodo_optimo="PLE_SciPy_HiGHS",
        cache_optimos=cache_optimos,
    )


if __name__ == "__main__":
    main()
