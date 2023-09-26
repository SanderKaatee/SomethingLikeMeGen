from moviepy.editor import *
clip = VideoFileClip("Y2Mate.is - American Psycho - Business Card scene [HD - 720p]-aZVkW9p-cCU-720p-1659390853741.mp4")
clip = clip.subclip(40, 65)
clip.write_videofile("test.mp4")