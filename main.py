from fastapi import Depends, FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import List
import uvicorn
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
r = requests.post("http://127.0.0.1:8005/items/", json={"title": "Hello", "description": "My first FastAPI call"})

r
<Response [200]>

r.json()
{'title': 'Hello', 'description': 'My first FastAPI call', 'id': 1}
"""
@app.post("/items/", response_model=schemas.Item)
def create_item(
    item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_item(db=db, item=item)


"""
>>> r = requests.get("http://127.0.0.1:8005/items/")
>>> r
<Response [200]>
>>> r.json()
[{'title': 'Hello', 'description': 'My first FastAPI call', 'id': 1}]
"""
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/file/" enctype="multipart/form-data" method="post">
# <input name="files" type="file">
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename}
#
#
# @app.post("/file/")
# async def create_file(file: UploadFile = File(...)):
#     return {
#         "file_content_type": file.content_type,
#     }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
