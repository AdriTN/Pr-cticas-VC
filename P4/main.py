# Importa las bibliotecas necesarias
from ultralytics import YOLO
import cv2
import easyocr
import csv
import math
import numpy as np
from collections import defaultdict

# Inicializa los modelos YOLO para detectar vehículos y el modelo de matrículas
detector_vehiculos = YOLO("yolo11n.pt")  # Modelo YOLO para detectar vehículos
detector_matriculas = YOLO("license_plate_detector.pt")  # Modelo para detectar matrículas

# Inicializa el lector de OCR
ocr_reader = easyocr.Reader(['en'])  # Cambia 'en' si necesitas otro idioma

# Diccionario para almacenar el historial de seguimiento
track_history = defaultdict(lambda: [])

# Nombres de clases para los vehículos y colores para dibujo
classNames = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]
color_palette = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Crear y abrir el archivo CSV para almacenar datos
with open("detecciones.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    # Escribe los encabezados
    writer.writerow(["fotograma", "tipo_objeto", "confianza", "identificador_tracking", 
                     "x1", "y1", "x2", "y2", "matricula_en_su_caso", "confianza_matricula", 
                     "mx1", "my1", "mx2", "my2", "texto_matricula"])

# Función para detectar y trackear vehículos y matrículas
def detectar_y_trackear(imagen, frame_id):
    # Realiza la detección con el modelo de vehículos y mantiene persistencia de ID
    resultados_vehiculos = detector_vehiculos.track(imagen, persist=True, classes=[2, 3, 5, 7])

    for r in resultados_vehiculos:
        boxes = r.boxes
        for box in boxes:
            # Extrae coordenadas y confianza del cuadro
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confianza = round(float(box.conf[0]), 2)
            
            # Etiqueta de seguimiento
            track_id = int(box.id[0].tolist()) if box.id is not None else -1

            # Verificar que cls esté dentro de los índices válidos para evitar IndexError
            cls = int(box.cls[0])
            if cls < 0 or cls >= len(classNames):
                print(f"Advertencia: Clase {cls} fuera de rango para classNames.")
                continue  # Salta a la siguiente detección si cls es inválido

            # Determina el color del cuadro según la clase
            color = color_palette[cls % len(color_palette)]

            # Dibuja el cuadro alrededor del vehículo y etiqueta con el ID y clase
            cv2.rectangle(imagen, (x1, y1), (x2, y2), color, 2)
            cv2.putText(imagen, f"ID {track_id} {classNames[cls]}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Actualiza el historial de seguimiento
            track_history[track_id].append((x1, y1, x2, y2))

            # Detecta matrículas dentro del cuadro del vehículo
            roi_vehiculo = imagen[y1:y2, x1:x2]
            resultados_matriculas = detector_matriculas(roi_vehiculo)

            # Inicializa datos de matrícula con valores por defecto
            abs_mx1, abs_my1, abs_mx2, abs_my2 = 0, 0, 0, 0
            texto_matricula = ""
            confianza_matricula = 0

            # Si se detecta una matrícula
            for m in resultados_matriculas[0].boxes:
                # Extrae coordenadas de la matrícula dentro del ROI
                mx1, my1, mx2, my2 = map(int, m.xyxy[0])
                confianza_matricula = round(float(m.conf[0]), 2)

                # Ajusta coordenadas a la imagen completa
                abs_mx1, abs_my1 = x1 + mx1, y1 + my1
                abs_mx2, abs_my2 = x1 + mx2, y1 + my2

                # OCR en la matrícula detectada
                roi_matricula = imagen[abs_my1:abs_my2, abs_mx1:abs_mx2]
                if roi_matricula.size > 0:
                    resultado_ocr = ocr_reader.readtext(roi_matricula)
                    if resultado_ocr:
                        texto_matricula = resultado_ocr[0][-2]  # Texto detectado en la matrícula
                break  # Salimos después de la primera detección de matrícula

            # Dibuja el cuadro de la matrícula y texto si hay OCR
            if abs_mx1 != 0 and abs_my1 != 0 and abs_mx2 != 0 and abs_my2 != 0:
                cv2.rectangle(imagen, (abs_mx1, abs_my1), (abs_mx2, abs_my2), (255, 0, 0), 2)
                if texto_matricula:
                    cv2.putText(imagen, texto_matricula, (abs_mx1, abs_my1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Escribe en el CSV los datos de la detección
            with open("detecciones.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([frame_id, classNames[cls], confianza, track_id, x1, y1, x2, y2,
                                 1 if texto_matricula else 0, confianza_matricula, 
                                 abs_mx1, abs_my1, abs_mx2, abs_my2, texto_matricula])

    return imagen

# Cargar el video y configurar el VideoWriter para guardar el video procesado
cap = cv2.VideoCapture("sample2.mp4")  # Cambia "sample.mp4" por tu archivo de video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
out = cv2.VideoWriter("video_modificado.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

frame_id = 0  # Contador de fotogramas

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Procesa cada fotograma con detección y seguimiento
    frame = detectar_y_trackear(frame, frame_id)

    # Escribe el frame procesado en el video de salida
    out.write(frame)

    # Incrementa el contador de fotogramas
    frame_id += 1



# Libera los recursos
cap.release()
out.release()
