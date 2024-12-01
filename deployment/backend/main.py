from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import ml, database, forms


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(ml.router)
app.include_router(database.router)
app.include_router(forms.router)


@app.get("/")
def root():
    return {}
