import ffmpegio
from rich import print
import rich.progress as progress
from pydub import AudioSegment
from ..Clip import Clip

Num = int | float
NumOrNone = None | Num

class AudioClip(Clip):
    def __init__(self) -> None:
        super().__init__()
        self.clip: AudioSegment | None = None
        self.bitrate = None
        self.channels = None
        self.sample_rate = None
        self.start = 0.0
        self.end: NumOrNone = None
        self.duration: NumOrNone = None

    def get_duration(self):
        return self.clip.duration_seconds if isinstance(self.clip, AudioSegment) else None
    def write_audio_file(self, output_file_name, bitrate=None, codec=None, ffmpeg_additional_options=None):
        with progress.Progress(transient=True) as progress_bar:
            task = progress_bar.add_task('Writing Audio ... :smiley:', total=None)
            self.clip.export(output_file_name, 
                            bitrate=(bitrate if bitrate else None), 
                            codec=(codec if codec else None), 
                            parameters=ffmpeg_additional_options,
                            ) if self.clip is not None else (_ for _ in ()).throw(Exception('Make Frame is Not Set.'))
            progress_bar.update(task, completed=True)
        print('[bold magenta]Vidiopy[/bold magenta] - Audio File has Been Written:thumbs_up:.')

class AudioFileClip(AudioClip):
    """Makes Audio CLip From any Media"""
    def __init__(self, filename: str) -> None:
        super().__init__()
        audio_basic_data = ffmpegio.probe.audio_streams_basic(filename)[0]
        self.bitrate = audio_basic_data['bit_rate']
        self.channels = audio_basic_data['channels']
        self.sample_rate = audio_basic_data['sample_rate']
        self.clip: AudioSegment = self._import_audio(filename)
    ...
    def _import_audio(self, filename, bitrate=None, sample_rate = None, *ffmpeg_additional_options) -> AudioSegment:
        
        return AudioSegment.from_file(filename, parameters=[
                                                            # *((f'-ar {sample_rate}',)if sample_rate else ()),
                                                            # *((f'-b:a {bitrate}',) if bitrate else ()),
                                                            *ffmpeg_additional_options])

class CompositeAudioClip(AudioClip):
    def __init__(self, audios: list[AudioClip]) -> None:
        super().__init__()
        self.clip = self._concat_clips(audios)
    
    def _concat_clips(self, clips):
        final_clip = AudioSegment.empty()
        for clip in clips:
            if isinstance(clip, AudioClip):
                if clip.clip is not None:
                    final_clip += clip.clip
                else:
                    print('Warning: The Clip is Not Set')
            else:
                raise TypeError()
        return final_clip


def audio_segment2composite_audio_clip(audios: list[AudioSegment]):
    final_clip = AudioSegment.empty()
    for audio in audios:
        final_clip+=audio
    audio = AudioClip()
    audio.clip = final_clip
    return audio

if __name__ == '__main__':
    SystemExit()