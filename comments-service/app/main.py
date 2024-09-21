from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import comment_router
from .middlewares import JWTValidationMiddleware
 
app = FastAPI()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTValidationMiddleware)

app.include_router(comment_router)

