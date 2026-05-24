import os

from openai import OpenAI

from dotenv import load_dotenv

# Load env
load_dotenv()

# OpenAI client
client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def generate_viral_script(
    topic,
    language="English",
    style="Brainrot"
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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.9
    )

    script = (
        response
        .choices[0]
        .message
        .content
    )

    return script