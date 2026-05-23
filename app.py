import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import streamlit as st

from services.tts_service import (
    generate_tts
)

from services.video_service import (
    replace_video_audio,
    burn_ass_subtitles
)

from services.ass_subtitle_service import (
    generate_ass_subtitles
)

from utils.helpers import (
    generate_filename,
    ensure_directories
)

# Create folders
ensure_directories()

# Page config
st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

# Title
st.title("🎬 AI Video Generator")

# Upload video
uploaded_video = st.file_uploader(
    "Upload Video",
    type=["mp4", "mov", "avi"]
)

# Text input
text = st.text_area(
    "Enter speech text"
)

# Language options
language_map = {
    "English": "en",
    "Hindi": "hi"
}

selected_language = st.selectbox(
    "Select Language",
    list(language_map.keys())
)

language_code = language_map[
    selected_language
]

# Generate button
if st.button("Generate Video"):

    # Validation
    if not uploaded_video:

        st.warning(
            "Please upload a video"
        )

        st.stop()

    if not text.strip():

        st.warning(
            "Please enter text"
        )

        st.stop()

    # Progress UI
    progress_text = st.empty()

    progress_bar = st.progress(0)

    try:

        # -----------------------------------
        # Upload Video
        # -----------------------------------

        progress_text.text(
            "Uploading video..."
        )

        progress_bar.progress(10)

        input_video_path = (
            f"outputs/temp/"
            f"{generate_filename('mp4')}"
        )

        with open(
            input_video_path,
            "wb"
        ) as file:

            file.write(
                uploaded_video.read()
            )

        # -----------------------------------
        # Generate TTS
        # -----------------------------------

        progress_text.text(
            "Generating AI voice..."
        )

        progress_bar.progress(30)

        audio_path = (
            f"outputs/temp/"
            f"{generate_filename('mp3')}"
        )

        generate_tts(
            text=text,
            language=language_code,
            output_path=audio_path
        )

        # -----------------------------------
        # Replace Audio
        # -----------------------------------

        progress_text.text(
            "Replacing video audio..."
        )

        progress_bar.progress(50)

        temp_video_path = (
            f"outputs/temp/"
            f"{generate_filename('mp4')}"
        )

        replace_video_audio(
            input_video=input_video_path,
            input_audio=audio_path,
            output_video=temp_video_path
        )

        # -----------------------------------
        # Generate ASS Subtitles
        # -----------------------------------

        progress_text.text(
            "Generating subtitles..."
        )

        progress_bar.progress(70)

        subtitle_path = (
            f"outputs/temp/"
            f"{generate_filename('ass')}"
        )

        generate_ass_subtitles(
            text=text,
            output_path=subtitle_path
        )

        # -----------------------------------
        # Burn Subtitles
        # -----------------------------------

        progress_text.text(
            "Rendering final video..."
        )

        progress_bar.progress(90)

        final_video_path = (
            f"outputs/final_videos/"
            f"{generate_filename('mp4')}"
        )

        burn_ass_subtitles(
            input_video=temp_video_path,
            subtitle_file=subtitle_path,
            output_video=final_video_path
        )

        # -----------------------------------
        # Completed
        # -----------------------------------

        progress_text.text(
            "Completed ✅"
        )

        progress_bar.progress(100)

        st.success(
            "Video generated successfully ✅"
        )

        # Preview video
        st.video(final_video_path)

        # Download button
        with open(
            final_video_path,
            "rb"
        ) as video_file:

            st.download_button(
                label="⬇ Download Video",
                data=video_file,
                file_name="final_video.mp4",
                mime="video/mp4"
            )

    except Exception as error:

        st.error(
            f"Error: {str(error)}"
        )