# 3rd party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# local
from localfit.db.database import create_all
from localfit.routes.activities import router


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
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
