from faster_whisper import WhisperModel

# Load model ONCE
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)


def format_time(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    milliseconds = int(
        (seconds - int(seconds)) * 1000
    )

    return (
        f"{hours:02}:{minutes:02}:"
        f"{secs:02},{milliseconds:03}"
    )


def generate_srt_from_audio(
    audio_path,
    output_path
):

    segments, info = model.transcribe(
        audio_path
    )

    srt_content = ""

    for index, segment in enumerate(
        segments,
        start=1
    ):

        start_time = format_time(
            segment.start
        )

        end_time = format_time(
            segment.end
        )

        text = segment.text.strip()

        srt_content += (
            f"{index}\n"
            f"{start_time} --> "
            f"{end_time}\n"
            f"{text}\n\n"
        )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(srt_content)

    return output_path