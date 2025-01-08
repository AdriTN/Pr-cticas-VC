import cv2
import mediapipe as mp
import numpy as np
import csv
import os

# Función para calcular el ángulo entre tres puntos
def calculate_angle(a, b, c):
    a = np.array(a)  # Punto A
    b = np.array(b)  # Punto B (vértice)&&
    c = np.array(c)  # Punto C
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    return np.degrees(angle)

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Carpeta de imágenes
input_folder = "posturas"  # Carpeta donde están las imágenes
output_csv = "angles.csv"  # Archivo CSV para almacenar resultados

# Crear o abrir el archivo CSV
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Escribir encabezados
    writer.writerow(["Image", "Left Elbow", "Right Elbow", "Left Knee", "Right Knee"])

    # Procesar cada imagen en la carpeta
    for image_name in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_name)

        # Leer la imagen
        image = cv2.imread(image_path)
        if image is None:
            print(f"No se pudo cargar la imagen: {image_name}")
            continue
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        # Extraer puntos clave
        landmarks = results.pose_landmarks
        if landmarks:
            # Lista de puntos clave
            keypoints = [
                (int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]))
                for landmark in landmarks.landmark
            ]
            
            # Calcular ángulos
            angles = {}
            angles['left_elbow'] = calculate_angle(
                keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value],
            )
            angles['right_elbow'] = calculate_angle(
                keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value],
            )
            angles['left_knee'] = calculate_angle(
                keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
                keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
                keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value],
            )
            angles['right_knee'] = calculate_angle(
                keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
                keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
            )

            # Guardar resultados en el CSV
            writer.writerow([
                input_folder+"/"+image_name, 
                angles['left_elbow'], 
                angles['right_elbow'], 
                angles['left_knee'], 
                angles['right_knee']
            ])

            print(f"Procesada imagen: {image_name}")
        else:
            print(f"No se detectaron puntos clave en la imagen: {image_name}")

# Cerrar MediaPipe
pose.close()

print(f"Resultados guardados en {output_csv}")
