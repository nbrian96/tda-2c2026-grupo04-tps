# Trabajo Práctico 1: El Problema de la Mochila 0-1
**Teoría de Algoritmos – 2C2026 (FIUBA)**

Este repositorio contiene las implementaciones, generación de datos, mediciones de rendimiento y análisis empírico de cuatro enfoques algorítmicos distintos para resolver el Problema de la Mochila 0-1: **Fuerza Bruta / Backtracking**, **Greedy**, **Programación Dinámica** (planteo tradicional y alternativo) y **Programación Lineal Entera**.

---

## Requisitos del Entorno

* **Sistema Operativo:** Probado en Linux (Ubuntu / Debian / Linux Mint), macOS y Windows.
* **Lenguaje:** Python 3.9 o superior.
* **Bibliotecas externas:** `matplotlib`, `numpy`, `scipy` y `pulp` (incluye el solver CBC).

### Instalación de dependencias

En sistemas basados en Debian/Ubuntu/Linux Mint (recomendado):
```bash
sudo apt update && sudo apt install python3-matplotlib python3-numpy python3-scipy python3-pulp
```

O mediante `pip` (utilizando un entorno virtual `venv`):
```bash
pip install matplotlib numpy scipy pulp
```

---

## Estructura del Proyecto y Generación de Datos

Todos los algoritmos evalúan exactamente las mismas instancias para garantizar la reproducibilidad y permitir una comparación justa entre paradigmas.

```text
.
├── crear_mochila.py        # Generador unificado de datasets (semilla determinista)
├── Mochilas/               # Carpeta generada con las instancias compartidas (mochila10.txt ... mochila1000.txt)
├── problema01/             # Fuerza Bruta y Backtracking con poda
├── problema02/             # Algoritmo Greedy con garantía de calidad 1/2
├── problema03/             # Programación Dinámica (Planteo Tradicional y Alternativo)
└── problema04/             # Programación Lineal Entera (PuLP + Solver CBC)
```

### Paso 0: Generar el set de datos común (Obligatorio antes de ejecutar)

Desde la **raíz del proyecto**, ejecutar:
```bash
python3 crear_mochila.py
```
Este script creará la carpeta `Mochilas/` con todas las instancias estandarizadas utilizando una semilla fija (`SEMILLA + n`).

---

## PROBLEMA 1 – FUERZA BRUTA vs. BACKTRACKING

1. Diseñar e implementar un algoritmo que resuelva el problema de la mochila mediante **fuerza bruta**.
2. Luego, modificarlo para que, mediante **backtracking**, llegue al mismo resultado en menos tiempo.
3. Calcular el orden de complejidad temporal de los algoritmos desarrollados.
4. Aplicarlos a diferentes sets de datos obtenidos con el código adjunto `crear_mochila.py`, de tamaños adecuados para poder comparar la curva de tiempos de ejecución teórica y real en ambos algoritmos.

Ubicarse dentro de la carpeta `problema01/`:

```bash
cd problema01

# Resolver Mochilas/mochila10.txt con ambos algoritmos y exportar la solución
python3 codigo.py

# Medir tiempos de ejecución, ajustar curvas teóricas O(n·2^n) y generar tiempos.csv y grafico_problema01.png
python3 grafico.py
```


## PROBLEMA 2 – GREEDY

1. Diseñar e implementar un algoritmo **greedy** que resuelva el problema de la mochila. Dicho algoritmo debe tener garantía de calidad \(1/2\).
2. Calcular el orden de complejidad temporal del algoritmo desarrollado.
3. Aplicarlo a diferentes sets de datos obtenidos con el código adjunto `crear_mochila.py`, de tamaños adecuados para poder comparar la curva de tiempos de ejecución teórica y real.
4. Aplicarlo a un set de datos creado manualmente donde actúe la garantía de calidad.


Ubicarse dentro de la carpeta `problema02/`:
```bash
cd problema02

# Ejecutar el ejemplo manual donde actúa la garantía de calidad 1/2
python3 problema02.py

# Resolver una instancia específica desde la carpeta compartida
python3 problema02.py ../Mochilas/mochila1000.txt

# Medir tiempos, realizar regresión O(n log n) y generar gráficos
python3 grafico.py

---

## PROBLEMA 3 – PROGRAMACIÓN DINÁMICA

1. Diseñar e implementar dos algoritmos que resuelvan el problema de la mochila mediante **programación dinámica**:
   - Uno de los algoritmos deberá resolverlo con el **planteo tradicional** (maximizar el beneficio para una capacidad fija).
   - El otro deberá resolverlo con el **planteo alternativo** (minimizar el peso para un beneficio fijo).
2. Calcular el orden de complejidad temporal de los algoritmos desarrollados.
3. Aplicarlos a diferentes sets de datos obtenidos con el código adjunto `crear_mochila.py`, de tamaños adecuados para poder comparar la curva de tiempos de ejecución teórica y real en ambos algoritmos.
4. Aplicar ambos algoritmos a diferentes sets de datos obtenidos con el código adjunto `crear_mochila.py`, de tamaños adecuados para poder comparar los tiempos de ejecución de ambos algoritmos. Analizar los resultados obtenidos.

Ambos algoritmos implementan optimización espacial ($O(C)$ y $O(B)$ respectivamente) para evitar desbordamientos de memoria en instancias grandes ($n=1000$).

Ubicarse dentro de la carpeta `problema03/`:

```bash
cd problema03

