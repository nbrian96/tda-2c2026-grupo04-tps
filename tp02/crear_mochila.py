import os
import random

SEMILLA = 42
TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 1000]

def crear_mochila(n, carpeta_salida="Mochilas"):
    os.makedirs(carpeta_salida, exist_ok=True)
    ruta = os.path.join(carpeta_salida, f"mochila{n}.txt")
    
    random.seed(SEMILLA + n)
    
    capacidad = n * 50
    with open(ruta, "w") as arch:
        arch.write(f"{capacidad}\n")
        for _ in range(n):
            peso = random.randint(1, 200)
            beneficio = random.randint(1, 1000)
            arch.write(f"{peso},{beneficio}\n")
    print(f"Generado: {ruta}")

if __name__ == "__main__":
    dir_raiz = os.path.dirname(os.path.abspath(__file__))
    carpeta_mochilas = os.path.join(dir_raiz, "Mochilas")
    
    for n in TAMANIOS:
        crear_mochila(n, carpeta_mochilas)