import os
import random

def crear_mochila(n, directorio="Mochilas"):
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        
    nombre = os.path.join(directorio, f"mochila{n}.txt")
    
    with open(nombre, "w") as arch:
        cap = n * 50
        arch.write(f"{cap}\n")
        for _ in range(n):
            peso = random.randint(1, 200)
            benef = random.randint(1, 1000)
            arch.write(f"{peso},{benef}\n")

def generar_set_comun():
    TAMANIOS = [10, 15, 20, 25, 30, 40, 100, 1000]
    SEMILLA_BASE = 42
    
    print("Generando set de datos unificado...")
    for n in TAMANIOS:
        random.seed(SEMILLA_BASE + n)
        crear_mochila(n, directorio="Mochilas")
        print(f"Generada: mochila{n}.txt")
    print("¡Set de datos común generado con éxito en la carpeta 'Mochilas/'!")


if __name__ == "__main__":
    generar_set_comun()
