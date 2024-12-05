
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}




Punkte = 4


@app.put("/Punkte/{Punkte_id}")
def update_Punkte(Punkte_id: str):
    if Punkte_id == "Ja":
        return {Punkte + 1}
    elif Punkte_id == "Nein":
        return {Punkte - 1}
    else:
        return{"FALSCH"}
        

@app.put("/user_ID/{user_ID}")
def gebe_Punkte(user_ID: int):
    return {"User Punkte": Punkte}






if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, log_level="debug")
