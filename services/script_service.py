import os

from dotenv import load_dotenv

from openai import OpenAI

from groq import Groq

# Load env
load_dotenv()

# OpenAI Client
openai_client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

# Groq Client
groq_client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

# -----------------------------------
# Models
# -----------------------------------

LLM_MODELS = {

    "OpenAI": [
        "gpt-4.1-mini",
        "gpt-4o-mini"
    ],

    "Groq": [
        "llama-3.3-70b-versatile",
        "llama3-8b-8192",
        "mixtral-8x7b-32768"
    ]
}


# -----------------------------------
# Generate Script
# -----------------------------------

def generate_viral_script(
    topic,
    language="English",
    style="Brainrot",
    provider="OpenAI",
    model_name="gpt-4.1-mini"
):

    prompt = f"""
Generate a viral short-form video script.

Topic:
{topic}

Language:
{language}

Style:
{style}

Requirements:
- Hook in first sentence
- Short punchy lines
- TikTok/Reels style
- Maximum 120 words
- Highly engaging
- Easy narration
"""

    # -----------------------------------
    # OpenAI
    # -----------------------------------

    if provider == "OpenAI":

        response = (
            openai_client
            .chat
            .completions
            .create(
                model=model_name,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.9
            )
        )

    # -----------------------------------
    # Groq
    # -----------------------------------

    elif provider == "Groq":

        response = (
            groq_client
            .chat
            .completions
            .create(
                model=model_name,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.9
            )
        )

    else:

        raise Exception(
            "Invalid provider"
        )

    script = (
        response
        .choices[0]
        .message
        .content
    )

    return script