import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def get_landmarks(frame, pose, draw=True):
  
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  #converts an image from one color space to another.
    results = pose.process(image_rgb)  #processes an RGB image and returns the pose landmarks on the most prominent person detected.
    landmarks = None
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        if draw:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2))
    return frame, landmarks


def landmark_to_xy(landmark, frame):
    
    h, w = frame.shape[:2]
    return int(landmark.x * w), int(landmark.y * h)


def calculate_angle(a, b, c):
    """
    Calcula el ángulo en grados formado por los puntos a-b-c (cada uno [x, y]).
    Uso: a = hip, b = knee, c = ankle => ángulo de la rodilla.
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # vectores BA y BC
    ba = a - b
    bc = c - b

    # protección contra división por cero
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0:
        return None

    cos_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    # recortar por imprecisiones numéricas
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle_rad = np.arccos(cos_angle)
    angle_deg = np.degrees(angle_rad)

    return float(angle_deg)

