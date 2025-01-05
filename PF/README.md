# Detección y Comparación de Poses con MediaPipe

> **Resumen**  
> Este repositorio reúne un conjunto de scripts en Python que permiten:  
> 1. **Extraer** ángulos corporales (codos y rodillas) a partir de un video.  
> 2. **Comparar** dichos ángulos con una referencia.  
> 3. Ejecutar un **mini-juego** (o comparador interactivo) para verificar poses en tiempo real.  
> 
> Se basa en [MediaPipe](https://google.github.io/mediapipe/) para la detección de *landmarks* corporales y [OpenCV](https://opencv.org/) para la lectura y visualización de video.

---

## Tabla de Contenidos
1. [Descripción](#descripción)
2. [Contenido del Repositorio](#contenido-del-repositorio)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalación de Dependencias con Anaconda](#instalación-de-dependencias-con-anaconda)
5. [Guía de Uso de Cada Script](#guía-de-uso-de-cada-script)
   - [extractVideo.py](#1-extractvideopy)
   - [compareVideo.py](#2-comparevideopy)
   - [final_comparator.py](#3-final_comparatorpy)
6. [Personalización](#personalización)
7. [Posibles Errores y Soluciones](#posibles-errores-y-soluciones)
8. [Notas Finales](#notas-finales)
9. [Autores](#autores)

---

## Descripción
Este proyecto consiste en un conjunto de scripts en **Python** que:
  - **Extraen** ángulos del cuerpo (codos y rodillas) usando la librería [MediaPipe](https://google.github.io/mediapipe/) a partir de un video (o streaming).
  - **Comparan** dichos ángulos con los de otro video (o la misma secuencia).
  - Ofrecen un **mini-juego** o **comparador interactivo** que mide ángulos corporales para verificar la ejecución de una rutina o actividad de movimiento.

Ejemplos de uso potencial:
  - Evaluación de una coreografía.
  - Seguimiento de rutina de ejercicios.
  - Entrenamiento en artes marciales o deportes.

> **Nota**: Se pueden ajustar varios parámetros (umbrales, rutas de video, etc.) según las necesidades específicas.

---

## Contenido del Repositorio

Este repositorio incluye los siguientes ficheros y su propósito:

- **`extractVideo.py`**  
  - Extrae los ángulos del cuerpo (codos y rodillas, tanto izquierdo como derecho) en cada fotograma de un video y los guarda en un archivo CSV (`angles.csv`).  
  - Permite visualizar de manera opcional el video con los *landmarks* de MediaPipe dibujados.

- **`compareVideo.py`**  
  - Compara los ángulos que se hayan extraído (en `angles.csv`) con los de otro video (o streaming de webcam).  
  - Calcula la precisión de la coincidencia fotograma a fotograma.  
  - Genera un archivo CSV (`comparison_results.csv`) con el detalle de la comparación y muestra estadísticas globales (precisión de ángulos y de fotogramas).

- **`final_comparator.py`**  
  - Inicia una interfaz gráfica (con `tkinter`) para seleccionar:  
    1. **Dificultad** (fácil, medio, difícil).  
    2. **Modo de juego** (con ayuda o sin ayuda).  
    3. **Nombre del jugador**.  
  - Compara ángulos en tiempo real usando un video (`mix2.mp4` por defecto) y muestra un *score* (puntaje).  
  - Guarda la partida (nombre, puntuación, tiempo jugado, modo, dificultad) en `records.json`.  
  - Muestra un **ranking** de las mejores puntuaciones al finalizar.

---

## Requisitos Previos

- **Python 3.7+** (recomendado 3.8 o superior, manejado con Anaconda).
- **Dependencias de Python**:
  - [OpenCV](https://pypi.org/project/opencv-python/) (`cv2`)
  - [MediaPipe](https://pypi.org/project/mediapipe/)
  - [NumPy](https://pypi.org/project/numpy/)
  - [tkinter](https://docs.python.org/3/library/tkinter.html) (suele venir incluido con Python; de lo contrario, revísese la documentación).
  - Módulos estándar: `csv`, `json`, `os`, `time`.

- **Archivos de video**:  
  - Por defecto, el proyecto asume la existencia de `PF/loveMe.mp4` y/o `mix2.mp4`. Ajustar las rutas en cada script si se desea usar otros archivos.

---

## Instalación de Dependencias con Anaconda

1. **Crear un entorno virtual con Anaconda**  
   Abra su terminal y ejecuta:
   ```bash
   conda create --name mediapipe_env python=3.8
   conda activate mediapipe_env
   ```
2. **Instalar las librerías necesarias**
   Ejecute los siguientes comandos dentro del entorno virtual:
   ```bash
   conda install -c conda-forge opencv
   pip install mediapipe numpy
   ```
   
---

## Guía de Uso de Cada Script

### 1) `extractVideo.py`

Este script lee un video (por defecto, PF/loveMe.mp4) y extrae los ángulos de:
  - Codo izquierdo
  - Codo derecho
  - Rodilla izquierda
  - Rodilla derecha

Cada fila en el CSV final corresponde a un fotograma del video y contiene:
  - El número de fotograma (frame).
  - Los ángulos calculados en ese fotograma (o “&&” si no se pudieron detectar).

**Uso:**
1. Abra el archivo extractVideo.py.
2. Modifique la variable video_path si desea cambiar la ruta del video de origen.
3. Ajuste la visualización (el script por defecto muestra el video mientras extrae los ángulos).
4. Ejecute el script:
  ```bash
  python extractVideo.py
  ```
5. Al finalizar, se genera un archivo angles.csv en el mismo directorio.

**Resultado:**
- Se genera el fichero angles.csv con la estructura:
  ```bash
  frame,left_elbow_angle,right_elbow_angle,left_knee_angle,right_knee_angle
  1, ...
  2, ...
  ...
  ```

---

### 2) `compareVideo.py`
Este script compara un video de entrada (por defecto PF/loveMe.mp4) con los ángulos de referencia que se hayan almacenado en angles.csv. Durante la comparación:
  - Se calcula cuántos fotogramas “coinciden” en la pose (basado en un umbral de ±5° de diferencia).
  - Se genera un archivo comparison_results.csv con el detalle de la comparación.
  - Muestra la precisión total de ángulos y la precisión en fotogramas (cuántos fotogramas cumplen todos los ángulos).

**Uso:**
1. Asegúrese de haber generado antes angles.csv (usando extractVideo.py o usando uno propio).
2. Abra y revise la variable video_path en compareVideo.py para cambiar la ruta del video a comparar.
3. Ejecute:
  ```bash
  python compareVideo.py
  ```
4. Observe en consola los ángulos que difieren, fotograma por fotograma, y la diferencia en grados.
5. Al finalizar, se muestra:
   - Precisión de ángulos: XX.XX%
   - Precisión de frames: XX.XX%
6. Se genera el archivo comparison_results.csv con el detalle de la comparación para cada fotograma.

---

### 3) `final_comparator.py`
Este script es un mini-juego o comparador interactivo con interfaz de usuario en tkinter.
Permite:
1. Elegir el nombre del jugador.
2. Seleccionar dificultad (Fácil, Medio, Difícil) — esto ajusta el margen de error (±20°, ±15°, ±5°) y el tiempo límite para mantener cada pose.
3. Seleccionar el modo (Con ayuda/Sin ayuda) — si se elige “Con ayuda”, los landmarks que no coinciden se pintan en rojo para guiar al usuario.

**Funcionamiento:**
  - Lee un archivo CSV de referencia (por defecto, angles.csv) que contiene una lista de fotogramas (aunque en este caso, el script asume que en la primera columna están rutas de imágenes de referencia y en las siguientes columnas, los ángulos, pero puede personalizarlo).
  - Usa un video (mix2.mp4) para detectar la pose del usuario en tiempo real (cada fotograma del video).
  - Compara los ángulos calculados con los ángulos de referencia actuales.
  - Cuando todos los ángulos caen dentro del margen de error, se sube la puntuación (score) en +1, se captura la imagen resultante y se avanza a la siguiente pose de referencia.
  - Hay un tiempo límite (en segundos) para lograr cada pose. Si se acaba el tiempo, avanza automáticamente a la siguiente pose.
  - Al final, guarda el registro en records.json, con el nombre, puntuación, tiempo jugado y modo.
  - Muestra un ranking de los 10 primeros puntajes en modo “Con ayuda” y en modo “Sin ayuda”.

**Uso:**
1. Ejecute:
  ```bash
  python final_comparator.py
  ```
2. En la ventana emergente:
  - Ingrese su nombre (opcional, si no, usará “test”).
  - Seleccione la dificultad (Fácil, Medio, Difícil).
  - Seleccione el modo (Con ayuda, Sin ayuda).
  - Pulse Iniciar.
3. Tras esto, se abre la ventana de OpenCV con el video mix2.mp4.
4. Verá un recuadro con la imagen de referencia (pose objetivo) y el tiempo restante para igualar la pose.
5. Si está en “Con ayuda”, podrá ver en verde los landmarks correctos y en rojo los incorrectos.
6. Una vez termine todas las poses o se acabe el video, aparecerá la ventana con el ranking de puntuaciones.

**Parámetros:**
  - `MARGIN_OF_ERROR`: Se ajusta según la dificultad.
  - `MODE_HELP`: Se activa si se selecciona “Con ayuda”.
  - `TIME_LIMIT`: Tiempo en segundos para mantener la pose antes de pasar a la siguiente.

**Archivos generados:**
  - `records.json`: Almacena los registros (nombre, score, tiempo, dificultad y modo).
  - `capturas/`: Carpeta donde se guardan capturas de pantalla cuando el usuario acierta una pose.
  - `diferencias.csv`: Guarda la diferencia en ángulos para cada fotograma.

---

## Personalización
1. **Cambio de videos:**
  - En cada script (`extractVideo.py`, `compareVideo.py`, `final_comparator.py`), modifique la variable `video_path` o rutas de referencia para usar sus propios archivos de video.
2. **Umbrales:**
  - En `compareVideo.py` la comparación por defecto usa ±5°. Puede ajustarlo en el código en la línea donde se compara `angle_diff <= 5`.
3. **Carpetas de salida:**
  - Si quiere cambiar dónde se guardan los resultados (`angles.csv`, `comparison_results.csv`, `capturas/`), puede modificar el path directamente en el código.

---

## Posibles Errores y Soluciones

1. **No se abre la ventana de tkinter o se cierra inmediatamente:**
  - Asegúrese de no estar ejecutando el script en un entorno que no soporte interfaces gráficas (por ejemplo, WSL sin configuración de X11).
2. **No se detecta bien la pose:**
  - Revise que haya buena iluminación y que la cámara (o video) muestre claramente las extremidades. En un ambiente real, MediaPipe se basa en la calidad de la imagen para detectar landmarks.
3. **El video no se reproduce fluidamente:**
  - Podría ser un tema de rendimiento. Reducir la resolución del video o usar un equipo con mayor capacidad de proceso.

## Notas Finales
- Este proyecto utiliza la detección de pose de MediaPipe, la cual aprovecha modelos de Machine Learning entrenados para ubicar con precisión los puntos clave en el cuerpo humano.
- Se recomienda usar Python 3.7 o superior para no tener conflictos con versiones de MediaPipe.
- Cualquier cambio en la estructura de los CSV (campos o formato) podría requerir ajustes en el código.
- El archivo records.json se va acumulando con cada partida nueva. Puede borrarlo si deseas reiniciar el historial.

# Autores 
- Adrián Talavera Naranjo
- Arhamis Gutierrez Caballero
