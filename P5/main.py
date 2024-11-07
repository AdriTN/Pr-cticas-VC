import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk

def obtener_resolucion_pantalla():
    root = tk.Tk()
    root.withdraw()
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    return ancho, alto

class Rectangle:
    def __init__(self, x1, y1, x2, y2, pasado):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.pasado = False

    def draw(self, frame):
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)

    def check_collision(self, other_x1, other_y1, other_x2, other_y2):
        return not (self.x2 < other_x1 or self.x1 > other_x2 or self.y2 < other_y1 or self.y1 > other_y2)

    def update_position(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def load_nose_overlay(image_path):
    nose_overlay = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if nose_overlay is None:
        raise ValueError("Error: No se pudo cargar la imagen de la nariz.")
    if nose_overlay.shape[2] != 4:
        raise ValueError("Error: La imagen no tiene un canal alfa.")
    return nose_overlay

def get_bird_region_and_mask(nose_overlay):
    alpha_channel = nose_overlay[:, :, 3] / 255.0
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
        return None
    mask = alpha_region[:, :, np.newaxis]
    roi = frame[y1:y2, x1:x2]
    combined = (roi * (1 - mask) + bird_region * mask).astype(np.uint8)
    frame[y1:y2, x1:x2] = combined
    return (x1, y1, x2, y2)

def main():
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh
    nose_overlay = load_nose_overlay('bird.png')
    bird_region, alpha_region = get_bird_region_and_mask(nose_overlay)
    ancho, alto = obtener_resolucion_pantalla()
    cap = cv2.VideoCapture(0)
    overlay_height, overlay_width = bird_region.shape[:2]
    espacio = 179
    dificultad = 100
    pasado = True
    pipes = [Rectangle(600, 0, 650, int(alto / 7), False), Rectangle(600, espacio + dificultad, 650, alto, False)]
    puntaje = 0

    with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection, \
         mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Error: No se pudo leer el marco del video.")
                break

            for pipe in pipes:
                pipe.draw(frame)
                pipe.x1 -= 1
                pipe.x2 -= 1

                # Reiniciar posición si x2 llega a 0
                if pipe.x2 <= 0:
                    pipe.pasado = False
                    pipe.x1 = 600
                    pipe.x2 = 650

            results = detect_faces(frame, face_detection)

            if results.detections:
                for detection in results.detections:
                    mesh_results = detect_face_landmarks(frame, face_mesh)
                    if mesh_results.multi_face_landmarks:
                        for face_landmarks in mesh_results.multi_face_landmarks:
                            nose_tip = face_landmarks.landmark[1]
                            ih, iw, _ = frame.shape
                            nose_x = int(nose_tip.x * iw)
                            nose_y = int(nose_tip.y * ih)
                            overlay_coords = place_nose_overlay(frame, nose_x, nose_y, bird_region, alpha_region)
                            if overlay_coords is not None:
                                x1, y1, x2, y2 = overlay_coords
                                
                                if nose_x > pipes[0].x2 and not pipes[0].pasado:
                                    puntaje += 1
                                    pipes[0].pasado = True
                                    print(f"Punto conseguido! Puntuaje: {puntaje}")
                                
                                collided = any(pipe.check_collision(x1, y1, x2, y2) for pipe in pipes)
                                if collided:
                                    print("¡Colisión detectada! Terminando ejecución.")
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return

            cv2.putText(frame, f"Puntuaje: {puntaje}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
