import os
import cv2
import dlib
import numpy as np
import shutil

from sklearn.cluster import OPTICS
import numpy as np

# Initialize dlib's face detector and facial landmark predictor
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

def extract_frame(video_path):
    # Initialize dlib's face detector
    cap = cv2.VideoCapture(video_path)
    print(video_path)
    print("Going into while loop now")
    iteration = 0
    while True:
        ret, frame = cap.read()
        iteration += 1
        print("iteration", iteration)

        if not ret:
            # If we've read all frames and found no face, delete the video
            os.remove(video_path)
            print(f"Video {video_path} deleted as no face was found.")
            return None

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray)
        
        if len(faces) > 0:
            # If a face is found, return the frame
            cap.release()
            return frame

    print("No face found")
    cap.release()
    return None

def get_face_encoding(image):
    dets = face_detector(image, 1)
    if len(dets) == 0:
        return None
    shape = shape_predictor(image, dets[0])
    return face_rec_model.compute_face_descriptor(image, shape)

def main():
    video_folder = './output/'
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mkv'))]
    encodings = {}
    
    # Extract face encodings from each video
    for video_file in video_files:
        frame = extract_frame(os.path.join(video_folder, video_file))
        if frame is not None:
            encoding = get_face_encoding(frame)
            if encoding is not None:
                encodings[video_file] = np.array(encoding)
    
    # Assuming encodings is a dictionary with video names as keys and face encodings as values
    face_encodings_list = list(encodings.values())

    # Apply OPTICS clustering
    optics = OPTICS(min_samples=1).fit(face_encodings_list)

    # Group videos based on cluster labels
    grouped_videos = {}
    for idx, label in enumerate(optics.labels_):
        video_name = list(encodings.keys())[idx]
        if label not in grouped_videos:
            grouped_videos[label] = []
        grouped_videos[label].append(video_name)
    
    # Move videos to their respective folders
    for idx, (video, similar_videos) in enumerate(grouped_videos.items()):
        video_path = os.path.join(video_folder, video)
        if os.path.exists(video_path):
            folder_name = f'face_{idx}'
            os.makedirs(os.path.join(video_folder, folder_name), exist_ok=True)
            shutil.move(video_path, os.path.join(video_folder, folder_name))
        
        for sim_video in similar_videos:
            sim_video_path = os.path.join(video_folder, sim_video)
            if os.path.exists(sim_video_path):
                shutil.move(sim_video_path, os.path.join(video_folder, folder_name))


if __name__ == "__main__":
    main()
