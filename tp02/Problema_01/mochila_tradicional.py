import sys

def leer_mochila(nombre_archivo):
    elementos = []
    with open(nombre_archivo, "r") as archivo:
        capacidad = int(archivo.readline().strip())
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            peso, beneficio = map(int, linea.split(","))
            elementos.append((peso, beneficio))
    return capacidad, elementos

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

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 mochila_tradicional.py <archivo>")
        return
    nombre_archivo = sys.argv[1]
    capacidad, elementos = leer_mochila(nombre_archivo)
    beneficio_maximo = mochila_tradicional(elementos, capacidad)
    print("Beneficio máximo:", beneficio_maximo)

if __name__ == "__main__":
    main()