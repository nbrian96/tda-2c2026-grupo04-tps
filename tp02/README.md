# Trabajo Práctico 2

**Teoría de Algoritmos – 2C2026 (FIUBA)**

---

## Requisitos e instalación

Se requiere Python 3.9+ (se recomienda trabajar dentro de un entorno virtual `venv` activado).

Dependencias externas necesarias para generar los gráficos y resolver Programación Lineal Entera (Problema 4):

```bash
pip install matplotlib scipy numpy
```

---

## Informe unificado

El informe único de los cuatro problemas se encuentra en [`tp02/informe/INFORME_TP02.md`](informe/INFORME_TP02.md) (listo para exportar a PDF).

---

## Problema 1 – Algoritmo Aproximado de Sahni

Carpeta de trabajo: `tp02/Problema_01/`

- `problema_01.py`: ejecuta Sahni ($k=1$), calcula las cotas RL ($U_1$) y Martello-Toth ($U_2$), compara con el óptimo exacto y exporta `resultados_problema1_k1.txt`.
- `graficar_problema_01.py`: genera `graficos/tiempos_sahni_ajuste_O_n2.png` con el ajuste teórico $O(n^2)$.

```bash
python tp02/Problema_01/problema_01.py
python tp02/Problema_01/graficar_problema_01.py
```

---

## Problema 2 – Algoritmo Arbitrariamente Bueno (FPTAS)

Carpeta de trabajo: `tp02/Problema_02/`

- `datos.py`: lectura de instancias y generación determinista de sets intermedios (`sets_datos/intermedios/`).
- `fptas.py`: implementación del esquema FPTAS para Mochila 0-1 con parámetro `epsilon` configurable.
- `mochila_tradicional.py`: implementación de Programación Dinámica exacta (base TP1) para comparar el óptimo.
- `problema_02.py`: ejecución de los experimentos variando $n$ y $\varepsilon$; exporta resultados en `resultados/`.
- `graficar_problema_02.py`: genera los gráficos de tiempos reales vs. ajustes teóricos $O(n^3)$ y $O(\varepsilon^{-1})$ en `graficos/`.

```bash
python tp02/Problema_02/fptas.py tp02/Mochilas/mochila100.txt 0.5
python tp02/Problema_02/problema_02.py
python tp02/Problema_02/graficar_problema_02.py
```

---

## Problema 3 – Algoritmo Randomizado (Monte Carlo)

Carpeta de trabajo: `tp02/Problema_03/`

- `greedy.py`: réplica local del algoritmo Greedy con garantía de 2-aproximación (base TP1).
- `randomizado.py`: algoritmo Monte Carlo (Greedy aleatorizado con ventana $k$ y multi-arranque de $T$ iteraciones).
- `problema_03.py`: comparativa entre Randomizado, Greedy y Programación Dinámica sobre `tp02/Mochilas/`; exporta `resultados/resultados_problema_03.csv`.
- `graficar_problema_03.py`: genera los gráficos en `graficos/`.

```bash
python tp02/Problema_03/randomizado.py tp02/Mochilas/mochila100.txt 50 3 42
python tp02/Problema_03/problema_03.py
python tp02/Problema_03/graficar_problema_03.py
```

---

## Problema 4 – Conclusiones (Comparativa TP1 y TP2)

Carpeta de trabajo: `tp02/Problema_04/`

- `algoritmos_tp1.py`: copias locales de Fuerza Bruta, Backtracking y Programación Lineal Entera (`scipy.optimize.milp` / HiGHS).
- `problema_04.py`: ejecuta en la misma máquina los 8 algoritmos (FB, BT, Greedy, PD, PL, Sahni, FPTAS y Randomizado) y exporta `resultados/comparacion_tiempos.csv` y `resultados/comparacion_aproximados_cotas.csv`.
- `graficar_problema_04.py`: genera `graficos/comparacion_tiempos_todos.png` y `graficos/comparacion_aproximados_cotas.png`.

```bash
python tp02/Problema_04/problema_04.py
python tp02/Problema_04/graficar_problema_04.py
```

---

## Preparar `.zip` de entrega (PowerShell)

Una vez compilado el PDF del informe dentro de `tp02/informe/`, se puede generar un `.zip` limpio excluyendo `__pycache__` y auxiliares de LaTeX:

```powershell
$dest = "tp02_grupo04.zip"
if (Test-Path $dest) { Remove-Item $dest }
$archivos = Get-ChildItem -Path tp02 -Recurse -File | Where-Object {
    $_.FullName -notmatch "__pycache__" -and $_.Extension -notin @(".aux", ".log", ".toc", ".out", ".pyc")
}
Compress-Archive -Path $archivos.FullName -DestinationPath $dest
```
