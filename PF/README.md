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
