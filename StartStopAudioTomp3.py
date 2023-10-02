import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import datetime
import os
import openai
from deepgram import Deepgram
import asyncio, json
import aiohttp

# Initialize your keys
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_KEY = os.getenv("OPEN_API_KEY")
MIMETYPE = 'audio/mp3'


def get_current_time_suffix():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")


def record_audio_for_duration(duration_minutes=1):
    samplerate = 44100
    channels = 1
    dtype = np.int16

    print("Press return to start recording...")
    input()
    print("Recording started. Press return again to stop recording...")

    duration_seconds = duration_minutes * 60
    audio = sd.rec(int(samplerate * duration_seconds), samplerate=samplerate, channels=channels, dtype=dtype,
                   blocking=False)
    input()
    sd.stop()
    return audio


def audio_to_mp3(audio_data, base_filename="startstop"):
    normalized_audio_data = (audio_data / np.max(np.abs(audio_data)) * 32767).astype(np.int16)
    audio_segment = AudioSegment(normalized_audio_data.tobytes(), frame_rate=44100,
                                 sample_width=normalized_audio_data.dtype.itemsize, channels=1)

    filename = f"{base_filename}_{get_current_time_suffix()}.mp3"
    audio_segment.export(filename, format="mp3")
    return filename


async def transcribe_audio(filename):
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    if filename.startswith('http'):
        source = {'url': filename}
    else:
        # with open(filename, 'rb') as audio:
        audio = open(filename, 'rb')

        source = {
            'buffer': audio,
            'mimetype': MIMETYPE
        }

    response = await deepgram.transcription.prerecorded(source, {'smart_format': True, 'model': 'nova'})
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]


def request_documentation_from_openai(transcription):
    openai.api_key = OPENAI_KEY
    prompt_content = {
        "role": "user",
        "content": transcription
    }

    base_conversation = [
        {"role": "system",
         "content": "You are a librarian with a list of document listed as urls. Whenever you encounter the word on the left, you substitute it with the url on the right:\n\nwheel: http://www.wheel.com/doc\nengine: http://www.engineroom.com/doc\ncooling system: http://www.hvac.com/doc\ntransmission: http://www.transmission.com/doc\nelectrical: http://www.zap.com/doc\n"},
        prompt_content
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=base_conversation,
        temperature=0,
        max_tokens=2602,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    audio_data = record_audio_for_duration()
    saved_filename = audio_to_mp3(audio_data)
    print(f"Recording saved as {saved_filename}")

    try:
        transcription = asyncio.run(transcribe_audio(saved_filename))
        print(transcription)
        response = request_documentation_from_openai(transcription)
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")
