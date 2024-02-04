import sys

if __name__ == "__main__":
    if "--install_ffmpeg" in sys.argv:
        from vidiopy.config import *

        print("Installing ffmpeg...")
        x = install_ffmpeg()
        print(f"ffmpeg installed successfully! at {x[0]} and {x[1]}")
    else:
        from vidiopy.__init__ import *
