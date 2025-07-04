from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
from dotenv import load_dotenv
from os import getenv
import uvicorn

load_dotenv()

app = FastAPI()

SIGHTENGINE_API_USER = getenv("SIGHTENGINE_API_USER")
SIGHTENGINE_API_SECRET = getenv("SIGHTENGINE_API_SECRET")
SIGHTENGINE_ENDPOINT = "https://api.sightengine.com/1.0/check.json"

ALLOWED_TYPES = {"image/jpeg", "image/png"}


@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, detail="Данный формат файла не поддерживается"
        )

    params = {
        "models": "nudity-2.1,recreational_drug,medical,gore-2.0,self-harm",
        "api_user": SIGHTENGINE_API_USER,
        "api_secret": SIGHTENGINE_API_SECRET,
    }

    response = requests.post(
        SIGHTENGINE_ENDPOINT,
        files={"media": (file.filename, file.file, file.content_type)},
        data=params,
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при запросе к API: {response.status_code} {response.text}",
        )

    data = response.json()

    if nsfw_check(data):
        return {"status": "REJECTED", "reason": "NSFW content"}
    else:
        return {"status": "OK"}


def nsfw_check(data: dict) -> bool:
    nudity_keys = (
        "sexual_activity",
        "sexual_display",
        "erotica",
        "very_suggestive",
        "suggestive",
        "mildly_suggestive",
    )

    nudity_score = max(data["nudity"][k] for k in nudity_keys)
    drug_score = data["recreational_drug"]["prob"]
    gore_score = data["gore"]["prob"]

    scores = [nudity_score, drug_score, gore_score]

    return any(score > 0.7 for score in scores)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000)
