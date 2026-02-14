import cv2
import mediapipe as mp

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(min_detection_confidence=0.7)

def detect_smile(image):
    # Convert to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)
    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            # Use landmarks 61, 291 (mouth corners) for smile detection
            left = face.landmark[61]
            right = face.landmark[291]
            if right.x - left.x > 0.05:  # Smile threshold
                return True
    return False