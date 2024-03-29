#pragma once

#ifdef _WIN32
#define SHARED_EXPORT_API __declspec(dllexport)
#else
#define SHARED_EXPORT_API
#endif

class Clip
{
public:
    double start = 0.0;
    double end = -1.0;
    double duration = -1.0;
    double fps = -1.0;

    Clip(double start, double end, double duration, double fps);
    void setStart(double start);
    void setEnd(double end);
    void setDuration(double duration);
    void setFps(double fps);
    double getStart();
    double getEnd();
    double getDuration();
    double getFps();
};
