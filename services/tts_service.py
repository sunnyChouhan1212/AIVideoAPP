from gtts import gTTS

import subprocess
import tempfile
import os
import asyncio
import edge_tts


# -----------------------------------
# Edge TTS Voices
# -----------------------------------

EDGE_VOICES = {
    "English Male":
    "en-US-GuyNeural",

    "English Female":
    "en-US-JennyNeural",

    "Hindi Female":
    "hi-IN-SwaraNeural",

    "Hindi Male":
    "hi-IN-MadhurNeural"
}


# -----------------------------------
# Generate Edge TTS
# -----------------------------------

async def edge_tts_generate(
    text,
    voice,
    output_path
):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    await communicate.save(
        output_path
    )


# -----------------------------------
# Main TTS Function
# -----------------------------------

def generate_tts(
    text,
    language,
    output_path,
    speed=1.0,
    tts_provider="gtts",
    edge_voice=None
):

    temp_path = None

    # -----------------------------------
    # gTTS
    # -----------------------------------

    if tts_provider == "gtts":

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as temp_file:

            temp_path = temp_file.name

        tts = gTTS(
            text=text,
            lang=language
        )

        tts.save(temp_path)

    # -----------------------------------
    # Edge TTS
    # -----------------------------------

    elif tts_provider == "edge":

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as temp_file:

            temp_path = temp_file.name

        asyncio.run(
            edge_tts_generate(
                text=text,
                voice=edge_voice,
                output_path=temp_path
            )
        )

    else:

        raise Exception(
            "Invalid TTS Provider"
        )

    # -----------------------------------
    # Speed Adjustment
    # -----------------------------------

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
    if temp_path and os.path.exists(temp_path):

        os.remove(temp_path)

    if result.returncode != 0:

        raise Exception(
            result.stderr
        )

    return output_path