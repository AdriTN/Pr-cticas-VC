import cv2
import mediapipe as mp
import numpy as np
import csv
import os

# Margen de error global en grados
MARGIN_OF_ERROR = 10  # Cambia este valor para ajustar el margen de error

# Función para calcular el ángulo entre tres puntos
def calculate_angle(a, b, c):
    a = np.array(a)  # Punto A
    b = np.array(b)  # Punto B (vértice)
    c = np.array(c)  # Punto C
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return int(angle)  # Mantén como float

# Cargar los ángulos del CSV anterior
def load_reference_angles(csv_file):
    reference_angles = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            # Validar que la fila tiene 5 columnas
            if len(row) != 5:
                print(f"Advertencia: Fila mal formateada o incompleta {row}")
                continue
            try:
                angles = {
                    'left_elbow': float(row[1]),
                    'right_elbow': float(row[2]),
                    'left_knee': float(row[3]),
                    'right_knee': float(row[4]),
                }
                reference_angles.append(angles)
            except ValueError:
                print(f"Advertencia: Fila con valores no válidos {row}")
                continue
    return reference_angles

# Comparar ángulos entre referencia y cuadro actual
def compare_angles(reference_angles, current_angles):
    for joint in reference_angles:
        if joint in current_angles:
            diff = abs(reference_angles[joint] - current_angles[joint])
            if diff > MARGIN_OF_ERROR:
                return False  # Si un ángulo no coincide, salir
    return True  # Todos los ángulos coinciden

# Procesar un video
def process_video(video_path, reference_angles_list, output_folder):
    # Inicializar MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    
    # Crear carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    
    # Abrir el video
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    capture_count = 0

    current_reference_index = 0

    while cap.isOpened() and current_reference_index < len(reference_angles_list):
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        # Extraer puntos clave y calcular ángulos
        landmarks = results.pose_landmarks
        if landmarks:
            keypoints = [
                (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                for landmark in landmarks.landmark
            ]

            current_angles = {
                'left_elbow': calculate_angle(
                    keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                    keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                    keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value],
                ),
                'right_elbow': calculate_angle(
                    keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                    keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                    keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                ),
                'left_knee': calculate_angle(
                    keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
                    keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
                    keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                ),
                'right_knee': calculate_angle(
                    keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
                    keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                    keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                ),
            }

            # Comparar ángulos con referencia actual
            if compare_angles(reference_angles_list[current_reference_index], current_angles):
                capture_count += 1
                capture_path = os.path.join(output_folder, f"capture_frame_{frame_number}_pose_{current_reference_index+1}.jpg")
                cv2.imwrite(capture_path, frame)
                print(f"Captura guardada: {capture_path}")
                
                # Avanzar al siguiente conjunto de ángulos y reiniciar búsqueda desde el inicio del video
                current_reference_index += 1
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    cap.release()
    pose.close()
    print(f"Proceso completado. Capturas guardadas: {capture_count}")

# Programa principal
if __name__ == "__main__":
    # Rutas
    reference_csv = "angles.csv"  # CSV generado por el primer programa
    video_path = "vela.mp4"  # Cambia a la ruta de tu video
    output_folder = "capturas"  # Carpeta donde se guardarán las capturas

    # Cargar los ángulos de referencia
    reference_angles_list = load_reference_angles(reference_csv)

    # Procesar el video
    process_video(video_path, reference_angles_list, output_folder)
