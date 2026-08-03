import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def count_faces(frame):
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        if results.detections:
            return len(results.detections)
        return 0