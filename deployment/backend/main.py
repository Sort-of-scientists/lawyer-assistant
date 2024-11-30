from fastapi import FastAPI

from routers import ml, database, forms


app = FastAPI()


app.include_router(ml.router)
app.include_router(database.router)
app.include_router(forms.router)

@app.get("/")
def root():
    return {}
