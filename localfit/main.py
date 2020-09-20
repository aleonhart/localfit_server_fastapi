# 3rd party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# local
from localfit.db.database import create_all
from localfit.activities.routes.activities import activities_router
from localfit.activities.routes.activity import activity_router
from localfit.monitor.routes import monitor_router


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(activities_router)
    app.include_router(activity_router)
    app.include_router(monitor_router)
    return app


create_all()

app = get_application()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)

