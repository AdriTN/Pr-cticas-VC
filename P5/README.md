# Práctica 5: Juego Interactivo con Detección Facial

Este proyecto es un juego interactivo que utiliza la detección facial para controlar un personaje en pantalla. Similar al juego "Flappy Bird", el jugador debe mover su cabeza para evitar obstáculos que se desplazan horizontalmente. El juego utiliza la cámara web para detectar la posición de la nariz del jugador y superpone una imagen de un pájaro en tiempo real.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Funcionamiento del Código](#funcionamiento-del-código)
  - [Importación de Librerías](#importación-de-librerías)
  - [Funciones Auxiliares](#funciones-auxiliares)
  - [Clases Principales](#clases-principales)
  - [Lógica del Juego](#lógica-del-juego)
- [Créditos](#créditos)

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

4. **Ejecutar el script:**

Navega hasta el directorio donde se encuentra el script y ejecuta:

```bash
python nombre_del_script.py
```

## Uso