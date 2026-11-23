import math
import sys
import time

try:
    from tp02.Problema_02 import datos
except ImportError:
    import datos


def validar_epsilon(epsilon):
    if isinstance(epsilon, bool) or not isinstance(epsilon, (int, float)):
        raise ValueError("epsilon debe ser un numero en (0, 1].")
    if not math.isfinite(epsilon) or epsilon <= 0 or epsilon > 1:
        raise ValueError("epsilon debe estar en el intervalo (0, 1].")

    k = round(1.0 / epsilon)
    if k < 1 or abs(1.0 / epsilon - k) > 1e-9:
        raise ValueError("1/epsilon debe ser un entero positivo.")
    return int(k)


def mochila_fptas(elementos, capacidad, epsilon=0.5):
    if capacidad < 0:
        raise ValueError("La capacidad no puede ser negativa.")
    k = validar_epsilon(epsilon)

    if capacidad == 0 or not elementos:
        return 0, 0

    # Descartamos items que no entran solos para garantizar v_max <= OPT
    candidatos = [
        (peso, beneficio)
        for peso, beneficio in elementos
        if 0 < peso <= capacidad and beneficio > 0
    ]
    if not candidatos:
        return 0, 0

    n = len(candidatos)
    v_max = max(beneficio for _, beneficio in candidatos)

    # Redondeo al multiplo superior de b = (epsilon / 2n) * v_max usando enteros
    factor = 2 * n * k
    escalados = [
        (peso, beneficio, (factor * beneficio + v_max - 1) // v_max)
        for peso, beneficio in candidatos
    ]

    v_esc_max = sum(vh for _, _, vh in escalados)
    infinito = capacidad + 1

    # dp[V] guarda el peso minimo para lograr beneficio escalado V
    dp = [infinito] * (v_esc_max + 1)
    dp[0] = 0
    beneficio_real = [0] * (v_esc_max + 1)

    v_acum = 0
    for peso, beneficio, vh in escalados:
        v_acum += vh
        for v_actual in range(v_acum, vh - 1, -1):
            nuevo_peso = dp[v_actual - vh] + peso
            if nuevo_peso < dp[v_actual]:
                dp[v_actual] = nuevo_peso
                beneficio_real[v_actual] = beneficio_real[v_actual - vh] + beneficio

    for v_actual in range(v_esc_max, -1, -1):
        if dp[v_actual] <= capacidad:
            return beneficio_real[v_actual], dp[v_actual]

    return 0, 0


def main():
    ruta = sys.argv[1] if len(sys.argv) >= 2 else datos.obtener_ruta_instancia(10)
    epsilon = float(sys.argv[2]) if len(sys.argv) >= 3 else 0.5

    capacidad, elementos = datos.leer_mochila(ruta)
    inicio = time.perf_counter()
    beneficio, peso = mochila_fptas(elementos, capacidad, epsilon)
    tiempo_s = time.perf_counter() - inicio

    print(f"Instancia: {ruta}")
    print(f"n = {len(elementos)} | Capacidad = {capacidad} | epsilon = {epsilon}")
    print(f"Beneficio: {beneficio} | Peso usado: {peso}/{capacidad} | Tiempo: {tiempo_s:.6f} s")


if __name__ == "__main__":
    main()
