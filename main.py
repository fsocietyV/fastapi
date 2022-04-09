from fastapi import FastAPI

app = FastAPI()

#domain where this api is hostes for example : localhost:5000/docs to see swagger documentation automagically generated.


@app.get("/")
def home():
    return {"message":"Hello world!"}