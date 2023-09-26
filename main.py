import os.path
import csv
import sys

from downscale import *
from facedetector import *

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
    
    print("series:")
    print(series)
    sections = []

    for i in range(len(series)):
        if numbers[series[i][1]] - numbers[series[i][0]] > 7:
            print("section is suitable:")
            print((numbers[series[i][0]], numbers[series[i][1]]))
            sections.append(((numbers[series[i][0]]) / fps,  (numbers[series[i][1]]) / fps)) 
    
    return sections

def main():
    name = "test.mp4"
    # downscale and reduce fps to speed up the face detection process
    fps = 3
    # downscale(name,fps)
    suitable_frames = detectFaces(name)
    print("suitable_frames:")
    print(suitable_frames)
    suitable_sections = find_series(suitable_frames, fps)
    print("suitable_sections:")
    print(suitable_sections)
    cut_video(suitable_sections, name)

    

if __name__ == "__main__":
    main()