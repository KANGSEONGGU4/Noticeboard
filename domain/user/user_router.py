from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Cookie, Header
from fastapi import Depends,Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from fastapi.templating import Jinja2Templates

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "dc55724a8aae1ab3c58471912694fcccfafc2c5bc1634187e0a1c125232f2e54"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/api/user",
)

@router.get("/create")
def qestion_site(request: Request):
     return templates.TemplateResponse("create_site.html", {"request": request})


@router.post("/create")
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):

    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    
    
    user_crud.create_user(db=db, user_create=_user_create)
    

@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    result = {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
    response = JSONResponse(content=result)  # Changed to JSONResponse
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)  # Set cookie
    

    return response




    

# async def get_current_user(access_token: str = Cookie(None)):
#     # print(access_token)
#     if access_token is None:
#         return None
#     try:
#         payload = jwt.decode(access_token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             return None
#         return {"username": username}
#     except JWTError:
#         return None

def get_current_user(request: Request, db: Session = Depends(get_db)):
    # 쿠키에서 토큰 추출
    token = request.cookies.get("access_token")
    if token is None:
        return None  # 토큰이 없을 때 None 반환

    try:
        # "Bearer " 접두사를 제거하고 토큰을 디코딩
        token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None

    user = user_crud.get_user(db, username=username)
    if user is None:
        return None
    return user

# async def get_current_user(token: str = Depends(oauth2_scheme),
#                            db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     else:
#         user = user_crud.get_user(db, username=username)
#         if user is None:
#             raise credentials_exception
#         return user


@router.get("/login")
def qestion_site(request: Request):
     return templates.TemplateResponse("login_site.html", {"request": request})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/api/question/list")
    response.delete_cookie("access_token")
    return response
