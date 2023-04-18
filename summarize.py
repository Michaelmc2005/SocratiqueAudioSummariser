import ssl
import os
import openai
import json
import whisper


from pydub import AudioSegment
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ssl._create_default_https_context = ssl._create_unverified_context

def summarize_text(text):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Provide a detailed analysis of the following, it is the audio from a video recording for some more context, ignore that they are in segments, purely analyse the topics mentioned and the information given: " + text}
        ]
    )
    return completion.choices[0].message['content']

def process_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    duration_ms = len(audio)
    duration_s = duration_ms // 1000
    num_segments = duration_s // 60 + 1

    segments = [audio[i*60000:(i+1)*60000] for i in range(num_segments)]

    for i, segment in enumerate(segments):
        segment.export(f"segment_{i}.mp3", format="mp3")

    model = whisper.load_model("base")
    transcriptions = [model.transcribe(f"segment_{i}.mp3") for i in range(num_segments)]

    summaries = [summarize_text(json.dumps(transcription)) for transcription in transcriptions]

    final_summary = " ".join(summaries)
    return final_summary
