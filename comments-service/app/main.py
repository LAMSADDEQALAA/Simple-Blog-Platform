from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import comment_router
from .middlewares import JWTValidationMiddleware
from .database import engine,Base
app = FastAPI()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTValidationMiddleware)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    
app.include_router(comment_router)
