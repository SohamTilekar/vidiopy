#include "vidiopy.hpp"

class Clip
{
public:
    double start;
    double end;
    double duration;
    double fps;
    std::string name;
    void setTimeTransforms(std::function<PositionBundle(double)> func)
    {
        timeTransforms.push_back(func);
    };

private:
    std::vector<std::function<PositionBundle(double)>> timeTransforms;
};
