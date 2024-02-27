from passlib.context import CryptContext

pwd_contect = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_contect.hash(password)