import numpy as np


def calc_knee_angle(hip, knee, ankle):
    """Calcula el ángulo de la rodilla en grados."""
    a = np.array(hip) - np.array(knee)
    b = np.array(ankle) - np.array(knee)
    cosang = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))
    

def detect_jump_height(ankle_y_values, baseline_y):
    """Devuelve la altura de salto relativa en píxeles."""
    min_y = np.min(ankle_y_values)
    return baseline_y - min_y  # cuanto menor es min_y, más alto el salto, ya que el origen se sitúa en la esquina superior izquierda
