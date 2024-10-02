# Práctica 2 de Visión por Computador.

Este proyecto aborda técnicas de procesamiento de imágenes utilizando OpenCV en python. El enfoque principal de la práctica está en el análisis de bordes y la transformación de imágenes en escala de grises para extraer información visual relevante. Se aplican operadores como el filtro Canny para detectar contornos y analizar la distribución de píxeles en la imagen.

## 2.1. Objetivos.

1. Aprender a cargar y manipular imágenes con OpenCV.
2. Aplicar técnicas de conversión de imágenes a escala de grises.
3. Implementar la detección de bordes con el operador Canny.
4. Visualizar los resultados del análisis de bordes utilizando gráficos de distribución de píxeles.

## 2.2. Tarea 1: Realiza la cuenta de píxeles blancos por filas (en lugar de por columnas). Determinar el máximo para filas y columnas (uno para cada). Muestra el número de filas con un número de píxeles blancos mayor o igual que 0.95*máximo.

En esta primera tarea se realizó el conteo de píxeles blancos por cada fila en una imagen procesada con el operador Canny, lo que permite identificar los bordes presentes en la imagen. El propósito de esta actividad es analizar la distribución de los bordes a lo largo de las filas de la imágen.

### 2.2.1. Descripción del Proceso.

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

## 2.3. Tarea 2: Aplicar umbralizado a la imagen resultante de Sobel y realizar el conteo por filas y columnas. Calcular los máximos por filas y columnas, y determinar las filas y columnas por encima del 0.95*máximo. Remarcar con alguna primitiva gráfica dichas filas y columnas sobre la imagen. ¿Cómo se comparan los resultados obtenidos a partir de Sobel y Canny?

En esta segunda tarea, se aplicó el operador de Sobel a una imagen en escala de grises para detectar bordes, seguidamente se realizó un umbralizado sobre la imagen resultante. Después, se calculó la cantidad de píxeles blancos por filas y columnas y se compararon estos resultados con los obtenidos en la tarea anterior utilizando el operador Canny. Finalmente, se remarcaron gráficamente las filas y columnas con un número de píxeles blancos superior al 95% del valor máximo.

### 2.3.1. Descripción del Proceso.

1. **Aplicación del operador Sobel:** Se utilizaron los filtros Sobel en las direcciones X e Y para detectar bordes en la imagen. La magnitud de los gradientes se calculó combinando ambas direcciones.
2. **Umbralización:** La imagen obtenida con Sobel fue binarizada utilizando un umbral fijo de 127, lo que nos permitió convertir la magnitud del gradiente a una imagen binaria (valores 0 o 255).
3. **Cálculo de píxeles blancos:** Se realizó el conteo de los píxeles blancos en la imagen umbralizada tanto por filas como por columnas.
4. **Determinación de filas y columnas por encima del 95% del máximo:** Se identificaron las filas y columnas que contienen un número de píxeles blancos superior al 95% del valor máximo ([Imagen 2](#Sobel)).
5. **Marcado gráfico:** Para destacar las filas y columnas relevantes, se sobreimpusieron colores sobre la imagen original en las posiciones donde el número de píxeles blancos era superior al 95% del máximo (rojo para filas y verde para columnas).

<a name="Sobel"></a>
![**Imagen 2.** Muestra de resultados con operador Sobel.](/P2/assets/MaxSobel.jpg)

### 2.3.2. Comparación de Sobel y Canny

+ **Operador Sobel:** El operador de Sobel se centra en el cálculo de los gradientes en las direcciones X e Y para detectar bordes. Esto permite una diferenciación clara de los cambios de intensidad en ambas direcciones. Sobel tiende a ser más sensible a los cambios graduales en la imagen y a producir bordes más gruesos en comparación con Canny.

+ **Operador Canny:** En contraste, Canny es más eficaz en la detección de bordes finos y está diseñado para minimizar el ruido en la imagen. Utiliza un proceso de detección más sofisticado que involucra suavizado gaussiano y eliminación de no máximos, lo que genera una representación más precisa de los bordes.

En la comparación gráfica ([Imagen 3](#Comparación)), se puede observar que:

+ La respuesta de **Sobel** presenta más variación en los bordes detectados por filas y columnas, siendo más robusta en zonas donde hay gradientes suaves.
+ La respuesta de **Canny** es más precisa en los contornos finos, con una menor cantidad de ruido en la detección de bordes.

### 2.3.3. Resultados

A continuación se muestra una visualización de las comparaciones de Sobel y Canny en términos de la respuesta por filas y columnas:

Esta comparación refleja cómo ambos operadores detectan bordes de manera distinta y nos da una idea de cómo elegir el operador adecuado dependiendo de las características de la imagen y de los detalles que se quieran resaltar.

<a name="Comparación"></a>
![**Imagen 3.** Comparativa gráfica de Sobel frente a Canny.](/P2/assets/Comparativa.jpg)

## 2.4. Tarea 3: Proponer un demostrador que capture las imágenes de la cámara, y les permita exhibir lo aprendido en estas dos prácticas ante quienes no cursen la asignatura :). Es por ello que además de poder mostrar la imagen original de la webcam, incluya al menos dos usos diferentes de aplicar las funciones de OpenCV trabajadas hasta ahora.



## 2.5. Ampliación:



## Desarrollado por: Adrián Talavera Naranjo y Arhamis Gutiérrez Caballero.