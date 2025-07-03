
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from secure_file_share.routes import ops
from secure_file_share.routes import client
from secure_file_share.database import Base, engine
from secure_file_share import models

app = FastAPI(
    title="Secure File Share",
    description="A secure file-sharing platform for Ops and Client users.",
    version="1.0.0"
)

# Allow CORS for Swagger UI and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for Ops and Client
app.include_router(ops.router, prefix="/ops", tags=["Ops"])
app.include_router(client.router, prefix="/client", tags=["Client"])

# Create all tables if they do not exist
Base.metadata.create_all(bind=engine)
