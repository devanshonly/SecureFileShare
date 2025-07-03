
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import database, models, auth
from ..utils import email as email_utils
import os
from pydantic import BaseModel

router = APIRouter()

ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")

class UserAuth(BaseModel):
    email: str
    password: str

@router.post("/register")
def register_ops(payload: UserAuth, db: Session = Depends(database.SessionLocal)):
    email = payload.email
    password = payload.password
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed_password, is_ops=True, is_active=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Simulate email verification
    token = email_utils.generate_token()
    email_utils.send_verification_email(email, token)
    return {"msg": "Ops user registered. Verification email sent (simulated)."}

@router.post("/verify-email")
def verify_email(email: str, token: str, db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    setattr(user, 'is_active', True)
    db.commit()
    return {"msg": "Email verified. You can now log in."}

@router.post("/login")
def login_ops(payload: UserAuth, db: Session = Depends(database.SessionLocal)):
    email = payload.email
    password = payload.password
    user = auth.authenticate_user(db, email, password)
    if not user or not bool(user.is_ops):
        raise HTTPException(status_code=401, detail="Invalid credentials or not an Ops user")
    if not bool(user.is_active):
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = auth.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload")
def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.SessionLocal)):
    if not bool(current_user.is_ops):
        raise HTTPException(status_code=403, detail="Only Ops users can upload files")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    db_file = models.File(filename=file.filename, filepath=file_path, owner_id=current_user.id, encrypted_url="-")
    db.add(db_file)
    db.commit()
    return {"msg": "File uploaded successfully"} 