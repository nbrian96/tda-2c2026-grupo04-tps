# Trabajo Práctico N°2 – Teoría de Algoritmos (TB024)

**Institución:** Universidad de Buenos Aires – Facultad de Ingeniería (FIUBA)  
**Cátedra:** Lic. Pablo Echevarría  
**Cuatrimestre:** 2do Cuatrimestre 2026  
**Grupo:** 4

| Alumno | Padrón |
|---|---:|
| González Hidalgo, Eduardo Eliezer | 110006 |
| Nelson Avila | 100244 |

---

## Índice

1. [Problema 1 – Algoritmos aproximados (Sahni)](#1-problema-1--algoritmos-aproximados-sahni)
2. [Problema 2 – Algoritmo arbitrariamente bueno (FPTAS)](#2-problema-2--algoritmo-arbitrariamente-bueno-fptas)
3. [Problema 3 – Algoritmos randomizados (Monte Carlo)](#3-problema-3--algoritmos-randomizados-monte-carlo)
4. [Problema 4 – Conclusiones](#4-problema-4--conclusiones)
5. [Lenguaje e instrucciones de ejecución](#5-lenguaje-e-instrucciones-de-ejecución)

---

## 1. Problema 1 – Algoritmos aproximados (Sahni)

### 1.1. Enunciado

Diseñar e implementar un algoritmo que resuelva el problema de la mochila en forma aproximada mediante el **algoritmo de Sahni (1975)** visto en clase. Ejecutarlo en instancias de diferentes tamaños y, para cada instancia, calcular:
- La cota superior planteada por la relajación lineal.
- La cota superior planteada por Martello y Toth.
- La solución óptima exacta por alguno de los métodos vistos en el TP1.

Comparar los cuatro resultados obtenidos.

### 1.2. Planteo, supuestos y notación

Partimos de $n$ elementos, cada uno con un beneficio (valor) $p_i > 0$ y un peso $w_i > 0$, y una mochila de capacidad máxima $c$. Se supone que $p_i$, $w_i$ y $c$ son enteros, que $w_i \le c$ para todo $i$ (los elementos que no cumplan se descartan, ya que no pueden pertenecer a ninguna solución) y que $\sum_{i=1}^{n} w_i > c$ (de lo contrario entran todos los elementos y el problema es trivial) (Martello & Toth, 1990, Sec. 2.1, p. 14). El parámetro $k$ del esquema ($0 \le k \le n$) se fija en $k = 1$ para las pruebas experimentales.

Lo primero que se hace es ordenar los elementos por densidad de valor de forma decreciente:

$$\frac{p_1}{w_1} \ge \frac{p_2}{w_2} \ge \dots \ge \frac{p_n}{w_n}$$

### 1.3. Elemento crítico y garantía de calidad

Si metemos los elementos en orden hasta que alguno ya no entre:
- Los elementos $1, 2, \dots, s-1$ entran completos.
- El elemento $s$ es el primer elemento que ya no entra debido a que $w_s > \text{capacidad restante}$. A este elemento lo llamamos *elemento crítico* (Martello & Toth, 1990, Sec. 2.2.1, p. 16).
- La capacidad sobrante antes de meter a $s$ es:

$$\bar{c} = c - \sum_{i=1}^{s-1} w_i$$

**Garantía de calidad:** si llamamos $z^*$ a la solución óptima, $z'$ a la solución del greedy básico y $p_c$ al beneficio del elemento crítico, siempre se cumple que $z^* < z' + p_c$. Por lo tanto, un algoritmo que devuelva $z'' = \max(z', p_c)$ garantiza estar al menos al $50\%$ del valor óptimo.

### 1.4. Cotas superiores para evaluar una solución particular

Cuando ejecutamos un algoritmo aproximado sobre una instancia concreta y no conocemos el óptimo $z^*$, necesitamos cotas superiores para saber qué tan lejos del óptimo puede estar nuestra solución particular.

#### Primera cota superior: relajación lineal ($U_1$)

Consiste en resolver el modelo de programación lineal del problema de la mochila eliminando la restricción de que las variables sean binarias ($x_i \in \{0,1\}$) y permitiendo que sean continuas:

$$\max \sum_{i=1}^{n} p_i x_i \quad \text{s.a.} \quad \sum_{i=1}^{n} w_i x_i \le c, \qquad 0 \le x_i \le 1$$

Al estar los elementos ordenados por $p_i/w_i$, la solución óptima de la relajación lineal incluye enteros los primeros $s-1$ elementos y llena exactamente la capacidad residual $\bar{c}$ con una fracción del elemento crítico $s$. Al ser los datos enteros, la cota entera se redondea por defecto:

$$z_{\text{cont}} = \sum_{i=1}^{s-1} p_i + \bar{c}\,\frac{p_s}{w_s}, \qquad U_1 = \sum_{i=1}^{s-1} p_i + \left\lfloor \frac{\bar{c}\, p_s}{w_s} \right\rfloor$$

#### Segunda cota superior: Martello y Toth ($U_2$)

Martello y Toth (1990, Teorema 2.1, pp. 16–17) mejoraron la cota de la relajación lineal observando que, en el problema entero, el elemento crítico no puede fraccionarse: o bien no se incluye ($x_s = 0$) o bien se incluye entero ($x_s = 1$).

- **1.ª alternativa (el elemento crítico $s$ no se incluye):** la capacidad residual $\bar{c}$ se rellena de forma fraccionaria con el mejor elemento disponible después de $s$, que es el elemento $s+1$:

$$W_1 = \sum_{i=1}^{s-1} p_i + \left\lfloor \bar{c}\,\frac{p_{s+1}}{w_{s+1}} \right\rfloor$$

- **2.ª alternativa (el elemento crítico $s$ sí se incluye):** se suma $p_s$ y se quita fraccionariamente el peso faltante $(w_s - \bar{c})$ del peor elemento incluido antes, que es el $s-1$:

$$W_2 = \sum_{i=1}^{s-1} p_i + \left\lfloor p_s - (w_s - \bar{c})\,\frac{p_{s-1}}{w_{s-1}} \right\rfloor$$

La cota de Martello y Toth toma el máximo: $U_2 = \max(W_1, W_2)$.

**Casos borde y relación entre cotas:** si $s = n$, $W_1 = \sum_{i=1}^{s-1} p_i$. Si $s = 1$, $W_2 = 0$ (o $p_s$ si $w_s \le c$). Si todos los elementos entran, ambas cotas valen $\sum_{i=1}^{n} p_i$. Siempre se verifica $z^* \le U_2 \le U_1$ (Martello & Toth, 1990, Teorema 2.2, pp. 20–21).

### 1.5. Esquema de aproximación polinomial de Sahni (1975)

#### Diseño, estructuras de datos y pseudocódigo

En la implementación (`tp02/Problema_01/`), cada ítem se representa como un diccionario con claves `id`, `beneficio`, `peso` e `indice` ($p_j / w_j$), ordenados en una lista `items_ordenados`. Los subconjuntos obligatorios $M$ se generan mediante `itertools.combinations` como conjuntos `indices_M` de posiciones.

```text
FUNCION procedimiento_gs(items_ordenados, c, M):
    z_g <- 0
    X <- []
    c_sombrero <- c - suma(items_ordenados[j].peso para j en M)
    PARA j <- 0 HASTA n - 1 HACER
        SI j NO EN M Y items_ordenados[j].peso <= c_sombrero ENTONCES
            z_g <- z_g + items_ordenados[j].beneficio
            c_sombrero <- c_sombrero - items_ordenados[j].peso
            AGREGAR j A X
        FIN SI
    FIN PARA
    RETORNAR (z_g, X)

FUNCION algoritmo_sahni(items_ordenados, c, k):
    z_h <- 0
    x_h <- []
    PARA tam <- 0 HASTA min(k, n) HACER
        PARA CADA combinacion M DE tam posiciones EN {0..n-1} HACER
            SI peso(M) <= c ENTONCES
                (z_g, X) <- procedimiento_gs(items_ordenados, c, M)
                SI z_g + beneficio(M) > z_h ENTONCES
                    z_h <- z_g + beneficio(M)
                    x_h <- M U X
                FIN SI
            FIN SI
        FIN PARA
    FIN PARA
    RETORNAR (z_h, ids(x_h))
```

#### Seguimiento con un set de datos reducido

Consideremos $n = 4$ ítems y capacidad $c = 7$, ya ordenados por $p_j / w_j$: ítem 1 $(w=2, p=4)$, ítem 2 $(w=3, p=5)$, ítem 3 $(w=4, p=6)$ e ítem 4 $(w=5, p=7)$.

- **Elemento crítico y cotas:** entran los ítems 1 y 2 ($w=5, p=9, \bar{c}=2$). El ítem 3 ($w=4, p=6$) es crítico ($s=2$ en base 0). Resulta $U_1 = 9 + \lfloor 2 \cdot 6 / 4 \rfloor = 12$ y $U_2 = \max(9 + \lfloor 2 \cdot 7 / 5 \rfloor,\; 9 + \lfloor 6 - 2 \cdot 5 / 3 \rfloor) = \max(11, 11) = 11$.
- **Ejecución de Sahni ($k = 1$):**
  - $M = \emptyset$: GS elige $\{1, 2\} \Rightarrow z_h = 9$.
  - $M = \{1\}$: GS agrega $\{2\} \Rightarrow 4 + 5 = 9$.
  - $M = \{2\}$: GS agrega $\{1\} \Rightarrow 5 + 4 = 9$.
  - $M = \{3\}$: GS agrega $\{1\} \Rightarrow 6 + 4 = 10$ (actualiza $z_h = 10$).
  - $M = \{4\}$: GS agrega $\{1\} \Rightarrow 7 + 4 = 11$ (actualiza $z_h = 11$).
- **Resultado:** $z^h = 11$ (coincide con el óptimo exacto y verifica $11 \le U_2 = 11 \le U_1 = 12$).

#### Complejidad y garantía de calidad

La cantidad de subconjuntos posibles de tamaño hasta $k$ es del orden $O(n^k)$. Por cada subconjunto hay que ejecutar el ciclo de GS recorriendo los $n$ elementos, que toma $O(n)$ (Martello & Toth, 1990, Teorema 2.3, p. 51). Por lo tanto, la complejidad temporal total es **$O(n^{k+1})$** (para $k = 1$, **$O(n^2)$**), y el espacio adicional es **$O(n)$**. El esquema garantiza $z^h \ge \frac{k}{k+1}\, z^*$ (Sahni, 1975).

### 1.6. Sets de datos, resultados y análisis

Se utilizaron las 15 instancias estándar de `tp02/Mochilas/` ($n \in [10, 1000]$, $c = 50n$, $w_i \in [1, 200]$, $p_i \in [1, 1000]$) generadas con `tp02/crear_mochila.py`.

| $n$ | $c$ | Sahni ($k=1$) | Óptimo (PD) | Cota MT ($U_2$) | Cota RL ($U_1$) | Tiempo (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 500 | 4526 | 4526 | 4661 | 4662 | 0.000080 |
| 15 | 750 | 4495 | 4495 | 4562 | 4571 | 0.000122 |
| 20 | 1000 | 9940 | 9940 | 10018 | 10036 | 0.000178 |
| 25 | 1250 | 12497 | 12497 | 12610 | 12652 | 0.000237 |
| 30 | 1500 | 10808 | 10901 | 11037 | 11053 | 0.000268 |
| 40 | 2000 | 16932 | 17020 | 17121 | 17136 | 0.000463 |
| 100 | 5000 | 41688 | 41688 | 41695 | 41695 | 0.002209 |
| 200 | 10000 | 84575 | 84580 | 84608 | 84609 | 0.009986 |
| 300 | 15000 | 116760 | 116760 | 116778 | 116778 | 0.019865 |
| 400 | 20000 | 160221 | 160221 | 160232 | 160232 | 0.034525 |
| 500 | 25000 | 198639 | 198651 | 198665 | 198665 | 0.052175 |
| 600 | 30000 | 255385 | 255388 | 255398 | 255400 | 0.077702 |
| 700 | 35000 | 292575 | 292586 | 292588 | 292589 | 0.101982 |
| 800 | 40000 | 330637 | 330664 | 330667 | 330667 | 0.137698 |
| 1000 | 50000 | 395613 | 395621 | 395624 | 395624 | 0.217418 |

![Tiempos Sahni vs ajuste O(n^2)](../Problema_01/graficos/tiempos_sahni_ajuste_O_n2.png)

**Análisis de resultados:** en todas las instancias se verificó $z^h \le z^* \le U_2 \le U_1$, siendo $U_2$ igual o más ajustada que $U_1$. El algoritmo alcanzó el óptimo exacto en 8 de las 15 instancias y nunca cayó por debajo del $99.1\%$ del óptimo (muy por encima de la cota teórica del $50\%$ para $k=1$). El ajuste de tiempos contra $t(n) = c \cdot n^2$ obtuvo $c = 2.153559 \times 10^{-7}$ y **$R^2 = 0.999628$**, confirmando el comportamiento cuadrático deducido teóricamente.

---

## 2. Problema 2 – Algoritmo arbitrariamente bueno (FPTAS)

### 2.1. Supuestos, condiciones y limitaciones

El algoritmo implementado (`tp02/Problema_02/fptas.py`) resuelve el Problema de la Mochila 0-1 bajo las siguientes premisas:
1. **Dominio de entrada:** capacidad entera no negativa $W \in \mathbb{Z}_{\ge 0}$ y $n$ ítems con $w_i \in \mathbb{Z}^+$ y $v_i \in \mathbb{Z}^+$.
2. **Prefiltrado previo de factibilidad:** se descartan todos los ítems con $w_i > W$ o $v_i \le 0$ antes de calcular $v^* = \max_i v_i$, garantizando que $v^* \le OPT$.
3. **Condición sobre $\varepsilon$:** debe cumplirse $\varepsilon \in (0, 1]$ y $k = 1/\varepsilon \in \mathbb{Z}^+$ (por ejemplo, $\varepsilon \in \{1.0, 0.5, 0.25, 0.2, 0.1, 0.05\}$).
4. **Limitación práctica (umbral $b \le 1$):** el factor de escala es $b = \frac{\varepsilon}{2n} \cdot v^*$. Cuando $v^*$ es pequeño respecto de $n$ (como en el set estándar donde $v_i \in [1, 1000]$), a partir de $n \ge \frac{\varepsilon \cdot v^*}{2}$ resulta $b \le 1$, por lo que el reescalado deja de comprimir el dominio de beneficios y permite verificar el crecimiento $O(n^3 \varepsilon^{-1})$.

### 2.2. Diseño, estructuras de datos y pseudocódigo

Se utilizan: la lista `escalados` de tuplas `(peso, beneficio_original, v_hat)` con aritmética entera exacta `(2 * n * k * v + v_max - 1) // v_max`, y dos arreglos unidimensionales de longitud $V_{\max} + 1$: `dp` (peso mínimo para lograr beneficio escalado $V$) y `beneficio_real` (beneficio original asociado).

```text
FUNCION Mochila_FPTAS(elementos, W, epsilon):
    VALIDAR W >= 0, epsilon en (0, 1], k = 1/epsilon entero positivo
    candidatos <- [(w, v) para (w, v) en elementos si 0 < w <= W y v > 0]
    SI candidatos está vacío ENTONCES DEVOLVER (0, 0)

    n <- longitud(candidatos)
    v_max <- max(v para (_, v) en candidatos)
    PARA CADA (w, v) en candidatos HACER
        v_hat <- techo((2 * n * k * v) / v_max)
    FIN PARA
    V_max <- suma(v_hat)

    dp[0] <- 0; dp[1..V_max] <- W + 1
    beneficio_real[0..V_max] <- 0
    v_acum <- 0
    PARA CADA (w, v, v_hat) en escalados HACER
        v_acum <- v_acum + v_hat
        PARA V <- v_acum bajando hasta v_hat HACER
            SI dp[V - v_hat] + w < dp[V] ENTONCES
                dp[V] <- dp[V - v_hat] + w
                beneficio_real[V] <- beneficio_real[V - v_hat] + v
            FIN SI
        FIN PARA
    FIN PARA

    PARA V <- V_max bajando hasta 0 HACER
        SI dp[V] <= W ENTONCES DEVOLVER (beneficio_real[V], dp[V])
    FIN PARA
    DEVOLVER (0, 0)
```

**Garantía de calidad $(1 + \varepsilon)$:** si $\tilde{v}_i = \hat{v}_i \cdot b$, entonces $v_i \le \tilde{v}_i < v_i + b$. Con $n b = \frac{\varepsilon}{2} v^*$ y $\sum_{i \in S} v_i \ge \frac{1}{2} v^*$, resulta $OPT = \sum_{i \in S^*} v_i \le (1 + \varepsilon) \sum_{i \in S} v_i$.

### 2.3. Seguimiento con set de datos reducido

Sea $n = 4$, $W = 10$, $\varepsilon = 0.5$ ($k = 2$) con ítems $(4, 300)$, $(5, 420)$, $(6, 510)$ y $(8, 800)$. Resulta $v^* = 800$, $b = \frac{0.5}{8} \cdot 800 = 50$, valores escalados $\hat{v} = [6, 9, 11, 16]$ y $V_{\max} = 42$:
- $i=1\;(w=4, \hat{v}=6)$: `dp[6]=4`.
- $i=2\;(w=5, \hat{v}=9)$: `dp[6]=4`, `dp[9]=5`, `dp[15]=9`.
- $i=3\;(w=6, \hat{v}=11)$: se agrega `dp[11]=6`, `dp[17]=10` (beneficio real `810`), `dp[20]=11`, `dp[26]=15`.
- $i=4\;(w=8, \hat{v}=16)$: agrega `dp[16]=8` (`800`) y combinaciones mayores con peso $> 10$.

El mayor $V$ con `dp[V] <= 10` es $V^* = 17$ (`peso = 10`, `beneficio_real = 810`), que coincide con el óptimo exacto y cumple $810 \le 1.5 \cdot 810$.

### 2.4. Complejidad temporal y espacial

Cada $\hat{v}_i \le \lceil 2n/\varepsilon \rceil = O(n \varepsilon^{-1})$, por lo que $V_{\max} = \sum_{i=1}^n \hat{v}_i = O(n^2 \varepsilon^{-1})$. El bucle externo corre $n$ veces y el interno recorre a lo sumo $V_{\max}$ columnas en $O(1)$, resultando:

$$T(n, \varepsilon) = O(n^3 \varepsilon^{-1}), \qquad S(n, \varepsilon) = O(V_{\max}) = O(n^2 \varepsilon^{-1})$$

Para $\varepsilon$ fijo es polinomial en $n$ ($O(n^3)$), mientras que crece linealmente con $1/\varepsilon$.

### 2.5. Sets de datos, mediciones y análisis

Se evaluaron instancias estándar de `tp02/Mochilas/` ($n \in \{10,15,20,25,30,40,100,200\}$) junto con instancias intermedias en `tp02/Problema_02/sets_datos/intermedios/` ($n \in \{60,80,120,150,180\}$, semilla `42 + n`) para cubrir la curva cúbica.

#### Experimento 1 – Variando $n$ con $\varepsilon \in \{1.0, 0.5\}$

| $n$ | $W$ | FPTAS ($\varepsilon=1.0 / 0.5$) | Óptimo (PD) | Gap Relativo | Tiempo $\varepsilon=1.0$ (s) | Tiempo $\varepsilon=0.5$ (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 500 | 4526 / 4526 | 4526 | 0.000000 | 0.000064 | 0.000077 |
| 15 | 750 | 4495 / 4495 | 4495 | 0.000000 | 0.000112 | 0.000204 |
| 20 | 1000 | 9940 / 9940 | 9940 | 0.000000 | 0.000350 | 0.000842 |
| 25 | 1250 | 12497 / 12497 | 12497 | 0.000000 | 0.000695 | 0.001406 |
| 30 | 1500 | 10901 / 10901 | 10901 | 0.000000 | 0.001087 | 0.002311 |
| 40 | 2000 | 17020 / 17020 | 17020 | 0.000000 | 0.002964 | 0.006339 |
| 60 | 3000 | 25198 / 25198 | 25198 | 0.000000 | 0.010147 | 0.021001 |
| 80 | 4000 | 31854 / 31854 | 31854 | 0.000000 | 0.022967 | 0.054605 |
| 100 | 5000 | 41688 / 41688 | 41688 | 0.000000 | 0.048734 | 0.091803 |
| 120 | 6000 | 51189 / 51189 | 51189 | 0.000000 | 0.077979 | 0.157022 |
| 150 | 7500 | 56588 / 56588 | 56589 | 0.000018 | 0.141687 | 0.311378 |
| 180 | 9000 | 76461 / 76461 | 76461 | 0.000000 | 0.331143 | 0.571270 |
| 200 | 10000 | 84580 / 84580 | 84580 | 0.000000 | 0.412545 | 0.880093 |

![FPTAS tiempos vs n ajuste O(n^3)](../Problema_02/graficos/tiempos_vs_n_ajuste_O_n3.png)

#### Experimento 2 – Variando $\varepsilon$ con $n \in \{20, 40, 100\}$

| $n$ | $\varepsilon \in \{1.0, 0.5, 0.25, 0.2, 0.1, 0.05\}$ ($k=1/\varepsilon$) | FPTAS / Óptimo | Tiempos (s) |
|---:|---|---|---|
| 20 | $k \in \{1, 2, 4, 5, 10, 20\}$ | 9940 / 9940 (todas) | 0.000362 / 0.000742 / 0.001731 / 0.001938 / 0.004000 / 0.009032 |
| 40 | $k \in \{1, 2, 4, 5, 10, 20\}$ | 17020 / 17020 (todas) | 0.004344 / 0.007161 / 0.014917 / 0.015744 / 0.035013 / 0.063434 |
| 100 | $k \in \{1, 2, 4, 5, 10, 20\}$ | 41688 / 41688 (todas) | 0.042813 / 0.090613 / 0.217342 / 0.248440 / 0.514531 / 1.252074 |

![FPTAS tiempos vs 1/epsilon ajuste lineal](../Problema_02/graficos/tiempos_vs_inv_epsilon_ajuste_lineal.png)

**Análisis de resultados:** los ajustes empíricos confirman la complejidad teórica $O(n^3 \varepsilon^{-1})$: $R^2 = 0.993532$ ($\varepsilon=0.5$) y $R^2 = 0.990636$ ($\varepsilon=1.0$) al variar $n$, con relación de pendientes $\approx 2.00$; y $R^2 \in [0.986016, 0.994257]$ al variar $1/\varepsilon$. En las 44 ejecuciones se cumplió la cota $(1+\varepsilon)$, obteniendo el óptimo exacto en 42 casos y un desvío de 1 unidad ($0.0018\%$) en $n=150$.

---

## 3. Problema 3 – Algoritmos randomizados (Monte Carlo)

### 3.1. Supuestos y clasificación

El algoritmo implementado (`tp02/Problema_03/randomizado.py`) es un **Greedy Aleatorizado con ventana $k$ y multi-arranque ($T$ iteraciones)**:
1. Capacidad entera $W \ge 0$ e ítems con $w_i, v_i \in \mathbb{Z}^+$, prefiltrando $0 < w_i \le W$.
2. **Enfoque Monte Carlo:** tiempo polinomial y acotado por $T$; siempre devuelve una solución factible ($\sum w_i \le W$), aunque puede no alcanzar el óptimo global con cierta probabilidad.
3. **Reproducibilidad:** generador pseudoaleatorio `random.Random(semilla)` con `semilla = 42`, $T = 50$ y $k = 3$ por defecto.

### 3.2. Fundamentación del uso del azar

El Greedy determinístico puede quedar atrapado en decisiones subóptimas cuando un ítem de buen ratio bloquea combinaciones mejores. Para superar esa rigidez:
- **Perturbación local (ventana $k$):** partiendo de los ítems ordenados por ratio $v_i/w_i$ descendente, en cada paso $i$ se elige al azar un índice $j \in [i, \min(i+k-1, n-1)]$ y se intercambian, explorando soluciones cercanas al orden voraz.
- **Multi-arranque ($T$ ensayos):** si un ensayo tiene probabilidad $p > 0$ de hallar una solución de alta calidad, la probabilidad de fallar en $T$ ensayos independientes cae exponencialmente a $(1 - p)^T$ mientras el tiempo crece linealmente en $T$.

### 3.3. Diseño, estructuras de datos y pseudocódigo

Se utilizan las listas `candidatos` (ordenada una vez por $v/w$), `copia` (para permutar localmente en cada ensayo), `seleccion` y `mejor_seleccion`.

```text
FUNCION Mochila_Randomizada(elementos, W, T, k, semilla):
    VALIDAR W >= 0, T >= 1, k >= 1
    candidatos <- [(w, v) para (w, v) en elementos si 0 < w <= W y v > 0]
    SI candidatos está vacío ENTONCES DEVOLVER (0, 0, [])

    ORDENAR candidatos descendentemente por (v / w, v)
    n <- longitud(candidatos); INICIALIZAR rng(semilla)
    mejor_beneficio <- 0; mejor_peso <- 0; mejor_seleccion <- []

    PARA iter <- 1 HASTA T HACER
        copia <- copia de candidatos; peso <- 0; beneficio <- 0; seleccion <- []
        PARA i <- 0 HASTA n - 1 HACER
            j <- entero aleatorio uniforme en [i, min(i + k - 1, n - 1)]
            INTERCAMBIAR copia[i] CON copia[j]
            (w, v) <- copia[i]
            SI peso + w <= W ENTONCES
                AGREGAR (w, v) A seleccion; peso <- peso + w; beneficio <- beneficio + v
            FIN SI
        FIN PARA
        SI beneficio > mejor_beneficio ENTONCES
            mejor_beneficio <- beneficio; mejor_peso <- peso; mejor_seleccion <- seleccion
        FIN SI
    FIN PARA
    DEVOLVER (mejor_beneficio, mejor_peso, mejor_seleccion)
```

### 3.4. Seguimiento con set de datos reducido

Con $W = 7$ y los ítems $(2,4), (3,5), (4,6), (5,7)$: Greedy determinístico obtiene $9$ (`(2,4)+(3,5)`), mientras el óptimo es $11$. Ejecutando `mochila_randomizada` con $T=5$, $k=3$ y `semilla=42`, ya en la iteración 1 las elecciones `0->2`, `1->1`, `2->2`, `3->3` evalúan `(4,6)` y `(3,5)` primero, alcanzando el óptimo $11$ con peso $7$.

### 3.5. Complejidad temporal y espacial

Ordenar una sola vez toma $O(n \log n)$ y cada una de las $T$ iteraciones recorre $n$ elementos realizando operaciones $O(1)$ ($O(T \cdot n)$). Por lo tanto:

$$T(n, T) = O(n \log n + T \cdot n), \qquad S(n) = O(n)$$

Con $T$ fijo resulta $O(n \log n)$ asintóticamente y linealmente dominado por $T \cdot n$ en el rango analizado.

### 3.6. Resultados y comparación con Greedy y Programación Dinámica

| $n$ | Rand | Greedy | Óptimo PD | % Rand | % Greedy | $t_{\text{rand}}$ (s) | $t_{\text{greedy}}$ (s) | $t_{\text{PD}}$ (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 4526 | 4328 | 4526 | 100.00 | 95.63 | 0.000270 | 0.000004 | 0.000407 |
| 15 | 4495 | 4495 | 4495 | 100.00 | 100.00 | 0.000444 | 0.000007 | 0.001011 |
| 20 | 9940 | 9940 | 9940 | 100.00 | 100.00 | 0.000495 | 0.000006 | 0.001792 |
| 25 | 12497 | 12483 | 12497 | 100.00 | 99.89 | 0.000638 | 0.000008 | 0.002874 |
| 30 | 10901 | 10771 | 10901 | 100.00 | 98.81 | 0.000720 | 0.000009 | 0.004171 |
| 40 | 17020 | 16899 | 17020 | 100.00 | 99.29 | 0.000966 | 0.000018 | 0.007634 |
| 100 | 41688 | 41688 | 41688 | 100.00 | 100.00 | 0.002454 | 0.000034 | 0.050119 |
| 200 | 84580 | 84566 | 84580 | 100.00 | 99.98 | 0.005080 | 0.000063 | 0.200589 |
| 300 | 116760 | 116760 | 116760 | 100.00 | 100.00 | 0.007575 | 0.000097 | 0.450889 |
| 400 | 160221 | 160221 | 160221 | 100.00 | 100.00 | 0.010966 | 0.000132 | 0.832195 |
| 500 | 198651 | 198589 | 198651 | 100.00 | 99.97 | 0.012522 | 0.000183 | 1.275662 |
| 600 | 255385 | 255385 | 255388 | 99.9988 | 99.9988 | 0.015475 | 0.000211 | 1.828946 |
| 700 | 292586 | 292484 | 292586 | 100.00 | 99.97 | 0.017628 | 0.000321 | 2.615983 |
| 800 | 330659 | 330621 | 330664 | 99.9985 | 99.99 | 0.021080 | 0.000287 | 3.415720 |
| 1000 | 395615 | 395601 | 395621 | 99.9985 | 99.99 | 0.026047 | 0.000372 | 5.361269 |

![Randomizado ajuste O(n log n + Tn)](../Problema_03/graficos/tiempos_randomizado_ajuste.png)
![Comparación de tiempos Problema 3](../Problema_03/graficos/comparacion_tiempos.png)
![Comparación de calidad Problema 3](../Problema_03/graficos/comparacion_calidad.png)

**Análisis:** el ajuste contra $n \log_2 n + 50n$ obtuvo $R^2 = 0.999022$ ($c = 4.353151 \times 10^{-7}$). El algoritmo randomizado igualó o superó a Greedy en las 15 instancias (mejora estricta en 8 de ellas, hasta $+198$ en $n=10$), alcanzó el $100\%$ del óptimo en 12 instancias y fue $>200\times$ más rápido que PD en $n=1000$ ($0.026047\text{ s}$ vs. $5.361269\text{ s}$).

---

## 4. Problema 4 – Conclusiones

### 4.1. Metodología de comparación

Para garantizar una comparación justa en igualdad de hardware y entorno, se ejecutaron los **8 algoritmos** de los TPs 1 y 2 desde `tp02/Problema_04/problema_04.py` sobre las mismas 15 instancias de `tp02/Mochilas/` dentro del rango viable de cada uno:
- **Exponenciales:** Fuerza Bruta ($n \le 25$) y Backtracking ($n \le 40$).
- **Pseudopolinomial / Exacto ILP:** Programación Dinámica tradicional ($n \le 1000$) y Programación Lineal Entera ($n \le 1000$, resuelta mediante el mismo modelo binario del TP1 con `scipy.optimize.milp` / HiGHS con `mip_rel_gap = 0.0`).
- **Aproximados y Randomizado:** Greedy ($n \le 1000$), Sahni $k=1$ ($n \le 1000$), FPTAS con $\varepsilon = 0.5$ fijo ($n \le 200$) y Randomizado $T=50, k=3$ ($n \le 1000$).

### 4.2. Comparación de tiempos de ejecución

| $n$ | FB (s) | BT (s) | Greedy (s) | PD (s) | PL (s) | Sahni $k=1$ (s) | FPTAS $\varepsilon=0.5$ (s) | Rand (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 0.000483 | 0.000077 | 0.000005 | 0.000435 | 0.010679 | 0.000033 | 0.000084 | 0.000268 |
| 15 | 0.007684 | 0.001019 | 0.000008 | 0.000966 | 0.006100 | 0.000050 | 0.000213 | 0.000385 |
| 20 | 0.592390 | 0.003616 | 0.000017 | 0.001717 | 0.005169 | 0.000135 | 0.000747 | 0.000776 |
| 25 | 21.199506 | 0.054486 | 0.000018 | 0.003188 | 0.006158 | 0.000129 | 0.001483 | 0.000765 |
| 30 | — | 1.148171 | 0.000033 | 0.004447 | 0.024104 | 0.000297 | 0.002353 | 0.000990 |
| 40 | — | 18.915169 | 0.000018 | 0.008252 | 0.017302 | 0.000221 | 0.006426 | 0.000993 |
| 100 | — | — | 0.000046 | 0.048404 | 0.007097 | 0.001644 | 0.093878 | 0.002496 |
| 200 | — | — | 0.000110 | 0.229571 | 0.056575 | 0.005945 | 0.764692 | 0.005121 |
| 300 | — | — | 0.000154 | 0.452114 | 0.023563 | 0.010822 | — | 0.007590 |
| 400 | — | — | 0.000161 | 0.808499 | 0.087834 | 0.019645 | — | 0.012804 |
| 500 | — | — | 0.000241 | 1.542001 | 0.153121 | 0.039449 | — | 0.017400 |
| 600 | — | — | 0.000245 | 2.356242 | 0.169199 | 0.045157 | — | 0.015179 |
| 700 | — | — | 0.000395 | 3.711331 | 0.160438 | 0.059954 | — | 0.021812 |
| 800 | — | — | 0.000460 | 3.716259 | 0.351301 | 0.096853 | — | 0.030801 |
| 1000 | — | — | 0.000423 | 7.105105 | 0.248014 | 0.124775 | — | 0.026757 |

![Comparación de tiempos de los 8 algoritmos](../Problema_04/graficos/comparacion_tiempos_todos.png)

### 4.3. Calidad de los algoritmos aproximados y cotas superiores

| $n$ | Óptimo | Greedy | Sahni $k=1$ | FPTAS ($\varepsilon=0.5$) | Rand | Cota MT ($U_2$) | Cota RL ($U_1$) | RL Cont. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 4526 | 4328 | 4526 | 4526 | 4526 | 4661 | 4662 | 4662.66 |
| 15 | 4495 | 4495 | 4495 | 4495 | 4495 | 4562 | 4571 | 4571.83 |
| 20 | 9940 | 9940 | 9940 | 9940 | 9940 | 10018 | 10036 | 10036.86 |
| 25 | 12497 | 12483 | 12497 | 12497 | 12497 | 12610 | 12652 | 12652.27 |
| 30 | 10901 | 10771 | 10808 | 10901 | 10901 | 11037 | 11053 | 11053.33 |
| 40 | 17020 | 16899 | 16932 | 17020 | 17020 | 17121 | 17136 | 17136.89 |
| 100 | 41688 | 41688 | 41688 | 41688 | 41688 | 41695 | 41695 | 41695.29 |
| 200 | 84580 | 84566 | 84575 | 84580 | 84580 | 84608 | 84609 | 84609.81 |
| 300 | 116760 | 116760 | 116760 | — | 116760 | 116778 | 116778 | 116778.70 |
| 400 | 160221 | 160221 | 160221 | — | 160221 | 160232 | 160232 | 160232.35 |
| 500 | 198651 | 198589 | 198639 | — | 198651 | 198665 | 198665 | 198665.33 |
| 600 | 255388 | 255385 | 255385 | — | 255385 | 255398 | 255400 | 255400.10 |
| 700 | 292586 | 292484 | 292575 | — | 292586 | 292588 | 292589 | 292589.25 |
| 800 | 330664 | 330621 | 330637 | — | 330659 | 330667 | 330667 | 330667.51 |
| 1000 | 395621 | 395601 | 395613 | — | 395615 | 395624 | 395624 | 395624.89 |

![Comparación de aproximados y cotas](../Problema_04/graficos/comparacion_aproximados_cotas.png)

### 4.4. Análisis global y conclusiones

1. **Inviabilidad de los métodos exponenciales:** Fuerza Bruta ($O(2^n)$) ya tarda $21.20\text{ s}$ en $n=25$; Backtracking con poda mejora sustancialmente el rango pero alcanza $18.92\text{ s}$ en $n=40$. Ninguno escala a cientos de ítems.
2. **Exactos en rango grande (PD vs. PL):** Programación Dinámica ($O(nW) = O(n^2)$ en estas instancias) es exacta pero llega a $7.11\text{ s}$ en $n=1000$. Programación Lineal Entera (Branch-and-Cut en HiGHS) resuelve la misma instancia exacta en $0.248\text{ s}$ ($\approx 28\times$ más rápido que PD), aunque presenta un costo inicial fijo de armado de modelo ($\approx 5\text{–}10\text{ ms}$) en instancias muy chicas.
3. **Compromiso de los algoritmos aproximados:**
   - **Greedy** es el más veloz de todos ($0.00042\text{ s}$ en $n=1000$), pero sufre los mayores desvíos en instancias chicas ($95.63\%$ en $n=10$).
   - **FPTAS ($\varepsilon=0.5$)** garantiza $(1+\varepsilon)$-aproximación y logró el $100\%$ del óptimo en todo su rango ($n \le 200$), pero su complejidad $O(n^3 \varepsilon^{-1})$ lo vuelve más lento que PD a partir de $n \ge 100$ cuando $v^*$ es acotado ($0.765\text{ s}$ en $n=200$).
   - **Sahni ($k=1$)** es cuadrático ($0.125\text{ s}$ en $n=1000$) y mejora sistemáticamente a Greedy sin llegar a ser tan costoso como FPTAS.
   - **Randomizado ($T=50, k=3$)** logró la mejor combinación práctica para instancias grandes: superó a Sahni ($k=1$) tanto en tiempo ($0.0268\text{ s}$ vs. $0.1248\text{ s}$ en $n=1000$) como en calidad (igualó o superó a Sahni en todas las instancias y alcanzó el óptimo en 12 de 15).
4. **Utilidad de las cotas superiores ($U_1$ y $U_2$):** en instancias grandes ($n \ge 100$), ambas cotas quedan a menos de $0.04\%$ por encima del óptimo, permitiendo certificar la calidad de las soluciones aproximadas sin necesidad de resolver el problema exacto.

---

## 5. Lenguaje e instrucciones de ejecución

Todos los algoritmos y scripts de experimentación fueron desarrollados en **Python 3** (probado en Python 3.13 dentro de un entorno virtual `.venv`).

- **Dependencias:** `matplotlib` (gráficos) y `scipy` + `numpy` (solver `milp` en Problema 4).

```bash
pip install matplotlib scipy numpy
```

- **Comandos de ejecución (desde la raíz de `tp02/` o del repositorio):**
  - **Problema 1:** `python tp02/Problema_01/problema_01.py` y `python tp02/Problema_01/graficar_problema_01.py`
  - **Problema 2:** `python tp02/Problema_02/fptas.py tp02/Mochilas/mochila100.txt 0.5`, `python tp02/Problema_02/problema_02.py` y `python tp02/Problema_02/graficar_problema_02.py`
  - **Problema 3:** `python tp02/Problema_03/randomizado.py tp02/Mochilas/mochila100.txt 50 3 42`, `python tp02/Problema_03/problema_03.py` y `python tp02/Problema_03/graficar_problema_03.py`
  - **Problema 4:** `python tp02/Problema_04/problema_04.py` y `python tp02/Problema_04/graficar_problema_04.py`
