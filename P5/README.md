# Práctica 5: Juego Interactivo con Detección Facial

Este proyecto es un juego interactivo que utiliza la detección facial para controlar un personaje en pantalla. Similar al juego "Flappy Bird", el jugador debe mover su cabeza para evitar obstáculos que se desplazan horizontalmente. El juego utiliza la cámara web para detectar la posición de la nariz del jugador y superpone una imagen de un pájaro en tiempo real.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Funcionamiento del Código](#funcionamiento-del-código)
- [Créditos](#créditos)
- [Resultado](#resultado)

## Descripción

El juego detecta la posición de la nariz del usuario mediante la cámara web y utiliza esa información para posicionar un pájaro en la pantalla. El jugador debe mover su cabeza hacia arriba y hacia abajo para esquivar obstáculos en forma de tuberías que se desplazan de derecha a izquierda. El objetivo es obtener la mayor cantidad de puntos posible evitando colisiones con los obstáculos.

## Requisitos

- Python 3.x
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
- Tkinter (`tkinter`)
- Webcam integrada o externa

## Instalación

1. **Clonar el repositorio o descargar el código fuente.**

2. **Instalar las dependencias necesarias:**

```bash
pip install opencv-python mediapipe numpy
```

3. **Asegurarse de tener las imágenes necesarias:**

* **bird.png**: Imagen del pájaro con canal alfa (transparencia).
* **pipe.png**: Imagen de la tubería con canal alfa.

Estas imágenes deben estar ubicadas en la carpeta P5/.

## Uso

**Controles:**

- Mueve tu cabeza hacia arriba y hacia abajo para controlar el pájaro.
- Evita las tuberías para acumular puntos.
- El juego termina al chocar con un obstáculo o al alcanzar el puntaje máximo.

**Salir del juego:**

- Presiona la tecla Esc para salir en cualquier momento.

## Funcionamiento del Código

El juego se organiza en varias secciones que realizan tareas específicas:

**Detección Facial:** El juego utiliza la cámara para detectar la cara del jugador y localizar la posición de la nariz. Esta posición se traduce en coordenadas que determinan la ubicación del pájaro en la pantalla. La biblioteca MediaPipe es la encargada de la detección facial en tiempo real, mientras que OpenCV convierte las imágenes y procesa los datos obtenidos de la cámara.

**Superposición de Imágenes:** Una imagen de pájaro se superpone en la nariz del jugador, y su posición se actualiza continuamente en función de los movimientos de la cabeza del jugador. Esto permite la sincronización del pájaro con los movimientos de la persona.

**Generación de Obstáculos:** Los obstáculos (tuberías) se generan en posiciones aleatorias con huecos de tamaño variable. Las tuberías se mueven horizontalmente de derecha a izquierda en la pantalla. Cada tubería es un objeto que actualiza su posición en el tiempo, lo que da la apariencia de movimiento.

**Detección de Colisiones:** Para asegurar que el juego sea desafiante, se verifica si el pájaro entra en contacto con alguna de las tuberías. Si se detecta una colisión entre el personaje y los obstáculos, el juego se detiene y muestra el puntaje del jugador.

**Aumento de Dificultad:** A medida que el jugador acumula puntos, la velocidad de los obstáculos aumenta gradualmente, incrementando la dificultad del juego. Cada cierto puntaje se incrementa la velocidad.

**Bucle de Juego Principal:** El juego opera dentro de un bucle que actualiza el estado de la pantalla en función de los datos de la cámara, los movimientos del jugador y la posición de los obstáculos. El bucle también monitorea las condiciones de finalización del juego.

## Resultado final
![video resultado](flappyBird.gif)

## Créditos
**Desarrollador: Adrián Talavera Naranjo y Arhamis Gutiérrez Caballero**
**Recursos: Este juego utiliza OpenCV para el procesamiento de video, MediaPipe para la detección facial, y NumPy para las operaciones con matrices.**
