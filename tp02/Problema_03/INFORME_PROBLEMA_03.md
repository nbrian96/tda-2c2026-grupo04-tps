# Problema 3 – Algoritmos Randomizados: Greedy Aleatorizado con Ventana y Multi-arranque

**Materia:** Teoría de Algoritmos (TB024) – FIUBA  
**Trabajo Práctico 2**

---

## 1. Supuestos, Condiciones y Limitaciones

El algoritmo implementado (`tp02/Problema_03/randomizado.py`) resuelve de manera aproximada el Problema de la Mochila 0-1 bajo las siguientes premisas:

1. **Dominio de entrada:**
   - Capacidad entera no negativa $W \in \mathbb{Z}_{\ge 0}$ y $n$ ítems con peso entero positivo $w_i \in \mathbb{Z}^+$ y beneficio entero positivo $v_i \in \mathbb{Z}^+$.
   - Cada ítem se incluye completo o se descarta ($x_i \in \{0, 1\}$).
2. **Prefiltrado de factibilidad:**
   - Antes de ordenar y ejecutar las iteraciones, se descartan los ítems con $w_i > W$ o $v_i \le 0$, ya que nunca pueden formar parte de una solución factible que mejore el beneficio.
3. **Clasificación Monte Carlo:**
   - El algoritmo tiene tiempo de ejecución polinomial y acotado por el parámetro de iteraciones $T$.
   - Toda solución devuelta es siempre **factible** ($\sum w_i \le W$), pero al ser un algoritmo aproximado de tipo Monte Carlo puede no alcanzar el óptimo global en una ejecución finita.
4. **Reproducibilidad mediante semilla:**
   - Se utiliza el generador pseudoaleatorio `random.Random(semilla)` de Python con semilla configurable (`semilla = 42` por defecto) para poder reproducir los experimentos.
5. **Sensibilidad a los parámetros ($T$ y $k$):**
   - Por defecto se utilizan $T = 50$ iteraciones y ventana $k = 3$. Un valor de $k$ demasiado grande degrada la heurística hacia una selección puramente aleatoria, mientras que $k = 1$ la reduce al Greedy determinístico.

---

## 2. Diseño del Algoritmo

### 2.1. Fundamentación del uso del azar

El algoritmo **Greedy determinístico** ordena los ítems por su ratio beneficio/peso ($v_i / w_i$) descendente y los agrega en ese único orden fijo. Su limitación clásica aparece cuando un ítem de muy buen ratio ocupa gran parte de la capacidad restante e impide combinar otros dos o más ítems que, juntos, producen mayor beneficio total.

Para superar esa rigidez sin perder la guía del criterio voraz, introducimos aleatoriedad en dos niveles:

1. **Perturbación local controlada (ventana de tamaño $k$):**
   - Partimos de la lista ordenada por ratio descendente. En cada paso $i$, en lugar de tomar obligatoriamente `copia[i]`, elegimos al azar con probabilidad uniforme un índice $j \in [i, \min(i + k - 1, n - 1)]$ e intercambiamos `copia[i]` con `copia[j]`.
   - De este modo, los ítems con mejor ratio siguen teniendo alta prioridad para entrar primero, pero se habilitan variaciones locales en el orden de selección que permiten evitar bloqueos de capacidad.
2. **Multi-arranque (repetición de $T$ ensayos independientes):**
   - Siguiendo el principio de los algoritmos **Monte Carlo** vistos en clase (como en el algoritmo de contracción de Karger), si en un ensayo individual la probabilidad de encontrar una solución óptima o de alta calidad es $p > 0$, la probabilidad de fallar en los $T$ ensayos independientes cae exponencialmente a $(1 - p)^T$.
   - Al conservar la mejor solución factible entre las $T$ corridas, se amplifica la calidad esperada manteniendo el tiempo total acotado y polinomial.

### 2.2. Estructuras de datos utilizadas

- `candidatos`: lista de tuplas `(peso, beneficio)` ordenada una sola vez por ratio $v/w$ descendente.
- `copia`: copia superficial de `candidatos` de tamaño $n$ utilizada en cada iteración para realizar los intercambios locales sin alterar el orden base.
- `seleccion` y `mejor_seleccion`: listas de tuplas `(peso, beneficio)` que almacenan los ítems elegidos en la iteración actual y en la mejor solución encontrada hasta el momento.
- `rng`: instancia aislada `random.Random(semilla)` para no interferir con el estado global del módulo `random`.

