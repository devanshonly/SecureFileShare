
import uuid

def generate_token() -> str:
    return str(uuid.uuid4())

def send_verification_email(email: str, token: str):
    print(f"[SIMULATED EMAIL] To: {email} | Verification Token: {token}") 