# Trabajo Práctico 2

**Teoría de Algoritmos – 2C2026 (FIUBA)**

---

## Problema 2 – Algoritmo Arbitrariamente Bueno (FPTAS)

Carpeta de trabajo: `tp02/Problema_02/`

### Requisitos e instalación

Se requiere Python 3.9+ (se recomienda trabajar dentro de un entorno virtual `venv` activado). Desde la raíz del repositorio:

```bash
pip install -r tp02/Problema_02/requirements.txt
```

### Archivos y sets de datos (`tp02/Problema_02/`)

- `requirements.txt`: dependencias Python (`matplotlib`, `numpy`, `scipy`, `pulp`).
- `datos.py`: lectura de instancias (`(capacidad, elementos)` con `(peso, beneficio)`) y generación determinista de sets complementarios.
- `fptas.py`: implementación del esquema FPTAS para Mochila 0-1 con parámetro `epsilon` configurable.
- `sets_datos/intermedios/`: instancias estándar para $n \in \{60, 80, 120, 150, 180\}$ (mismas reglas que `tp01/crear_mochila.py`, semilla `42 + n`).
- `sets_datos/valores_grandes/`: instancias con pesos, beneficios y capacidades grandes para $n \in \{20, 40, 60, 80, 100\}$ (semilla `1000 + n`).

También se reutilizan las instancias base ubicadas en `tp01/Mochilas/`. Para regenerar los sets complementarios del Problema 2:

```bash
python tp02/Problema_02/datos.py
```

Para ejecutar el algoritmo FPTAS sobre una instancia individual:

```bash
python tp02/Problema_02/fptas.py [ruta_instancia] [epsilon]
```
