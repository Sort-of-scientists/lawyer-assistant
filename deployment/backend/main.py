from fastapi import FastAPI

from routers import summary, generate, database


app = FastAPI()


app.include_router(summary.router)
app.include_router(generate.router)
app.include_router(database.router)


@app.get("/")
def root():
    return {}
