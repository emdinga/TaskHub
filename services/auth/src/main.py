from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

class LoginRequest(BaseModel):
    username: str

@app.post("/login")
def login(data: LoginRequest):
    return {
        "token": str(uuid.uuid4()),
        "user": data.username
    }
