"""Gestión y generación de instancias para el Problema 2 (FPTAS).

Provee lectura compatible con el formato unificado del TP1 (``(peso, beneficio)``),
acceso a las instancias base en ``tp01/Mochilas`` y generación determinista de
instancias intermedias y de valores grandes dentro de ``tp02/Problema_02/sets_datos``.
"""

from __future__ import annotations

import os
import random

SEMILLA_TP1 = 42
SEMILLA_VALORES_GRANDES = 1000

TAMANIOS_TP1 = [10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 1000]
TAMANIOS_INTERMEDIOS = [60, 80, 120, 150, 180]
TAMANIOS_VALORES_GRANDES = [20, 40, 60, 80, 100]

DIR_PROBLEMA_02 = os.path.dirname(os.path.abspath(__file__))
DIR_MOCHILAS_TP1 = os.path.normpath(
    os.path.join(DIR_PROBLEMA_02, "..", "..", "tp01", "Mochilas")
)
DIR_SETS_INTERMEDIOS = os.path.join(DIR_PROBLEMA_02, "sets_datos", "intermedios")
DIR_SETS_VALORES_GRANDES = os.path.join(
    DIR_PROBLEMA_02, "sets_datos", "valores_grandes"
)


def leer_instancia(ruta_archivo: str) -> tuple[int, list[tuple[int, int]]]:
    """Lee una instancia de mochila desde disco.

    Formato esperado:
    - Primera línea: capacidad máxima entera ``W``.
    - Líneas siguientes no vacías: ``peso,beneficio`` (enteros).

    Returns:
        Tupla ``(capacidad, elementos)``, donde cada elemento es ``(peso, beneficio)``.
    """
    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo de instancia: {ruta_archivo}")

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().strip()
        if not primera_linea:
            raise ValueError(f"El archivo de instancia está vacío: {ruta_archivo}")
        capacidad = int(primera_linea)

        elementos: list[tuple[int, int]] = []
        for num_linea, linea in enumerate(archivo, start=2):
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(",")
            if len(partes) != 2:
                raise ValueError(
                    f"Formato inválido en {ruta_archivo} (línea {num_linea}): {linea!r}"
                )
            peso = int(partes[0].strip())
            beneficio = int(partes[1].strip())
            elementos.append((peso, beneficio))

    return capacidad, elementos


def _resolver_ruta_existente(carpeta: str, nombre_archivo: str) -> str:
    """Devuelve la ruta completa validando que el archivo exista."""
    ruta = os.path.join(carpeta, nombre_archivo)
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró la instancia esperada: {ruta}")
    return ruta


def obtener_ruta_instancia_tp1(n: int) -> str:
    """Devuelve la ruta a ``mochila{n}.txt`` dentro de ``tp01/Mochilas``."""
    return _resolver_ruta_existente(DIR_MOCHILAS_TP1, f"mochila{n}.txt")


def obtener_ruta_instancia_intermedia(n: int) -> str:
    """Devuelve la ruta a ``mochila{n}.txt`` en ``sets_datos/intermedios``."""
    return _resolver_ruta_existente(DIR_SETS_INTERMEDIOS, f"mochila{n}.txt")


def obtener_ruta_instancia_grande(n: int) -> str:
    """Devuelve la ruta a ``mochila_grande{n}.txt`` en ``sets_datos/valores_grandes``."""
    return _resolver_ruta_existente(DIR_SETS_VALORES_GRANDES, f"mochila_grande{n}.txt")


def _escribir_instancia(
    ruta_salida: str, capacidad: int, elementos: list[tuple[int, int]]
) -> str:
    """Escribe una instancia de mochila en el formato estándar ``W`` y ``peso,beneficio``."""
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write(f"{capacidad}\n")
        for peso, beneficio in elementos:
            archivo.write(f"{peso},{beneficio}\n")
    return ruta_salida


def generar_mochila_estandar(n: int, carpeta_salida: str) -> str:
    """Genera una instancia estándar replicando exactamente ``tp01/crear_mochila.py``."""
    random.seed(SEMILLA_TP1 + n)
    capacidad = n * 50
    elementos = [
        (random.randint(1, 200), random.randint(1, 1000)) for _ in range(n)
    ]
    ruta = os.path.join(carpeta_salida, f"mochila{n}.txt")
    return _escribir_instancia(ruta, capacidad, elementos)


def generar_mochila_valores_grandes(n: int, carpeta_salida: str) -> str:
    """Genera una instancia con pesos, beneficios y capacidad de gran magnitud."""
    random.seed(SEMILLA_VALORES_GRANDES + n)
    capacidad = n * 250_000
    elementos = [
        (random.randint(10_000, 1_000_000), random.randint(100_000, 10_000_000))
        for _ in range(n)
    ]
    ruta = os.path.join(carpeta_salida, f"mochila_grande{n}.txt")
    return _escribir_instancia(ruta, capacidad, elementos)


def generar_todos_los_sets_extra() -> tuple[list[str], list[str]]:
    """Genera todas las instancias intermedias y de valores grandes para el Problema 2."""
    os.makedirs(DIR_SETS_INTERMEDIOS, exist_ok=True)
    os.makedirs(DIR_SETS_VALORES_GRANDES, exist_ok=True)

    rutas_intermedias = [
        generar_mochila_estandar(n, DIR_SETS_INTERMEDIOS)
        for n in TAMANIOS_INTERMEDIOS
    ]
    rutas_grandes = [
        generar_mochila_valores_grandes(n, DIR_SETS_VALORES_GRANDES)
        for n in TAMANIOS_VALORES_GRANDES
    ]
    return rutas_intermedias, rutas_grandes


if __name__ == "__main__":
    intermedias, grandes = generar_todos_los_sets_extra()
    print("Instancias intermedias generadas:")
    for ruta in intermedias:
        print(f"  - {ruta}")
    print("Instancias de valores grandes generadas:")
    for ruta in grandes:
        print(f"  - {ruta}")
