import os
import subprocess


def compile_manim(file_name="animation.py", output_dir="media_output"):
    """Compile the Manim script into a video."""
    command = ["manim", file_name, "-o", "output.mp4", "--media_dir", output_dir]
    subprocess.run(command, check=True)
    return output_dir


def get_video_duration(video_path):
    """Get the duration of the generated video using ffprobe."""
    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip()) if result.stdout else None


# if __name__ == "__main__":
    # compile_manim("experiments/animation_v3.py", "media/videos")
