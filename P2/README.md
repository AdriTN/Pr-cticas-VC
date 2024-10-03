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
En esta tarea, se desarrolló un demostrador interactivo utilizando la cámara web del sistema para capturar imágenes en tiempo real y aplicar diferentes técnicas de procesamiento de imágenes que hemos trabajado en las prácticas. El objetivo principal es mostrar el procesamiento de imágenes de manera didáctica, a través de varios modos de visualización que permiten cambiar entre diferentes técnicas de procesamiento de imagen utilizando OpenCV.

### 2.4.1. Descripción del Proceso
1. **Inicialización de la cámara y configuración del eliminador de fondo:** El sistema se inicia accediendo a la cámara del ordenador usando cv2.VideoCapture(0), lo que permite capturar imágenes en tiempo real. También se utiliza un eliminador de fondo mediante cv2.createBackgroundSubtractorMOG2(), que genera un modelo del fondo y lo separa de los objetos en movimiento.

2. **Modos de visualización:** Se han implementado diferentes modos de visualización que permiten cambiar dinámicamente entre diversas técnicas de procesamiento de imágenes:

- **Modo Diferencia de Fondo:** Utiliza el eliminador de fondo para resaltar objetos en movimiento eliminando el fondo estático.
- **Modo Diferencia con el Fotograma Anterior:** Compara el fotograma actual con el anterior usando la función cv2.absdiff(), lo que permite identificar diferencias entre dos fotogramas consecutivos.
- **Modo Espejado:** Refleja horizontalmente el fotograma capturado con cv2.flip().
- **Modo Escala de Grises:** Convierte el fotograma actual a escala de grises mediante cv2.cvtColor().
- **Modo Fondo:** Muestra el fondo generado por el eliminador de fondo, útil para observar cómo el algoritmo modela la escena estática.
- **Modo Normal:** Muestra la imagen original capturada por la cámara sin modificaciones.

3.Interfaz del menú: En cada fotograma, se superpone un menú de texto que guía al usuario sobre las teclas disponibles para cambiar entre los diferentes modos de visualización. El menú incluye instrucciones para alternar entre los modos y salir del programa, lo que mejora la interactividad del demostrador.

### 2.4.2. Resultados
El demostrador permite al usuario observar en tiempo real cómo los diferentes algoritmos de procesamiento de imágenes modifican la visualización de la cámara. Las técnicas aplicadas incluyen eliminación de fondo, detección de diferencias entre fotogramas, espejado y conversión a escala de grises, las cuales son útiles para entender cómo se puede manipular y analizar la información visual de una cámara.

A continuación, se listan algunos de los resultados destacados:

- #### Modo Diferencia de Fondo
![**Imagen 4.** Resultado modo diferencia de fondo.](/P2/assets/diferencia_de_fondo.png)

- #### Modo Diferencia con el Fotograma Anterior
![**Imagen 5.** Resultado modo diferencia anterior.](/P2/assets/Diferencia_anterior.png)
- #### Modo Espejado
![**Imagen 6.** Resultado modo diferencia de fondo.](/P2/assets/image2.png)
- #### Modo Escala de Grises
![**Imagen 7.** Resultado modo diferencia de fondo.](/P2/assets/image.png)

Este demostrador ofrece una plataforma interactiva que no solo ilustra los conceptos teóricos aprendidos en las prácticas, sino que también puede ser utilizada para presentaciones, demostraciones en tiempo real o proyectos creativos relacionados con la visión por computador.

## 2.5.Tarea 4: Tras ver los vídeos My little piece of privacy, Messa di voce y Virtual air guitar proponer un demostrador reinterpretando la parte de procesamiento de la imagen, tomando como punto de partida alguna de dichas instalaciones.
Para esta tarea, se diseñó un demostrador inspirado en las obras audiovisuales mencionadas, integrando procesamiento de imágenes en tiempo real y una interfaz interactiva que permite detectar objetos de un color específico en la imagen capturada por una cámara web. Este demostrador utiliza técnicas de visión por computador para detectar color y dibujar líneas dinámicas que conectan los objetos detectados en la imagen, creando una interacción visual similar a las instalaciones mencionadas.

