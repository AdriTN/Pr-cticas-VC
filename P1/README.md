# Práctica 1 de Visión por Computador

Este cuaderno de Jupyter contiene varias tareas de manipulación de imágenes utilizando 'numpy', 'matplotlib' y 'OpenCV'. Desde la creación de texturas hasta la manipulación de videos en tiempo real, cada tarea tiene como objetivo demostrar diferentes técnicas de procesamiento de imágenes.

## Contenido

### Tarea 1: Crear una imagen con la textura de un tablero de ajedrez.
  - Se crea un tablero de ajedrez de 800 x 800 píxeles con casillas de tamaño cuadrado,  en este caso 100 píxeles.
  - Para crear el patrón del tablero, se alternan bloques negros y blancos utilizando    numpy.
  - Se utiliza 'matplotlib' para ver la imagen producida.

### Tarea 2: Crear una imagen estilo Mondrian.
  - Se crea una imagen blanca inicial y se definen los colores primarios característicos del estilo Mondian (rojo, azul y amarillo)
  - Se define el grosor de los bordes de las figuras.
  - Para simular el estilo Mondrian se hace uso de la libreria 'random'.
  - El resultado se muestra usando 'matplotlib'.

### Tarea 3.1: Resolver una de las tareas anteriores con las funciones de dibujo de 'OpenCV' (Tablero de ajedrez).
  - Se importa el módulo 'cv2' para usar las funciones mencionadas.
  - Se usa la función de dibujo 'rectangle' sobre la imágen generada en el ejercicio 1.
  - Se muestra el resultado usando 'matplotlib'.

### Tarea 3.2: Resolver una de las tareas anteriores con las funciones de dibujo de 'OpenCV' (Estilo Mondrian).
  - Se crea una nueva imagen para no escribir sobre figuras generadas aleatoriamente.
  - Se definen las lineas y los bloques de colores con sus posiciones y tamaños fijos.
  - Se usan las funciones 'rectangle' y 'line' para dibujar sobre la imagen nueva el estilo Mondrian.
  - Se muestra el resultado usando 'matplotlib'.

### Tarea 4.1: Modificar de forma libre los valores de un plano de la imagen.
  - Se captura la imagen de la cámara principal y se libera el objeto de la cámara.
  - Se modifica el plano eliminando el rojo.
  - Se muestra el resultado con 'matplotlib'.

### Tarea 4.2: Modifica de forma libre los valores de un plano de la imagen con un video (esc para cerrar).
  - Se captura la imagen de la cámara principal.
  - Mediante un bucle se van capturando los fotogramas.
  - Se modifica cada fotograma eliminando el color azul.
  - Se muestra el fotograma modificado.
  - Al salir del bucle pulsando 'ESC' se libera la cámara y se cierran la ventanas.

### Tarea 5.1: Pintar círculos en las posiciones del píxel más claro y oscuro de la imagen ¿Si quisieras hacerlo sobre la zona 8x8 más clara/oscura?
  - Se captura la imagen como el ejercicio 4.1.
  - Se convierte la imagen a escala de grises usando la función 'cvtColor'.
  - Se encuentra el píxel más claro (valor máximo) y el más oscuro (valor mínimo).
  - Se dibuja un círculo verde (0, 255, 0) en el pixel más claro y uno rojo (0, 0, 255) en el más oscuro.
  - Se muestra la imagen con 'matplotlib'.

### Tarea 5.2: ¿Si quisieras hacerlo sobre la zona 8x8 más clara/oscura?
  - Se captura la imagen.
  - Se define el tamaño del bloque a 8.
  - Se definen las variables para almacenar las posiciones más claras y oscuras.
  - Se itera sobre la imagen en bloques de 8x8 píxeles extrayendo cada bloque para calcular el promedio de brillo del bloque y encontrar la zona más clara y la más oscura con cada iteración.
  - Una vez terminado el bucle se dibuja un rectángulo verde en el bloque de 8x8 más claro y un rectángulo rojo en la más oscura.
  - Se muestra el resultado con 'matplotlib'.

### Tarea 5.3: Pintar círculos en las posiciones del píxel más claro y oscuro de la imagen ¿Si quisieras hacerlo sobre la zona 8x8 más clara/oscura? Con video.
  - Se sigue el mismo procedimiento que en los ejercicios 5.1 y 5.2 pero unificados y haciendo uso de un bucle while que va capturando y modificando cada fotograma.
  - Cuando se sale del bucle pulsando la tecla 'ESC' se libera la cámara y se cierran todas las ventanas.

### Tarea 6: LLevar a cabo una propuesta propia de pop art.
  - Se captura la imagen a través de la cámara principal, se guarda el frame y se libera la cámara.
  - Se redimensiona el frame para trabajar de forma más simple.
  - Se generan 4 versiones diferentes de la imagen con distintos efectos:
      1. Imagen saturada: Se usa la función 'convertScaleAbs' con alpha=1.5 y beta=50.
      2. Colores invertidos: Se usa la función 'bitewise_not'.
      3. Filtro de colores brillantes: Se modifica el canal azul para aumentar la cantidad de este color en la imagen (siempre dentro de los límites).
      4. Blanco y negro con alto contraste: Se convierte la imagen a una escala de grises para luego convertirla nuevamente a BGR pero con la misma información de la escala de grises. Por último, se ajusta el contraste de la imagen con la función 'convertScaleAbs'.

### Ampliación:
  - Se captura la imagen en tiempo real a través de la cámara principal.
  - El tamaño de los círculos es definido por el usuario mediante un input.
  - Se dibujan los círculos sobre la imagen, utilizando la función 'cv2.circle' para crear el mosaico de manera uniforme.
  - El efecto final da la apariencia de un mosaico en tiempo real con círculos coloreados según los píxeles de la imagen capturada.
  - Al salir del bucle pulsando 'ESC' se libera la cámara y se cierran la ventanas.

## Requisitos
Para ejecutar este cuaderno, es necesario tener instalados los siguientes paquetes:
  - numpy
  - matplotlib
  - opencv-python
Pueden ser instalados con el siguiente comando:

    pip installnumpy matplotlib opencv-python

## Instalación de Anaconda (Opcional)
En este proyecto see ha hecho uso de Anaconda para la gestión de dependencias y el entorno virtual. Si se desea replicar el entorno de desarrollo, se deben seguir los siguientes pasos:
  1. Instalar Anaconda.
  2. Crear un entorno virtual:
       conda create --name VC_P1 python=3.11.5
  3. Activar el entorno:
       conda activate VC_P1
  4. Instalar las dependencias:
       conda install numpy matplotlib opencv

## Ejecución
Los pasos a seguir para su ejecución son:
  1. Descargar el cuaderno Jupyter.
  2. Abrir el cuaderno en un entorno compatible como VisualStudio.
  3. Ejecutar cada celda para ver el resultado de las tareas.

## Nota:
Algunas de las tareas requieren de una cámara conectada a la computadora para capturar imágenes y video.
