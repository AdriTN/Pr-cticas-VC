# Detección y Comparación de Poses con MediaPipe

> **Resumen**  
> Este repositorio reúne un conjunto de scripts en Python que permiten:  
> 1. **Extraer** ángulos corporales (codos y rodillas) a partir de imágenes en una carpeta.  
> 2. **Comparar** dichos ángulos con una referencia durante la ejecución de un **mini-juego** o **comparador interactivo** para verificar poses en tiempo real.  
>
> Se basa en [MediaPipe](https://google.github.io/mediapipe/) para la detección de *landmarks* corporales y [OpenCV](https://opencv.org/) para la lectura y visualización de video.

---

## Tabla de Contenidos
1. [Descripción](#descripción)  
2. [Contenido del Repositorio](#contenido-del-repositorio)  
3. [Requisitos Previos](#requisitos-previos)  
4. [Instalación de Dependencias con Anaconda](#instalación-de-dependencias-con-anaconda)  
5. [Guía de Uso de Cada Script](#guía-de-uso-de-cada-script)  
   - [final_extract.py](#1-final_extractpy)  
   - [final_comparator.py](#2-final_comparatorpy)  
6. [Funciones Principales](#funciones-principales)  
   - [final_extract.py](#final_extractpy)  
   - [final_comparator.py](#final_comparatorpy)  
7. [Personalización](#personalización)  
8. [Posibles Errores y Soluciones](#posibles-errores-y-soluciones)  
9. [Notas Finales](#notas-finales)  
10. [Autores](#autores) 

---

## Descripción
Este proyecto consiste en un conjunto de scripts en **Python** que:

- **Extraen** ángulos del cuerpo (codos y rodillas) usando la librería [MediaPipe](https://google.github.io/mediapipe/) a partir de imágenes estáticas en una carpeta.
- **Comparan** dichos ángulos con los de un video en tiempo real o pregrabado, mostrando retroalimentación visual de cada pose.
- Ofrecen un **mini-juego** o **comparador interactivo** que mide ángulos corporales para verificar la ejecución de una rutina o actividad de movimiento.

Ejemplos de uso potencial:
  - Evaluación de una coreografía.
  - Seguimiento de rutina de ejercicios.
  - Entrenamiento en artes marciales o deportes.

> **Nota**: Se pueden ajustar varios parámetros (umbrales, rutas de video, etc.) según las necesidades específicas.

---

## Contenido del Repositorio

Este repositorio incluye los siguientes ficheros y su propósito:

- **`final_extract.py`**  
  - Lee todas las imágenes de una carpeta (por defecto, `posturas`) y para cada imagen detecta la pose con MediaPipe.
  - Extrae los ángulos de codos y rodillas (tanto izquierdo como derecho) y los guarda en un archivo CSV (`angles.csv`).
  - Útil para generar una base de poses de referencia que luego se pueden comparar.

- **`final_comparator.py`**  
  - Inicia una interfaz gráfica (con `tkinter`) para seleccionar:  
    1. **Dificultad** (Fácil, Medio, Difícil).  
    2. **Modo de juego** (Con ayuda o Sin ayuda).  
    3. **Nombre del jugador**.  
  - Compara los ángulos en tiempo real usando un video (`mix2.mp4` por defecto) y muestra un *score* (puntaje).  
  - Guarda la partida (nombre, puntuación, tiempo jugado, modo, dificultad) en `records.json`.  
  - Muestra un **ranking** de las mejores puntuaciones al finalizar.

---

## Requisitos Previos

- **Python 3.7+** (recomendado 3.8 o superior, preferiblemente manejado con Anaconda).
- **Dependencias de Python**:
  - [OpenCV](https://pypi.org/project/opencv-python/) (`cv2`)
  - [MediaPipe](https://pypi.org/project/mediapipe/)
  - [NumPy](https://pypi.org/project/numpy/)
  - [tkinter](https://docs.python.org/3/library/tkinter.html) (suele venir incluido con Python; de lo contrario, revisa la documentación).
  - Módulos estándar: `csv`, `json`, `os`, `time`.

- **Archivos y carpeta**:
  - Carpeta `posturas` con las imágenes que deseas procesar (para `final_extract.py`).
  - Un video (por ejemplo, `mix2.mp4`) que se usa en `final_comparator.py` para detectar la pose en tiempo real.

---

## Instalación de Dependencias con Anaconda

1. **Crear un entorno virtual con Anaconda**  
   Abra su terminal y ejecute:
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

### 1) `final_extract.py`

Este script lee todas las imágenes en la carpeta `posturas` (o la que configures) y:
  - Detecta la pose con MediaPipe.
  - Calcula los ángulos de codos y rodillas (izquierda y derecha).
  - Guarda los resultados en un archivo CSV (`angles.csv`).

Cada fila en el CSV final corresponde a **una imagen** y contiene:
  - El nombre de la imagen.
  - Los ángulos calculados en esa imagen (si no se detectaron landmarks, mostrará un mensaje en consola).

**Uso:**
1. Abre el archivo `final_extract.py`.
2. Modifica la variable `input_folder` si deseas cambiar la carpeta de origen de las imágenes (por defecto, `posturas`).
3. Ejecuta el script:
   ```bash
   python final_extract.py
   ```
4. Al finalizar, se genera un archivo angles.csv en el mismo directorio.

**Resultado:**
- Se genera el fichero angles.csv con la estructura:
  ```bash
  Image,Left Elbow,Right Elbow,Left Knee,Right Knee
   imagen1.jpg, ...
   imagen2.jpg, ...
   ...
  ```

---

### 2) `final_comparator.py`
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

## Funciones Principales

### `final_extract.py`

#### `calculate_angle(a, b, c)`
- **Objetivo**: Calcular el ángulo entre tres puntos (A, B, C).  
- **Uso principal**: Se utiliza para determinar la inclinación de codos y rodillas a partir de las coordenadas (x, y) de cada *landmark*.  
- **Parámetros**:  
  - `a`: Coordenadas del primer punto (ej. hombro).  
  - `b`: Coordenadas del punto central (ej. codo).  
  - `c`: Coordenadas del tercer punto (ej. muñeca).  
- **Devuelve**: Un valor en grados (float) con el ángulo calculado.

#### Bucle principal
- **Flujo general**:  
  1. Lee todas las imágenes de la carpeta (`posturas` por defecto).  
  2. Para cada imagen, usa MediaPipe Pose para detectar los landmarks.  
  3. Llama a `calculate_angle()` para codo izquierdo, codo derecho, rodilla izquierda y rodilla derecha.  
  4. Almacena los resultados en `angles.csv` (columnas: `Image, Left Elbow, Right Elbow, Left Knee, Right Knee`).  

---

### `final_comparator.py`

#### `calculate_angle(a, b, c)`
- **Objetivo**: Mismo propósito que en `final_extract.py`, pero en el flujo de procesamiento de video.  
- **Uso principal**: Calcular el ángulo de cada articulación (codo, rodilla) en tiempo real o en cada fotograma del video.

#### `load_reference_angles(csv_file)`
- **Objetivo**: Cargar los ángulos de referencia desde un CSV (por defecto, `angles.csv`).  
- **Contenido**:
  - Primera columna: rutas de imágenes de referencia.  
  - Siguientes columnas: ángulos de codos y rodillas.  
- **Devuelve**:
  - `images`: Lista de rutas/nombres de imágenes.  
  - `reference_angles`: Lista de listas con los ángulos correspondientes a cada imagen.

#### `calculate_differences(reference_angles, current_angles)`
- **Objetivo**: Calcular la diferencia entre los ángulos de referencia y los ángulos actuales.  
- **Flujo**:
  1. Calcula la diferencia absoluta para cada ángulo.  
  2. Verifica si está dentro de un margen de error (`MARGIN_OF_ERROR`).  
- **Devuelve**:
  - `differences`: Lista de diferencias numéricas (float).  
  - `results`: Lista booleana indicando si cada ángulo coincide o no.

#### `save_record(player_name, score, difficulty)`
- **Objetivo**: Guardar en `records.json` (formato JSON) la información de la partida.  
- **Campos**:  
  - `name`, `score`, `time_played`, `mode`, `difficulty`.

#### `process_video(video_path, reference_images, reference_angles, output_folder)`
- **Objetivo**: Procesar un video para comparar pose por pose con las referencias.  
- **Pasos principales**:
  1. Inicializa la captura de video con OpenCV.  
  2. Detecta la pose en cada fotograma con MediaPipe Pose.  
  3. Llama a `calculate_differences(...)` para comparar contra la referencia actual.  
  4. Si se cumple la pose, aumenta `score`, guarda captura y pasa a la siguiente pose.  
  5. Maneja el tiempo límite (`TIME_LIMIT`).  
  6. Al finalizar, llama a `save_record(...)` para guardar los resultados.

#### `load_and_sort_records(file_path)`
- **Objetivo**: Cargar `records.json` y separar registros según modo (Con ayuda / Sin ayuda).  
- **Flujo**:
  - Ordena los registros por puntuación (score).  
- **Devuelve**:
  - Dos listas (`con_ayuda`, `sin_ayuda`) con los registros ordenados de mayor a menor score.

#### `display_rankings(con_ayuda, sin_ayuda)`
- **Objetivo**: Mostrar en una ventana `tkinter` el ranking de los mejores puntajes.  
- **Flujo**:
  - Dos columnas: Con ayuda y Sin ayuda.  
  - Muestra los top 10 de cada modalidad.

#### `start_program()`
- **Objetivo**: Función que se llama al pulsar **Iniciar** en la interfaz.  
- **Flujo**:
  1. Toma el nombre, dificultad, modo.  
  2. Ajusta `MARGIN_OF_ERROR` y `TIME_LIMIT`.  
  3. Cierra la ventana de configuración.  
  4. Carga `angles.csv` con `load_reference_angles()`.  
  5. Ejecuta `process_video()`.  
  6. Carga los registros y muestra el ranking.

#### Interfaz gráfica (Ventana principal `tkinter`)
- **Objetivo**: Capturar la información de la partida (nombre, dificultad, modo) y llamar a `start_program()`.

---

## Personalización
1. **Cambio de carpeta de imágenes (`final_extract.py`):**
  - Ajusta la variable input_folder si tus imágenes están en otra ubicación distinta a posturas.
2. **Cambio de video (`final_comparator.py`)**
  - Modifica la variable `video_path` si deseas usar un video propio en lugar de `mix2.mp4`.
3. **Umbrales y tiempo límite:**
  - En `final_comparator.py`, la dificultad ajusta los valores de `MARGIN_OF_ERROR` y `TIME_LIMIT`. Puedes cambiarlos a tu gusto.
4. **Carpetas de salida:**
  - Si quieres otro nombre o ubicación para `angles.csv`, `records.json` o las capturas, modifica el path directamente en el código.

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
