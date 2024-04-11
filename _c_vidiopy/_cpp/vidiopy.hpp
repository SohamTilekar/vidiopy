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
        char xChar = '\0';
        int xInt = 0;
        double xDouble = 0.0;

        char yChar = '\0';
        int yInt = 0;
        double yDouble = 0.0;
    };

public:
    int size[2];
    AudioClip *audio;
    bool relativePos;
    std::function<PositionBundle(double)> Pos;

    void setAudio(AudioClip *audio);
    void withoutAudio();
    VideoClip *copy();
    virtual VideoClip *subClip(double tStart, double tEnd);
    virtual VideoClip *subClipCopy(double tStart, double tEnd);
    virtual uint8_t ***getFrame(double time);
    virtual uint8_t *getFrameFlattened(double time);
    void syncAudioVideoSED();
    void setPos(int x, int y);
    void setPos(double x, double y);
    void setPos(char x, char y);
    void setPos(int x, char y);
    void setPos(char x, int y);
    void setPos(double x, char y);
    void setPos(char x, double y);
    void setPos(std::function<PositionBundle(double)> func, bool relative = false);
    void writeVideoFile();
    void writeVideoFileSubclip();
    void writeImageSequence();
    void saveFrame();
};