### 2.5.1. Descripción del Proceso
1. **Captura de vídeo en tiempo real:** El sistema comienza capturando vídeo en tiempo real desde la cámara web del dispositivo utilizando cv2.VideoCapture(0). Esta captura es el punto de partida para aplicar la detección de color y los efectos visuales interactivos.

2. **Selector de color personalizado:** Se implementó un panel de control en la ventana del sistema que permite seleccionar dinámicamente el color que se utilizará para las líneas. Este panel, gestionado por trackbars de OpenCV, permite al usuario ajustar los valores de los canales BGR para cambiar el color de las líneas que conectan los objetos detectados. Esto hace que la interacción visual sea más creativa y flexible, similar a las instalaciones artísticas.

3. **Detección de objetos de color azul:** El algoritmo convierte cada frame de la webcam al espacio de color HSV, y luego utiliza una máscara que resalta los objetos dentro del rango de color azul definido. La elección del color azul se basa en la facilidad de detección en diferentes entornos, pero podría modificarse para detectar otros colores si se requiere. Los contornos de los objetos azules se detectan con cv2.findContours(), y se dibujan rectángulos alrededor de ellos en la imagen.

4. **Conexión de objetos con líneas dinámicas:** Después de detectar los objetos de color azul, el sistema calcula el centro de cada rectángulo delimitador y dibuja líneas que conectan estos centros en tiempo real. Las líneas se dibujan utilizando el color seleccionado por el usuario desde las trackbars, añadiendo una capa de personalización a la visualización interactiva.

5. **Almacenamiento de las líneas fijas:** Una característica adicional permite al usuario "guardar" las líneas que conectan los objetos presionando la tecla 's'. Estas líneas se mantienen fijas en la pantalla, lo que crea una visualización más artística y similar a las instalaciones de arte mencionadas. Las líneas almacenadas se dibujan continuamente en cada frame hasta que el programa termina.

6. **Interactividad y control en tiempo real:** El usuario puede cambiar el color de las líneas dinámicamente utilizando las trackbars y también puede detener el programa en cualquier momento presionando la tecla ESC. Esta interacción en tiempo real recuerda las características interactivas de las instalaciones vistas, donde los usuarios pueden influir directamente en el resultado visual.

### 2.5.2. Resultados
El demostrador final proporciona una experiencia visual interactiva en la que el usuario puede observar cómo los objetos de color azul en la escena se detectan y se conectan mediante líneas. Esta representación gráfica dinámica, que conecta diferentes objetos y permite la selección de colores, se asemeja a las interacciones artísticas de las obras My little piece of privacy y Messa di voce, donde el procesamiento en tiempo real de los elementos visuales es clave para generar una experiencia estética inmersiva.

![**Imagen 8.** Resultado modo diferencia de fondo.](/P2/assets/dibujo.png)

## 2.6. Ampliación:Implementación de un sistema de detección de movimiento en tiempo real con captura automática.
En esta tarea se ha implementado un sistema que detecta movimiento en tiempo real utilizando la cámara del sistema y, cuando se detecta movimiento, guarda una captura de pantalla automáticamente. Se utiliza OpenCV para el procesamiento de video y la detección de movimiento, y se integran técnicas vistas anteriormente, como el eliminador de fondo y la diferencia de fotogramas.

### 2.6.1. Descripción del Proceso
1. **Inicialización de la cámara y el eliminador de fondo:** Se accede a la cámara del sistema usando cv2.VideoCapture(0) para capturar video en tiempo real. Se emplea cv2.createBackgroundSubtractorMOG2() para eliminar el fondo y resaltar los objetos en movimiento en la escena.

