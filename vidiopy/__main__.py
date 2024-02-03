import sys

if __name__ == "__main__":
    if "--install_ffmpeg" in sys.argv:
        from vidiopy.config import *

        print("Installing ffmpeg...")
        install_ffmpeg()
        print("ffmpeg installed successfully!")
    else:
        from vidiopy.__init__ import *
