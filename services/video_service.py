import subprocess


def replace_video_audio(
    input_video,
    input_audio,
    output_video
):

    command = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-i", input_audio,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_video
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:

        raise Exception(
            result.stderr
        )

    return output_video


def burn_ass_subtitles(
    input_video,
    subtitle_file,
    output_video
):

    command = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vf",
        f"ass={subtitle_file}",
        "-c:a",
        "copy",
        output_video
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:

        raise Exception(
            result.stderr
        )

    return output_video