import cv2
import numpy as np

def overlay_png(frame, png, x, y):
    h, w = png.shape[:2]

    # Limitar para no salirse por la izquierda
    if x < 0:
        png = png[:, -x:]
        w = png.shape[1]
        x = 0

    # Limitar para no salirse por arriba
    if y < 0:
        png = png[-y:, :]
        h = png.shape[0]
        y = 0

    # Limitar para no salirse por la derecha
    if x + w > frame.shape[1]:
        png = png[:, :frame.shape[1] - x]
        w = png.shape[1]

    # Limitar para no salirse por abajo
    if y + h > frame.shape[0]:
        png = png[:frame.shape[0] - y, :]
        h = png.shape[0]

    # Si no queda nada, salir
    if w <= 0 or h <= 0:
        return frame

    # Canal alfa
    alpha = png[:, :, 3] / 255.0
    overlay = png[:, :, :3]

    for c in range(3):
        frame[y:y+h, x:x+w, c] = (
            alpha * overlay[:, :, c] +
            (1 - alpha) * frame[y:y+h, x:x+w, c]
        )

    return frame
