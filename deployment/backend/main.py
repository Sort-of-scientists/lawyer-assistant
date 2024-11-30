from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import summary, generate, database, test_router

from routers import summary, generate, database, forms


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(summary.router)
app.include_router(generate.router)
app.include_router(database.router)
app.include_router(forms.router)

@app.get("/")
def root():
    return {}
