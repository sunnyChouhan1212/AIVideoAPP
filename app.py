import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import streamlit as st

from services.tts_service import (
    generate_tts,
    EDGE_VOICES
)

from services.video_service import (
    replace_video_audio,
    burn_ass_subtitles
)

from services.ass_subtitle_service import (
    generate_ass_subtitles
)

from services.script_service import (
    generate_viral_script,
    LLM_MODELS
)

from utils.helpers import (
    generate_filename,
    ensure_directories
)

# Create folders
ensure_directories()

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

# -----------------------------------
# Title
# -----------------------------------

st.title("🎬 AI Video Generator")

# -----------------------------------
# Sidebar
# -----------------------------------

st.sidebar.title(
    "⚙ AI Settings"
)

# LLM Provider
selected_provider = st.sidebar.selectbox(
    "Select LLM Provider",
    [
        "OpenAI",
        "Groq"
    ]
)

# Model Selection
selected_model = st.sidebar.selectbox(
    "Select Model",
    LLM_MODELS[
        selected_provider
    ]
)

# -----------------------------------
# Video Source Selection
# -----------------------------------

video_source = st.radio(
    "Select Video Source",
    [
        "Upload Video",
        "Use Gameplay Video"
    ]
)

uploaded_video = None

selected_gameplay_path = None

# Upload custom video
if video_source == "Upload Video":

    uploaded_video = st.file_uploader(
        "Upload Video",
        type=["mp4", "mov", "avi"]
    )

# Use gameplay video
else:

    gameplay_options = {

        "Minecraft":
        "assets/gameplays/minecraft.mp4",

        "Subway Surfers":
        "assets/gameplays/subway.mp4",

        "GTA":
        "assets/gameplays/gta.mp4",

        "Satisfying":
        "assets/gameplays/satisfying.mp4"
    }

    selected_gameplay = st.selectbox(
        "Select Gameplay",
        list(gameplay_options.keys())
    )

    selected_gameplay_path = (
        gameplay_options[
            selected_gameplay
        ]
    )

    st.video(
        selected_gameplay_path
    )

# -----------------------------------
# Language Selection
# -----------------------------------

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

# -----------------------------------
# AI Script Generator
# -----------------------------------

st.subheader(
    "🤖 AI Script Generator"
)

topic = st.text_input(
    "Enter Video Topic"
)

script_style = st.selectbox(
    "Script Style",
    [
        "Brainrot",
        "Motivation",
        "Scary",
        "Facts",
        "Storytelling"
    ]
)

if st.button("✨ Generate AI Script"):

    if not topic.strip():

        st.warning(
            "Please enter topic"
        )

    else:

        with st.spinner(
            "Generating viral script..."
        ):

            try:

                generated_script = (
                    generate_viral_script(
                        topic=topic,
                        language=selected_language,
                        style=script_style,
                        provider=selected_provider,
                        model_name=selected_model
                    )
                )

                st.session_state[
                    "generated_script"
                ] = generated_script

                st.success(
                    "Script generated ✅"
                )

            except Exception as error:

                st.error(
                    str(error)
                )

# -----------------------------------
# Speech Text
# -----------------------------------

text = st.text_area(
    "Enter speech text",
    value=st.session_state.get(
        "generated_script",
        ""
    ),
    height=220
)

# -----------------------------------
# TTS Provider
# -----------------------------------

tts_provider = st.selectbox(
    "Select TTS Provider",
    [
        "gtts",
        "edge"
    ]
)

edge_voice = None

# Edge voices
if tts_provider == "edge":

    selected_voice = st.selectbox(
        "Select Edge Voice",
        list(EDGE_VOICES.keys())
    )

    edge_voice = EDGE_VOICES[
        selected_voice
    ]

# -----------------------------------
# Audio Speed
# -----------------------------------

audio_speed = st.slider(
    "Audio Speed",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

# -----------------------------------
# Subtitle Theme
# -----------------------------------

subtitle_theme = st.selectbox(
    "Subtitle Theme",
    [
        "TikTok",
        "Gaming",
        "Meme",
        "Minimal"
    ]
)

# -----------------------------------
# Buttons
# -----------------------------------

col1, col2 = st.columns(2)

generate_audio_btn = col1.button(
    "🎤 Generate Audio"
)

generate_video_btn = col2.button(
    "🎬 Generate Video"
)

# -----------------------------------
# Generate Audio Only
# -----------------------------------

if generate_audio_btn:

    if not text.strip():

        st.warning(
            "Please enter text"
        )

        st.stop()

    try:

        st.info(
            "Generating audio..."
        )

        audio_path = (
            f"outputs/temp/"
            f"{generate_filename('mp3')}"
        )

        generate_tts(
            text=text,
            language=language_code,
            output_path=audio_path,
            speed=audio_speed,
            tts_provider=tts_provider,
            edge_voice=edge_voice
        )

        st.success(
            "Audio generated successfully ✅"
        )

        st.audio(audio_path)

        with open(
            audio_path,
            "rb"
        ) as audio_file:

            st.download_button(
                label="⬇ Download Audio",
                data=audio_file,
                file_name="ai_audio.mp3",
                mime="audio/mp3"
            )

    except Exception as error:

        st.error(
            f"Error: {str(error)}"
        )

# -----------------------------------
# Generate Video
# -----------------------------------

if generate_video_btn:

    # Validation
    if (
        not uploaded_video
        and not selected_gameplay_path
    ):

        st.warning(
            "Please upload or select a video"
        )

        st.stop()

    if not text.strip():

        st.warning(
            "Please enter text"
        )

        st.stop()

    # Progress
    progress_text = st.empty()

    progress_bar = st.progress(0)

    try:

        # -----------------------------------
        # Prepare Video
        # -----------------------------------

        progress_text.text(
            "Preparing video..."
        )

        progress_bar.progress(10)

        input_video_path = (
            f"outputs/temp/"
            f"{generate_filename('mp4')}"
        )

        # Upload video
        if uploaded_video:

            with open(
                input_video_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_video.read()
                )

        # Gameplay video
        else:

            with open(
                selected_gameplay_path,
                "rb"
            ) as source_file:

                with open(
                    input_video_path,
                    "wb"
                ) as dest_file:

                    dest_file.write(
                        source_file.read()
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
            output_path=audio_path,
            speed=audio_speed,
            tts_provider=tts_provider,
            edge_voice=edge_voice
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
        # Generate Subtitles
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
            output_path=subtitle_path,
            subtitle_theme=subtitle_theme
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
        # Complete
        # -----------------------------------

        progress_text.text(
            "Completed ✅"
        )

        progress_bar.progress(100)

        st.success(
            "Video generated successfully ✅"
        )

        st.video(final_video_path)

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