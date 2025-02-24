from moviepy.editor import VideoFileClip
from logging import logger


def extract_audio_from_video(video_path: str, audio_path: str):
    """
    Извлекает аудиодорожку из видеофайла и сохраняет её в указанный путь.
    """
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, codec='mp3')
        audio.close()
        video.close()
        return True
    except Exception as e:
        logger.error(f"Ошибка при извлечении аудиодорожки: {e}")
        return False
