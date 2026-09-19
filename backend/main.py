import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from firebase_service import get_favorites, toggle_favorite
from google import genai
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


load_dotenv()


# Constants
GEMINI_MODEL = "gemini-3.5-flash-lite"
ELEVENLABS_MODEL = "eleven_multilingual_v2"
ELEVENLABS_STT_MODEL = "scribe_v2"


# Create FastAPI app
app = FastAPI(title="Chef Voice Backend")


# Allow frontend and backend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Generate a chef reply using Gemini
def make_chef_reply(
    user_text: str,
    gemini_api_key: str,
) -> str:

    prompt = (
        "You are a distinguished chef with a quirky sense of humor. "
        "Listen for a user's cooking question or request. "
        "Always be very concise: answer in 1 to 2 short sentences max. "
        "Focus on practical cooking help. "
        "Use simple words, light humor, and occasional clever remarks. "
        "Do not use markdown, lists, or long explanations. "
        f"User: {user_text}"
    )

    try:
        client = genai.Client(
            api_key=gemini_api_key
        )

        gemini_response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        reply_text = gemini_response.text.strip()

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini request failed: {error}",
        )

    if not reply_text:
        raise HTTPException(
            status_code=502,
            detail="Gemini returned no text",
        )

    return reply_text


# Convert chef reply into audio using ElevenLabs
def make_audio(
    reply_text: str,
    elevenlabs_api_key: str,
    voice_id: str,
) -> bytes:

    elevenlabs_response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": elevenlabs_api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        json={
            "text": reply_text,
            "model_id": ELEVENLABS_MODEL,
        },
        timeout=300,
    )

    if elevenlabs_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=(
                "ElevenLabs audio generation failed: "
                f"{elevenlabs_response.text}"
            ),
        )

    return elevenlabs_response.content


# Convert uploaded audio into text using ElevenLabs
def transcribe_audio(
    file: UploadFile,
    elevenlabs_api_key: str,
) -> str:

    audio_bytes = file.file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty",
        )

    stt_response = requests.post(
        "https://api.elevenlabs.io/v1/speech-to-text",
        headers={
            "xi-api-key": elevenlabs_api_key,
        },
        files={
            "file": (
                file.filename or "recording.webm",
                audio_bytes,
                file.content_type or "audio/webm",
            )
        },
        data={
            "model_id": ELEVENLABS_STT_MODEL,
        },
        timeout=300,
    )

    if stt_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=(
                "ElevenLabs transcription failed: "
                f"{stt_response.text}"
            ),
        )

    transcript = (
        stt_response.json()
        .get("text", "")
        .strip()
    )

    if not transcript:
        raise HTTPException(
            status_code=502,
            detail="ElevenLabs returned no transcript",
        )

    return transcript


# Voice agent endpoint
@app.post("/chef/voice/audio")
def create_chef_voice_from_audio(
    file: UploadFile = File(...),
):

    gemini_api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    elevenlabs_api_key = os.getenv(
        "ELEVENLABS_API_KEY"
    )

    voice_id = os.getenv(
        "ELEVENLABS_VOICE_ID"
    )

    if not gemini_api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing Gemini API key",
        )

    if not elevenlabs_api_key or not voice_id:
        raise HTTPException(
            status_code=500,
            detail="Missing ElevenLabs API key or voice ID",
        )

    transcript = transcribe_audio(
        file,
        elevenlabs_api_key,
    )

    reply_text = make_chef_reply(
        transcript,
        gemini_api_key,
    )

    audio_bytes = make_audio(
        reply_text,
        elevenlabs_api_key,
        voice_id,
    )

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
    )


# -------------------------
# FAVORITES REQUEST MODELS
# -------------------------

class FoodItem(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )

    id: int | str
    name: str

    emoji: str = ""
    description: str = ""

    cookTime: int = Field(
        default=0,
        validation_alias=AliasChoices(
            "cookTime",
            "cook_time",
        ),
    )

    difficulty: str = ""

    ingredients: list[str] = Field(
        default_factory=list
    )

    instructions: list[str] = Field(
        default_factory=list
    )


class FavoriteRequest(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )

    userID: str = Field(
        validation_alias=AliasChoices(
            "userID",
            "userId",
            "user_id",
        )
    )

    food: FoodItem = Field(
        validation_alias=AliasChoices(
            "food",
            "foodItem",
            "recipe",
        )
    )


# Toggle favorite
@app.post("/favorites/toggle")
def toggle_user_favorite(
    request: FavoriteRequest,
):

    food_data = request.food.model_dump(
        exclude_none=True
    )

    updated_favorites = toggle_favorite(
        request.userID,
        food_data,
    )

    return {
        "favorites": updated_favorites
    }


# Get favorites
@app.get("/favorites/{user_id}")
def get_user_favorites(
    user_id: str,
):

    return {
        "favorites": get_favorites(
            user_id
        )
    }