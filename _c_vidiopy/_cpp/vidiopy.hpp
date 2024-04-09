#pragma once

#ifdef _WIN32
#define SHARED_EXPORT_API __declspec(dllexport)
#else
#define SHARED_EXPORT_API
#endif

#include <vector>
#include <functional>
#include <string>

class Clip
{
public:
    double start;
    double end;
    double duration;
    double fps;
    std::string name;
    void setTimeTransforms(std::function<double(double)> func);

private:
    std::vector<std::function<double(double)>> timeTransforms;
};

class AudioClip : public Clip
{
};

class VideoClip : public Clip
{
private:
    struct PositionBundle
    {
        char xChar;
        int xInt;
        double xDouble;

        char yChar;
        int yInt;
        double yDouble;
    };

public:
    int size[2];
    AudioClip *audio;
    bool relativePos;

    void setAudio(AudioClip *audio);
    void withoutAudio();
    VideoClip *copy();
    PositionBundle getPosition(double time);
    virtual VideoClip subClip(double tStart, double tEnd);
    virtual VideoClip subClipCopy(double tStart, double tEnd);
    void syncAudioVideoSED();
    void writeVideoFile();
    void writeVideoFileSubclip();
    void writeImageSequence();
    void saveFrame();
};
