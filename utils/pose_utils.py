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
    return landmarks


def landmark_to_y(landmark, frame):
    
    h, _ = frame.shape[:2]
    return  int(landmark.y * h)
