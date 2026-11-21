def procedimiento_gs(items_ordenados, capacidad_mochila, indices_M):
    """
    Se recibe una lista de items ordenados por cociente p_j/w_j de mayor a menor, la capacidad de la mochila y los indices 
    de un conjunto (set) con las posiciones j (0 a n-1) de los items que fueron seleccionados obligatoriamente en M. Devuelve 
    z_g que representa el beneficio acumulado unicamente por los items agregados en este paso greedy y también devuelve
    X, una lista de posiciones j de los items agregados en este paso. 
    """

    n = len(items_ordenados)
    z_g = 0
    X = []

    peso_total_M = 0
    for j in indices_M:
        peso_total_M += items_ordenados[j]["peso"]

    c_sombrero = capacidad_mochila - peso_total_M

    for j in range(n):
        peso_j = items_ordenados[j]["peso"]
        beneficio_j = items_ordenados[j]["beneficio"]

        if (j not in indices_M) and (peso_j <= c_sombrero):
            z_g += beneficio_j
            c_sombrero -= peso_j
            X.append(j)
    
    return z_g, X