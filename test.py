from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

# 위에서 제공한 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "dc55724a8aae1ab3c58471912694fcccfafc2c5bc1634187e0a1c125232f2e54"
ALGORITHM = "HS256"

# 사용자의 정보
fake_user_db = {
    "username": "john_doe",
    "password": pwd_context.hash("password123"),
    "email": "john.doe@example.com",
}

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 사용자 인증 함수
def authenticate_user(username: str, password: str):
    if username in fake_user_db:
        hashed_password = fake_user_db[username]["password"]
        if pwd_context.verify(password, hashed_password):
            return fake_user_db[username]

# JWT 토큰 검증 함수
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # 토큰이 만료됨
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰

# 예시
access_token = create_access_token(data={"username": "john_doe"}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
print("Access Token:", access_token)

decoded_token = decode_access_token(access_token)
print("Decoded Token:", decoded_token)
