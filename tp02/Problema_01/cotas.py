def buscar_elemento_critico(items_ordenados, capacidad_mochila):
    """Recibe items ordenados de mayor a menor por el cociente de pi/wi y va metiendo los items en la mochila
    hasta que se encuentra el elemento critico, es decir, el primer item que no cabe en la mochila
    
    Devuelve tres valores:
    - s: el indice del elemento critico, si todos los items entran en la mochila, devuelve None
    - suma_beneficios_previos: la sumatoria de los p_j hasta s-1
    - capacidad_residual: la capacidad restante de la mochila luego de meter los items hasta s-1
    """
    capacidad_residual = capacidad_mochila
    suma_beneficios_previos = 0
    n = len(items_ordenados)

    for j in range(n):
        item_actual = items_ordenados[j]
        peso_actual = item_actual["peso"]
        beneficio_actual = item_actual["beneficio"]
        if peso_actual <= capacidad_residual:
            suma_beneficios_previos += beneficio_actual
            capacidad_residual -= peso_actual
        else:
            s = j
            return s, suma_beneficios_previos, capacidad_residual

    return None, suma_beneficios_previos, capacidad_residual


    def calcular_cota_relajacion_lineal(items_ordenados, capacidad_mochila):
        """
        Calcula la cota superior U1 (Dantzig, 1957) y devuelve tanto el valor continuo exacto z(C(KP)) como la cota entera U1.
        """ 
        s, suma_beneficios_previos, c_sombrero = buscar_elemento_critico(items_ordenados, capacidad_mochila)

        if s is None:
            return suma_beneficios_previos, suma_beneficios_previos

        item_critico = items_ordenados[s]
        p_s = item_critico["beneficio"]
        w_s = item_critico["peso"]

        aporte_fraccionario = c_sombrero * (p_s / w_s)
        z_continuo = suma_beneficios_previos + aporte_fraccionario
        u1 = suma_beneficios_previos + math.floor(aporte_fraccionario)
        
        return z_continuo, u1

def calcular_cota_martello_toth(items_ordenados, capacidad_mochila):
    """
    Calcula la cota superior U2 (Martello y Toth, 1990). Evalúa excluir el elemento crítico (W1) o incluirlo a la fuerza (W2)..
    """ 
    s, suma_beneficios_previos, c_sombrero = buscar_elemento_critico(items_ordenados, capacidad_mochila)
    n = len(items_ordenados)

    if s is None:
        return suma_beneficios_previos, suma_beneficios_previos
    
    item_critico = items_ordenados[s]
    p_s = item_critico["beneficio"]
    w_s = item_critico["peso"]

    if s + 1 < n:
        item_siguiente = items_ordenados[s + 1]
        p_siguiente = item_siguiente["beneficio"]
        w_siguiente = item_siguiente["peso"]

        w1 = suma_beneficios_previos + math.floor(c_sombrero * (p_siguiente / w_siguiente))
    else:
        w1 = suma_beneficios_previos

    if s-1 >= 0:
        item_anterior = items_ordenados[s - 1]
        p_anterior = item_anterior["beneficio"]
        w_anterior = item_anterior["peso"]

        peso_faltante = w_s - c_sombrero
        ajuste = p_s - (peso_faltante * (p_anterior / w_anterior))
        w2 = suma_beneficios_previos + math.floor(ajuste)
    else:
        w2 = p_s if w_s <= capacidad_mochila else 0

    u2 = max(w1, w2)
    return u2