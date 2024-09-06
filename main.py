from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str

items: List[Item] = []

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Server is running"}

@app.get("/items")
def get_items():
    return items

@app.post("/items", status_code=201)
def add_item(item: Item):
    items.append(item)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)