# AudioToText

This repo contains several programs created as we progress through the Audio->Text-LLM use case

# StartStopAudioTomp3.py

20231001 This version improves on the previous version by letting the user determine the duration of the audio instead of limiting him/her to 10 seconds
The transcription is done by Whisper AI and that transcript is sent as a pronmpt to OpenAI

Demo video is here ( https://drive.google.com/file/d/1pzGVayxMH24AmO3Bf-g2IymJysQiO_zm/view?usp=sharing )

## Prereq

You have to set the api keys for Deepgram and OpenAI

 export DEEPGRAM_API_KEY="<Deepgram key>"
 
 export OPEN_API_KEY="<OpenAI key>"

## Execution

% python StartStopAudioTomp3.py

# TenSecsWriteTomp3.py

Simple program that records ten seconds of audio through the microphone and sends the sound file to
The Google Speech to Text API for transcription

## Prereq

You need to set up an account with Google API and get a key.json in order to use the service.  Watch this video ( https://youtu.be/DtlJH6MgBso?si=c1DPKETm1gIwQJY7 ) starting from 1:35 instead of going through the Google API docs ( https://cloud.google.com/speech-to-text/docs/before-you-begin ), which can be confusing.

## Execution

After you get your key.json file installed, you can run

% python TenSecsWriteTomp3.py 

For now it'll write to an output.mp3 file which it subsequently sends to the API and returns the transcript

## Demo

A quick video demo can be found here ( https://drive.google.com/file/d/1coIQejWS6_M8QOEUBoqBv9bTNdI5nz3T/view?usp=sharing )



