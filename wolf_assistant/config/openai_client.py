from openai import OpenAI

from wolf_assistant.config.tokens import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def generate_response(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        max_tokens=1024,
        temperature=0.5,
    )
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()


def generate_transcription(audio_bytes):
    transcription = client.audio.transcriptions.create(model="whisper-1", file=("audio.oga", audio_bytes, "audio/ogg"))
    return transcription.text.strip()


__all__ = [
    'client',
    'generate_response',
    'generate_transcription'
]
