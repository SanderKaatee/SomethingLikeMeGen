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

def organize_videos_by_cluster(grouped_videos, base_path="./output"):
    for label, videos in grouped_videos.items():
        # Create a new directory for the cluster
        cluster_dir = os.path.join(base_path, f"faces_{label}")
        if not os.path.exists(cluster_dir):
            os.makedirs(cluster_dir)

        # Move each video into the new directory
        for video in videos:
            src_path = os.path.join(base_path, video)
            dst_path = os.path.join(cluster_dir, video)
            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)


def extract_frame(video_path):
    # Initialize dlib's face detector
    cap = cv2.VideoCapture(video_path)
    print(video_path)
    print("Going into while loop now")
    iteration = 0
    while True:
        ret, frame = cap.read()
        iteration += 1

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
            print("Found at iteration", iteration)
            return frame

    print("NO FACE FOUND")
    cap.release()
    return None

def get_face_encoding(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dets = face_detector(gray)
    if len(dets) == 0:
        print("LENGTH OF DETS = 0")
        return None
    shape = shape_predictor(image, dets[0])
    return face_rec_model.compute_face_descriptor(image, shape)

def recognize_faces():
    video_folder = './output/'
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mkv'))]
    encodings = {}
    
    # Extract face encodings from each video
    for video_file in video_files:
        frame = extract_frame(os.path.join(video_folder, video_file))
        if frame is not None:
            encoding = get_face_encoding(frame)
            if encoding is not None:
                encodings[video_file] = encoding
            else:
                print("ENCODING IS NONE")
        else:
            print("FRAME IS NONE")
    
    print("encoding length", len(encodings))
    # Extract just the descriptors for clustering
    descriptors = list(encodings.values())
    print("descriptor length", len(descriptors))

    # Cluster using Chinese Whispers
    labels = dlib.chinese_whispers_clustering(descriptors, 0.5)
    print(labels)
    num_classes = len(set(labels))
    print("Number of clusters: {}".format(num_classes))

    # Group videos by cluster label
    video_names = list(encodings.keys())
    grouped_videos = {}
    for i, label in enumerate(labels):
        video_name = video_names[i]
        if label not in grouped_videos:
            grouped_videos[label] = []
        grouped_videos[label].append(video_name)

    # Print out the grouped videos
    for label, videos in grouped_videos.items():
        print(f"Cluster {label}:")
        for video in videos:
            print(f"  {video}")
    
    # Move videos to their respective folders
    organize_videos_by_cluster(grouped_videos)


if __name__ == "__main__":
    recognize_faces()