# 1. Medir tiempos de ambos planteos (genera res_tradicional.txt y res_alternativo.txt)
# Nota: La evaluación hasta n=1000 demora unos minutos debido a la complejidad pseudo-polinomial.
python3 medir_tiempos.py

# 2. Generar los gráficos comparativos y ajustes O(nC) y O(nB) (tradicional.png, alternativo.png, comparacion.png)
python3 graficar_tiempos.py
```

**Ejecución individual sobre una instancia:**
```bash
python3 mochila_tradicional.py ../Mochilas/mochila10.txt
python3 mochila_alternativo.py ../Mochilas/mochila10.txt
```
*(Ambos comandos imprimen el beneficio máximo y deben devolver exactamente el mismo valor).*

---

## PROBLEMA 4 – PROGRAMACIÓN LINEAL

1. Diseñar e implementar un algoritmo que resuelva el problema de la mochila mediante **programación lineal entera** utilizando la biblioteca `PuLP`.
2. Calcular el orden de complejidad temporal del algoritmo desarrollado.
3. Aplicarlos a diferentes sets de datos obtenidos con el código adjunto `crear_mochila.py`, de tamaños adecuados para poder comparar la curva de tiempos de ejecución teórica y real.

Ubicarse dentro de la carpeta `problema04/`:
```bash
cd problema04

# Medir tiempos del solver CBC, exportar resultados_PL.txt y generar tiempos_PL.png
python3 graficar_tiempos.py
```
*(Nota: `problema04.py` contiene la formulación matemática del modelo y es importado directamente por `graficar_tiempos.py`; no requiere ejecución independiente).*

## CONCLUSIÓN

- Comparar en los rangos en que sea posible los tiempos obtenidos para los mismos problemas por los 6 algoritmos desarrollados.
- Analizar los resultados obtenidos.

---

## CONDICIONES GENERALES DE LOS PROBLEMAS

Para cada algoritmo, se debe incluir:

- **Supuestos:** Identificar supuestos, condiciones, limitaciones y/o premisas bajo los cuales funcionará el algoritmo desarrollado.
- **Diseño:**
  - Incluir un Pseudocódigo.
  - Detallar las estructuras de datos utilizadas.
- **Seguimiento:** Ejemplo de seguimiento con un set de datos reducido.
- **Complejidad:** Análisis de la complejidad temporal a partir del pseudocódigo.
- **Sets de datos:** Adjuntar los sets de datos utilizados. Indicar los criterios con que se tomaron.
- **Tiempos de Ejecución:** Medir los tiempos de ejecución de cada set de datos y presentarlos en un gráfico.
- **Informe de Resultados:** Redactar un informe de resultados comparando los tiempos de ejecución. ¿Se corresponde con la complejidad determinada inicialmente? El gráfico comparativo de tiempos debe incluir tanto la curva con los valores medidos como la curva teórica de ajuste.

---

## CONDICIONES GENERALES DE ENTREGA

El trabajo debe ser entregado en un archivo `.zip` conteniendo:

1. **Documento:**
   - Carátula, índice y numeración de páginas.
   - La carátula debe incluir nombre y padrón de los integrantes del grupo.
   - Debe presentarse en formato **PDF**.
2. **Archivos de código fuente:**
   - Fuentes desarrollados.
   - Indicar en el documento el lenguaje de programación utilizado e incluir instrucciones para compilar (de ser necesario) y ejecutar.
3. **Archivos con los sets de datos utilizados.**
4. **Archivos con resultados obtenidos para cada set de datos.**
5. **Referencias bibliográficas:** Si se incluyeran, utilizar normas **APA 7ma edición**.

## Ramas del repositorio

Este proyecto utiliza un flujo de trabajo basado en ramas para organizar el desarrollo individual y la integración del equipo.

### 🔹 Ramas principales

- **Master**
  - Rama estable del proyecto.
  - Contiene versiones listas para entrega.

- **Entrega**
  - Rama de integración.
  - Aquí se unen los cambios de las ramas de trabajo individuales.
  - Representa la versión más actual del proyecto en desarrollo.

### Ramas de desarrollo (feature branches)

Cada integrante trabaja en su propia rama:

- `Greedy`
- `lineal`
- `Backtracking`
- `Pd`

Cada una contiene el trabajo individual antes de ser integrado a `Entrega`.

---

## Flujo de trabajo

### 1. Actualizar rama develop

Antes de empezar a trabajar:

```bash
git checkout Entrega
git pull origin Entrega
```

### 2. Actualizar tu rama de trabajo

Cambiar a tu rama de desarrollo:
```bash
git checkout rama_problema
```

Traer los últimos cambios de entrega:
```bash
git pull --rebase origin entrega
```

### 3. Trabajar en la feature

Realizar los cambios necesarios en el código.
```bash
git add .
git commit -m "Descripción clara del cambio realizado"
```

### 4. Subir los cambios a tu rama

Una vez quieras guardar tus cambios, los guardas en tu rama:
```bash
git push origin rama_problema
```

### 5. Integrar cambios a la rama entrega

Cuando la funcionalidad esté lista para integrarse:

Cambiar a la rama entrega:
```bash
git checkout Entrega
```

Actualiza la rama entrega:
```bash
git pull origin Entrega
```

Fusionar la rama de trabajo feature con la rama entrega:
```bash
git merge rama_problema
```

Subir la versión integrada:
```bash
git push origin Entrega
```
