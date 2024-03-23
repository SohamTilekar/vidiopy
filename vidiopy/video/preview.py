from vidiopy.video.VideoClip import VideoClip


def preview(video: VideoClip, fps: int | float | None) -> None:
    import pygame

    """Preview the video using pygame."""
    fps = fps or (video.fps or 16)
    pygame.init()
    screen = pygame.display.set_mode(video.size)
    clock = pygame.time.Clock()
    for frame in video.iterate_frames_array_t(fps=fps):
        for event in pygame.event.get():  # Add this line
            if event.type == pygame.QUIT:  # And this line
                pygame.quit()  # And this line
                return  # And this line
        frame = pygame.pixelcopy.make_surface(
            (
                frame[:, :, :-1].swapaxes(0, 1)
                if frame.shape[2] == 4
                else frame.swapaxes(0, 1)
            )
        )
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
