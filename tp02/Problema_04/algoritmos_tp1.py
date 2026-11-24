import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


class Elemento:
    def __init__(self, peso, valor):
        self.peso = peso
        self.valor = valor


class Mochila:
    def __init__(self, peso):
        self.peso = peso
        self.pesoDisponible = peso
        self.valorActual = 0
        self.itemsDentro = []

    def agregarElemento(self, elemento):
        self.itemsDentro.append(elemento)
        self.pesoDisponible -= elemento.peso
        self.valorActual += elemento.valor

    def quitarElemento(self):
        elemento = self.itemsDentro.pop()
        self.pesoDisponible += elemento.peso
        self.valorActual -= elemento.valor
        return elemento

    def puedeAgregarElemento(self, elemento):
        return self.pesoDisponible >= elemento.peso

    def copiar(self):
        copia = Mochila(self.peso)
        copia.pesoDisponible = self.pesoDisponible
        copia.valorActual = self.valorActual
        copia.itemsDentro = list(self.itemsDentro)
        return copia


def _fuerza_bruta(mochila, elementos, mejor_resultado):
    resultado = mejor_resultado
    if mochila.valorActual > resultado.valorActual:
        resultado = mochila.copiar()

    elementos_a_probar = list(elementos)
    for _ in elementos:
        pivote = elementos_a_probar.pop(0)
        if mochila.puedeAgregarElemento(pivote):
            mochila.agregarElemento(pivote)
            resultado_rec = _fuerza_bruta(mochila.copiar(), list(elementos_a_probar), resultado)
            if resultado_rec.valorActual > resultado.valorActual:
                resultado = resultado_rec
            mochila.quitarElemento()

    return resultado


def resolver_fuerza_bruta(elementos, capacidad):
    """Resuelve Mochila 0-1 por Fuerza Bruta (copia local de la lógica del TP1)."""
    items = [Elemento(w, v) for w, v in elementos]
    mochila = Mochila(capacidad)
    res = _fuerza_bruta(mochila.copiar(), items, mochila.copiar())
    return res.valorActual, capacidad - res.pesoDisponible


def _cota_superior(mochila, elementos):
    cota = mochila.valorActual
    for elemento in elementos:
        if mochila.puedeAgregarElemento(elemento):
            cota += elemento.valor
    return cota


def _backtracking(mochila, elementos, mejor_resultado):
    resultado = mejor_resultado
    if mochila.valorActual > resultado.valorActual:
        resultado = mochila.copiar()

    if _cota_superior(mochila, elementos) <= resultado.valorActual:
        return resultado

    elementos_a_probar = list(elementos)
    for _ in elementos:
        pivote = elementos_a_probar.pop(0)
        if mochila.puedeAgregarElemento(pivote):
            mochila.agregarElemento(pivote)
            resultado_rec = _backtracking(mochila, elementos_a_probar, resultado)
            if resultado_rec.valorActual > resultado.valorActual:
                resultado = resultado_rec
            mochila.quitarElemento()
            if _cota_superior(mochila, elementos_a_probar) <= resultado.valorActual:
                break

    return resultado


def resolver_backtracking(elementos, capacidad):
    """Resuelve Mochila 0-1 por Backtracking con poda (copia local de la lógica del TP1)."""
    items = [Elemento(w, v) for w, v in elementos]
    mochila = Mochila(capacidad)
    res = _backtracking(mochila.copiar(), items, mochila.copiar())
    return res.valorActual, capacidad - res.pesoDisponible


def resolver_programacion_lineal(elementos, capacidad):
    """Resuelve Mochila 0-1 con Programación Lineal Entera usando SciPy MILP (HiGHS)."""
    n = len(elementos)
    if n == 0 or capacidad <= 0:
        return 0, 0

    pesos = np.array([w for w, _ in elementos], dtype=float)
    valores = np.array([v for _, v in elementos], dtype=float)

    resultado = milp(
        c=-valores,
        integrality=np.ones(n, dtype=int),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(pesos.reshape(1, -1), -np.inf, float(capacidad)),
        options={"mip_rel_gap": 0.0},
    )
    if not resultado.success:
        raise RuntimeError(f"El solver MILP no convergió: {resultado.message}")

    valor_total = 0
    peso_total = 0
    for i in range(n):
        if round(resultado.x[i]) == 1:
            peso_total += elementos[i][0]
            valor_total += elementos[i][1]
    return valor_total, peso_total
