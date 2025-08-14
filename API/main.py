from fastapi import FastAPI
import uvicorn
from PIL import Image


app=FastAPI()

@app.get("/")


def saludo():
    img = Image.open("./oscarin.png")
    img.show()
    return {"mensaje": "Hola mundo"}

def main ():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()