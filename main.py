import sys
import cv2
import mediapipe as mp
import numpy as np
import time
from config import config



BaseOptions = mp.tasks.BaseOptions(model_asset_path=config.model_path)
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions,
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)