### 2.3. Pseudocódigo

```text
Algoritmo Mochila_Randomizada(elementos, W, T, k, semilla):
    Validar W >= 0, T >= 1, k >= 1
    Si W == 0 o elementos está vacío:
        Devolver (0, 0, [])

    candidatos <- [(w, v) para cada (w, v) en elementos si 0 < w <= W y v > 0]
    Si candidatos está vacío:
        Devolver (0, 0, [])

    Ordenar candidatos descendentemente por (v / w, v)
    n <- longitud(candidatos)
    Inicializar generador rng con semilla

    mejor_beneficio <- 0
    mejor_peso <- 0
    mejor_seleccion <- []

    Para iter = 1 hasta T:
        copia <- copia de candidatos
        peso <- 0
        beneficio <- 0
        seleccion <- []

        Para i = 0 hasta n - 1:
            limite <- min(i + k - 1, n - 1)
            j <- entero aleatorio uniforme en [i, limite]
            Intercambiar copia[i] con copia[j]
            (w, v) <- copia[i]

            Si peso + w <= W:
                Agregar (w, v) a seleccion
                peso <- peso + w
                beneficio <- beneficio + v

        Si beneficio > mejor_beneficio:
            mejor_beneficio <- beneficio
            mejor_peso <- peso
            mejor_seleccion <- seleccion

    Devolver (mejor_beneficio, mejor_peso, mejor_seleccion)
```

---

## 3. Seguimiento con un Set de Datos Reducido

Consideremos una instancia pequeña con capacidad $W = 7$ y 4 ítems ya ordenados por ratio $v_i / w_i$ descendente:

| Índice | Ítem $(w, v)$ | Ratio $v/w$ |
|---|---|---|
| `0` | $(2, 4)$ | $2.00$ |
| `1` | $(3, 5)$ | $1.67$ |
| `2` | $(4, 6)$ | $1.50$ |
| `3` | $(5, 7)$ | $1.40$ |

- **Greedy determinístico:** toma $(2, 4)$ y $(3, 5)$ (peso $5$, beneficio $9$). El siguiente $(4, 6)$ no entra (pasa a ser elemento crítico, con valor $6 < 9$). **Resultado Greedy = 9**.
- **Óptimo exacto (PD):** $(3, 5) + (4, 6)$ o $(2, 4) + (5, 7)$, ambos con peso $7$ y **beneficio óptimo = 11**.

Ejecutando `mochila_randomizada` con $T = 5$, ventana $k = 3$ y `semilla = 42`:

| Iteración | Elecciones aleatorias $(i \to j)$ | Ítems evaluados | Entra | Peso | Beneficio | Mejor hasta el momento |
|---|---|---|---|---|---|---|
| 1 | `0->2`, `1->1`, `2->2`, `3->3` | `(4,6)`, `(3,5)`, `(2,4)`, `(5,7)` | Sí, Sí, No, No | 7 | **11** | **11** |
| 2 | `0->0`, `1->1`, `2->2`, `3->3` | `(2,4)`, `(3,5)`, `(4,6)`, `(5,7)` | Sí, Sí, No, No | 5 | 9 | 11 |
| 3 | `0->2`, `1->3`, `2->2`, `3->3` | `(4,6)`, `(5,7)`, `(2,4)`, `(3,5)` | Sí, No, Sí, No | 6 | 10 | 11 |
| 4 | `0->0`, `1->1`, `2->2`, `3->3` | `(2,4)`, `(3,5)`, `(4,6)`, `(5,7)` | Sí, Sí, No, No | 5 | 9 | 11 |
| 5 | `0->0`, `1->3`, `2->2`, `3->3` | `(2,4)`, `(5,7)`, `(4,6)`, `(3,5)` | Sí, Sí, No, No | 7 | **11** | 11 |

En la propia primera iteración, la ventana $k=3$ permite elegir `(4, 6)` en lugar de `(2, 4)` y combinarlo luego con `(3, 5)`, alcanzando el óptimo $11$ que el Greedy determinístico no lograba ver.

---

## 4. Análisis de Complejidad

### 4.1. Complejidad Temporal

Analizando el pseudocódigo paso a paso sobre $n$ ítems:

1. **Prefiltrado:** recorrer los $n$ ítems para filtrar factibles toma $O(n)$.
2. **Ordenamiento inicial:** ordenar hasta $n$ candidatos por ratio toma $O(n \log n)$ (se ejecuta **una sola vez**).
3. **Bucle de $T$ iteraciones:**
   - Copiar `candidatos` toma $O(n)$.
   - El bucle interno recorre $i = 0 \dots n-1$. En cada paso calcula `min`, genera un entero aleatorio en $O(1)$, realiza un intercambio en $O(1)$ y verifica la capacidad en $O(1)$. Por lo tanto, cada iteración completa toma $O(n)$.
   - Actualizar la mejor solución toma $O(1)$ (copia de referencia de la lista ya construida).
   - Total de las $T$ iteraciones: $O(T \cdot n)$.

Sumando todas las etapas:

$$T_{\text{total}}(n, T) = O(n \log n + T \cdot n)$$

Para un número de iteraciones constante ($T = 50$), la complejidad asintótica respecto de $n$ es **$O(n \log n)$**, aunque en el rango práctico $n \in [10, 1000]$ el término lineal $T \cdot n = 50n$ domina sobre $n \log_2 n \le 10n$.

### 4.2. Complejidad Espacial

- `candidatos`: $O(n)$.
- `copia`: $O(n)$ (se reutiliza o reemplaza en cada iteración, sin acumularse entre iteraciones).
- `seleccion` y `mejor_seleccion`: a lo sumo $O(n)$ cada una.

Por lo tanto, la complejidad espacial total es **$O(n)$**, independiente de la capacidad $W$ de la mochila.

---

## 5. Sets de Datos y Criterios de Selección

Se utilizaron las 15 instancias estándar de `tp02/Mochilas/` generadas con `tp02/crear_mochila.py`:
- Tamaños: $n \in \{10, 15, 20, 25, 30, 40, 100, 200, 300, 400, 500, 600, 700, 800, 1000\}$.
- Criterios de generación: capacidad $W = 50n$, pesos aleatorios enteros en $[1, 200]$ y beneficios enteros en $[1, 1000]$.
- Al reutilizar exactamente los mismos sets del TP1 y del Problema 1/2 del TP2, la comparación contra Greedy (Ej 2 TP1) y Programación Dinámica tradicional (Ej 3A TP1) es directa y consistente.

---

## 6. Resultados Experimentales y Gráficos

Las mediciones se ejecutaron con `tp02/Problema_03/problema_03.py` usando $T = 50$, $k = 3$ y `semilla = 42` (promedio de 5 corridas para Randomizado y Greedy; 3 corridas para PD en $n \le 100$ y 1 corrida en $n > 100$). Los datos completos se encuentran en `tp02/Problema_03/resultados/resultados_problema_03.csv`.

