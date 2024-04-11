#include "vidiopy.hpp"

VideoClip::VideoClip()
{
    size[0] = -1;
    size[1] = -1;
    audio = nullptr;
    relativePos = false;
}

void VideoClip::setAudio(AudioClip *audio)
{
    this->audio = audio;
}

void VideoClip::withoutAudio()
{
    this->audio = nullptr;
}

VideoClip *VideoClip::copy()
{
    VideoClip *newClip = new VideoClip();
    newClip->start = start;
    newClip->end = end;
    newClip->duration = duration;
    newClip->fps = fps;
    newClip->name = name;
    newClip->size[0] = size[0];
    newClip->size[1] = size[1];
    newClip->audio = audio;
    newClip->relativePos = relativePos;
    return newClip;
}

VideoClip *VideoClip::subClip(double tStart, double tEnd)
{
    return nullptr;
};

VideoClip *VideoClip::subClipCopy(double tStart, double tEnd)
{
    VideoClip *clip = copy();
    return clip->subClip(tStart, tEnd);
};

uint8_t ***VideoClip::getFrame(double time)
{
    return nullptr;
};

uint8_t *VideoClip::getFrameFlattened(double time)
{
    return nullptr;
};

void VideoClip::syncAudioVideoSED(){};

void VideoClip::setPos(int x, int y)
{
    relativePos = false;
    PositionBundle pos;
    pos.xInt = x;
    pos.yInt = y;
    this->Pos = [pos](double time)
    { return pos; };
};

void VideoClip::setPos(double x, double y)
{
    relativePos = true;
    PositionBundle pos;
    pos.xDouble = x;
    pos.yDouble = y;
    this->Pos = [pos](double time)
    { return pos; };
};

void VideoClip::setPos(char x, char y)
{
    relativePos = false;
    PositionBundle pos;
    pos.xChar = x;
    pos.yChar = y;
    this->Pos = [pos](double time)
    { return pos; };
};

void VideoClip::setPos(int x, char y)
{
    relativePos = false;
    PositionBundle pos;
    pos.xInt = x;
    pos.yChar = y;
    this->Pos = [pos](double time)
    { return pos; };
};

void VideoClip::setPos(char x, int y)
{
    relativePos = false;
    PositionBundle pos;
    pos.xChar = x;
    pos.yInt = y;
    this->Pos = [pos](double time)
    { return pos; };
};

void VideoClip::setPos(double x, char y)
{
    relativePos = true;
    PositionBundle pos;
    pos.xDouble = x;
    pos.yChar = y;
    this->Pos = [pos](double time)
    { return pos; };
};

void VideoClip::setPos(char x, double y)
{
    relativePos = true;
    PositionBundle pos;
    pos.xChar = x;
    pos.yDouble = y;
};

void VideoClip::setPos(std::function<PositionBundle(double)> func, bool relative = false)
{
    this->relativePos = relative;
    this->Pos = func;
};

extern "C"
{
    SHARED_EXPORT_API VideoClip *VideoClip_new()
    {
        return new VideoClip();
    }

    SHARED_EXPORT_API void VideoClip_setAudio(VideoClip *clip, AudioClip *audio)
    {
        clip->setAudio(audio);
    }

    SHARED_EXPORT_API void VideoClip_withoutAudio(VideoClip *clip)
    {
        clip->withoutAudio();
    }

    SHARED_EXPORT_API VideoClip *VideoClip_copy(VideoClip *clip)
    {
        return clip->copy();
    }

    SHARED_EXPORT_API VideoClip *VideoClip_subClip(VideoClip *clip, double tStart, double tEnd)
    {
        return clip->subClip(tStart, tEnd);
    }

    SHARED_EXPORT_API VideoClip *VideoClip_subClipCopy(VideoClip *clip, double tStart, double tEnd)
    {
        return clip->subClipCopy(tStart, tEnd);
    }

    SHARED_EXPORT_API uint8_t ***VideoClip_getFrame(VideoClip *clip, double time)
    {
        return clip->getFrame(time);
    }

    SHARED_EXPORT_API uint8_t *VideoClip_getFrameFlattened(VideoClip *clip, double time)
    {
        return clip->getFrameFlattened(time);
    }

    SHARED_EXPORT_API void VideoClip_syncAudioVideoSED(VideoClip *clip)
    {
        clip->syncAudioVideoSED();
    }
};
