from typing import Any, Self
import numpy as np
import ffmpegio
from pydub import AudioSegment
# from ..Clip import Clip

class Clip:...

type Num = int | float
type NumOrNone = None | Num

class AudioClip(Clip):
    def __init__(self) -> None:
        super().__init__()
        self.clip: np.ndarray | None | AudioSegment = None
        self.duration: NumOrNone = None
        self.bitrate = None
        self.channels = None
        self.channel_layout = None
        self.codec_name = None
        self.sample_rate = None

    def _array2audio_segent(self) -> AudioSegment:
        if isinstance(self.clip, np.ndarray):
            audio = AudioSegment(self.clip.tobytes(), frame_rate=self.sample_rate, 
                                sample_width=self.clip.dtype.itemsize, channels=self.channels)
            self.clip = audio
            return audio
        elif isinstance(self.clip, AudioSegment):
            return self.clip
        elif self.clip is None:
            raise ValueError("Clip is Not Set")
        else:
            raise TypeError("Clip must be a numpy array or a pydub.AudioSegment")
        
    def _audio_segment2array(self) -> np.ndarray[Any, Any]:
        if isinstance(self.clip, AudioSegment):
            audio = np.ndarray(self.clip.get_array_of_samples())
            self.clip = audio
            return audio
        elif isinstance(self.clip, np.ndarray):
            return self.clip
        elif self.clip is None:
            raise ValueError("Clip is Not Set")
        else:
            raise TypeError("Clip must be a numpy array or a pydub.AudioSegment")


    def write_audio_file(self, output_file_name, bitrate=None, channels=1, codec=None, sample_rate=44100, ffmpeg_aditional_options=None):
        
        self._audio_segment2array()

        ffmpeg_options = {
            **(ffmpeg_aditional_options if ffmpeg_aditional_options else {}),
            **({'b:a': bitrate} if bitrate else {}),
            'ac': self.channels if self.channels else channels,
            **({'c:a': codec} if codec else {}),
            # **({'': ''} if _ else {})
        }

        ffmpegio.audio.write(output_file_name, sample_rate if sample_rate else self.sample_rate, self.clip, overwrite=True,**ffmpeg_options)

class AudioFileClip(AudioClip):
    def __init__(self, filename: str) -> None:
        super().__init__()
        audio_basic_data = ffmpegio.probe.audio_streams_basic(filename)[0]
        self.duration: NumOrNone = float(audio_basic_data['duration'])
        self.bitrate = audio_basic_data['bit_rate']
        self.channels = audio_basic_data['channels']
        self.sample_rate = audio_basic_data['sample_rate']
        self.clip: np.ndarray | None = self._import_audio(filename)
    ...
    def _import_audio(self, filename, bitrate=None, channels=None, sample_rate = None, **ffmpeg_aditional_options) -> np.ndarray:
        options = {
            **(ffmpeg_aditional_options if ffmpeg_aditional_options else {}),
            **({'b:a': bitrate} if bitrate else {}),
            **({'a:c': channels} if channels else {}),
            **({'ar': sample_rate} if sample_rate else {})
        }
        if self.channels:
            self.channels
        elif self.bitrate:
            self.bitrate
        elif self.sample_rate:
            self.sample_rate

        data = ffmpegio.audio.read(filename, **options)
        return data[1]

if __name__ == '__main__':
    audio = AudioFileClip(r'D:\soham_code\video_py\video_py\test\crunching.mp3')
    audio.write_audio_file(r'D:\soham_code\video_py\video_py\test\test.wav')