#
# 20230930: This version uses the return key to start and stop recording.
# The audio is saved to an mp3 file and sent to deepgram for transcription.
# The transcription will be sent to GPT-4 and the response is expected to be
# documentation related to the query.

# For now, we expect the query to be something like "I'd like to get documentation for X"
# where X is supposed to be an object selected from the AR device

# GPT-4 will know what to return because it will be pre-prompted with a list of keywords and their associated
# URLs, which serve as a standin for the documentation.


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

whisper_text = "I'd like to get documentation for a thingamajig"

def append_time_suffix(filename):
    # Extract the file extension
    base_name, extension = filename.rsplit('.', 1)

    # Get the current time and format it as a string
    now = datetime.datetime.now()
    time_suffix = now.strftime("%Y%m%d_%H%M%S")

    # Construct the new filename by appending the time-based suffix
    new_filename = f"{base_name}_{time_suffix}.{extension}"

    return new_filename


def record_audio():
    # Settings for the recording
    samplerate = 44100  # Hertz
    channels = 1  # Stereo
    dtype = np.int16  # 16-bit audio

    print("Press return to start recording...")
    input()

    print("Recording started. Press return again to stop recording...")
    audio = sd.rec(int(samplerate * 60), samplerate=samplerate, channels=channels, dtype=dtype, blocking=False)

    input()  # Wait for another return key press
    sd.stop()  # Stop the recording

    return audio


def save_to_mp3(audio_data, filename="startstop.mp3"):
    audio_data_norm = (audio_data / np.max(np.abs(audio_data)) * 32767).astype(np.int16)
    audio_segment = AudioSegment(audio_data_norm.tobytes(),
                                 frame_rate=44100,
                                 sample_width=audio_data_norm.dtype.itemsize,
                                 channels=1)
    audio_segment.export(filename, format="mp3")


def call_open_ai(prompt="I'd like to get documentation for a somesuchnonsense"):
    global openai
    openai.api_key = OPENAI_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a librarian with a list of document listed as urls.  You have the following list in your library:  Whenever you encounter the word on the left, you substitute it with the url on the right:\n\nwheel:  http://www.wheel.com/doc\nengine: http://www.engineroom.com/doc\ncooling system: http://www.hvac.com/doc\ntransmission: http://www.transmission.com/doc\nelectrical: http://www.zap.com/doc\n\n"
            },
            {
                "role": "user",
                "content": "I would like documentation on the engine"
            },
            {
                "role": "assistant",
                "content": "A customer comes in and asks for documents on the following topics:\n\n1. Wheel\n2. Engine\n3. Cooling system\n4. Transmission\n5. Electrical\n\nYou provide them with the following URLs:\n\n1. http://www.wheel.com/doc\n2. http://www.engineroom.com/doc\n3. http://www.hvac.com/doc\n4. http://www.transmission.com/doc\n5. http://www.zap.com/doc"
            },
            {
                "role": "assistant",
                "content": "Sure, you can find the documentation on the engine at this URL: http://www.engineroom.com/doc"
            },
            {
                "role": "user",
                "content": "I would like documentation on this item: electrical"
            },
            {
                "role": "assistant",
                "content": "Sure, you can find the documentation on electrical at this URL: http://www.zap.com/doc"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=2602,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response)

    print(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    audio_data = record_audio()
    filename = append_time_suffix("startstop.mp3")
    save_to_mp3(audio_data, filename)
    print("Recording saved as " + filename)

    FILE = filename


    async def main():
        global whisper_text
        # Initialize the Deepgram SDK
        deepgram = Deepgram(DEEPGRAM_API_KEY)

        # Check whether requested file is local or remote, and prepare source
        if FILE.startswith('http'):
            # file is remote
            # Set the source
            source = {
                'url': FILE
            }
        else:
            # file is local
            # Open the audio file
            audio = open(FILE, 'rb')

            # Set the source
            source = {
                'buffer': audio,
                'mimetype': MIMETYPE
            }

        # Send the audio to Deepgram and get the response
        response = await asyncio.create_task(
            deepgram.transcription.prerecorded(
                source,
                {
                    'smart_format': True,
                    'model': 'nova',
                }
            )
        )

        # Write the response to the console
        # print(json.dumps(response, indent=4))

        # Write only the transcript to the console
        whisper_text = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(whisper_text)


    try:
        # If running in a Jupyter notebook, Jupyter is already running an event loop, so run main with this line instead:
        # await main()
        asyncio.run(main())
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno
        print(f'line {line_number}: {exception_type} - {e}')

    call_open_ai(whisper_text)

