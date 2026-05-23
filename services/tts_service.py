from gtts import gTTS

def generate_tts(
    text,
    language,
    output_path
):

    tts = gTTS(
        text=text,
        lang=language
    )

    tts.save(output_path)

    return output_path