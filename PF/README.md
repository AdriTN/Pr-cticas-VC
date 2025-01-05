# Detección y Comparación de Poses con MediaPipe

## Descripción

Este proyecto consiste en un conjunto de scripts en Python que permiten extraer ángulos del cuerpo usando la librería MediaPipe a partir de un video (previamente grabado o captado en vivo), 
comparar esos ángulos con los de otro video (o con la misma secuencia) y, finalmente, ejecutar un mini-juego (o comparador interactivo) en el que se miden ángulos corporales para verificar
la ejecución de una rutina, una coreografía o cualquier actividad que implique el seguimiento de una pose.

---

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

---

## Requisitos Previos

- **Python 3.7+.**
- **Dependencias de Python:**
  - opencv-python (cv2)
  - mediapipe
  - numpy
  - tkinter (suele venir instalado por defecto con Python; de lo contrario, debe instalarlo según su SO).
  - Módulos estándar: csv, json, os, time.
- **Archivos de video:**
  - Se asume que cuenta con un archivo PF/loveMe.mp4 (o cualquier otro) y/o mix2.mp4. Ajuste las rutas en los scripts para usar tus propios videos.

---

## Instalación de dependencias

Para instalar las principales librerías, si aún no las tiene, ejecute en consola:
```bash
pip install opencv-python mediapipe numpy
```
> **Nota: En la mayoría de instalaciones de Python en sistemas operativos comunes, tkinter viene incluido. De no ser así, revise la documentación oficial.**

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

# Autores: Adrián Talavera Naranjo y Arhamis Gutierrez Caballero
