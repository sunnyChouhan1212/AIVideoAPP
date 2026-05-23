import uuid
import os

def generate_filename(extension):

    unique_id = uuid.uuid4().hex

    return f"{unique_id}.{extension}"


def ensure_directories():

    folders = [
        "outputs",
        "outputs/temp",
        "outputs/final_videos"
    ]

    for folder in folders:

        os.makedirs(
            folder,
            exist_ok=True
        )