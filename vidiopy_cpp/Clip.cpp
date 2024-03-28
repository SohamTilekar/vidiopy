#ifdef _WIN32
#define SHARED_EXPORT_API __declspec(dllexport)
#else
#define SHARED_EXPORT_API
#endif

#pragma region Clip

class Clip
{
public:
	double start;
	double end;
	double duration;
	double fps;

	Clip(double start, double end, double duration, double fps)
	{
		this->start = start;
		this->end = end;
		this->duration = duration;
		this->fps = fps;
	};

	void setStart(double start)
	{
		this->start = start;
	};

	void setEnd(double end)
	{
		this->end = end;
	};

	void setDuration(double duration)
	{
		this->duration = duration;
	};

	void setFps(double fps)
	{
		this->fps = fps;
	};

	double getStart()
	{
		return this->start;
	};

	double getEnd()
	{
		return this->end;
	};

	double getDuration()
	{
		return this->duration;
	};

	double getFps()
	{
		return this->fps;
	};
};

extern "C"
{
	SHARED_EXPORT_API Clip *_Clip_new(double start, double end, double duration, double fps)
	{
		return new Clip(start, end, duration, fps);
	}

	SHARED_EXPORT_API void _Clip_setStart(Clip *clip, double start)
	{
		clip->setStart(start);
	}

	SHARED_EXPORT_API void _Clip_setEnd(Clip *clip, double end)
	{
		clip->setEnd(end);
	}

	SHARED_EXPORT_API void _Clip_setDuration(Clip *clip, double duration)
	{
		clip->setDuration(duration);
	}

	SHARED_EXPORT_API void _Clip_setFps(Clip *clip, double fps)
	{
		clip->setFps(fps);
	}

	SHARED_EXPORT_API double _Clip_getStart(Clip *clip)
	{
		return clip->getStart();
	}

	SHARED_EXPORT_API double _Clip_getEnd(Clip *clip)
	{
		return clip->getEnd();
	}

	SHARED_EXPORT_API double _Clip_getDuration(Clip *clip)
	{
		return clip->getDuration();
	}

	SHARED_EXPORT_API double _Clip_getFps(Clip *clip)
	{
		return clip->getFps();
	}
}

#pragma endregion
