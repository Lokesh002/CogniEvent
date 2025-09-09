# convert video to audio
from moviepy import VideoFileClip
import tempfile
import os
def video_file_to_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    audio.close()
    video.close()
    # Optionally, remove the original video file
    os.remove(video_path)

# convert video buffer to audio and save audio to a folder
def video_buffer_to_audio(video_buffer, audio_path):
    # Write buffer to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_buffer)
        temp_video_path = temp_video.name
    try:
        video = VideoFileClip(temp_video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        audio.close()
        video.close()
    finally:
        os.remove(temp_video_path)