# TRABAJO PRÁCTICO 2

**Materia:** Teoría de Algoritmos (TB024)  
**Institución:** Universidad de Buenos Aires – Facultad de Ingeniería  
**Cátedra:** Lic. Pablo Echevarría  
**Cuatrimestre:** 2do Cuatrimestre 2026  

---

## PROBLEMA 1 – ALGORITMOS APROXIMADOS

Diseñar e implementar un algoritmo que resuelva el problema de la mochila en forma aproximada mediante el **algoritmo de Sahni (1975)** visto en clase.

Ejecutarlo en instancias de diferentes tamaños. Para cada una de dichas instancias calcular:
- La cota inferior planteada por la relajación lineal.
- La cota inferior planteada por Martello y Toth.
- La solución óptima exacta, por alguno de los métodos vistos en el TP1.

Comparar los cuatro valores obtenidos.

---

## PROBLEMA 2 – ALGORITMOS APROXIMADOS

Diseñar e implementar un esquema de algoritmo que resuelva en forma aproximada el problema de la mochila mediante el **algoritmo arbitrariamente bueno** visto en clase. El valor de épsilon (cota de distancia al óptimo) debe ser parametrizable.

Ejecutarlo en instancias de diferentes tamaños y con diferentes valores de épsilon. Para cada ejecución, indicar:
- El resultado del algoritmo.
- El resultado óptimo (por alguno de los métodos vistos en el TP1).
- El valor de épsilon.
- El tiempo de ejecución.

---

## PROBLEMA 3 – ALGORITMOS RANDOMIZADOS

Diseñar e implementar un algoritmo **randomizado** para resolver en forma aproximada el problema de la mochila. Ejecutarlo en instancias de diferentes tamaños.

- Indicar y justificar el orden de complejidad temporal y espacial del algoritmo desarrollado.
- Explicar y fundamentar el uso del azar en el algoritmo.
- Comparar el resultado obtenido y el tiempo de ejecución con los obtenidos por los algoritmos **Greedy** (Ej 2 del TP1) y **Programación Dinámica** (Ej 3A del TP1).

---

## PROBLEMA 4 – CONCLUSIONES

Comparar en los rangos en que sea posible los tiempos obtenidos para los mismos problemas por los algoritmos desarrollados en los TPs 1 y 2:

- Fuerza bruta
- Backtracking
- Greedy (aproximado)
- Programación dinámica (tradicional)
- Programación lineal
- Algoritmo aproximado 1
- Algoritmo aproximado 2 (con un épsilon fijo)
- Algoritmo randomizado propio (aproximado)

Para los algoritmos aproximados, indicar también las cotas planteadas por la relajación lineal y por Martello y Toth.

Analizar los resultados obtenidos.

---

## CONDICIONES GENERALES DE LOS PROBLEMAS

Para cada algoritmo, se debe incluir:

1. **Supuestos:** Identificar supuestos, condiciones, limitaciones y/o premisas bajo los cuales funcionará el algoritmo desarrollado.
2. **Diseño:**
   - Incluir un pseudocódigo.
   - Detallar las estructuras de datos utilizadas.
3. **Seguimiento:** Ejemplo de seguimiento con un set de datos reducido.
4. **Complejidad:** Análisis de la complejidad temporal a partir del pseudocódigo.
5. **Sets de datos:** Adjuntar los sets de datos utilizados. Indicar los criterios con que se tomaron.
6. **Tiempos de Ejecución:** Medir los tiempos de ejecución de cada set de datos y presentarlos en un gráfico.
7. **Informe de Resultados:** Redactar un informe de resultados comparando los tiempos de ejecución. ¿Se corresponde con la complejidad determinada inicialmente? El gráfico comparativo de tiempos debe incluir tanto la curva con los valores medidos como la curva teórica de ajuste.

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

