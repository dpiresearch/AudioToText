from google.cloud import speech
import subprocess

# Record audio from a macOS microphone for a given duration and save to an mp3 file.
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

    # Start recording and write to an mp3 file
    record_audio(duration, output_filename)
    print(f"Recording saved as {output_filename}")

    # Call Google's speech to text API
    client = speech.SpeechClient.from_service_account_json('key.json')

    file_name = (output_filename)

    # Read mp3 file and send to Google speech to text
    with open(file_name, "rb") as f:
        mp3_data = f.read()

    audio_file = speech.RecognitionAudio(content=mp3_data)

    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    response = client.recognize(config=config, audio=audio_file)
    print(response)

    # parse transcript
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")

    # Next: Get transcript, decorate with user context and action
    # send to GPT-4 and take the next action ( open a doc, explain functionality, etc.. ).