| $n$ | $W$ | Randomizado | Greedy (TP1) | Óptimo PD (TP1) | % Ópt. Rand | % Ópt. Greedy | Mejora vs Greedy | $t_{\text{rand}}$ (s) | $t_{\text{greedy}}$ (s) | $t_{\text{PD}}$ (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 500 | 4526 | 4328 | 4526 | 100.00% | 95.63% | +198 | 0.000270 | 0.000004 | 0.000407 |
| 15 | 750 | 4495 | 4495 | 4495 | 100.00% | 100.00% | 0 | 0.000444 | 0.000007 | 0.001011 |
| 20 | 1000 | 9940 | 9940 | 9940 | 100.00% | 100.00% | 0 | 0.000495 | 0.000006 | 0.001792 |
| 25 | 1250 | 12497 | 12483 | 12497 | 100.00% | 99.89% | +14 | 0.000638 | 0.000008 | 0.002874 |
| 30 | 1500 | 10901 | 10771 | 10901 | 100.00% | 98.81% | +130 | 0.000720 | 0.000009 | 0.004171 |
| 40 | 2000 | 17020 | 16899 | 17020 | 100.00% | 99.29% | +121 | 0.000966 | 0.000018 | 0.007634 |
| 100 | 5000 | 41688 | 41688 | 41688 | 100.00% | 100.00% | 0 | 0.002454 | 0.000034 | 0.050119 |
| 200 | 10000 | 84580 | 84566 | 84580 | 100.00% | 99.98% | +14 | 0.005080 | 0.000063 | 0.200589 |
| 300 | 15000 | 116760 | 116760 | 116760 | 100.00% | 100.00% | 0 | 0.007575 | 0.000097 | 0.450889 |
| 400 | 20000 | 160221 | 160221 | 160221 | 100.00% | 100.00% | 0 | 0.010966 | 0.000132 | 0.832195 |
| 500 | 25000 | 198651 | 198589 | 198651 | 100.00% | 99.97% | +62 | 0.012522 | 0.000183 | 1.275662 |
| 600 | 30000 | 255385 | 255385 | 255388 | 99.9988% | 99.9988% | 0 | 0.015475 | 0.000211 | 1.828946 |
| 700 | 35000 | 292586 | 292484 | 292586 | 100.00% | 99.97% | +102 | 0.017628 | 0.000321 | 2.615983 |
| 800 | 40000 | 330659 | 330621 | 330664 | 99.9985% | 99.99% | +38 | 0.021080 | 0.000287 | 3.415720 |
| 1000 | 50000 | 395615 | 395601 | 395621 | 99.9985% | 99.99% | +14 | 0.026047 | 0.000372 | 5.361269 |

### Gráficos generados

- `tp02/Problema_03/graficos/tiempos_randomizado_ajuste.png`: curva de tiempos reales del algoritmo randomizado frente a la curva teórica ajustada $c \cdot (n \log_2 n + T \cdot n)$ ($c = 4.353 \times 10^{-7}$, **$R^2 = 0.999022$**).
- `tp02/Problema_03/graficos/comparacion_tiempos.png`: comparación de tiempos de ejecución (en escala lineal y logarítmica) entre Randomizado, Greedy y Programación Dinámica.
- `tp02/Problema_03/graficos/comparacion_calidad.png`: comparación del porcentaje del óptimo alcanzado por Randomizado frente a Greedy.

---

## 7. Informe de Resultados y Conclusiones

1. **Correspondencia con la complejidad teórica:**
   - El ajuste por mínimos cuadrados del tiempo medido contra la función teórica $n \log_2 n + T \cdot n$ arroja un coeficiente de determinación **$R^2 = 0.9990$**, confirmando una correspondencia casi exacta entre la complejidad deducida en el análisis del pseudocódigo y el comportamiento empírico.
   - A medida que $n$ crece de $100$ a $1000$ (10x), el tiempo de ejecución pasa de $0.002454\text{ s}$ a $0.026047\text{ s}$ (~10.6x), reflejando el comportamiento esperado donde el término $T \cdot n$ domina en este rango junto al aporte suave de $n \log n$.

2. **Comparación frente a Greedy (Ej 2 del TP1):**
   - **Calidad de solución:** el algoritmo randomizado **iguala o supera a Greedy en las 15 instancias evaluadas**. En 8 de ellas obtiene una mejora estricta (destacándose $n=10$ con +198, donde Greedy alcanzaba 95.63% del óptimo y el randomizado alcanza el 100%, y $n=30, 40, 700$ con mejoras de +130, +121 y +102).
   - **Tiempo de ejecución:** Greedy realiza una sola pasada tras ordenar ($O(n \log n)$), por lo que es ~60x a 70x más rápido que el randomizado con $T = 50$ ($0.000372\text{ s}$ vs. $0.026047\text{ s}$ en $n=1000$). Sin embargo, ambos algoritmos se mantienen en el orden de las decenas de milisegundos incluso para $n=1000$.

3. **Comparación frente a Programación Dinámica tradicional (Ej 3A del TP1):**
   - **Calidad de solución:** el algoritmo randomizado alcanza el **100% del óptimo exacto en 12 de las 15 instancias**, y en las 3 restantes ($n=600, 800, 1000$) queda a apenas 3, 5 y 6 unidades del óptimo respectivamente (más del **99.998%** del óptimo).
   - **Tiempo de ejecución:** al tener complejidad pseudopolinomial $O(n \cdot W)$ con $W = 50n$, la PD escala cuadráticamente ($O(n^2)$) en estas instancias y demora **$5.361\text{ s}$** para $n=1000$, mientras que el algoritmo randomizado resuelve la misma instancia en **$0.026\text{ s}$** (**~206 veces más rápido**) con una pérdida de beneficio de apenas $0.0015\%$.

En conclusión, el enfoque Monte Carlo basado en Greedy aleatorizado con ventana $k=3$ y $T=50$ iteraciones logra un equilibrio muy favorable: mejora de forma consistente la calidad del Greedy determinístico manteniendo tiempos prácticamente despreciables frente a Programación Dinámica y un uso de memoria $O(n)$ independiente de $W$.
