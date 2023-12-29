from src.video.VideoClips import VideoFileClip

video = VideoFileClip('media/test_video.mp4')

print(f'size: {video.size}')
print(f'duration: {video.duration}')