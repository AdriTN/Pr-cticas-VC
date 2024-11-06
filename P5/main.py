import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk

def obtener_resolucion_pantalla():
    """Obtenemos la resolución de la pantalla."""
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    return ancho, alto

class Rectangle:
    """Clase para representar un rectángulo."""
    def __init__(self, x1, y1, x2, y2,pasado):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.pasado = False

    def draw(self, frame):
        """Dibuja el rectángulo en el marco dado."""
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)

    def check_collision(self, other_x1, other_y1, other_x2, other_y2):
        """Verifica si hay colisión con otro rectángulo."""
        return not (self.x2 < other_x1 or self.x1 > other_x2 or self.y2 < other_y1 or self.y1 > other_y2)

    def update_position(self, x1, y1, x2, y2):
        """Actualiza las coordenadas del rectángulo."""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def load_nose_overlay(image_path):
    """Carga la imagen de la nariz con canal alfa y verifica su validez."""
    nose_overlay = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if nose_overlay is None:
        raise ValueError("Error: No se pudo cargar la imagen de la nariz.")
    if nose_overlay.shape[2] != 4:
        raise ValueError("Error: La imagen no tiene un canal alfa. Asegúrate de usar una imagen PNG con transparencia.")
    return nose_overlay

def get_bird_region_and_mask(nose_overlay):
    """Extrae la región del pájaro y su máscara a partir de la imagen de la nariz."""
    alpha_channel = nose_overlay[:, :, 3] / 255.0  # Normaliza el canal alfa
    overlay_img = nose_overlay[:, :, :3]  # Imagen RGB sin transparencia

    coords = np.column_stack(np.where(alpha_channel > 0))
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    bird_region = overlay_img[y_min:y_max + 1, x_min:x_max + 1]
    alpha_region = alpha_channel[y_min:y_max + 1, x_min:x_max + 1]

    return bird_region, alpha_region

def detect_faces(frame, face_detection):
    """Detecta rostros en el marco usando MediaPipe Face Detection."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_detection.process(frame_rgb)

def detect_face_landmarks(frame, face_mesh):
    """Detecta las marcas faciales en el marco usando MediaPipe Face Mesh."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_mesh.process(frame_rgb)

def place_nose_overlay(frame, nose_x, nose_y, bird_region, alpha_region):
    """Coloca la superposición de la nariz en el marco en las coordenadas dadas."""
    overlay_height, overlay_width = bird_region.shape[:2]
    y1 = int(nose_y - overlay_height / 2)
    y2 = y1 + overlay_height
    x1 = int(nose_x - overlay_width / 2)
    x2 = x1 + overlay_width

    if y1 < 0 or x1 < 0 or y2 > frame.shape[0] or x2 > frame.shape[1]:
        return None  # Si la imagen no cabe, devolver None

    mask = alpha_region[:, :, np.newaxis]
    roi = frame[y1:y2, x1:x2]
    combined = (roi * (1 - mask) + bird_region * mask).astype(np.uint8)

    frame[y1:y2, x1:x2] = combined
    return (x1, y1, x2, y2)  # Retornar las coordenadas de la superposición

def main():
    # Inicializar MediaPipe Face Detection y Face Mesh
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh

    # Cargar la imagen de la nariz
    nose_overlay = load_nose_overlay('bird.png')
    bird_region, alpha_region = get_bird_region_and_mask(nose_overlay)

    ancho, alto = obtener_resolucion_pantalla()

    # Inicializar la captura de video
    cap = cv2.VideoCapture(0)
    
    # Variables del juego
    overlay_height, overlay_width = bird_region.shape[:2]
    espacio = 179
    dificultad = 100
    pasado = True

    # Lista de rectángulos
    pipes = []
    pipes.append(Rectangle(0, 0, 100, int(alto / 7),False))  # Primer rectángulo en la parte superior
    pipes.append(Rectangle(0, espacio + dificultad, 100, alto,False))  # Segundo rectángulo en la parte inferior

    puntaje = 0  # Inicializa el puntaje

    with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection, \
         mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Error: No se pudo leer el marco del video.")
                break

            # Dibujar todos los rectángulos en el marco
            for pipe in pipes:
                pipe.draw(frame)
                pipe.x1 += 1
                pipe.x2 += 1

            # Detectar rostros
            results = detect_faces(frame, face_detection)

            if results.detections:
                for detection in results.detections:
                    mesh_results = detect_face_landmarks(frame, face_mesh)
                    if mesh_results.multi_face_landmarks:
                        for face_landmarks in mesh_results.multi_face_landmarks:
                            nose_tip = face_landmarks.landmark[1]  # Landmark 1 es la punta de la nariz
                            ih, iw, _ = frame.shape
                            nose_x = int(nose_tip.x * iw)
                            nose_y = int(nose_tip.y * ih)

                            # Colocar la superposición de la nariz
                            overlay_coords = place_nose_overlay(frame, nose_x, nose_y, bird_region, alpha_region)
                            if overlay_coords is not None:
                                x1, y1, x2, y2 = overlay_coords
                                
                                # Verificar si la nariz está entre los rectángulos
                                if (nose_x < pipes[0].x2):
                                    if(pipes[0].pasado == False):
                                        puntaje += 1
                                        pipes[0].pasado = True
                                        print(f"Punto conseguido! Puntaje: {puntaje}")
                                
                                # Comprobar colisión con todos los rectángulos
                                collided = False
                                for pipe in pipes:
                                    if pipe.check_collision(x1, y1, x2, y2):
                                        collided = True
                                        break

                                # Si hay colisión, termina el juego
                                if collided:
                                    print("¡Colisión detectada! Terminando ejecución.")
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return

            # Mostrar el puntaje en la esquina superior izquierda
            cv2.putText(frame, f"Puntaje: {puntaje}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Mostrar el marco
            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(5) & 0xFF == 27:  # Presiona ESC para salir
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
