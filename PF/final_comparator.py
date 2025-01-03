import cv2
import mediapipe as mp
import numpy as np
import csv
import os
import tkinter as tk
from tkinter import ttk
import time
import json

# Inicializar MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Variables globales
MARGIN_OF_ERROR = 10
MODE_HELP = False
TIME_LIMIT = 10
PLAYER_NAME = "test"
START_TIME = 0

# Función para calcular el ángulo entre tres puntos
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# Cargar los ángulos de referencia desde un CSV
def load_reference_angles(csv_file):
    reference_angles = []
    images = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            images.append(row[0])
            angles = list(map(float, row[1:]))
            reference_angles.append(angles)
    return images, reference_angles

# Calcular diferencias y verificar si están dentro del margen
def calculate_differences(reference_angles, current_angles):
    differences = []
    results = []
    for ref, curr in zip(reference_angles, current_angles):
        diff = abs(ref - curr)
        differences.append(diff)
        results.append(diff <= MARGIN_OF_ERROR)
    return differences, results

# Guardar registro en JSON
def save_record(player_name, score):
    end_time = time.time()
    duration = int(end_time - START_TIME)
    record = {
        "name": player_name,
        "score": score,
        "time_played": duration,
        "mode": "Con ayuda" if MODE_HELP else "Sin ayuda"
    }
    if os.path.exists("records.json"):
        with open("records.json", "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(record)

    with open("records.json", "w") as file:
        json.dump(data, file, indent=4)

# Procesar el video y comparar ángulos
def process_video(video_path, reference_images, reference_angles, output_folder):
    global MODE_HELP, TIME_LIMIT, PLAYER_NAME
    pose = mp_pose.Pose()
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    capture_count = 0
    current_ref = 0
    score = 0

    ref_image = cv2.imread(reference_images[current_ref])
    ref_image = cv2.resize(ref_image, (200, 200))

    differences_csv = os.path.join(output_folder, "diferencias.csv")
    with open(differences_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "Left Elbow", "Right Elbow", "Left Knee", "Right Knee"])

        start_time = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_number += 1
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            frame[10:210, -210:-10] = ref_image

            remaining_time = TIME_LIMIT - (time.time() - start_time)
            cv2.putText(frame, f"Tiempo: {int(remaining_time)}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if results.pose_landmarks:
                keypoints = [
                    (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                    for landmark in results.pose_landmarks.landmark
                ]

                current_angles = [
                    calculate_angle(
                        keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                        keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                        keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value],
                    ),
                    calculate_angle(
                        keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                        keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                    ),
                    calculate_angle(
                        keypoints[mp_pose.PoseLandmark.LEFT_HIP.value],
                        keypoints[mp_pose.PoseLandmark.LEFT_KNEE.value],
                        keypoints[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                    ),
                    calculate_angle(
                        keypoints[mp_pose.PoseLandmark.RIGHT_HIP.value],
                        keypoints[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                        keypoints[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                    ),
                ]

                differences, match_results = calculate_differences(reference_angles[current_ref], current_angles)
                writer.writerow([frame_number] + differences)

                if MODE_HELP:
                    for i, result in enumerate(match_results):
                        color = (0, 255, 0) if result else (0, 0, 255)
                        keypoints_indices = [
                            (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_WRIST),
                            (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_WRIST),
                            (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_ANKLE),
                            (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_ANKLE),
                        ]

                        for index in keypoints_indices[i]:
                            landmark = results.pose_landmarks.landmark[index.value]
                            cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 10, color, -1)

                if all(match_results):
                    capture_count += 1
                    score += 1
                    capture_path = os.path.join(output_folder, f"capture_frame_{frame_number}.jpg")
                    cv2.imwrite(capture_path, frame)
                    current_ref += 1
                    start_time = time.time()
                    if current_ref >= len(reference_angles):
                        break
                    ref_image = cv2.imread(reference_images[current_ref])
                    ref_image = cv2.resize(ref_image, (200, 200))

            cv2.putText(frame, f"Score: {score}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Video Pose Matching', frame)

            if time.time() - start_time > TIME_LIMIT:
                current_ref += 1
                start_time = time.time()
                if current_ref >= len(reference_angles):
                    break
                ref_image = cv2.imread(reference_images[current_ref])
                ref_image = cv2.resize(ref_image, (200, 200))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    pose.close()
    cv2.destroyAllWindows()
    save_record(PLAYER_NAME, score)

# Interfaz gráfica para seleccionar dificultad y modo
def start_program():
    global MARGIN_OF_ERROR, MODE_HELP, TIME_LIMIT, PLAYER_NAME, START_TIME

    PLAYER_NAME = name_var.get() if name_var.get() else "test"
    difficulty = difficulty_var.get()
    mode = mode_var.get()

    if difficulty == "Fácil":
        MARGIN_OF_ERROR = 20
        TIME_LIMIT = 10
    elif difficulty == "Medio":
        MARGIN_OF_ERROR = 15
        TIME_LIMIT = 7
    elif difficulty == "Difícil":
        MARGIN_OF_ERROR = 5
        TIME_LIMIT = 5

    MODE_HELP = True if mode == "Con ayuda" else False
    START_TIME = time.time()

    root.destroy()
    reference_csv = "angles.csv"
    video_path = "mix2.mp4"
    output_folder = "capturas"
    reference_images, reference_angles = load_reference_angles(reference_csv)
    process_video(video_path, reference_images, reference_angles, output_folder)

root = tk.Tk()
root.title("Configuración del Juego")

tk.Label(root, text="Introduce tu nombre:").pack()
name_var = tk.StringVar()
name_entry = tk.Entry(root, textvariable=name_var)
name_entry.pack()

tk.Label(root, text="Selecciona la dificultad:").pack()
difficulty_var = tk.StringVar(value="Fácil")
difficulty_menu = ttk.Combobox(root, textvariable=difficulty_var, values=["Fácil", "Medio", "Difícil"])
difficulty_menu.pack()

tk.Label(root, text="Selecciona el modo de juego:").pack()
mode_var = tk.StringVar(value="Con ayuda")
mode_menu = ttk.Combobox(root, textvariable=mode_var, values=["Con ayuda", "Sin ayuda"])
mode_menu.pack()

tk.Button(root, text="Iniciar", command=start_program).pack()

root.mainloop()
