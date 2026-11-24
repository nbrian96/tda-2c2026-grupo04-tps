def resolver_mochila_greedy(elementos, capacidad):
    """Resuelve Mochila 0-1 con el algoritmo Greedy con garantía de 2-aproximación."""
    if capacidad <= 0 or not elementos:
        return 0, 0

    candidatos = [(w, v) for w, v in elementos if 0 < w <= capacidad and v > 0]
    if not candidatos:
        return 0, 0

    candidatos.sort(key=lambda item: (item[1] / item[0], item[1]), reverse=True)

    peso_voraz = 0
    valor_voraz = 0
    elemento_critico = None

    for w, v in candidatos:
        if peso_voraz + w <= capacidad:
            peso_voraz += w
            valor_voraz += v
        elif elemento_critico is None:
            elemento_critico = (w, v)

    if elemento_critico is not None and elemento_critico[1] > valor_voraz:
        return elemento_critico[1], elemento_critico[0]

    return valor_voraz, peso_voraz
