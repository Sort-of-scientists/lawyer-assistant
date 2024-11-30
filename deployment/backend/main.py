from fastapi import FastAPI

from routers import summary, generate, database, forms


app = FastAPI()


app.include_router(summary.router)
app.include_router(generate.router)
app.include_router(database.router)
app.include_router(forms.router)

@app.get("/")
def root():
    return {}
