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
        self.bitrate = 44100
        self.channels = None
        self.sample_rate = None
        self.start: Num = 0.0
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
        self.start = int(audio_basic_data['start_time'])
        self.duration = int(audio_basic_data['duration'])
        self.end = self.duration
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
    def __init__(self, audios: list[AudioClip], use_bgclip=False, bitrate=44100) -> None:
        super().__init__()
        self.clip, bitrate = self._concat_clips(audios, use_bgclip, bitrate=bitrate)
        self.bitrate = bitrate
    def _max_bitrate(self, clips: list[AudioClip]):
        bitrate = 0
        if not bitrate:
            for clip in clips:
                bitrate = max(bitrate, clip.bitrate)
        self.bitrate = bitrate

    def _concat_clips(self, clips: list[AudioClip], use_bgclip, bitrate: int):
        if use_bgclip:
            self.bg_clip = clips[0]
            self.bitrate = self.bg_clip.bitrate
        else:
            self._max_bitrate(clips)
            dur = 0
            for clip in clips:
                if clip.duration:
                    dur = max(dur, clip.duration)
            clip = AudioClip()
            clip.clip = AudioSegment.silent(int(dur*1000), frame_rate=self.bitrate)
            self.bg_clip = clip
        bg_clip = self.bg_clip
        if bg_clip.clip:
            bg_clip.clip
        else:
                raise
        
        for clip in clips:
            bg_clip.clip = bg_clip.clip.overlay(clip.clip, 
                                 int(clip.start * (bg_clip.clip.frame_rate / bg_clip.clip.duration_seconds)))
        clip = AudioClip()
        clip.clip = bg_clip.clip
        clip.clip = clip.clip.set_frame_rate(bitrate)
        return clip.clip, bitrate

if __name__ == '__main__':
    SystemExit()