import numpy as np

def detect_jump_height(ankle_y_values, baseline_y):
    """Devuelve la altura de salto relativa en píxeles."""
    min_y = np.min(ankle_y_values)
    return baseline_y - min_y  # cuanto menor es min_y, más alto el salto, ya que el origen se sitúa en la esquina superior izquierda
