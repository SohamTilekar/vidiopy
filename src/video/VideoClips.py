import time
from typing import (Any, Callable, Self, Generator,
                    )
from copy import copy as _copy
import imageio as iio
import ffmpegio
# from src.audio.AudioClip import AudioClip
# from src.Clip import Clip
import numpy as np
import functools
import subprocess


class Clip:...
class AudioClip(Clip):...

class VideoClip(Clip):
    def __init__(self, clip:np.ndarray | None = None, start: float = 0.0, end: float | None = None, duration: float | None = None) -> None:
        super().__init__()
        self.start: float = start
        self.end: float | None = end
        self.duration: float | None = duration
        self.audio: AudioClip | None = None
        self.is_audio = False
        self.relative_pos: bool = False
        self.pos = lambda t: (0, 0)
        self.clip: np.ndarray | None = clip
        self.size: tuple[int, int] = (0, 0)
        self.fps: float | int = 0

    def width(self):
        return self.size[0]

    def height(self):
        return self.size[1]

    def aspect_ratio(self):
        return self.width() / self.height()

    def set_size(self, wh: tuple[int, int] | None = None, w: int | None = None, h: int | None = None):
        if wh != None:
            self.size = wh
        elif w != None:
            self.size = (w, self.size[0])
        elif h!= None:
            self.size = (self.size[0], h)

    def set_pos(self, pos: tuple[int, int] | Callable):
        if callable(pos):
            self.pos = lambda t: pos
        else:
            self.pos = pos
        return self
    
    def n_frames(self):
        if self.duration is not None and self.fps:
            return int(self.duration * self.fps)
        raise ValueError('FPS & Duration is Missing')

    def get_fps(self):
        if self.fps != 0 or None:
            return self.fps
        else:
            raise ValueError('FPS is Not Set')

    def set_make_frame(self, make_frame: Callable[[int, bool], np.ndarray]):
        self.make_frame = make_frame

    def set_start(self, t, change_end=True) -> Self:
        self.start = t
        if (self.duration is not None) and change_end:
            self.end = t + self.duration
        elif self.end is not None:
            self.duration = self.end - self.start
        return self

    def set_end(self, t) -> Self:
        self.end = t

        if self.start is not None:
            self.duration = self.end - self.start
        return self
    
    def set_duration(self, t, change_end=True) -> Self:
        self.duration = t

        if change_end:
            self.end = None if (t is None) else (self.start + t)
        else:
            if self.duration is None:
                raise Exception("Cannot change clip start when new"
                                "duration is None")
            self.start = self.end - t
        return self
    
    def set_fps(self, fps) -> Self:
        self.fps = fps
        return self

    def set_clip(self, clip: np.ndarray) -> Self:
        self.clip = clip
        return self

    def set_audio(self, audio: AudioClip):
        self.audio = audio
        self.is_audio = True
        return self

    def __copy__(self) -> Self:
        cls = self.__class__  # Get the class of the current instance
        new_clip = cls.__new__(cls)  # Create a new instance of the class

        # Iterate over each attribute in the current instance's dictionary
        for attr in self.__dict__:
            value = getattr(self, attr)  # Get the value of the attribute

            # If the attribute is "mask" or "audio," create a shallow copy
            if attr in ("audio"):
                value = _copy.copy(value)

            # Set the attribute in the new instance with the copied or original value
            setattr(new_clip, attr, value)

        return new_clip  # Return the new instance

    copy = __copy__

    def save_frame(
        self,
        filename: str,
        t: float = 0,
    ) -> None:
        if hasattr(self, 'get_frame'):
            im: np.ndarray = self.get_frame(t)  # type: ignore
        else:
            raise AttributeError("Object does not have 'get_frame' attribute.")

        iio.imwrite(filename, im)

    def get_frame(self, t, is_time=True):
            return self.make_frame(t, is_time)

    def iter_frames(self) -> Generator[np.ndarray[Any, Any], Any, None]:
        if self.clip is not None:
            for t in range(len(self.clip)):
                yield self.get_frame(t, False)
        else:
            raise AttributeError("Object does not have 'clip' attribute.")

    def iter_frames_t(self, fps: float = 0.0):
        if self.clip is not None:
            if isinstance(self.duration, (int, float)) and self.duration > 0:
                x = 1 / (self.get_fps() if fps == 0.0 else fps)
                t = 0
                while t < self.duration:
                    yield self.get_frame(t, True)
                    t += x
            else:
                raise ValueError(f"Invalid duration value, {self.duration}, {type(self.duration)}")
        else:
            raise AttributeError("Object does not have 'clip' attribute.")


    def write_video_file(self, filename, fps=None, codec=None,
                        bitrate=None, audio=True, audio_fps=44100,
                        preset="medium", pixel_format=None,
                        audio_codec=None, audio_bitrate=None,
                        write_logfile=False, verbose=True,
                        threads=None, ffmpeg_params: dict[str, str] | None = None,
                        logger='bar', over_write_output=True):

        final_fps = fps if fps is not None else self.fps if self.fps else 24

        ffmped_options = {
            **(ffmpeg_params if ffmpeg_params else {})
        }
        if threads:
            ffmped_options['threads'] = threads
        if codec:
            ffmped_options['vcodec'] = codec
        if bitrate:
            ffmped_options['b:v'] = bitrate
        if preset:
            ffmped_options['preset'] = preset
        if pixel_format:
            ffmped_options['pix_fmt'] = pixel_format
        
        ffmpegio.video.write(filename, final_fps, self.clip, overwrite=over_write_output, show_log=True, )

class VideoFileClip(VideoClip):
    def __init__(self, filename: str, transparent=True, pix_fmt_in=None, audio: bool = False, target_resolution: tuple[int, int] | None = None, preset='medium'):
        super().__init__()
        video_basic_data = ffmpegio.probe.video_streams_basic(filename)[0]
        ffmpeg_options = {
            'pix_fmt': 'rgba' if transparent else 'rgb24',
            'preset': preset,
        }
        if pix_fmt_in is not None:
            ffmpeg_options['pix_fmt'] = pix_fmt_in
        if target_resolution is not None:
            ffmpeg_options['vf'] = f'scale={target_resolution[0]}:{target_resolution[1]}'

        frame_rate, video_frame_data = ffmpegio.video.read(filename, show_log=True, **ffmpeg_options)
        self.clip = video_frame_data
        self.set_start(0.0)
        self.set_duration(video_basic_data['duration'])
        self.set_size(wh=(video_basic_data['width'], video_basic_data['height']))
        self.set_make_frame(self.vid_make_frame)
        self.set_fps(frame_rate)

    def vid_make_frame(self, t, is_time=True) -> np.ndarray:
        if is_time:
            frame_num = round(t * self.fps)-1
        else:
            frame_num = int(t)
        
        if self.clip is not None:
            return self.clip[frame_num]
        else:
            raise AttributeError("Object does not have 'clip' attribute.")

if __name__ == '__main__':
    clip = VideoFileClip(r'D:\soham_code\video_py\video_py\test\sintel_with_14_chapters.mp4', transparent=False)
    st = time.perf_counter()
    clip.write_video_file(r'D:\soham_code\video_py\video_py\test\test_sintel_with_14_chapters.mp4', fps=25)
    ed = time.perf_counter()
    print(f"Time taken: {ed-st}")