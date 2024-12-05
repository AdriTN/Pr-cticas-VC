import cv2
import mediapipe as mp
import numpy as np
import csv

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

# Ruta del video
video_path = "PF/loveMe.mp4"  # Cambia por tu archivo de video
output_csv = "angles.csv"  # Archivo donde se guardarán los datos

# Abrir el video
cap = cv2.VideoCapture(video_path)

# Lista para guardar los ángulos
angles_data = []

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        # Inicializar datos del frame
        frame_angles = {
            "frame": int(cap.get(cv2.CAP_PROP_POS_FRAMES)),
            "left_elbow_angle": "&&",
            "right_elbow_angle": "&&",
            "left_knee_angle": "&&",
            "right_knee_angle": "&&"
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

            if left_elbow_angle is not None: frame_angles["left_elbow_angle"] = left_elbow_angle
            if right_elbow_angle is not None: frame_angles["right_elbow_angle"] = right_elbow_angle
            if left_knee_angle is not None: frame_angles["left_knee_angle"] = left_knee_angle
            if right_knee_angle is not None: frame_angles["right_knee_angle"] = right_knee_angle

        angles_data.append(frame_angles)

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

# Escribir los datos en un archivo CSV
with open(output_csv, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["frame", "left_elbow_angle", "right_elbow_angle", "left_knee_angle", "right_knee_angle"])
    writer.writeheader()
    writer.writerows(angles_data)

print(f"Ángulos capturados y guardados en {output_csv}")
