import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

def is_finger_open(landmarks, tip, pip):
    return landmarks[tip].y < landmarks[pip].y

def is_thumb_open(landmarks):
    tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    cmc = landmarks[mp_hands.HandLandmark.THUMB_CMC]
    distance = ((tip.x - cmc.x)**2 + (tip.y - cmc.y)**2)**0.5
    return distance > 0.15

def get_hand_gesture(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = {
        "Thumb": is_thumb_open(lm),
        "Index": is_finger_open(lm, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
        "Middle": is_finger_open(lm, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
        "Ring": is_finger_open(lm, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
        "Pinky": is_finger_open(lm, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)
    }

    open_fingers = [f for f, open_ in fingers.items() if open_]
    return open_fingers

def draw_hand_landmarks(image, hand_landmarks):
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)