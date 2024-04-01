#pragma once

#ifdef _WIN32
#define SHARED_EXPORT_API __declspec(dllexport)
#else
#define SHARED_EXPORT_API
#endif

#include <functional>
#include <vector>

class Clip
{
public:
    double start;
    double end;
    double duration;
    double fps;
    char *name;
    std::vector<std::function<double(double)>> time_transforms;
};

class AudioClip : public Clip
{
};

class VideoClip : public Clip
{
};
