import cv2
import dlib
import os

def crop_videos():
    # Initialize face detector
    detector = dlib.get_frontal_face_detector()

    # List all the video files
    video_files = [f for f in os.listdir('./output') if f.startswith('output_') and f.endswith('.mp4')]

    alpha = 0.1  # Smoothing factor, adjust as needed (0 < alpha <= 1)
    smoothed_center_x = None

    for video_file in video_files:
        cap = cv2.VideoCapture(os.path.join('./output', video_file))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Create a VideoWriter object to save the output video
        out_filename = os.path.join('./output', f"cropped_{video_file}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        height = int(cap.get(4))
        width = int((9/16) * height)
        out = cv2.VideoWriter(out_filename, fourcc, fps, (width, height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            
            # If faces are detected, calculate the horizontal range
            if faces:
                start_x = min([face.left() for face in faces])
                end_x = max([face.right() for face in faces])
                center_x = (start_x + end_x) // 2
                
                # Apply exponential smoothing
                if smoothed_center_x is None:
                    smoothed_center_x = center_x
                else:
                    smoothed_center_x = (1 - alpha) * smoothed_center_x + alpha * center_x
                
                # Calculate the left and right boundaries for the cropped video
                half_width = width // 2
                left_boundary = max(0, int(smoothed_center_x - half_width))
                right_boundary = min(frame.shape[1], int(smoothed_center_x + half_width))
                
                # Adjust if the video is too close to one of the edges
                if right_boundary - left_boundary < width:
                    if left_boundary == 0:
                        right_boundary = width
                    else:
                        left_boundary = frame.shape[1] - width
                
                cropped_frame = frame[:, left_boundary:right_boundary]
                out.write(cropped_frame)
            else:
                cropped_frame = frame[:, left_boundary:right_boundary]
                out.write(cropped_frame)
        
        cap.release()
        out.release()
        smoothed_center_x = None  # Reset for the next video
        os.remove(os.path.join('./output', video_file))


    print("Processing complete!")
