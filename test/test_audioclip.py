# import pytest
# import numpy as np
# from vidiopy import AudioClip


# def test_audio_clip_init():
#     clip = AudioClip()
#     assert clip.fps is None
#     assert clip._original_dur is None
#     assert clip._audio_data is None
#     assert clip.channels is None
#     assert clip._st == 0.0
#     assert clip._ed is None

#     clip = AudioClip(5, 44100)
#     assert clip.fps == 44100
#     assert clip._original_dur == 5.0
#     assert clip._audio_data is None
#     assert clip.channels is None
#     assert clip._st == 0.0
#     assert clip._ed == 5.0


# def test_audio_clip_audio_data():
#     clip = AudioClip()
#     with pytest.raises(ValueError):
#         _ = clip.audio_data

#     clip.audio_data = np.array([1, 2, 3])
#     assert np.array_equal(clip.audio_data, np.array([1, 2, 3]))


# def test_audio_clip_set_data():
#     clip = AudioClip()
#     clip.set_data(np.array([1, 2, 3]))
#     assert np.array_equal(clip._audio_data, np.array([1, 2, 3]))


# def test_audio_clip_duration():
#     clip = AudioClip(5, 44100)
#     assert clip.duration == 5.0

#     with pytest.raises(AttributeError):
#         clip.duration = 10


# def test_audio_clip_start():
#     clip = AudioClip()
#     assert clip.start == 0.0

#     clip.start = 1.0
#     assert clip.start == 1.0


# def test_audio_clip_end():
#     clip = AudioClip(5, 44100)
#     assert clip.end == 5.0

#     clip.end = 10.0
#     assert clip.end == 10.0


# def test_audio_clip_get_frame_at_t():
#     clip = AudioClip(5, 44100)
#     clip.set_data(np.array([1, 2, 3, 4, 5]))

#     with pytest.raises(ValueError):
#         _ = clip.get_frame_at_t(6)

#     clip = AudioClip(5, 44100)
#     clip.set_data(np.array([1, 2, 3, 4, 5]))
#     assert clip.get_frame_at_t(1) == 1


# def test_audio_clip_iterate_frames_at_fps():
#     clip = AudioClip(5, 44100)
#     clip.set_data(np.array([1, 2, 3, 4, 5]))

#     with pytest.raises(ValueError):
#         _ = list(clip.iterate_frames_at_fps())

#     clip = AudioClip(5, 44100)
#     clip.set_data(np.array([1, 2, 3, 4, 5]))
#     assert list(clip.iterate_frames_at_fps(44100)) == [1, 2, 3, 4, 5]


# def test_audio_clip_iterate_all_frames():
#     clip = AudioClip()
#     clip.set_data(np.array([1, 2, 3, 4, 5]))
#     assert list(clip.iterate_all_frames()) == [1, 2, 3, 4, 5]


# def test_audio_clip_fl_frame_transform():
#     clip = AudioClip()
#     clip.set_data(np.array([1, 2, 3, 4, 5]))
#     clip.fl_frame_transform(lambda x: x * 2)
#     assert np.array_equal(clip._audio_data, np.array([2, 4, 6, 8, 10]))
