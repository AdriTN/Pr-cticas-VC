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

# Extraer el canal alfa
overlay_img = nose_overlay[:, :, :3]  # RGB
alpha_channel = nose_overlay[:, :, 3] / 255.0  # Normaliza el canal alfa

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

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

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # Procesar la malla facial
                mesh_results = face_mesh.process(frame_rgb)
                if mesh_results.multi_face_landmarks:
                    for face_landmarks in mesh_results.multi_face_landmarks:
                        # Obtener las coordenadas de la punta de la nariz
                        nose_tip = face_landmarks.landmark[1]  # Landmark 1 es la punta de la nariz
                        nose_x = int(nose_tip.x * iw)
                        nose_y = int(nose_tip.y * ih)

                        # Imprimir coordenadas de la nariz para depuración
                        print(f"Coordenadas de la nariz: ({nose_x}, {nose_y})")

                        # Obtener dimensiones originales de la imagen de la nariz
                        overlay_height, overlay_width = nose_overlay.shape[:2]

                        # Definir la región donde se superpondrá la imagen
                        y1 = int(nose_y - (overlay_height / 2))
                        y2 = int(y1 + overlay_height)
                        x1 = int(nose_x - (overlay_width / 2))
                        x2 = int(x1 + overlay_width)

                        # Asegúrate de que las coordenadas no salgan del marco
                        if y1 < 0 or x1 < 0 or y2 > frame.shape[0] or x2 > frame.shape[1]:
                            print("La imagen no cabe en el marco. Saltando superposición.")
                            continue  # Saltar si la imagen no cabe

                        # Crear la máscara y el fondo
                        mask = alpha_channel  # Usar el canal alfa
                        mask = cv2.resize(mask, (overlay_width, overlay_height))  # Redimensionar máscara
                        mask = mask[:, :, np.newaxis]  # Agregar dimensión para multiplicación

                        # Redimensionar el roi al tamaño de la superposición
                        roi = frame[y1:y2, x1:x2]
                        roi = cv2.resize(roi, (overlay_width, overlay_height))  # Redimensionar roi

                        # Asegúrate de que overlay_img se ajuste a la región
                        overlay_img_resized = cv2.resize(overlay_img, (overlay_width, overlay_height))

                        # Combinar las imágenes
                        combined = (roi * (1 - mask) + overlay_img_resized * mask).astype(np.uint8)

                        # Colocar la imagen combinada de vuelta en el fondo
                        frame[y1:y2, x1:x2] = combined

                        # Dibujar un rectángulo alrededor de la imagen del pájaro sin espacios
                        rect_x1 = int(nose_x - (overlay_width / 2))
                        rect_y1 = int(nose_y - (overlay_height / 2))
                        rect_x2 = int(rect_x1 + overlay_width)
                        rect_y2 = int(rect_y1 + overlay_height)

                        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)  # Rectángulo verde

        # Mostrar el marco con la imagen superpuesta y el rectángulo
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(5) & 0xFF == 27:  # Presiona ESC para salir
            break

cap.release()
cv2.destroyAllWindows()
