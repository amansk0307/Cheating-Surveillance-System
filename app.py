import cv2
import numpy as np
import base64
import os
import time
from flask import Flask, render_template, request, jsonify
from eye_movement import process_eye_movement
from head_pose import process_head_pose
from mobile_detection import process_mobile_detection
from person_detection import count_faces

app = Flask(__name__)

# Create log directory
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Calibration variables
calibrated_angles = None
calibration_start_time = time.time()

# Detection timers
head_timer = None
eye_timer = None
mobile_timer = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global calibrated_angles, calibration_start_time, head_timer, eye_timer, mobile_timer

    data = request.get_json()
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    status_messages = []
    
    # Count number of faces
    num_faces = count_faces(frame)
    if num_faces > 1:
        return jsonify({"status": "⚠️ Multiple people detected! Please stay alone in frame."})
    elif num_faces == 0:
        return jsonify({"status": "😐 No person detected. Please stay in front of camera."})
    
    # Process eye movement
    frame, gaze_direction = process_eye_movement(frame)
    if gaze_direction != "Looking Center":
        if eye_timer is None:
            eye_timer = time.time()
        elif time.time() - eye_timer >= 3:
            filename = os.path.join(log_dir, f"eye_{gaze_direction}_{int(time.time())}.png")
            cv2.imwrite(filename, frame)
            status_messages.append(f"Gaze issue: {gaze_direction}")
            eye_timer = None
    else:
        eye_timer = None

    # Process head pose
    if time.time() - calibration_start_time <= 5 and calibrated_angles is None:
        result = process_head_pose(frame, None)
        if result and len(result) == 4:
            frame, pitch_offset, yaw_offset, roll_offset = result
            calibrated_angles = (pitch_offset, yaw_offset, roll_offset)
            status_messages.append("Calibrating head pose...")
    elif calibrated_angles:
        frame, head_direction = process_head_pose(frame, calibrated_angles)
        if head_direction != "Looking at Screen":
            if head_timer is None:
                head_timer = time.time()
            elif time.time() - head_timer >= 3:
                filename = os.path.join(log_dir, f"head_{head_direction}_{int(time.time())}.png")
                cv2.imwrite(filename, frame)
                status_messages.append(f"Head issue: {head_direction}")
                head_timer = None
        else:
            head_timer = None

    # Process mobile detection
    frame, mobile_detected = process_mobile_detection(frame)
    if mobile_detected:
        if mobile_timer is None:
            mobile_timer = time.time()
        elif time.time() - mobile_timer >= 2:
            filename = os.path.join(log_dir, f"mobile_detected_{int(time.time())}.png")
            cv2.imwrite(filename, frame)
            status_messages.append("Mobile detected!")
            mobile_timer = None
    else:
        mobile_timer = None

    # Combine all messages
    if not status_messages:
        status = "No issues detected"
    else:
        status = " | ".join(status_messages)

    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(debug=True)