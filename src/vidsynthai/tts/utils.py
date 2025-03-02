import os
import subprocess


def merge_audio_with_video(video_path: str, audio_path: str, output_path: str):
    """Merges the generated audio with the generated video"""

    command = [
        "ffmpeg", "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac",
        "-map", "0:v:0", "-map", "1:a:0",
        output_path
    ]


    # command = ["ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_path] if audio_path.endswith(".mp3") else ["ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "-ar", "44100", output_path]
    # command = ["ffmpeg", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_path]
    print(command)
    subprocess.run(command, check=True)
    return output_path


if __name__ == "__main__":
    video_path = r"media_output\videos\animation_v7\1080p60\output.mp4"
    audio_path = r"media_output\videos\animation_v7\1080p60\merged_audio.wav"
    output_path = r"media_output\videos\animation_v7\1080p60\final_merged_video2.mp4"
    merge_audio_with_video(video_path, audio_path, output_path)

