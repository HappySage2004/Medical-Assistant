from typing import Union
from fastapi import FastAPI

app = FastAPI()
app_version = "/v1"

@app.get(app_version + "/health_check")
def read_root():
    return {"Hello": "World"}


@app.get(app_version + "/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}