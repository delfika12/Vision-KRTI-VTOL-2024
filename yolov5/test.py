import torch
import cv2
import numpy as np
from pathlib import Path
import time

def draw_grid(frame, rows=3, cols=3):
    height, width = frame.shape[:2]
    row_height = height // rows
    col_width = width // cols
    
    # Draw horizontal lines
    for i in range(1, rows):
        y = i * row_height
        cv2.line(frame, (0, y), (width, y), (255, 255, 255), 2)
    
    # Draw vertical lines
    for i in range(1, cols):
        x = i * col_width
        cv2.line(frame, (x, 0), (x, height), (255, 255, 255), 2)
        
def get_grid_position(center_x, center_y, frame, rows=3, cols=3):
    height, width = frame.shape[:2]
    row_height = height // rows
    col_width = width // cols
    
    col_pos = center_x // col_width
    row_pos = center_y // row_height
    
    return (int(row_pos), int(col_pos))

# Mapping grid positions to messages
grid_messages_front = {
    (0, 0): "Yaw--",
    (0, 1): "Go Forward",
    (0, 2): "Yaw++",
    (1, 0): "Yaw--",
    (1, 1): "Go Forward",
    (1, 2): "Yaw++",
    (2, 0): "Yaw--",
    (2, 1): "Go Forward",
    (2, 2): "Yaw++",
}

grid_messages_bottom = {
    (0, 0): "Roll--",
    (0, 1): "Go Forward",
    (0, 2): "Roll++",
    (1, 0): "Roll--",
    (1, 1): "Go Down",
    (1, 2): "Roll++",
    (2, 0): "Roll--",
    (2, 1): "Go backward",
    (2, 2): "Roll++",
}

# Tentukan lokasi model relatif terhadap folder tempat program ini berada
model_path = Path(__file__).parent / 'yolov5n.pt'

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path))

# Capture video from two webcams
cap1 = cv2.VideoCapture(0)  # Webcam 1
cap2 = cv2.VideoCapture(1)  # Webcam 2

while cap1.isOpened() and cap2.isOpened():
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    # Perform inference on the frames
    results1 = model(frame1)
    results2 = model(frame2)

    # Process the results for webcam 1
    labels1, cord1 = results1.xyxyn[0][:, -1].numpy(), results1.xyxyn[0][:, :-1].numpy()
    for i in range(len(labels1)):
        row = cord1[i]
        if row[4] >= 0.5:  # Threshold for object confidence
            x1, y1, x2, y2 = int(row[0] * frame1.shape[1]), int(row[1] * frame1.shape[0]), int(row[2] * frame1.shape[1]), int(row[3] * frame1.shape[0])
            bgr = (0, 255, 0)  # Color for the bounding box
            cv2.rectangle(frame1, (x1, y1), (x2, y2), bgr, 2)
            cv2.putText(frame1, f'{model.names[int(labels1[i])]} {row[4]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
            grid_position1 = get_grid_position(center_x, center_y, frame1)
            print(f'Detected on Webcam 1: {model.names[int(labels1[i])]} at ({center_x}, {center_y}) Grid: {grid_position1}')

            # Display message based on grid position
            if grid_position1 in grid_messages_front:
                message = grid_messages_front[grid_position1]
                cv2.putText(frame1, message, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Process the results for webcam 2
    labels2, cord2 = results2.xyxyn[0][:, -1].numpy(), results2.xyxyn[0][:, :-1].numpy()
    for i in range(len(labels2)):
        row = cord2[i]
        if row[4] >= 0.5:  # Threshold for object confidence
            x1, y1, x2, y2 = int(row[0] * frame2.shape[1]), int(row[1] * frame2.shape[0]), int(row[2] * frame2.shape[1]), int(row[3] * frame2.shape[0])
            bgr = (0, 255, 0)  # Color for the bounding box
            cv2.rectangle(frame2, (x1, y1), (x2, y2), bgr, 2)
            cv2.putText(frame2, f'{model.names[int(labels2[i])]} {row[4]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
            grid_position2 = get_grid_position(center_x, center_y, frame2)
            print(f'Detected on Webcam 2: {model.names[int(labels2[i])]} at ({center_x}, {center_y}) Grid: {grid_position2}')

            # Display message based on grid position
            if grid_position2 in grid_messages_bottom:
                message = grid_messages_bottom[grid_position2]
                cv2.putText(frame2, message, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Draw grid on frames
    draw_grid(frame1)
    draw_grid(frame2)

    # Display the frames with detections and grid
    cv2.imshow('Front Cam', frame1)
    cv2.imshow('Bottom Cam', frame2)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcams and close all OpenCV windows
cap1.release()
cap2.release()
cv2.destroyAllWindows()
