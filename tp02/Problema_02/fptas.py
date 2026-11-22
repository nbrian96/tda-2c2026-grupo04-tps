"""Esquema de aproximación totalmente polinomial (FPTAS) para Mochila 0-1.

Implementa el algoritmo arbitrariamente bueno visto en la cátedra:
- Factor de escala ``b = (epsilon / (2 * n)) * max(v_i)`` con ``1 / epsilon`` entero.
- Redondeo hacia arriba al múltiplo de ``b`` superior más cercano.
- Programación dinámica alternativa ``OPT(i, V)`` (mínimo peso para beneficio ``V``).
- Reconstrucción de los ítems seleccionados para devolver el beneficio real.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
import sys
import time

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
if DIR_ACTUAL not in sys.path:
    sys.path.insert(0, DIR_ACTUAL)

import datos


@dataclass
class ResultadoFPTAS:
    """Resultado completo de una ejecución del algoritmo FPTAS."""

    beneficio_total: int
    peso_total: int
    indices_elegidos: list[int]
    elementos_elegidos: list[tuple[int, int]]
    epsilon: float
    k_inv_epsilon: int
    factor_escala_b: float
    v_max_original: int
    beneficio_escalado_optimo: int
    beneficio_escalado_maximo: int


def validar_epsilon(epsilon: float) -> int:
    """Valida ``0 < epsilon <= 1`` con ``1 / epsilon`` entero y devuelve ``k = 1 / epsilon``."""
    if isinstance(epsilon, bool) or not isinstance(epsilon, (int, float)):
        raise ValueError("epsilon debe ser un número real en (0, 1].")
    if not math.isfinite(epsilon) or epsilon <= 0 or epsilon > 1:
        raise ValueError(f"epsilon debe pertenecer al intervalo (0, 1]; se recibió {epsilon}.")

    inv = 1.0 / float(epsilon)
    k = int(round(inv))
    if k < 1 or abs(inv - k) > 1e-9:
        raise ValueError(
            f"La condición de la cátedra exige que 1/epsilon sea entero positivo; "
            f"para epsilon={epsilon}, 1/epsilon={inv}."
        )
    return k


def _preparar_candidatos(
    elementos: list[tuple[int, int]], capacidad: int, k_inv: int
) -> tuple[list[tuple[int, int, int, int]], int, float]:
    """Filtra ítems factibles (0 < w <= W, v > 0) y calcula sus beneficios escalados."""
    candidatos = [
        (idx, int(peso), int(beneficio))
        for idx, (peso, beneficio) in enumerate(elementos)
        if 0 < peso <= capacidad and beneficio > 0
    ]
    if not candidatos:
        return [], 0, 0.0

    n = len(candidatos)
    v_max = max(beneficio for _, _, beneficio in candidatos)
    epsilon_exacto = 1.0 / k_inv
    b = (epsilon_exacto / (2 * n)) * v_max

    # Aritmética entera exacta para ceil(v_i / b) = ceil((2 * n * k * v_i) / v_max)
    factor_num = 2 * n * k_inv
    escalados = [
        (idx, peso, beneficio, (factor_num * beneficio + v_max - 1) // v_max)
        for idx, peso, beneficio in candidatos
    ]
    return escalados, v_max, b


def mochila_fptas(
    elementos: list[tuple[int, int]], capacidad: int, epsilon: float = 0.5
) -> ResultadoFPTAS:
    """Resuelve el problema de la mochila 0-1 de forma aproximada mediante FPTAS."""
    if capacidad < 0:
        raise ValueError(f"La capacidad no puede ser negativa: {capacidad}.")
    k_inv = validar_epsilon(epsilon)

    if capacidad == 0 or not elementos:
        return ResultadoFPTAS(
            beneficio_total=0,
            peso_total=0,
            indices_elegidos=[],
            elementos_elegidos=[],
            epsilon=float(epsilon),
            k_inv_epsilon=k_inv,
            factor_escala_b=0.0,
            v_max_original=0,
            beneficio_escalado_optimo=0,
            beneficio_escalado_maximo=0,
        )

    escalados, v_max, b = _preparar_candidatos(elementos, capacidad, k_inv)
    if not escalados:
        return ResultadoFPTAS(
            beneficio_total=0,
            peso_total=0,
            indices_elegidos=[],
            elementos_elegidos=[],
            epsilon=float(epsilon),
            k_inv_epsilon=k_inv,
            factor_escala_b=0.0,
            v_max_original=0,
            beneficio_escalado_optimo=0,
            beneficio_escalado_maximo=0,
        )

    v_esc_max = sum(vh for _, _, _, vh in escalados)
    infinito = sum(w for _, w, _, _ in escalados) + 1

    dp = [infinito] * (v_esc_max + 1)
    dp[0] = 0
    seleccion = [0] * (v_esc_max + 1)

    v_acum = 0
    for j, (_, w, _, vh) in enumerate(escalados):
        v_acum += vh
        bit_j = 1 << j
        for v_actual in range(v_acum, vh - 1, -1):
            nuevo_peso = dp[v_actual - vh] + w
            if nuevo_peso < dp[v_actual]:
                dp[v_actual] = nuevo_peso
                seleccion[v_actual] = seleccion[v_actual - vh] | bit_j

    v_esc_optimo = 0
    for v_actual in range(v_esc_max, -1, -1):
        if dp[v_actual] <= capacidad:
            v_esc_optimo = v_actual
            break

    mascara = seleccion[v_esc_optimo]
    indices_elegidos: list[int] = []
    elementos_elegidos: list[tuple[int, int]] = []
    peso_total = 0
    beneficio_total = 0

    for j, (idx_orig, w, v, _) in enumerate(escalados):
        if mascara & (1 << j):
            indices_elegidos.append(idx_orig)
            elementos_elegidos.append((w, v))
            peso_total += w
            beneficio_total += v

    assert peso_total == dp[v_esc_optimo], (
        f"Inconsistencia en reconstrucción: peso={peso_total}, dp={dp[v_esc_optimo]}"
    )
    assert peso_total <= capacidad, (
        f"Solución infactible: peso={peso_total} > capacidad={capacidad}"
    )

    return ResultadoFPTAS(
        beneficio_total=beneficio_total,
        peso_total=peso_total,
        indices_elegidos=indices_elegidos,
        elementos_elegidos=elementos_elegidos,
        epsilon=float(epsilon),
        k_inv_epsilon=k_inv,
        factor_escala_b=b,
        v_max_original=v_max,
        beneficio_escalado_optimo=v_esc_optimo,
        beneficio_escalado_maximo=v_esc_max,
    )


def construir_tabla_opt_fptas(
    elementos: list[tuple[int, int]], capacidad: int, epsilon: float = 0.5
) -> dict:
    """Construye la matriz completa ``OPT(i, V)`` para seguimiento manual y depuración."""
    if capacidad < 0:
        raise ValueError(f"La capacidad no puede ser negativa: {capacidad}.")
    k_inv = validar_epsilon(epsilon)
    escalados, v_max, b = _preparar_candidatos(elementos, capacidad, k_inv)
    resultado = mochila_fptas(elementos, capacidad, epsilon)

    if not escalados:
        return {
            "candidatos": [],
            "factor_escala_b": 0.0,
            "v_max_original": 0,
            "v_escalados_enteros": [],
            "v_escalados_reales": [],
            "tabla_opt": [[0]],
            "resultado": resultado,
        }

    n = len(escalados)
    v_esc_max = sum(vh for _, _, _, vh in escalados)
    infinito = float("inf")

    tabla_opt: list[list[float | int]] = [
        [infinito] * (v_esc_max + 1) for _ in range(n + 1)
    ]
    for i in range(n + 1):
        tabla_opt[i][0] = 0

    for i in range(1, n + 1):
        _, w_i, _, vh_i = escalados[i - 1]
        for v_actual in range(1, v_esc_max + 1):
            sin_item = tabla_opt[i - 1][v_actual]
            if vh_i <= v_actual:
                con_item = w_i + tabla_opt[i - 1][v_actual - vh_i]
                tabla_opt[i][v_actual] = min(sin_item, con_item)
            else:
                tabla_opt[i][v_actual] = sin_item

    return {
        "candidatos": [(idx, w, v) for idx, w, v, _ in escalados],
        "factor_escala_b": b,
        "v_max_original": v_max,
        "v_escalados_enteros": [vh for _, _, _, vh in escalados],
        "v_escalados_reales": [vh * b for _, _, _, vh in escalados],
        "tabla_opt": tabla_opt,
        "resultado": resultado,
    }


def _imprimir_resumen(ruta_archivo: str, capacidad: int, n_total: int, res: ResultadoFPTAS, tiempo_s: float) -> None:
    print(f"Instancia:                 {ruta_archivo}")
    print(f"Ítems totales / capacidad: {n_total} / {capacidad}")
    print(f"Épsilon (1/k):             {res.epsilon} (k = {res.k_inv_epsilon})")
    print(f"Beneficio máximo v*:       {res.v_max_original}")
    print(f"Factor de escala b:        {res.factor_escala_b:.6f}")
    print(f"V_max / V* escalados:      {res.beneficio_escalado_maximo} / {res.beneficio_escalado_optimo}")
    print(f"Ítems elegidos:            {len(res.elementos_elegidos)}")
    print(f"Peso utilizado:            {res.peso_total} / {capacidad}")
    print(f"Beneficio real obtenido:   {res.beneficio_total}")
    print(f"Tiempo de ejecución:       {tiempo_s:.6f} s")


def main() -> None:
    ruta_archivo = (
        sys.argv[1]
        if len(sys.argv) >= 2
        else datos.obtener_ruta_instancia_tp1(10)
    )
    epsilon = float(sys.argv[2]) if len(sys.argv) >= 3 else 0.5

    capacidad, elementos = datos.leer_instancia(ruta_archivo)
    inicio = time.perf_counter()
    res = mochila_fptas(elementos, capacidad, epsilon)
    tiempo_s = time.perf_counter() - inicio

    _imprimir_resumen(ruta_archivo, capacidad, len(elementos), res, tiempo_s)


if __name__ == "__main__":
    main()
