from gtts import gTTS

import subprocess

import tempfile

import os


def generate_tts(
    text,
    language,
    output_path,
    speed=1.0
):

    # Temp file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as temp_file:

        temp_path = temp_file.name

    # Generate speech
    tts = gTTS(
        text=text,
        lang=language
    )

    tts.save(temp_path)

    # FFmpeg speed adjustment
    command = [
        "ffmpeg",
        "-y",
        "-i", temp_path,
        "-filter:a",
        f"atempo={speed}",
        output_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Cleanup
    if os.path.exists(temp_path):

        os.remove(temp_path)

    if result.returncode != 0:

        raise Exception(
            result.stderr
        )

    return output_path