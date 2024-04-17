#include "vidiopy.hpp"

void Clip::setTimeTransforms(std::function<double(double)> func)
{
    timeTransforms.push_back(func);
};

uint8_t ***Clip::iterFrame(double fps)
{
    return getFrame(fps);
};

uint8_t *Clip::iterFrameFlattened(double fps)
{
    return getFrameFlattened(fps);
};

uint8_t ***Clip::getFrame(double time) { return nullptr; };
uint8_t *Clip::getFrameFlattened(double time) { return nullptr; };
void Clip::frameTransform(std::function<uint8_t ***(uint8_t ***data)> func){};
void Clip::clipTransform(std::function<uint8_t ***(uint8_t ***data, double time)> func){};

extern "C"
{
    SHARED_EXPORT_API Clip *Clip_new()
    {
        return new Clip();
    }

    SHARED_EXPORT_API void Clip_setStart(Clip *clip, double start)
    {
        clip->start = start;
    }

    SHARED_EXPORT_API double Clip_getStart(Clip *clip)
    {
        return clip->start;
    }

    SHARED_EXPORT_API void Clip_setEnd(Clip *clip, double end)
    {
        clip->end = end;
    }

    SHARED_EXPORT_API double Clip_getEnd(Clip *clip)
    {
        return clip->end;
    }

    SHARED_EXPORT_API void Clip_setDuration(Clip *clip, double duration)
    {
        clip->duration = duration;
    }

    SHARED_EXPORT_API double Clip_getDuration(Clip *clip)
    {
        return clip->duration;
    }

    SHARED_EXPORT_API void Clip_setFps(Clip *clip, double fps)
    {
        clip->fps = fps;
    }

    SHARED_EXPORT_API double Clip_getFps(Clip *clip)
    {
        return clip->fps;
    }

    SHARED_EXPORT_API void Clip_setName(Clip *clip, char name[])
    {
        clip->name = name;
    }

    SHARED_EXPORT_API std::string Clip_getName(Clip *clip)
    {
        return clip->name;
    }

    SHARED_EXPORT_API void Clip_setTimeTransforms(Clip *clip, std::function<double(double)> func)
    {
        clip->setTimeTransforms(func);
    }
    SHARED_EXPORT_API uint8_t ***Clip_getFrame(Clip *clip, double time)
    {
        return clip->getFrame(time);
    }

    SHARED_EXPORT_API uint8_t *Clip_getFrameFlattened(Clip *clip, double time)
    {
        return clip->getFrameFlattened(time);
    }

    SHARED_EXPORT_API void Clip_frameTransform(Clip *clip, std::function<uint8_t ***(uint8_t ***data)> func)
    {
        clip->frameTransform(func);
    }

    SHARED_EXPORT_API void Clip_clipTransform(Clip *clip, std::function<uint8_t ***(uint8_t ***data, double time)> func)
    {
        clip->clipTransform(func);
    }
}
