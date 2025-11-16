import cv2

def draw_feedback(frame, diff):
    if abs(diff) < 10:
        text = "Sin descompensaciones significativas"
        color = (0, 255, 0)
    elif diff > 0:
        text = "Pierna izquierda mas fuerte"
        color = (0, 255, 255)
    else:
        text = "Pierna derecha mas fuerte"
        color = (255, 255, 0)
    
    cv2.putText(frame, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return frame
