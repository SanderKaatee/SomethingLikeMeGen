from moviepy.editor import *

def downscale(name,fps):
    clip = VideoFileClip(name)
    # clip = clip.subclip(40, 65)
    clip = clip.without_audio()
    clip = clip.resize(height=480)
    clip = clip.set_fps(fps)
    clip.write_videofile("resized_" + name)
    return