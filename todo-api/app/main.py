from fastapi import FastAPI
from app.core.database import Base, engine
from app.endpoints.v1.auth import router as auth_router

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routes
app.include_router(auth_router)

