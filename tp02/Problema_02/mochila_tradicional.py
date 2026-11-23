def mochila_tradicional(elementos, capacidad):
    n = len(elementos)

    # Mantenemos solo dos filas en memoria (O(Capacidad) en espacio)
    prev = [0] * (capacidad + 1)
    curr = [0] * (capacidad + 1)

    for i in range(1, n + 1):
        peso, beneficio = elementos[i - 1]

        for c in range(1, capacidad + 1):
            if peso > c:
                curr[c] = prev[c]
            else:
                no_incluir = prev[c]
                incluir = beneficio + prev[c - peso]
                curr[c] = max(no_incluir, incluir)

        prev = curr[:]

    return prev[capacidad]
