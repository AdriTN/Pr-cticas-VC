import cv2
import mediapipe as mp
import numpy as np
import csv

# Leer angles.csv y almacenarlo en angles_reference
angles_reference = {}
with open('angles.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        frame_number = int(row['frame'])
        angles_reference[frame_number] = {
            'left_elbow_angle': row['left_elbow_angle'],
            'right_elbow_angle': row['right_elbow_angle'],
            'left_knee_angle': row['left_knee_angle'],
            'right_knee_angle': row['right_knee_angle']
        }

# Inicializar Mediapipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Función para calcular los ángulos
def calculate_angle(a, b, c):
    a = np.array(a)  # Punto A
    b = np.array(b)  # Punto B (vértice)
    c = np.array(c)  # Punto C
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return int(angle)

# Ruta del video o fuente de la cámara
video_path = "PF/loveMe.mp4"  # Cambia por tu archivo de video o pon 0 para usar la cámara web

# Abrir el video
cap = cv2.VideoCapture(video_path)

# Lista para guardar los resultados de la comparación
comparison_results = []

# Variables para calcular la precisión
total_frames = 0
matching_frames = 0
matching_angles_count = 0
total_angles_count = 0

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        # Obtener el número de frame
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # Convertir a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        # Inicializar datos del frame
        current_angles = {
            "frame": frame_number,
            "left_elbow_angle": "&&",
            "right_elbow_angle": "&&",
            "left_knee_angle": "&&",
            "right_knee_angle": "&&",
            "match_left_elbow_angle": "",
            "match_right_elbow_angle": "",
            "match_left_knee_angle": "",
            "match_right_knee_angle": ""
        }

        if results.pose_landmarks:
            # Obtener landmarks
            landmarks = results.pose_landmarks.landmark

            def get_coords(landmark):
                # Devuelve coordenadas si el punto es visible
                return [landmark.x, landmark.y] if landmark.visibility > 0.5 else None

            # Coordenadas de interés
            keypoints = {
                "left_shoulder": get_coords(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]),
                "left_elbow": get_coords(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]),
                "left_wrist": get_coords(landmarks[mp_pose.PoseLandmark.LEFT_WRIST]),
                "right_shoulder": get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]),
                "right_elbow": get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]),
                "right_wrist": get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]),
                "left_hip": get_coords(landmarks[mp_pose.PoseLandmark.LEFT_HIP]),
                "left_knee": get_coords(landmarks[mp_pose.PoseLandmark.LEFT_KNEE]),
                "left_ankle": get_coords(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]),
                "right_hip": get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_HIP]),
                "right_knee": get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]),
                "right_ankle": get_coords(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]),
            }

            def safe_calculate_angle(a, b, c):
                # Devuelve el ángulo o None si algún punto está ausente
                return calculate_angle(a, b, c) if a and b and c else None

            # Calcular ángulos y actualizar el frame
            left_elbow_angle = safe_calculate_angle(keypoints["left_shoulder"], keypoints["left_elbow"], keypoints["left_wrist"])
            right_elbow_angle = safe_calculate_angle(keypoints["right_shoulder"], keypoints["right_elbow"], keypoints["right_wrist"])
            left_knee_angle = safe_calculate_angle(keypoints["left_hip"], keypoints["left_knee"], keypoints["left_ankle"])
            right_knee_angle = safe_calculate_angle(keypoints["right_hip"], keypoints["right_knee"], keypoints["right_ankle"])

            if left_elbow_angle is not None:
                current_angles["left_elbow_angle"] = left_elbow_angle
            if right_elbow_angle is not None:
                current_angles["right_elbow_angle"] = right_elbow_angle
            if left_knee_angle is not None:
                current_angles["left_knee_angle"] = left_knee_angle
            if right_knee_angle is not None:
                current_angles["right_knee_angle"] = right_knee_angle

        # Obtener los ángulos de referencia para este frame
        ref_angles = angles_reference.get(frame_number)
        if ref_angles is None:
            # No hay datos de referencia para este frame
            continue

        # Comparar ángulos
        angles_matched = True
        for angle_key in ["left_elbow_angle", "right_elbow_angle", "left_knee_angle", "right_knee_angle"]:
            ref_angle = ref_angles[angle_key]
            curr_angle = current_angles[angle_key]
            total_angles_count += 1

            match_key = f"match_{angle_key}"

            if ref_angle == "&&" or curr_angle == "&&":
                # No se puede comparar, saltar
                current_angles[match_key] = "N/A"
                continue
            else:
                ref_angle = int(ref_angle)
                curr_angle = int(curr_angle)
                # Definir un umbral para considerar que los ángulos coinciden (por ejemplo, 5 grados)
                angle_diff = abs(ref_angle - curr_angle)
                if angle_diff <= 5:
                    matching_angles_count += 1
                    current_angles[match_key] = "Yes"
                else:
                    angles_matched = False
                    current_angles[match_key] = "No"
                    # Imprimir en la terminal los ángulos que son distintos
                    print(f"Frame {frame_number}, {angle_key}:")
                    print(f"  Ángulo de referencia: {ref_angle}°")
                    print(f"  Ángulo actual      : {curr_angle}°")
                    print(f"  Diferencia         : {angle_diff}°")

        if angles_matched:
            matching_frames += 1

        comparison_results.append(current_angles)

        # Visualizar los landmarks en el video (opcional)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3),
            )

        # Mostrar video (opcional)
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla ESC
            break

cap.release()
cv2.destroyAllWindows()

# Calcular precisión
if total_angles_count > 0:
    angle_accuracy = (matching_angles_count / total_angles_count) * 100
else:
    angle_accuracy = 0

if total_frames > 0:
    frame_accuracy = (matching_frames / total_frames) * 100
else:
    frame_accuracy = 0

print(f"Precisión de ángulos: {angle_accuracy:.2f}%")
print(f"Precisión de frames: {frame_accuracy:.2f}%")

# Escribir los resultados de la comparación en un archivo CSV
with open('comparison_results.csv', mode='w', newline='') as file:
    fieldnames = [
        "frame",
        "left_elbow_angle", "right_elbow_angle", "left_knee_angle", "right_knee_angle",
        "match_left_elbow_angle", "match_right_elbow_angle", "match_left_knee_angle", "match_right_knee_angle"
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(comparison_results)

print("Resultados de la comparación guardados en comparison_results.csv")
