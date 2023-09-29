from moviepy.editor import AudioFileClip

def process_audio():
    # Constants
    BPM = 138
    BEAT_DURATION = 60 / BPM  # Duration of one beat in seconds
    SKIP_BEATS = 32
    KEEP_BEATS = 64

    # Calculate start and end times
    start_time = SKIP_BEATS * BEAT_DURATION
    end_time = start_time + KEEP_BEATS * BEAT_DURATION

    # Load the audio file
    audio = AudioFileClip('somethinglikeme.wav')

    # Cut the audio
    cut_audio = audio.subclip(start_time, end_time)

    # Save the cut audio
    cut_audio.write_audiofile('cutsomethinglikeme.wav')

if __name__ == "__main__":
    process_audio()
