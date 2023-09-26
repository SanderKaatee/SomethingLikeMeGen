import cv2
import numpy as np
import os

def stabilize_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Parameters for optical flow
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    prev_gray = None
    prev_points = None
    global_motion = [0, 0]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        curr_points = cv2.goodFeaturesToTrack(gray, mask=None, maxCorners=200, qualityLevel=0.3, minDistance=7, blockSize=7)

        if prev_gray is not None:
            # Calculate optical flow
            curr_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None, **lk_params)
            valid_curr_points = curr_points[status == 1]
            valid_prev_points = prev_points[status == 1]

            # Estimate global motion
            dx = np.median(valid_curr_points[:, 0] - valid_prev_points[:, 0])
            dy = np.median(valid_curr_points[:, 1] - valid_prev_points[:, 1])
            global_motion = [0.99 * gm + 0.01 * d for gm, d in zip(global_motion, [dx, dy])]

            # Stabilize frame
            M = np.float32([[1, 0, -global_motion[0]], [0, 1, -global_motion[1]]])
            stabilized_frame = cv2.warpAffine(frame, M, (width, height))
            out.write(stabilized_frame)

        prev_gray = gray
        prev_points = curr_points

    cap.release()
    out.release()

# Stabilize all videos in the './output' directory
video_files = [f for f in os.listdir('./output') if f.startswith('cropped_') and f.endswith('.mp4')]
for video_file in video_files:
    input_path = os.path.join('./output', video_file)
    output_path = os.path.join('./output', f"stabilized_{video_file}")
    stabilize_video(input_path, output_path)

print("Stabilization complete!")
