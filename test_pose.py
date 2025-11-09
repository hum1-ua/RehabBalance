# test_pose.py
import cv2
from utils.pose_utils import get_landmarks, landmark_to_xy, calculate_angle
from mediapipe import solutions
    
def main():
    mp_pose = solutions.pose
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se ha podido abrir la cámara.")
        return

    print("Pulsa ESC para salir.")
    while True:
        ret, frame = cap.read()
        if not ret: #si no se ha retenido ningun frame
            break
        frame = cv2.flip(frame, 1)  #invertir la imagen horizontalmente
        frame_drawn, lm = get_landmarks(frame, mp_pose.Pose(), draw=True)

        if lm:
            # obtener coordenadas en píxeles
            r_hip = landmark_to_xy(lm[mp_pose.PoseLandmark.RIGHT_HIP.value], frame_drawn)
            r_knee = landmark_to_xy(lm[mp_pose.PoseLandmark.RIGHT_KNEE.value], frame_drawn)
            r_ankle = landmark_to_xy(lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value], frame_drawn)

            l_hip = landmark_to_xy(lm[mp_pose.PoseLandmark.LEFT_HIP.value], frame_drawn)
            l_knee = landmark_to_xy(lm[mp_pose.PoseLandmark.LEFT_KNEE.value], frame_drawn)
            l_ankle = landmark_to_xy(lm[mp_pose.PoseLandmark.LEFT_ANKLE.value], frame_drawn)

            angle_r = calculate_angle(r_hip, r_knee, r_ankle)
            angle_l = calculate_angle(l_hip, l_knee, l_ankle)

            if angle_r is not None:
                cv2.putText(frame_drawn, f"R: {int(angle_r)} deg", (r_knee[0]+10, r_knee[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            if angle_l is not None:
                cv2.putText(frame_drawn, f"L: {int(angle_l)} deg", (l_knee[0]+10, l_knee[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.imshow("Test Pose - Knees", frame_drawn)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    main()
