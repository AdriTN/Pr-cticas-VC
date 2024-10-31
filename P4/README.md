# Proyecto de Visión Computacional: Sistema de Detección y Reconocimiento de Vehículos y Matrículas

Este proyecto de visión por computador está enfocado en la detección y seguimiento de vehículos y personas, así como en el reconocimiento óptico de caracteres (OCR) de matrículas. El sistema está diseñado para analizar secuencias de video, identificar distintos tipos de objetos en movimiento y extraer información de las matrículas de los vehículos detectados.

Este README detalla las funcionalidades, configuración y estructura del cuaderno de Jupyter.
---

## Descripción General

Este proyecto combina técnicas de detección de objetos y OCR para crear un sistema que pueda procesar eficazmente imágenes de video. Utiliza modelos de detección YOLO preentrenados y la biblioteca EasyOCR, lo que permite no solo detectar y clasificar objetos, sino también leer matrículas y corregir posibles errores de reconocimiento.

### Componentes Principales
1. **Modelos YOLO**: Usamos dos modelos YOLO especializados: uno para detectar vehículos y personas y otro para detectar matrículas.
2. **EasyOCR**: Implementamos OCR para leer y decodificar caracteres de las matrículas.
3. **Procesamiento y Almacenamiento**: Toda la información obtenida se guarda en un archivo CSV, lo que facilita su análisis posterior.

---

## Instalación y Configuración

### Dependencias
Antes de ejecutar el cuaderno, debe instalar todas las bibliotecas necesarias. Esta es la lista:
- **ultralytics**: Para cargar y ejecutar los modelos YOLO.
- **OpenCV (cv2)**: Para manejar la lectura y procesamiento de video e imágenes.
- **easyocr**: Para el reconocimiento óptico de caracteres.
- **numpy**: Para manipulación de datos numéricos y arrays.
- **csv**: Para escribir y manejar los datos de detecciones en formato CSV.
- **collections**: Para gestionar eficientemente los historiales de seguimiento.

Puede instalar las dependencias ejecutando el siguiente comando en el entorno de Python:

```bash
pip install ultralytics opencv-python easyocr numpy
```

---

## Estructura del Proyecto

El cuaderno se organiza en diferentes secciones, cada una de las cuales desempeña un papel esencial en la detección y reconocimiento de objetos.

### 1. **Importación de Librerías**
La primera celda del cuaderno importa todas las bibliotecas necesarias:

```python
from ultralytics import YOLO
import cv2
import easyocr
import csv
import numpy as np
import string
from collections import defaultdict, Counter
```

---

### 2. **Inicialización de Modelos YOLO**
- **Modelo de Detección General**: Se carga el modelo YOLO preentrenado `yolo11n.pt` para detectar vehículos (coches, camiones, autobuses, etc.) y personas.
- **Modelo de Detección de Matrículas**: Se carga `license_plate_detector.pt` para localizar matrículas en los vehículos detectados.

```python
detector = YOLO("yolo11n.pt")
detector_matriculas = YOLO("license_plate_detector.pt")
```
---

### 3. **Configuración del Lector de OCR**
Se inicializa EasyOCR para leer los caracteres de las matrículas. El idioma predeterminado es el inglés (`en`), pero puedes ajustarlo según tu región.

```python
ocr_reader = easyocr.Reader(['en'])
```

Se utiliza un defaultdict para llevar un historial de seguimiento de cada objeto detectado, lo que ayuda a realizar un seguimiento eficaz en múltiples fotogramas.
---

### 4. **Configuración de Clases y Paleta de Colores**
Aquí definimos las clases de objetos que detectará el modelo y asignamos colores para diferenciarlos visualmente:

- **Clases Detectadas**: Personas, bicicletas, coches, motocicletas, autobuses y camiones.
- **Paleta de Colores**: Cada clase tiene un color distintivo para facilitar la identificación visual en los fotogramas procesados.

También se define una lógica para corregir errores comunes de OCR, como la confusión entre ‘O’ y ‘0’ o ‘I’ y ‘1’:

```python
dict_char_to_int = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5'}
dict_int_to_char = {'0': 'O', '1': 'I', '3': 'J', '4': 'A', '6': 'G', '5': 'S'}
```
---

### 5. **Creación del Archivo CSV**
Se crea un archivo CSV llamado `detecciones.csv` para registrar los resultados. Los datos incluyen:

- Número de fotograma.
- Tipo de objeto (vehículo o persona).
- Confianza de detección.
- Coordenadas de los cuadros delimitadores.
- Texto de la matrícula (en caso de detección exitosa).
- Confianza del OCR y coordenadas de la matrícula.

```python
with open("detecciones.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["fotograma", "tipo_objeto", "confianza", "identificador_tracking", 
                     "x1", "y1", "x2", "y2", "matricula_en_su_caso", "confianza_matricula", 
                     "mx1", "my1", "mx2", "my2", "texto_matricula"])
```

Este archivo se actualiza continuamente a medida que se procesan más fotogramas.

---

### 6. **Procesamiento de Video**
El núcleo del proyecto es el procesamiento de video, que se ejecuta de manera fotograma por fotograma. Aquí se realiza la detección, se extraen las matrículas, y se utilizan algoritmos de seguimiento para manejar múltiples objetos en movimiento. Las lecturas de OCR se corrigen automáticamente según sea necesario.

> **Advertencia de Rendimiento**: Si ejecutas este proyecto en un entorno sin GPU, el procesamiento será más lento. Puedes optimizarlo ejecutándolo en un entorno de GPU, como Google Colab o una estación de trabajo con una GPU compatible.

---

## Resultados y Visualización

Los resultados se almacenan en `detecciones.csv` para facilitar el análisis posterior. El archivo incluye todos los detalles importantes de cada detección, lo que es ideal para:
- **Análisis estadístico**: Identificar patrones de tráfico o comportamientos de vehículos.
- **Validación de OCR**: Verificar la precisión del reconocimiento de matrículas y ajustar según sea necesario.

El cuaderno también muestra ejemplos visuales de las detecciones, lo que permite validar visualmente el rendimiento del sistema.


# Cradores: AAdrián Talavera Naranjo y Arhamis Gutiérrez Caballero.
