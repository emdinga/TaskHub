from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
import json

# Initialize app
app = FastAPI()

# Globals for DB and cache
db = None
cache = None

# -----------------------
# Health & Root endpoints
# -----------------------
@app.get("/health")
def health():
    # Always return ok, even if DB/Redis not ready
    return {"status": "ok"}

@app.get("/")
def root():
    return {
        "app": os.getenv("APP_NAME"),
        "environment": os.getenv("ENVIRONMENT")
    }

# -----------------------
# Startup Event
# -----------------------
@app.on_event("startup")
def startup_event():
    global db, cache
    import psycopg2
    import redis

    # Initialize Postgres
    db = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    # Initialize Redis
    cache = redis.Redis(
        host="redis",
        port=6379,
        decode_responses=True
    )

# -----------------------
# Models
# -----------------------
class Task(BaseModel):
    title: str

# -----------------------
# Tasks Endpoints
# -----------------------
@app.get("/tasks")
def get_tasks(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401)

    # Use cache if available
    cached = cache.get("tasks") if cache else None
    if cached:
        return {"tasks": json.loads(cached), "source": "cache"}

    # Fetch from DB if available
    if db:
        cur = db.cursor()
        cur.execute("SELECT id, title FROM tasks;")
        rows = cur.fetchall()
        tasks = [{"id": r[0], "title": r[1]} for r in rows]
        if cache:
            cache.setex("tasks", 30, json.dumps(tasks))
        return {"tasks": tasks, "source": "database"}

    # DB not ready yet
    raise HTTPException(status_code=503, detail="Database not available")

@app.post("/tasks")
def create_task(task: Task, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401)

    if db:
        cur = db.cursor()
        cur.execute(
            "INSERT INTO tasks (title) VALUES (%s);",
            (task.title,)
        )
        db.commit()
        if cache:
            cache.delete("tasks")
        return {"status": "created", "title": task.title}

    raise HTTPException(status_code=503, detail="Database not available")
