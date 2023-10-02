import cv2
import dlib
import os

def crop_videos():
    # Initialize face detector
    detector = dlib.get_frontal_face_detector()

    # List all the video files
    video_files = [f for f in os.listdir('./output') if f.startswith('output_') and f.endswith('.mp4')]

    alpha = 0.1  # Smoothing factor, adjust as needed (0 < alpha <= 1)

    for video_file in video_files:
        print("Cropping", video_file)
        cap = cv2.VideoCapture(os.path.join('./output', video_file))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Create a VideoWriter object to save the output video
        out_filename = os.path.join('./output', f"cropped_{video_file}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        height = int(cap.get(4))
        width = int((9/16) * height)
        half_width = width // 2
        ret, frame = cap.read()
        center_x = None
        smoothed_center_x = None
        left_boundary = None


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
                prominent_face = max(faces, key=lambda face: face.width())
                
                start_x = prominent_face.left()
                end_x = prominent_face.right()
                center_x = (start_x + end_x) // 2

                if smoothed_center_x == None:
                    smoothed_center_x = center_x
                
                smoothed_center_x = (1 - alpha) * smoothed_center_x + alpha * center_x
                
                # Calculate the left and right boundaries for the cropped video
                left_boundary = max(0, int(smoothed_center_x - half_width))
                right_boundary = min(frame.shape[1], int(smoothed_center_x + half_width))

                cropped_frame = frame[:, left_boundary:right_boundary]
                
                out.write(cropped_frame)
            else:
                if left_boundary:
                    cropped_frame = frame[:, left_boundary:right_boundary]
                    out.write(cropped_frame)
        
        cap.release()
        out.release()
        # os.remove(os.path.join('./output', video_file))

    print("Processing complete!")

if __name__ == "__main__":
    crop_videos()