
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import database, models, auth
from ..utils import encryptor, email as email_utils
import os
from pydantic import BaseModel

router = APIRouter()

class UserAuth(BaseModel):
    email: str
    password: str

@router.post("/register")
def register_client(payload: UserAuth, db: Session = Depends(database.SessionLocal)):
    email = payload.email
    password = payload.password
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed_password, is_ops=False, is_active=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Simulate email verification
    token = email_utils.generate_token()
    email_utils.send_verification_email(email, token)
    return {"msg": "Client registered. Verification email sent (simulated)."}

@router.post("/verify-email")
def verify_email(email: str, token: str, db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    setattr(user, 'is_active', True)
    db.commit()
    return {"msg": "Email verified. You can now log in."}

@router.post("/login")
def login_client(payload: UserAuth, db: Session = Depends(database.SessionLocal)):
    email = payload.email
    password = payload.password
    user = auth.authenticate_user(db, email, password)
    if not user or bool(user.is_ops):
        raise HTTPException(status_code=401, detail="Invalid credentials or not a Client user")
    if not bool(user.is_active):
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = auth.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/files")
def list_files(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    if bool(current_user.is_ops):
        raise HTTPException(status_code=403, detail="Ops users cannot list client files")
    files = db.query(models.File).filter(models.File.owner_id == current_user.id).all()
    return [{"filename": f.filename, "encrypted_url": f.encrypted_url} for f in files]

@router.get("/download/{encrypted_url}")
def download_file(encrypted_url: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    if bool(current_user.is_ops):
        raise HTTPException(status_code=403, detail="Ops users cannot download client files")
    file = db.query(models.File).filter(models.File.encrypted_url == encrypted_url, models.File.owner_id == current_user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file_path = file.filepath if isinstance(file.filepath, str) else str(file.filepath)
    with open(file_path, "rb") as f:
        data = f.read()
    return Response(content=data, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file.filename}"}) 