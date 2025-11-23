import cv2
import time
import numpy as np
import mediapipe as mp

from utils.jump_analysis import detect_jump_height
from utils.session_manager import save_session
from utils.log import overlay_png

def main():

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    MODEL_PATH = "models/pose_landmarker_full.task"

    flag = False

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.VIDEO,
        num_poses=1
    )

    with PoseLandmarker.create_from_options(options) as landmarker:
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:  # seguridad si la cámara no da fps
            fps = 30

        mp_pose = mp.solutions.pose
        frame_ms = int(1000 / fps)

        #Inicializar valores
        phase = 0
        start_time = None
        timestamp = 0
        left_baseline = right_baseline = None  #punto de referencia para calcular la altura del salto
        left_y_values = []
        right_y_values = []
        left_jump = right_jump = None

        # Cargar tronco
        scale=0.25
        tronco = cv2.imread("log.png", cv2.IMREAD_UNCHANGED)
        tronco = cv2.resize(tronco, (0, 0), fx=scale, fy=scale)
        tronco_h, tronco_w = tronco.shape[:2]

        # Variables del tronco
        log_x = -tronco_w
        log_speed = 20
        
        cv2.namedWindow("FullScreen", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("FullScreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
           
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            log_y = frame.shape[0] - tronco_h
            # Convertir frame a formato MediaPipe
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # Ejecutar detección
            result = landmarker.detect_for_video(mp_image, timestamp)
            timestamp += frame_ms

            if result.pose_landmarks:
                
                lm = result.pose_landmarks[0]   # solo una persona detectada
                for person_landmarks in result.pose_landmarks:  # para mantener tu estructura
                    h, w, _ = frame.shape

                    # Dibuja líneas entre los landmarks
                    for connection in mp_pose.POSE_CONNECTIONS:
                        start_idx, end_idx = connection
                        start = person_landmarks[start_idx]
                        end = person_landmarks[end_idx]

                        x1, y1 = int(start.x * w), int(start.y * h)
                        x2, y2 = int(end.x * w), int(end.y * h)

                        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    # Dibuja los puntos (landmarks)
                    for landmark in person_landmarks:
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)


                #obtenemos la componente y de los tobillos

                left_ankle = int(lm[28].y * h)  #el 28 corresponde al derecho, pero se pone al revés debido a la inversión del frame con cv2.flip()
                right_ankle = int(lm[27].y * h)

                ############# FASE 0 — CALIBRACIÓN #############
                if phase == 0:
                    
                    if start_time is None:
                        start_time = time.time()
                        left_y_values, right_y_values = [], []

                    transcurrido = time.time() - start_time
                    if transcurrido <= 10:
                        msg = "Pongase en posicion"
                    elif 10 < transcurrido <= 20 or len(left_y_values) < 100:  #para asegurarnos que tenemos suficientes puntos para estimar el baseline,
                        left_y_values.append(left_ankle)
                        right_y_values.append(right_ankle)
                        msg = "Quedese quieto. Calibrando..."
                        
                    elif 20 < transcurrido <= 25:
                        if left_baseline is None:
                            left_baseline = np.mean(left_y_values)
                            right_baseline = np.mean(right_y_values)
                            msg = "Calibracion completada. Preparate..."
                    else:
                        phase = 1
                        start_time = None
                        continue

                    cv2.putText(frame, msg, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                ############# FASE 1 — SALTO IZQUIERDA #############
                elif phase == 1:

                    cv2.putText(frame, "Salta con la pierna IZQUIERDA!", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                    left_y_values.append(left_ankle)

                    log_x += log_speed

                    # Si se sale, volver al inicio
                    if log_x > frame.shape[1]:
                        log_x = -tronco_w

                    # Pintar PNG en el frame
                    frame = overlay_png(frame, tronco, log_x, log_y)

                    if start_time is None:
                        start_time = time.time()

                    elif time.time() - start_time > 6:
                        left_jump = detect_jump_height(left_y_values, left_baseline)

                        if left_jump > 20:  #umbral para asegurarnos que el usuario salta de verdad
                            print(f"Altura salto izquierdo: {left_jump:.2f}")
                            phase = 2
                            start_time = None
                            left_y_values = []
                        else:
                            start_time = time.time()

                ############# FASE 2 — DESCANSO #############
                elif phase == 2:

                    cv2.putText(frame, "Descansa. Preparate...", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                    if start_time is None:
                        start_time = time.time()

                    elif time.time() - start_time > 6:
                        phase = 3
                        start_time = None

                ############# FASE 3 — SALTO DERECHA #############
                elif phase == 3:

                    cv2.putText(frame, "Salta con la pierna DERECHA!", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                    if start_time is None:
                        start_time = time.time()
                        log_x = -tronco_w

                    right_y_values.append(right_ankle)

                    log_x += log_speed

                    # Si se sale, volver al inicio
                    if log_x > frame.shape[1]:
                        log_x = -tronco_w

                    # Pintar PNG en el frame
                    frame = overlay_png(frame, tronco, log_x, log_y)

                    if time.time() - start_time > 6:
                        right_jump = detect_jump_height(right_y_values, right_baseline)

                        if right_jump > 20:
                            print(f"Altura salto derecho: {right_jump:.2f}")
                            phase = 4
                            start_time = None
                            right_y_values = []
                        else:
                            start_time = time.time()

                ############# FASE 4 — FEEDBACK FINAL #############
                elif phase == 4:

                    # Calculo del porcentaje de asimetría
                    asymmetry = abs(left_jump - right_jump) / max(left_jump, right_jump) * 100

                    # Mostrar alturas
                    cv2.putText(frame, f"Salto IZQ: {left_jump:.1f}px", 
                                (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                    cv2.putText(frame, f"Salto DER: {right_jump:.1f}px", 
                                (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                    # Mostrar diferencia porcentual
                    cv2.putText(frame, f"Diferencia: {asymmetry:.1f}%", 
                                (30, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                                (0,255,0) if asymmetry < 10 else (0,0,255), 2)

                    # Mensaje de riesgo
                    if asymmetry < 10:
                        risk_msg = "NO hay riesgo (asimetria < 10%)"
                        color = (0, 255, 0)
                    else:
                        risk_msg = "SI hay riesgo (asimetria > 10%)"
                        color = (0, 0, 255)

                    cv2.putText(frame, risk_msg, 
                                (30, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

                    cv2.putText(frame, "Pulsa R para reiniciar o ESC para salir",
                                (30, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)

                    if not flag:
                        diff = left_jump - right_jump
                        save_session(left_jump, right_jump, diff)
                        flag = True

            # Mostrar frame
            cv2.imshow("FullScreen", frame)

            key = cv2.waitKey(1)

            if key == 27:
                break

            if key == ord('r') and phase == 4:
                phase = 0
                left_jump = right_jump = None
                print("Reiniciando sesión...")

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
