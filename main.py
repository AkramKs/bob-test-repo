from fastapi import FastAPI

app = FastAPI(
    title="Grocery Store API",
    description="A simple API for a grocery store",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the Grocery Store API"}
