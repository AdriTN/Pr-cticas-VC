import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Detection y Face Mesh
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

# Cargar la imagen de la nariz con canal alfa
nose_overlay = cv2.imread('bird.png', cv2.IMREAD_UNCHANGED)
if nose_overlay is None:
    print("Error: No se pudo cargar la imagen de la nariz.")
    exit()

# Verificar que la imagen tiene un canal alfa
if nose_overlay.shape[2] != 4:
    print("Error: La imagen no tiene un canal alfa. Asegúrate de usar una imagen PNG con transparencia.")
    exit()

# Extraer el canal alfa y calcular la bounding box del pájaro
alpha_channel = nose_overlay[:, :, 3] / 255.0  # Normaliza el canal alfa
overlay_img = nose_overlay[:, :, :3]  # Imagen RGB sin transparencia

# Encontrar la bounding box de la región no transparente
coords = np.column_stack(np.where(alpha_channel > 0))
y_min, x_min = coords.min(axis=0)
y_max, x_max = coords.max(axis=0)

# Extraer la región de interés del pájaro y su máscara
bird_region = overlay_img[y_min:y_max + 1, x_min:x_max + 1]
alpha_region = alpha_channel[y_min:y_max + 1, x_min:x_max + 1]

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Definir las coordenadas y tamaño del cuadrado fijo
square_x, square_y = 100, 100  # Posición del cuadrado
square_size = 50  # Tamaño del cuadrado

with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection, \
     mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Error: No se pudo leer el marco del video.")
            break

        # Convertir el marco a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)

        # Dibujar el cuadrado fijo en el marco
        cv2.rectangle(frame, (square_x, square_y), (square_x + square_size, square_y + square_size), (0, 0, 255), 2)

        if results.detections:
            for detection in results.detections:
                # Procesar la malla facial
                mesh_results = face_mesh.process(frame_rgb)
                if mesh_results.multi_face_landmarks:
                    for face_landmarks in mesh_results.multi_face_landmarks:
                        # Obtener las coordenadas de la punta de la nariz
                        nose_tip = face_landmarks.landmark[1]  # Landmark 1 es la punta de la nariz
                        ih, iw, _ = frame.shape
                        nose_x = int(nose_tip.x * iw)
                        nose_y = int(nose_tip.y * ih)

                        # Dimensiones de la región del pájaro
                        overlay_height, overlay_width = bird_region.shape[:2]

                        # Definir la región donde se superpondrá la imagen
                        y1 = int(nose_y - overlay_height / 2)
                        y2 = y1 + overlay_height
                        x1 = int(nose_x - overlay_width / 2)
                        x2 = x1 + overlay_width

                        # Verificar que la imagen quepa en el marco
                        if y1 < 0 or x1 < 0 or y2 > frame.shape[0] or x2 > frame.shape[1]:
                            continue  # Saltar si la imagen no cabe

                        # Crear la máscara y fondo
                        mask = alpha_region[:, :, np.newaxis]  # Usar el canal alfa de la región ajustada
                        roi = frame[y1:y2, x1:x2]

                        # Combinar la imagen de fondo con la superposición
                        combined = (roi * (1 - mask) + bird_region * mask).astype(np.uint8)

                        # Colocar la imagen combinada en el marco
                        frame[y1:y2, x1:x2] = combined

                        # Dibujar el rectángulo ajustado alrededor de la imagen
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                        # Comprobar colisión con el cuadrado fijo
                        if (x1 < square_x + square_size and x2 > square_x and
                            y1 < square_y + square_size and y2 > square_y):
                            print("¡Colisión detectada! Terminando ejecución.")
                            cap.release()
                            cv2.destroyAllWindows()
                            exit()  # Finalizar el programa

        # Mostrar el marco
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Presiona ESC para salir
            break

cap.release()
cv2.destroyAllWindows()
