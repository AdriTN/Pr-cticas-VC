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
def save_record(player_name, score, difficulty):
    end_time = time.time()
    duration = int(end_time - START_TIME)
    record = {
        "name": player_name,
        "score": score,
        "time_played": duration,
        "mode": "Con ayuda" if MODE_HELP else "Sin ayuda",
        "difficulty": difficulty
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
def process_video(reference_images, reference_angles, output_folder):
    global MODE_HELP, TIME_LIMIT, PLAYER_NAME
    pose = mp_pose.Pose()
    os.makedirs(output_folder, exist_ok=True)

    # Capturar desde la cámara
    cap = cv2.VideoCapture(0)  # Usa la cámara predeterminada
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

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
    save_record(PLAYER_NAME, score, difficulty_var.get())


def load_and_sort_records(file_path):
    """Load records from JSON and sort them by score."""
    try:
        with open(file_path, "r") as file:
            records = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return []

    # Separate and sort by mode
    con_ayuda = sorted(
        [record for record in records if record["mode"] == "Con ayuda"],
        key=lambda x: -x["score"],
    )
    sin_ayuda = sorted(
        [record for record in records if record["mode"] == "Sin ayuda"],
        key=lambda x: -x["score"],
    )

    return con_ayuda, sin_ayuda


def display_rankings(con_ayuda, sin_ayuda):
    """Display the rankings in a graphical interface."""
    root = tk.Tk()
    root.title("Ranking de Jugadores")
    root.geometry("600x400")

    # Create main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Titles for columns
    ttk.Label(main_frame, text="Modo: Con ayuda", font=("Arial", 14)).grid(
        row=0, column=0, padx=10, pady=5
    )
    ttk.Label(main_frame, text="Modo: Sin ayuda", font=("Arial", 14)).grid(
        row=0, column=1, padx=10, pady=5
    )

    # Populate rankings
    for i, record in enumerate(con_ayuda[:10], start=1):  # Top 10 players
        ttk.Label(main_frame, text=f"{i}. {record['name']} - {record['score']} pts").grid(
            row=i, column=0, padx=10, pady=2, sticky="w"
        )

    for i, record in enumerate(sin_ayuda[:10], start=1):  # Top 10 players
        ttk.Label(main_frame, text=f"{i}. {record['name']} - {record['score']} pts").grid(
            row=i, column=1, padx=10, pady=2, sticky="w"
        )

    # Run the GUI loop
    root.mainloop()

# Interfaz gráfica para seleccionar dificultad y modo
def start_program():
    global MARGIN_OF_ERROR, MODE_HELP, TIME_LIMIT, PLAYER_NAME, START_TIME

    PLAYER_NAME = name_var.get() if name_var.get() else "test"
    difficulty = difficulty_var.get()
    mode = mode_var.get()

    if difficulty == "Facil":
        MARGIN_OF_ERROR = 15
        TIME_LIMIT = 20
    elif difficulty == "Medio":
        MARGIN_OF_ERROR = 15
        TIME_LIMIT = 7
    elif difficulty == "Dificil":
        MARGIN_OF_ERROR = 5
        TIME_LIMIT = 5

    MODE_HELP = True if mode == "Con ayuda" else False
    START_TIME = time.time()

    root.destroy()
    reference_csv = "angles.csv"
    output_folder = "capturas"
    reference_images, reference_angles = load_reference_angles(reference_csv)
    process_video(reference_images, reference_angles, output_folder)  # Corregido aquí
    file_path = "records.json"
    con_ayuda, sin_ayuda = load_and_sort_records(file_path)

    # Display in GUI
    display_rankings(con_ayuda, sin_ayuda)


root = tk.Tk()
root.title("Configuración del Juego")

tk.Label(root, text="Introduce tu nombre:").pack()
name_var = tk.StringVar()
name_entry = tk.Entry(root, textvariable=name_var)
name_entry.pack()

tk.Label(root, text="Selecciona la dificultad:").pack()
difficulty_var = tk.StringVar(value="Facil")
difficulty_menu = ttk.Combobox(root, textvariable=difficulty_var, values=["Facil", "Medio", "Dificil"])
difficulty_menu.pack()

tk.Label(root, text="Selecciona el modo de juego:").pack()
mode_var = tk.StringVar(value="Con ayuda")
mode_menu = ttk.Combobox(root, textvariable=mode_var, values=["Con ayuda", "Sin ayuda"])
mode_menu.pack()

tk.Button(root, text="Iniciar", command=start_program).pack()

root.mainloop()
