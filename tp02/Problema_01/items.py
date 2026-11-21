def obtener_indice(item):
    """Función auxiliar que devuelve el cociente de pi/wi de un item"""
    return item["indice"]

def crear_y_ordenar_items(beneficios, pesos):
    """Función que recibe una lista de items y devuelve una lista de items ordenada de mayor a menor por el cociente pi/wi"""
    n = len(beneficios)
    items = []
    for i in range(n):
        p_j=beneficios[i]
        w_j=pesos[i]
        indice_calidad = p_j / w_j
        nuevo_item = {
            "id" : i + 1,
            "beneficio": p_j,
            "peso": w_j,
            "indice": indice_calidad
        }
        items.append(nuevo_item)
    items.sort(key=obtener_indice, reverse=True)
    return items