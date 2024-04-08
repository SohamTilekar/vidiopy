#pragma once

#ifdef _WIN32
#define SHARED_EXPORT_API __declspec(dllexport)
#else
#define SHARED_EXPORT_API
#endif

#include <vector>
#include <functional>
#include <string>

typedef struct PositionBundle
{
    char xChar;
    int xInt;
    double xDouble;

    char yChar;
    int yInt;
    double yDouble;
};

class Clip
{
public:
    double start;
    double end;
    double duration;
    double fps;
    std::string name;
    void setTimeTransforms(std::function<PositionBundle(double)> func);

private:
    std::vector<std::function<PositionBundle(double)>> timeTransforms;
};

class AudioClip : public Clip
{
};

class VideoClip : public Clip
{
};
