from fastapi import FastAPI

from routers import summary, generate


app = FastAPI()

app.include_router(summary.router)
app.include_router(generate.router)


@app.get("/")
def root():
    return {}
