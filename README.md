# AudioToText

Simple program that records ten seconds of audio through the microphone and sends the sound file to
The Google Speech to Text API for transcription

## Prereq

You need to set up an account with Google API and get a key.json in order to use the service.  Watch this video ( https://youtu.be/DtlJH6MgBso?si=c1DPKETm1gIwQJY7 ) starting from 1:35 instead of going through the Google API docs ( https://cloud.google.com/speech-to-text/docs/before-you-begin ), which can be confusing.

## Execution

After you get your key.json file installed, you can run

% python TenSecsWriteTomp3.py 

For now it'll write to an output.mp3 file which it subsequently sends to the API and returns the transcript



