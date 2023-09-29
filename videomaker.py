import os
import random
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip

number = 0

def get_random_video(videos, min_duration=0):
    global number
    number += 1
    min_duration += 0.05
    """Get a random video from the list. If min_duration is specified, ensure the video is at least that long."""
    suitable_videos = [v for v in videos if VideoFileClip(v).duration >= min_duration]
    if not suitable_videos:
        raise ValueError("No suitable videos found with the required minimum duration.")
    chosen_video = random.choice(suitable_videos)
    print(str(number) + ": " + chosen_video)
    videos.remove(chosen_video)
    return chosen_video

def get_subclip(video_path, length):
    clip = VideoFileClip(video_path)
    clip = clip.set_fps(138)
    clip = clip.subclip(0.05, length+0.05)
    return clip

def make_video():
    # Constants
    BEAT_DURATION = 4348 / 10000  # 435ms in seconds
    LONG_BEAT_DURATION = BEAT_DURATION * 8
    FOLDER_PATH = "./output"

    # Get all video paths
    all_videos = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if f.endswith(('.mp4', '.avi', '.mov'))]

    # Construct the video sequence
    final_clips = []


    # Two sequences of 9 short beats followed by 1 long beat
    for _ in range(2):
        for _ in range(8):
            video_path = get_random_video(all_videos, BEAT_DURATION)
            clip = get_subclip(video_path, BEAT_DURATION)
            final_clips.append(clip)

        video_path = get_random_video(all_videos, LONG_BEAT_DURATION)
        clip = get_subclip(video_path, LONG_BEAT_DURATION)
        final_clips.append(clip)

    # 32 short beats
    for _ in range(4):
        for _ in range(6):
            video_path = get_random_video(all_videos, BEAT_DURATION)
            clip = get_subclip(video_path, BEAT_DURATION)
            final_clips.append(clip)
        video_path = get_random_video(all_videos, BEAT_DURATION)
        clip = get_subclip(video_path, 2 * BEAT_DURATION)
        final_clips.append(clip)

    # Concatenate all clips and write to output
    final_video = concatenate_videoclips(final_clips, method="compose")
    audio = AudioFileClip('cutsomethinglikeme.wav')
    final_video = final_video.set_audio(audio)
    final_video.write_videofile("final_output.mp4", codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    make_video()