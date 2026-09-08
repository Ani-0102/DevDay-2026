const API_URL = "http://localhost:8000";

export function getUserId() {
  let userId = localStorage.getItem("devday-user-id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("devday-user-id", userId);
  }
  return userId;
}

export async function toggleFavoriteRequest(userId, recipe) {
  const response = await fetch(
    `${API_URL}/favorites/toggle`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userId,
        food: recipe,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to update favorites");
  }

  const data = await response.json();

  return data.favorites;
}

export async function sendVoiceRecording(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob, "recording.webm" );
  const response = await fetch(
    `${API_URL}/chef/voice/audio`,
    {
      method: "POST",
      body: formData,
    }
  );
  if (!response.ok) {
    throw new Error("Voice request failed");
  }
  return response.blob();
}