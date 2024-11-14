import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
import random

def obtener_resolucion_pantalla():
    root = tk.Tk()
    root.withdraw()
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight() - 300
    return ancho, alto

class Pipe:
    def __init__(self, x1, y1, x2, y2, img, flip_image=False):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.img = img
        self.flip_image = flip_image
        self.mask = None
        self.mask_coords = None

    def draw(self, frame):
        frame_height, frame_width = frame.shape[:2]
        x1 = max(0, int(self.x1))
        y1 = max(0, int(self.y1))
        x2 = min(frame_width, int(self.x2))
        y2 = min(frame_height, int(self.y2))

        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            return

        pipe_img = self.img.copy()
        if self.flip_image:
            pipe_img = cv2.flip(pipe_img, 0)

        pipe_resized = cv2.resize(pipe_img, (width, height), interpolation=cv2.INTER_AREA)

        self.mask_coords = (x1, y1, x2, y2)

        if pipe_resized.shape[2] == 4:
            pipe_rgb = pipe_resized[:, :, :3]
            pipe_alpha = pipe_resized[:, :, 3] / 255.0
            roi = frame[y1:y2, x1:x2]

            h, w = roi.shape[:2]
            if h != pipe_rgb.shape[0] or w != pipe_rgb.shape[1]:
                pipe_rgb = cv2.resize(pipe_rgb, (w, h), interpolation=cv2.INTER_AREA)
                pipe_alpha = cv2.resize(pipe_alpha, (w, h), interpolation=cv2.INTER_AREA)

            for c in range(3):
                roi[:, :, c] = (pipe_alpha * pipe_rgb[:, :, c] +
                                (1 - pipe_alpha) * roi[:, :, c])

            frame[y1:y2, x1:x2] = roi

            self.mask = (pipe_alpha * 255).astype(np.uint8)
        else:
            roi = frame[y1:y2, x1:x2]
            frame[y1:y2, x1:x2] = pipe_resized
            self.mask = np.ones((roi.shape[0], roi.shape[1]), dtype=np.uint8) * 255

    def update_position(self, x_delta):
        self.x1 -= x_delta
        self.x2 -= x_delta
        if self.mask_coords is not None:
            x1, y1, x2, y2 = self.mask_coords
            self.mask_coords = (x1 - x_delta, y1, x2 - x_delta, y2)

    def check_collision(self, bird_mask, bird_coords):
        if self.mask is None or self.mask_coords is None:
            return False

        x1 = max(self.mask_coords[0], bird_coords[0])
        y1 = max(self.mask_coords[1], bird_coords[1])
        x2 = min(self.mask_coords[2], bird_coords[2])
        y2 = min(self.mask_coords[3], bird_coords[3])

        if x1 >= x2 or y1 >= y2:
            return False

        pipe_mask_region = self.mask[y1 - self.mask_coords[1]:y2 - self.mask_coords[1],
                                     x1 - self.mask_coords[0]:x2 - self.mask_coords[0]]

        bird_mask_region = bird_mask[y1 - bird_coords[1]:y2 - bird_coords[1],
                                     x1 - bird_coords[0]:x2 - bird_coords[0]]

        overlap = cv2.bitwise_and(pipe_mask_region, bird_mask_region)
        return np.any(overlap)

class Obstacle:
    def __init__(self, x, pipe_width, top_height, gap_height, bottom_height, alto, pipe_img):
        self.x = x
        self.pipe_width = pipe_width
        self.pasado = False
        self.top_pipe = Pipe(self.x, 0, self.x + self.pipe_width, top_height, pipe_img, flip_image=True)
        self.bottom_pipe = Pipe(self.x, alto - bottom_height, self.x + self.pipe_width, alto, pipe_img)

    def update_position(self, x_delta):
        self.x -= x_delta
        self.top_pipe.update_position(x_delta)
        self.bottom_pipe.update_position(x_delta)

    def draw(self, frame):
        self.top_pipe.draw(frame)
        self.bottom_pipe.draw(frame)

    def check_collision(self, bird_mask, bird_coords):
        return (self.top_pipe.check_collision(bird_mask, bird_coords) or
                self.bottom_pipe.check_collision(bird_mask, bird_coords))

    def is_off_screen(self):
        return self.top_pipe.x2 <= 0

