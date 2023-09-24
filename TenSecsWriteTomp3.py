from google.cloud import speech
import subprocess
import json

def record_audio(duration, output_file):
    """
    Record audio from a macOS microphone for a given duration and save to an mp3 file.

    Parameters:
    - duration: Duration of recording in seconds.
    - output_file: The name of the mp3 file to save the recording.
    """

    # ffmpeg command to record audio
    cmd = [
        "ffmpeg",
        "-f", "avfoundation",
        "-i", ":1",
        "-t", str(duration),
        output_file
    ]

    # Execute the command
    subprocess.run(cmd)


if __name__ == "__main__":
    duration = 10  # recording time in seconds
    output_filename = "output.mp3"

    print("Press ENTER to start recording...")
    input()  # Wait for Enter key press
    print("Recording started...")

    record_audio(duration, output_filename)
    print(f"Recording saved as {output_filename}")

    # Call Google's speech to text API
    client = speech.SpeechClient.from_service_account_json('key.json')

    file_name = (output_filename)

    with open(file_name, "rb") as f:
        mp3_data = f.read()

    audio_file = speech.RecognitionAudio(content=mp3_data)

    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    response = client.recognize(config=config, audio=audio_file)
    # print(response)

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")

#    parsed_data = json.loads(str(response))

#    transcript = parsed_data["results"]["alternatives"]["transcript"]

#    print(transcript)

    # Next: Get response and take the next action based on what GPT-4 says

