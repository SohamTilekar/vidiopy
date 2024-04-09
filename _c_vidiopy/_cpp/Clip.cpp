#include "vidiopy.hpp"

class Clip
{
public:
    double start;
    double end;
    double duration;
    double fps;
    std::string name;
    void setTimeTransforms(std::function<double(double)> func)
    {
        timeTransforms.push_back(func);
    };

private:
    std::vector<std::function<double(double)>> timeTransforms;
};

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
}