def load_image_with_alpha(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Error: No se pudo cargar la imagen en {image_path}.")
    if img.shape[2] != 4:
        alpha_channel = np.ones((img.shape[0], img.shape[1], 1), dtype=img.dtype) * 255
        img = np.concatenate((img, alpha_channel), axis=2)
    return img

def get_bird_region_and_mask(nose_overlay):
    alpha_channel = nose_overlay[:, :, 3]
    overlay_img = nose_overlay[:, :, :3]
    coords = np.column_stack(np.where(alpha_channel > 0))
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    bird_region = overlay_img[y_min:y_max + 1, x_min:x_max + 1]
    alpha_region = alpha_channel[y_min:y_max + 1, x_min:x_max + 1]
    return bird_region, alpha_region

def detect_faces(frame, face_detection):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_detection.process(frame_rgb)

def detect_face_landmarks(frame, face_mesh):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_mesh.process(frame_rgb)

def place_nose_overlay(frame, nose_x, nose_y, bird_region, alpha_region):
    overlay_height, overlay_width = bird_region.shape[:2]
    y1 = int(nose_y - overlay_height / 2)
    y2 = y1 + overlay_height
    x1 = int(nose_x - overlay_width / 2)
    x2 = x1 + overlay_width

    if y1 < 0 or x1 < 0 or y2 > frame.shape[0] or x2 > frame.shape[1]:
        return None, None

    roi = frame[y1:y2, x1:x2]
    alpha_mask = alpha_region / 255.0

    for c in range(3):
        roi[:, :, c] = (alpha_mask * bird_region[:, :, c] +
                        (1 - alpha_mask) * roi[:, :, c])

    bird_mask = (alpha_mask * 255).astype(np.uint8)
    bird_coords = (x1, y1, x2, y2)
    return bird_mask, bird_coords

def create_random_obstacle(alto, pipe_img, pipe_width, initial_x):
    # Definir tamaños mínimos y máximos basados en la altura de la ventana
    min_pipe_height = int(alto * 0.1)  # 10% de la altura
    max_pipe_height = int(alto * 0.30)  # 30% de la altura
    min_gap_height = int(alto * 0.2)   # 20% de la altura
    max_gap_height = int(alto * 0.35)  # 35% de la altura

    # Asegurar que la suma de las alturas mínimas no exceda la altura total
    total_max_heights = 2 * max_pipe_height + max_gap_height
    if total_max_heights > alto:
        raise ValueError("La altura de la ventana es demasiado pequeña para las dimensiones máximas definidas.")

    # Calcular el espacio disponible para el hueco
    total_available_height = alto - 2 * min_pipe_height
    max_gap_height = min(max_gap_height, total_available_height)

    # Seleccionar aleatoriamente el tamaño del hueco dentro de los límites
    gap_height = random.randint(min_gap_height, max_gap_height)

    # Calcular la altura disponible para las tuberías
    available_pipe_height = alto - gap_height

    # Asegurar que la altura máxima de la tubería superior no sea menor que la mínima
    max_top_height = available_pipe_height - min_pipe_height
    if max_top_height < min_pipe_height:
        max_top_height = min_pipe_height

    # Seleccionar aleatoriamente la altura de la tubería superior
    top_height = random.randint(min_pipe_height, max_top_height)

    # Calcular la altura de la tubería inferior
    bottom_height = available_pipe_height - top_height

    x = initial_x
    return Obstacle(x, pipe_width, top_height, gap_height, bottom_height, alto, pipe_img)

def main():
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh
    nose_overlay = load_image_with_alpha('P5/bird.png')
    pipe_img = load_image_with_alpha('P5/pipe.png')
    ancho, alto = obtener_resolucion_pantalla()
    cap = cv2.VideoCapture(0)
    velocidad = 8
    max_score = 20
    pipe_width = 100
    puntaje = 0
    min_distance_between_obstacles = 300

    bird_region, alpha_region = get_bird_region_and_mask(nose_overlay)
    obstacles = [create_random_obstacle(alto, pipe_img, pipe_width, initial_x=600)]

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection, \
         mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5) as face_mesh:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Error: No se pudo leer el marco del video.")
                break

            frame = cv2.flip(frame, 1)

            # Actualizar y dibujar obstáculos
            for obstacle in obstacles:
                obstacle.update_position(velocidad)
                obstacle.draw(frame)

            # Eliminar obstáculos que salen de la pantalla
            if obstacles and obstacles[0].is_off_screen():
                obstacles.pop(0)

            # Generar nuevos obstáculos
            if len(obstacles) == 0 or (obstacles[-1].x < ancho - min_distance_between_obstacles):
                new_x = obstacles[-1].x + min_distance_between_obstacles if obstacles else 600
                obstacles.append(create_random_obstacle(alto, pipe_img, pipe_width, initial_x=new_x))

            results = detect_faces(frame, face_detection)

            if results.detections:
                mesh_results = detect_face_landmarks(frame, face_mesh)
                if mesh_results.multi_face_landmarks:
                    for face_landmarks in mesh_results.multi_face_landmarks:
                        nose_tip = face_landmarks.landmark[1]
                        ih, iw, _ = frame.shape
                        nose_x = int(nose_tip.x * iw)
                        nose_y = int(nose_tip.y * ih)
                        bird_mask, bird_coords = place_nose_overlay(frame, nose_x, nose_y, bird_region, alpha_region)
                        if bird_mask is not None:
                            for obstacle in obstacles:
                                if not obstacle.pasado and nose_x > obstacle.top_pipe.x2:
                                    puntaje += 1
                                    obstacle.pasado = True
                                    print(f"Punto conseguido! Puntaje: {puntaje}")

                                    if puntaje % 5 == 0:
                                        velocidad += 1
                                        print(f"¡Aumenta la dificultad! Velocidad: {velocidad}")

                                if obstacle.check_collision(bird_mask, bird_coords):
                                    print("¡Colisión detectada! Terminando ejecución.")
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return

                            if puntaje >= max_score:
                                print("¡Felicidades! Has alcanzado el puntaje máximo.")
                                cap.release()
                                cv2.destroyAllWindows()
                                return

            cv2.putText(frame, f"Puntaje: {puntaje}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
