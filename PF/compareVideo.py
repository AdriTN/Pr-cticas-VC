import cv2
import mediapipe as mp
import numpy as np
import csv
import pandas as pd

# Función para calcular los ángulos
def calculate_angle(a, b, c):
    a = np.array(a)  # Punto A
    b = np.array(b)  # Punto B (vértice)
    c = np.array(c)  # Punto C
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return int(angle)  # Mantén como float

# Función para obtener coordenadas
def get_coords(landmark, default=[0, 0]):
    return [landmark.x, landmark.y] if landmark and landmark.visibility > 0.5 else default

# Parámetros
video_path = "loveMe.mp4"  # Ruta del video a procesar
csv_base_path = "angles.csv"  # Archivo CSV base para comparación
output_csv = "video_angles_corrected.csv"  # Nuevo archivo CSV con diferencias corregidas
margin_of_error = 10  # Margen de error en grados

# Leer y procesar los datos del CSV base
base_data = pd.read_csv(csv_base_path, skiprows=1, usecols=[1, 2, 3, 4])

# Convertir '&&' y otros valores no numéricos a NaN
base_data = base_data.replace("&&", np.nan).apply(pd.to_numeric, errors='coerce')

# Inicializar Mediapipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Abrir el video
cap = cv2.VideoCapture(video_path)

# Abrir el archivo CSV para escribir
with open(output_csv, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Frame', 'LeftElbow', 'RightElbow', 'LeftKnee', 'RightKnee', 
                        'Similarity (%)', 'Diff_LeftElbow', 'Diff_RightElbow', 
                        'Diff_LeftKnee', 'Diff_RightKnee'])

    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_idx = 0
        q = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or q >= len(base_data):
                break

            # Convertir a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                # Obtener landmarks
                landmarks = results.pose_landmarks.landmark

                # Coordenadas de interés
                left_shoulder = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
                left_elbow = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value])
                left_wrist = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

                right_shoulder = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
                right_elbow = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
                right_wrist = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

                left_hip = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
                left_knee = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
                left_ankle = get_coords(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

                right_hip = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
                right_knee = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
                right_ankle = get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

                # Calcular ángulos
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

                # Calcular diferencias y coincidencias
                matches = 0
                diffs = []
                print(left_elbow_angle)
                print(base_data.iloc[q,0])

                for idx, (calculated_angle, base_angle) in enumerate(zip(
                    [left_elbow_angle, right_elbow_angle, left_knee_angle, right_knee_angle], 
                    base_data.iloc[q]
                )):
                    if pd.isna(base_angle):  # Si el valor base es NaN ('&&')
                        diffs.append(0)
                        matches += 1
                    else:
                        diff = abs(calculated_angle - base_angle)
                        diffs.append(diff)
                        if diff <= margin_of_error:
                            matches += 1

                # Calcular porcentaje de similitud
                similarity_percentage = (matches / 4) * 100

                # Guardar ángulos, similitud y diferencias en el CSV
                csvwriter.writerow([frame_idx, left_elbow_angle, right_elbow_angle, left_knee_angle, 
                                    right_knee_angle, similarity_percentage, *diffs])

                q += 1

            frame_idx += 1

cap.release()

print(f"Resultados guardados en: {output_csv}")
