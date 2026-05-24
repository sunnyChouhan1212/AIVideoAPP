from utils.subtitle_styles import (
    SUBTITLE_STYLES
)

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


def chunk_words(
    words,
    chunk_size=4
):

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = words[
            i:i + chunk_size
        ]

        chunks.append(chunk)

    return chunks


def generate_karaoke_line(
    words,
    word_duration_cs=60
):

    karaoke_text = ""

    for word in words:

        karaoke_text += (
            f"{{\\k{word_duration_cs}}}"
            f"{word} "
        )

    return karaoke_text.strip()


def generate_ass_subtitles(
    text,
    output_path,
    subtitle_theme="TikTok"
):

    # Split text into words
    words = text.split()

    # Create chunks
    subtitle_chunks = chunk_words(
        words,
        chunk_size=4
    )

    # Timing
    word_duration = 0.6

    ass_content = """
    [Script Info]
    Title: Karaoke Viral Captions
    ScriptType: v4.00+

    [V4+ Styles]
    Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

    {SUBTITLE_STYLES[subtitle_theme]}

    [Events]
    Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    """

    current_time = 0

    for chunk in subtitle_chunks:

        # Chunk duration
        chunk_duration = (
            len(chunk) * word_duration
        )

        start_time = format_ass_time(
            current_time
        )

        end_time = format_ass_time(
            current_time +
            chunk_duration
        )

        karaoke_text = (
            generate_karaoke_line(
                chunk,
                word_duration_cs=60
            )
        )

        ass_content += (
            f"Dialogue: 0,"
            f"{start_time},"
            f"{end_time},"
            f"Default,,0,0,0,,"
            f"{karaoke_text}\n"
        )

        current_time += chunk_duration

    # Save ASS file
    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(ass_content)

    return output_path