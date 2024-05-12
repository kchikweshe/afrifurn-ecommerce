from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from middlewares.cors import apply_cors_middleware
from routers import api_router
from auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


afrifurn_app = FastAPI()


origins = [

    "http://localhost:3000",
]
image_dir = Path(__file__).parent / "product_images"

directory=StaticFiles(directory='static')
afrifurn_app.mount("/static",directory , name="images")
afrifurn_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuring routers
afrifurn_app.include_router(api_router)
afrifurn_app.include_router(auth_router)

if __name__ == "__main__":
    afrifurn_app.run()