2. **Detección de diferencias entre fotogramas:** En cada ciclo, se compara el fotograma actual con el anterior usando cv2.absdiff(). Esta diferencia se convierte a escala de grises y se aplica un umbral para identificar las áreas con cambios significativos en la imagen, lo que permite detectar el movimiento.

3. **Detección de movimiento:** Si se detecta un cambio considerable entre dos fotogramas consecutivos (más de 5 millones de píxeles diferentes), el sistema interpreta que hay movimiento en la escena y muestra un mensaje visual en la ventana de video.

4. **Captura de pantalla:** Cuando se detecta movimiento, el sistema guarda automáticamente una captura de pantalla de la escena en un archivo de imagen, que es nombrado de forma única usando la fecha y hora actuales.

5. **Interfaz visual:** El sistema muestra dos ventanas: una con el video normal y otra con el video donde se destacan las áreas que han cambiado entre los fotogramas.

### 2.6.3. Resultados
Este sistema permite visualizar en tiempo real cualquier movimiento capturado por la cámara y generar capturas automáticas cuando se detecta un cambio significativo. Las capturas se guardan con nombres únicos, facilitando su almacenamiento. Esta tarea refuerza el uso de técnicas avanzadas como el eliminador de fondo, la detección de diferencias y la captura de fotogramas, haciendo que el sistema sea útil tanto para demostraciones didácticas como para aplicaciones prácticas en seguridad o monitoreo.

## 2.7. Ampliación:Sistema de detección de movimiento con cuenta regresiva para selfies automáticas
En esta tarea se ha implementado un sistema de detección de movimiento que toma una selfie automática cuando se detecta actividad en la cámara. El sistema realiza una cuenta regresiva de tres segundos antes de capturar la imagen. La detección se realiza utilizando OpenCV, aprovechando el eliminador de fondo y la comparación de fotogramas consecutivos.

### 2.7.1. Descripción del Proceso
1. **Inicialización de la cámara y el eliminador de fondo:** El sistema usa la cámara del dispositivo a través de cv2.VideoCapture(0) para capturar video en tiempo real. Se emplea cv2.createBackgroundSubtractorMOG2() para eliminar el fondo y detectar movimientos en la escena.
   
2. **Detección de diferencias entre fotogramas:** El sistema compara el fotograma actual con el anterior utilizando cv2.absdiff(). Esta diferencia es procesada para identificar cambios significativos, lo que permite detectar cuando algo o alguien se mueve en la imagen.

3. **Detección de movimiento:** Si la diferencia entre fotogramas es suficientemente grande (más de 5 millones de píxeles diferentes), el sistema reconoce que ha habido movimiento. En ese caso, se inicia una cuenta regresiva de tres segundos para tomar una selfie.

4. **Captura de pantalla con cuenta regresiva:** Una vez detectado el movimiento, se muestra una cuenta regresiva en la pantalla durante 3 segundos. Al finalizar, el sistema guarda automáticamente una captura de pantalla del momento, nombrando el archivo de forma única con la fecha y hora actuales.

5. **Interfaz visual:** El sistema muestra el video normal con la cuenta regresiva en caso de detección de movimiento, y permite la visualización de las diferencias entre fotogramas cuando hay actividad.

### 2.7.2. Resultados
Este sistema implementa una solución creativa para la detección de movimiento que toma selfies automáticas después de una cuenta regresiva, lo cual añade una capa interactiva al proyecto. Las capturas se guardan con nombres únicos y la cuenta regresiva se muestra en pantalla de forma visible, permitiendo al usuario prepararse antes de que se tome la foto. Este enfoque puede ser útil para aplicaciones de entretenimiento, seguridad, o para proyectos creativos en los que se requiera capturar momentos específicos tras detectar movimiento.

## Desarrollado por: Adrián Talavera Naranjo y Arhamis Gutiérrez Caballero.
