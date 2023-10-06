import os.path
import csv
import sys
import time
import shutil
import re



from downscale import *
from facedetector import *
from cropper import crop_videos
from scene_splitter import split_scenes
from videomaker import make_video
from facerecognizer import recognize_faces

def simplify_name(filename):
    # Extract title and year using regular expressions
    matches = re.findall(r'\b[a-zA-Z]{4,}\b', filename)
    if matches:
        title = ''.join(matches)

        return title[:8]
    else:
        filename.replace('.mp4', '')
        stripped_name = ''.join([char if char.isalpha() or char.isspace() else ' ' for char in filename])
        stripped_name = ' '.join(stripped_name.split())  # Remove extra spaces

        return stripped_name


def clip_vertical(clip):
    desired_width = int(clip.size[1] * 9 / 16)

    # Calculate the left and right cropping boundaries
    left_boundary = (clip.size[0] - desired_width) // 2
    right_boundary = left_boundary + desired_width

    cropped_clip = clip.crop(x_center=clip.size[0] / 2, width=desired_width)
    return cropped_clip


def cut_video(input_list, destination_path, name):
    clip = VideoFileClip(destination_path + name)
    for i in range(len(input_list)):
        start = input_list[i][0]
        end = input_list[i][1]
        if end < clip.duration:
            subclip = clip.subclip(start,end)
        else:
            subclip = clip.subclip(start, clip.duration)

        subclip.write_videofile(destination_path + "output/output_"+str(i)+".mp4")

def find_series(numbers, fps):
    # given a set of suitable frames, finds which frames are 
    # a sequential series (e.g. a suitable clip)
    series = []
    start = 0
    end = 0
    for i in range(len(numbers)):
        # if we are at the end of the frames set
        if i == len(numbers) - 1:
            # check whether we had a suitable series ready and add it
            if end - start > 0:
                series.append((start, end))
            break

        if numbers[i] + 3 >= numbers[i + 1]:
            end = i + 1
        else:
            if end - start > 0:
                series.append((start, end))
            start = i + 1
            end = i + 1

    sections = []

    for i in range(len(series)):
        if numbers[series[i][1]] - numbers[series[i][0]] > (1.75 * fps):
            sections.append(((numbers[series[i][0]]) / fps,  (numbers[series[i][1]]) / fps)) 
    
    return sections

def main():
    files = []
    for filename in os.listdir('./movies/'):
        if filename.endswith('.mp4'):
            print(filename)
            files.append(filename)
            
    for name in files:
        all_time = time.time()
        new_name = simplify_name(name)

        if not os.path.exists(new_name):
            os.makedirs(new_name)
            os.makedirs(new_name + '/output')

        destination_path = './' + new_name + '/'
        shutil.move('./movies/' + name, destination_path)

        # downscale and reduce fps to speed up the face detection process
        print("Downscaling")
        start_time = time.time()
        fps = 4
        downscale(name,fps,new_name,destination_path)
        end_time = time.time()
        downscale_time = end_time - start_time

        print("Detecting")
        start_time = time.time()
        suitable_frames = detect_faces(new_name + '.mp4', destination_path)
        end_time = time.time()
        face_detect_time = end_time - start_time

        suitable_sections = find_series(suitable_frames, fps)
        
        print("Cutting")
        start_time = time.time()
        cut_video(suitable_sections, destination_path, name)
        end_time = time.time()
        cut_video_time = end_time - start_time

        start_time = time.time()
        split_scenes(destination_path)
        end_time = time.time()
        split_video_time = end_time - start_time

        start_time = time.time()
        crop_videos(destination_path)
        end_time = time.time()
        crop_video_time = end_time - start_time

        split_scenes(destination_path)

        start_time = time.time()
        recognize_faces(destination_path)
        end_time = time.time()
        recognize_time = end_time - start_time

        start_time = time.time()
        make_video(destination_path, new_name)
        end_time = time.time()
        make_video_time = end_time - start_time


        print('Downscale: ', downscale_time)
        print('Face_detect: ', face_detect_time)
        print('Cut_video: ', cut_video_time)
        print('Split_video: ', split_video_time)
        print('Crop_video: ', crop_video_time)
        print('Recognize: ', recognize_time)
        print('Make videotime: ', make_video_time)
        print('Total: ', time.time() - all_time)
    

if __name__ == "__main__":
    main()