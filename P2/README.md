# Práctica 2 de Visión por Computador.

Este proyecto aborda técnicas de procesamiento de imágenes utilizando OpenCV en python. El enfoque principal de la práctica está en eñ análisis de bordes y la transformación de imágenes en escala de grises para extraer información visual relevante. Se aplican operadores como el filtro Canny para detectar contornos y analizar la distribución de píxeles en la imagen.

## 2.1. Objetivos.

    1. Aprender a cargar y manipular imágenes con OpenCV.
    2. Aplicar técnicas de conversión de imágenes a escala de grises.
    3. Implementar la detección de bordes con el operador Canny.
    4. Visualizar los resultados del análisis de bordes utilizando gráficos de distribución de píxeles.

## 2.2. Tarea 1: Realiza la cuenta de píxeles blancos por filas (en lugar de por columnas). Determinar el máximo para filas y columnas (uno para cada). Muestra el número de filas con un número de píxeles blancos mayor o igual que 0.95*máximo.

En esta primera tarea se realizó el conteo de píxeles blancos por cada fila en una imagen procesada con el operador Canny, lo que permite identificar los bordes presentes en la imagen. El propósito de esta actividad es analizar la distribución de los bordes a lo largo de las filas de la imágen.

### 2.2.1. Descripción delproceso.

1. **Lectura y conversión de la imagen:** Se cargó una imagen en formato BGR usando OpenCV y luego se convirtió a una imagen en escala de grises. Dicha conversión es indispensable para aplicar técnicas de detección de bordes.
2. **Detección de bordes con Canny:** Se utilizó el operador Canny para obtener los contornos de la imagen. Dicho operador genera una imagen binaria donde los píxeles correspondientes a los bordes tienen un valor de 255 (blanco) y el resto un valor de 0 (negro).
3. **Cuenta de píxeles blancos por fila:** PAra cada fila de la imagen resultante, se realizóla suma de los valores de los píxeles blancos (255). Esto permitió calcular el porcentaje de píxeles blancos por fila.
4. **Visualización:** Los resultados de la cuenta se graficaron utilizando Matplotlib para observar cómo se distribuyen los bordes a lo largo de las filas de la imagen ([Imagen 1](#Canny)). Además se determinaron las filas con mayor número de píxeles blancos y aquellas filas cuyo número de píxeles blancos supera el 95% del valor máximo.

### 2.2.2. Resultados.

+ **Fila con el mayor número de píxeles blancos:** Se identificó la fila con la mayor concentración de bordes detectados por el operador Canny.
+ **Visualización de distribución de bordes por filas:** El gráfico ([Imagen 1](#Canny)) resultante muestra la distribución porcentual de píxeles blancos a lo largo de las filas de la imagen.
+ **Detección de filas significativas:** Se identificaron las filas deonde el número de píxeles blancos supera el 95% del valor máximos.

<a name="Canny"></a>
![**Imagen 1.** Imagen procesada con el operador Canny y representación de píxeles blanco por fila.](/P2/assets/Canny.jpg)