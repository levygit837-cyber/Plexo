from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_db_and_tables
from backend.routers.profiles import router as profiles_router

app = FastAPI(title="Browser Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
