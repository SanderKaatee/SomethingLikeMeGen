import os.path
import csv
import sys
import time


from downscale import *
from facedetector import *
from cropper import crop_videos
from scene_splitter import split_scenes
from videomaker import make_video

def clip_vertical(clip):
    desired_width = int(clip.size[1] * 9 / 16)

    # Calculate the left and right cropping boundaries
    left_boundary = (clip.size[0] - desired_width) // 2
    right_boundary = left_boundary + desired_width

    cropped_clip = clip.crop(x_center=clip.size[0] / 2, width=desired_width)
    return cropped_clip


def cut_video(input_list, name):
    clip = VideoFileClip(name)
    for i in range(len(input_list)):
        start = input_list[i][0]
        end = input_list[i][1]
        if end < clip.duration:
            subclip = clip.subclip(start,end)
        else:
            subclip = clip.subclip(start, clip.duration)

        subclip.write_videofile("output/output_"+str(i)+".mp4")

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
    name = "nocountry.mp4"
    # downscale and reduce fps to speed up the face detection process
    fps = 2

    start_time = time.time()
    downscale(name,fps)
    end_time = time.time()
    downscale_time = end_time - start_time

    start_time = time.time()
    suitable_frames = detect_faces(name)
    end_time = time.time()
    face_detect_time = end_time - start_time

    suitable_sections = find_series(suitable_frames, fps)
    
    start_time = time.time()
    cut_video(suitable_sections, name)
    end_time = time.time()
    cut_video_time = end_time - start_time

    
    crop_videos()
    split_scenes()
    make_video()

    print('Downscale: ', downscale_time)
    print('Face_detect: ', face_detect_time)
    print('Cut_video: ', cut_video_time)
    

if __name__ == "__main__":
    main()