from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shadowstream.space"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_TOKEN = GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "Randomz4-debug"
REPO = "Memory-Vault-backend"

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    content = await file.read()

    encoded = base64.b64encode(content).decode()

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/vault/{file.filename}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "message": f"Upload {file.filename}",
        "content": encoded
    }

    r = requests.put(url, headers=headers, json=data)

    return r.json()

@app.get("/memories")
async def memories(folder: str = ""):

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{folder}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    files = []

    for file in response.json():

        if file["type"] != "file":
            continue

        files.append({
            "name": file["name"],
            "download_url": file["download_url"]
        })

    return files