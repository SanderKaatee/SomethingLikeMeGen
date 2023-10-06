from moviepy.editor import *

def downscale(name,fps, new_name, destination):
    clip = VideoFileClip(destination + name)
    # clip = clip.subclip(40, 65)
    clip = clip.without_audio()
    clip = clip.resize(height=480)
    clip = clip.set_fps(fps)
    clip.write_videofile(destination + "resized_" + new_name + ".mp4")
    return