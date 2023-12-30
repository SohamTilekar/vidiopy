from .audio.AudioClip import AudioClip, AudioFileClip
from .video.VideoClips import VideoClip, VideoFileClip, ImageClip, Data2ImageClip, ImageSequenceClip, ColorClip, TextClip, CompositeVideoClip


if __name__ == '__main__':
    clip = VideoFileClip(r'D:\soham_code\video_py\video_py\test\chaplin.mp4')
    clip.write_videofile(r'D:\soham_code\video_py\video_py\test\test_clip.mp4', audio=True)