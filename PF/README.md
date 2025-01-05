# Detección y Comparación de Poses con MediaPipe

## Descripción

Este proyecto consiste en un conjunto de scripts en Python que permiten extraer ángulos del cuerpo usando la librería MediaPipe a partir de un video (previamente grabado o captado en vivo), 
comparar esos ángulos con los de otro video (o con la misma secuencia) y, finalmente, ejecutar un mini-juego (o comparador interactivo) en el que se miden ángulos corporales para verificar
la ejecución de una rutina, una coreografía o cualquier actividad que implique el seguimiento de una pose.

## Contenido del Repositorio

El repositorio incluye los siguientes ficheros:
- **extractVideo.py**
  - Extrae los ángulos del cuerpo (codos y rodillas, izquierdo y derecho) de cada fotograma de un video y los guarda en un archivo CSV.
  - Permite visualizar (de forma opcional) el video con los landmarks de MediaPipe dibujados encima.
- **compareVideo.py**
  - Compara los ángulos extraídos de un video (almacenados en angles.csv) con los ángulos de otro video (o el streaming de la webcam).
  - Calcula y muestra la precisión de la coincidencia fotograma a fotograma.
  - Genera un archivo CSV con los resultados de la comparación.
- **final_comparator.py**
  - Inicia una interfaz gráfica (con tkinter) para:
    - Seleccionar la dificultad (fácil, medio, difícil).
    - Escoger el modo de juego (con ayuda o sin ayuda).
    - Ingresar el nombre del jugador.
  - Realiza una comparación de ángulos en tiempo real utilizando un video (mix2.mp4 es el nombre por defecto).
  - Muestra un score (puntaje) y guarda la partida (nombre, puntuación, tiempo jugado y modo/dificultad) en records.json.
  - Presenta un ranking de los mejores puntajes tras finalizar la ejecución.

## Requisitos Previos

- **Python 3.7+.**
- **Dependencias de Python:**
  - opencv-python (cv2)
  - mediapipe
  - numpy
  - tkinter (suele venir instalado por defecto con Python; de lo contrario, debe instalarlo según su SO).
  - Módulos estándar: csv, json, os, time.
- **Archivos de video:**
  - Se asume que cuentas con un archivo PF/loveMe.mp4 (o cualquier otro) y/o mix2.mp4. Ajusta las rutas en los scripts para usar tus propios videos.

## Instalación de dependencias

Para instalar las principales librerías, si aún no las tienes, ejecuta en consola:
```bash
pip install opencv-python mediapipe numpy
```
> **Nota: En la mayoría de instalaciones de Python en sistemas operativos comunes, tkinter viene incluido. De no ser así, revisa la documentación oficial.**
