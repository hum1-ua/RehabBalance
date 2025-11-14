import cv2
import time
import numpy as np
import mediapipe as mp

from utils.pose_utils import get_landmarks, landmark_to_y
from utils.jump_analysis import detect_jump_height
from utils.feedback import draw_feedback
from utils.session_manager import save_session

mp_pose = mp.solutions.pose


def main():

    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose()

    phase = 0
    start_time = None

    left_baseline = right_baseline = None
    left_y_values = []
    right_y_values = []
    left_jump = right_jump = None

    print("Iniciando Jump Trainer...")

    cv2.namedWindow("FullScreen", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("FullScreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        landmarks = get_landmarks(frame, pose, draw=True)

        if landmarks:

            # coordenadas limpias
            left_ankle = landmark_to_y(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE], frame)
            right_ankle = landmark_to_y(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE], frame)

            ############# FASE 0 — CALIBRACIÓN #############
            if phase == 0:

                if start_time is None:
                    start_time = time.time()
                    left_y_values, right_y_values = [], []

                elapsed = time.time() - start_time

                left_y_values.append(left_ankle)
                right_y_values.append(right_ankle)

                if elapsed <= 10:
                    msg = "Mantente quieto para calibrar..."
                elif 10 < elapsed <= 15:
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

                if start_time is None:
                    start_time = time.time()

                elif time.time() - start_time > 6:
                    left_jump = detect_jump_height(left_y_values, left_baseline)

                    if left_jump > 20:
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

                right_y_values.append(right_ankle)

                if start_time is None:
                    start_time = time.time()

                elif time.time() - start_time > 6:
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

                diff = left_jump - right_jump
                frame = draw_feedback(frame, diff)

                cv2.putText(frame, f"Izq: {left_jump:.1f}px | Der: {right_jump:.1f}px",
                            (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
                cv2.putText(frame, "Pulsa R para reiniciar o ESC para salir",
                            (30, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 1)

                # Espera visible real (sin parpadeo)
                if start_time is None:
                    start_time = time.time()

                if time.time() - start_time > 4:
                    save_session(left_jump, right_jump, diff)

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
