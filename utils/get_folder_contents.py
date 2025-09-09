from utils.config import Config
import os
def get_base_filename(file_path):
    """Returns the filename without the extension."""
    return os.path.splitext(os.path.basename(file_path))[0]

def get_video_files():
    """Returns a sorted list of video files."""
    return sorted([f for f in os.listdir(Config.Folders.VIDEO_DIR) if f.endswith(('.mp4', '.mov', '.avi'))])

def get_audio_files():
    """Returns a sorted list of audio files."""
    return sorted([f for f in os.listdir(Config.Folders.AUDIO_DIR) if f.endswith(('.mp3', '.wav', '.m4a'))])

def get_transcript_files():
    """Returns a sorted list of transcript files."""
    return sorted([f for f in os.listdir(Config.Folders.TRANSCRIPT_DIR) if f.endswith('.txt')])

def get_vector_store_dirs():
    """Returns a sorted list of vector store directories."""
    return sorted([d for d in os.listdir(Config.Folders.VECTOR_STORE_DIR) if os.path.isdir(os.path.join(Config.Folders.VECTOR_STORE_DIR, d))])

