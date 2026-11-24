# Trabajo Práctico 2

**Teoría de Algoritmos – 2C2026 (FIUBA)**

---

## Problema 2 – Algoritmo Arbitrariamente Bueno (FPTAS)

Carpeta de trabajo: `tp02/Problema_02/`

### Requisitos e instalación

Se requiere Python 3.9+ (se recomienda trabajar dentro de un entorno virtual `venv` activado). Los scripts del algoritmo y experimentos usan solo la biblioteca estándar de Python; únicamente para generar los gráficos se necesita `matplotlib`:

```bash
pip install matplotlib
```

### Archivos y sets de datos (`tp02/Problema_02/`)

- `datos.py`: lectura de instancias y generación determinista de sets intermedios.
- `fptas.py`: implementación del esquema FPTAS para Mochila 0-1 con parámetro `epsilon` configurable.
- `mochila_tradicional.py`: implementación de Programación Dinámica exacta (base TP1) para comparar el óptimo.
- `problema_02.py`: ejecución de los experimentos variando $n$ y $\varepsilon$; exporta resultados en `resultados/`.
- `graficar_problema_02.py`: genera los gráficos de tiempos reales vs. ajustes teóricos $O(n^3)$ y $O(\varepsilon^{-1})$ en `graficos/`.
- `INFORME_PROBLEMA_02.md`: informe técnico del Problema 2 con supuestos, pseudocódigo, seguimiento manual, complejidad, sets, gráficos y análisis de resultados.
- `resultados/`: tablas `.csv` generadas por `problema_02.py`.
- `graficos/`: gráficos `.png` generados por `graficar_problema_02.py`.
- `sets_datos/intermedios/`: instancias estándar para $n \in \{60, 80, 120, 150, 180\}$ (mismas reglas que `tp02/crear_mochila.py`, semilla `42 + n`).

También se utilizan las instancias base ubicadas en `tp02/Mochilas/`. Para regenerar los sets intermedios:

```bash
python tp02/Problema_02/datos.py
```

Para ejecutar el algoritmo FPTAS sobre una instancia individual:

```bash
python tp02/Problema_02/fptas.py [ruta_instancia] [epsilon]

# Ejemplo:
python tp02/Problema_02/fptas.py tp02/Mochilas/mochila100.txt 0.5
```

Para correr la batería de experimentos y generar `resultados/`:

```bash
python tp02/Problema_02/problema_02.py
```

Para generar los gráficos comparativos en `graficos/`:

```bash
python tp02/Problema_02/graficar_problema_02.py
```

---

## Problema 3 – Algoritmo Randomizado (Monte Carlo)

Carpeta de trabajo: `tp02/Problema_03/`

### Archivos y estructura

- `greedy.py`: réplica del algoritmo Greedy con garantía de 2-aproximación (base TP1) para comparación directa sin dependencias entre entregas.
- `randomizado.py`: implementación del algoritmo Monte Carlo (Greedy aleatorizado con ventana $k$ y multi-arranque de $T$ iteraciones).
- `problema_03.py`: ejecuta la comparativa entre Randomizado, Greedy y Programación Dinámica sobre las instancias de `tp02/Mochilas/` y exporta `resultados/resultados_problema_03.csv`.
- `graficar_problema_03.py`: genera los gráficos de ajuste teórico $O(n \log n + T \cdot n)$, comparación de tiempos y comparación de calidad en `graficos/`.
- `INFORME_PROBLEMA_03.md`: informe técnico del Problema 3.

### Ejecución

Para ejecutar el algoritmo randomizado sobre una instancia individual (`[iteraciones] [ventana] [semilla]` son opcionales):

```bash
python tp02/Problema_03/randomizado.py tp02/Mochilas/mochila100.txt 50 3 42
```

Para correr los experimentos comparativos y generar `resultados/resultados_problema_03.csv`:

```bash
python tp02/Problema_03/problema_03.py
```

Para generar los gráficos en `graficos/`:

```bash
python tp02/Problema_03/graficar_problema_03.py
```
