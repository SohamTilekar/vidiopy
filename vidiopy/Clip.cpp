#include "vidiopy.h"

#pragma region Clip

#pragma region Methods

/**
 * @brief Constructs a new Clip object.
 *
 * @param start The start time of the clip. Default value is 0.0.
 * @param end The end time of the clip. Default value is -1.0.
 * @param duration The duration of the clip. Default value is -1.0.
 * @param fps The frames per second (fps) of the clip. Default value is -1.0.
 */
Clip::Clip(double start = 0.0, double end = -1.0, double duration = -1.0, double fps = -1.0)
{
	this->start = start;
	this->end = end;
	this->duration = duration;
	this->fps = fps;
};

/**
 * @brief Sets the start time of the clip.
 *
 * @param start The start time to set.
 */
void Clip::setStart(double start)
{
	this->start = start;
};

/**
 * @brief Sets the end time of the clip.
 *
 * @param end The end time to set.
 */
void Clip::setEnd(double end)
{
	this->end = end;
};

/**
 * @brief Sets the duration of the clip.
 *
 * @param duration The duration to set.
 */
void Clip::setDuration(double duration)
{
	this->duration = duration;
};

/**
 * @brief Sets the frames per second (fps) of the clip.
 *
 * @param fps The frames per second (fps) to set.
 */
void Clip::setFps(double fps)
{
	this->fps = fps;
};

/**
 * @brief Gets the start time of the clip.
 *
 * @return The start time of the clip.
 */
double Clip::getStart()
{
	return this->start;
};

/**
 * @brief Gets the end time of the clip.
 *
 * @return The end time of the clip.
 */
double Clip::getEnd()
{
	return this->end;
};

/**
 * @brief Gets the duration of the clip.
 *
 * @return The duration of the clip.
 */
double Clip::getDuration()
{
	return this->duration;
};

/**
 * @brief Gets the frames per second (fps) of the clip.
 *
 * @return The frames per second (fps) of the clip.
 */
double Clip::getFps()
{
	return this->fps;
};

#pragma endregion

#pragma region Extern "C"
extern "C"
{
	/**
	 * @brief Creates a new Clip object with the specified start, end, duration, and fps.
	 *
	 * @param start The start time of the clip.
	 * @param end The end time of the clip.
	 * @param duration The duration of the clip.
	 * @param fps The frames per second of the clip.
	 * @return A pointer to the newly created Clip object.
	 */
	SHARED_EXPORT_API Clip *_Clip_new(double start, double end, double duration, double fps)
	{
		return new Clip(start, end, duration, fps);
	}

	/**
	 * @brief Sets the start time of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @param start The new start time of the clip.
	 */
	SHARED_EXPORT_API void _Clip_setStart(Clip *clip, double start)
	{
		clip->setStart(start);
	}

	/**
	 * @brief Sets the end time of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @param end The new end time of the clip.
	 */
	SHARED_EXPORT_API void _Clip_setEnd(Clip *clip, double end)
	{
		clip->setEnd(end);
	}

	/**
	 * @brief Sets the duration of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @param duration The new duration of the clip.
	 */
	SHARED_EXPORT_API void _Clip_setDuration(Clip *clip, double duration)
	{
		clip->setDuration(duration);
	}

	/**
	 * @brief Sets the frames per second of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @param fps The new frames per second of the clip.
	 */
	SHARED_EXPORT_API void _Clip_setFps(Clip *clip, double fps)
	{
		clip->setFps(fps);
	}

	/**
	 * @brief Gets the start time of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @return The start time of the clip.
	 */
	SHARED_EXPORT_API double _Clip_getStart(Clip *clip)
	{
		return clip->getStart();
	}

	/**
	 * @brief Gets the end time of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @return The end time of the clip.
	 */
	SHARED_EXPORT_API double _Clip_getEnd(Clip *clip)
	{
		return clip->getEnd();
	}

	/**
	 * @brief Gets the duration of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @return The duration of the clip.
	 */
	SHARED_EXPORT_API double _Clip_getDuration(Clip *clip)
	{
		return clip->getDuration();
	}

	/**
	 * @brief Gets the frames per second of the specified clip.
	 *
	 * @param clip A pointer to the Clip object.
	 * @return The frames per second of the clip.
	 */
	SHARED_EXPORT_API double _Clip_getFps(Clip *clip)
	{
		return clip->getFps();
	}
};
#pragma endregion

#pragma endregion
