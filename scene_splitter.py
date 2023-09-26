import cv2
import numpy as np
import os

# Parameters
threshold_value = 25.0  # Adjust this value based on your needs
min_scene_length = 0.45  # in seconds

# List all the video files
video_files = [f for f in os.listdir('./output') if f.startswith('output_') and f.endswith('.mp4')]

for video_file in video_files:
    cap = cv2.VideoCapture(os.path.join('./output', video_file))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    min_frames = int(fps * min_scene_length)
    
    prev_frame = None
    scene_start = 0
    scene_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            if np.mean(diff) > threshold_value:
                if cap.get(cv2.CAP_PROP_POS_FRAMES) - scene_start > min_frames:
                    scene_count += 1
                    out_filename = os.path.join('./output', f"{video_file.split('.')[0]}_{scene_count}.mp4")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(out_filename, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
                    for i in range(scene_start, int(cap.get(cv2.CAP_PROP_POS_FRAMES))-1):
                        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                        ret, scene_frame = cap.read()
                        out.write(scene_frame)
                    out.release()
                scene_start = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        
        prev_frame = gray
    
    cap.release()
    os.remove(os.path.join('./output', video_file))


print("Processing complete!")
