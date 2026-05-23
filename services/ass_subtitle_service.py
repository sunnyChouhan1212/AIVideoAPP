def format_ass_time(seconds):

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = int(seconds % 60)

    centiseconds = int(
        (seconds - int(seconds)) * 100
    )

    return (
        f"{hours}:{minutes:02}:"
        f"{secs:02}.{centiseconds:02}"
    )


def chunk_words(words, chunk_size=3):

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = words[
            i:i + chunk_size
        ]

        chunks.append(
            " ".join(chunk)
        )

    return chunks


def generate_ass_subtitles(
    text,
    output_path
):

    # Split text into words
    words = text.split()

    # Create small chunks
    subtitle_chunks = chunk_words(
        words,
        chunk_size=3
    )

    # Duration per chunk
    chunk_duration = 1.2

    ass_content = """
[Script Info]
Title: Viral Captions
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: Default,Noto Sans Devanagari,28,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,1,2,20,20,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    for index, chunk in enumerate(
        subtitle_chunks
    ):

        start_time = (
            index * chunk_duration
        )

        end_time = (
            start_time + chunk_duration
        )

        start_time = format_ass_time(
            start_time
        )

        end_time = format_ass_time(
            end_time
        )

        ass_content += (
            f"Dialogue: 0,"
            f"{start_time},"
            f"{end_time},"
            f"Default,,0,0,0,,"
            f"{chunk}\n"
        )

    # Save ASS file
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(ass_content)

    return output_path