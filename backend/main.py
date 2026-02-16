import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import create_db_and_tables
from backend.routers.profiles import router as profiles_router
from backend.routers.proxy import router as proxy_router
from backend.services.browser import browser_manager

app = FastAPI(title="Browser Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profiles_router)
app.include_router(proxy_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
async def on_shutdown():
    await browser_manager.shutdown()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# Serve React production build
frontend_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "frontend", "dist"
)
if os.path.exists(frontend_dir):
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(frontend_dir, "assets")),
        name="assets",
    )

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(frontend_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dir, "index.html"))
