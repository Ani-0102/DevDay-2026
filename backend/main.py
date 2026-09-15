# import some important libraries
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from firebase_service import get_favorites, toggle_favorite
from google import genai
from pydantic import BaseModel

load_dotenv() 

# define some of our constants
GEMINI_MODEL = "gemini-3.5-flash-lite"
ELEVENLABS_MODEL = "eleven_multilingual_v2"
ELEVENLABS_STT_MODEL = "scribe_v2"

# 1. create the fastapi app here:


# need this so our frontend and backend can talk to each other
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# code health endpoint here:
#2. create a check health endpoint here:


# helper function to generate a chef-like reply using Gemini API
def make_chef_reply(user_text: str, gemini_api_key: str) -> str:
    prompt = (
        "You are a distinguished chef with a quirky sense of humor. Listen for a user's cooking question or request.  "
        "Always be very concise: answer in 1 to 2 short sentences max. "
        "Focus on practical cooking help. "
        "Use simple words, light humor, and occasional clever rmarks "
        "Do not use markdown, lists, or long explanations. "
        f"User: {user_text}"
    )

    # 3. Make gemini API call here:
    

# function to make audio from the chef reply using ElevenLabs API
def make_audio(reply_text: str, elevenlabs_api_key: str, voice_id: str) -> bytes:
    # 4. Make elevenlabs text-to-speech API call here:
    
    # end of elevenlabs text-to-speech API call

    # if there is an erorr we will return a 502 error to the frontend
    if elevenlabs_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"ElevenLabs audio generation failed: {elevenlabs_response.text}",
        )

    return elevenlabs_response.content


# function to transcribe audio using ElevenLabs API

def transcribe_audio(file: UploadFile, elevenlabs_api_key: str) -> str:
    audio_bytes = file.file.read() # file is an object which has a file attribute, read bytes with .read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Uploaded audio file is empty")

    # 5. Make elevenlabs speech-to-text API call here:
    
    # end of elevenlabs speech-to-text API call

    # check if the transcription was successful
    if stt_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"ElevenLabs transcription failed: {stt_response.text}",
        )

    # 6. Extract the transcript from the response and return it
    


# to generate a chef-like voice from an audio file
@app.post("/chef/voice/audio")
def create_chef_voice_from_audio(file: UploadFile = File(...)):
    # 7. Get our API keys from environment variables here:
    
    # 8. Call our helper functions to transcribe the audio, generate a chef reply, and create audio from that reply:
    


#13. Define request models here 



# 14. Make endpoint to toggle a user's favorite here:



#15. Make endpoint to return a user's favorites here:
