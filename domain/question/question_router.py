from fastapi import APIRouter, Depends , Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
from models import Question

from domain.user.user_router import get_current_user

from starlette import status
from domain.user.user_router import get_current_user
from models import User


# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/api/question",
)

# # response_model = question_list의 리턴 값이 Question스키마로 구성된 리스트
# @router.get("/list", response_model=list[question_schema.Question])
# def question_list(request: Request, db: Session = Depends(get_db)):
    
#     _question_list = question_crud.get_question_list(db)
#     # return _question_list
#     return templates.TemplateResponse("index.html", {"request": request,'question_list' : _question_list})

# @router.get("/list", response_model=question_schema.QuestionList)
# def question_list(request: Request, db: Session = Depends(get_db),
#                   page: int = 0, size: int = 10, user: dict = Depends(get_current_user)):
#     total, _question_list = question_crud.get_question_list(
#         db, skip=page*size, limit=size)
    
#     # 총 페이지 수 계산
#     total_pages = total // size + 1
    
#     # 한 화면에 보여줄 페이지 수
#     display_pages = 11
    
#     # 시작 페이지와 끝 페이지 계산
    
#     start_page = max(0, page - (display_pages // 2)) if page >= (display_pages // 2) else 0
#     end_page = min(total_pages, start_page + display_pages)
#     if start_page + display_pages > end_page:
#         start_page = total_pages - display_pages

    
#     # 시작 페이지가 0보다 크면 이전 버튼 표시
#     has_previous = start_page > 0
    
#     # 끝 페이지가 총 페이지 수보다 작으면 다음 버튼 표시
#     has_next = end_page < total_pages

#     return templates.TemplateResponse("index.html", {
#         'request': request, 
#         'total': total,
#         'question_list': _question_list,
#         'page' : page,
#         'size' : size,
#         'start_page': start_page,
#         'end_page': end_page,
#         'has_previous': has_previous,
#         'has_next': has_next,
#         'user' : user
#     })
    

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(request: Request, db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):

    user = get_current_user(request, db)  # 사용자 정보 가져오기

    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size)
    
    # 총 페이지 수 계산
    total_pages = total // size + 1
    
    # 한 화면에 보여줄 페이지 수
    display_pages = 11
    
    # 시작 페이지와 끝 페이지 계산
    
    start_page = max(0, page - (display_pages // 2)) if page >= (display_pages // 2) else 0
    end_page = min(total_pages, start_page + display_pages)
    if start_page + display_pages > end_page:
        start_page = total_pages - display_pages

    
    # 시작 페이지가 0보다 크면 이전 버튼 표시
    has_previous = start_page > 0
    
    # 끝 페이지가 총 페이지 수보다 작으면 다음 버튼 표시
    has_next = end_page < total_pages

    return templates.TemplateResponse("index.html", {
        'request': request, 
        'total': total,
        'question_list': _question_list,
        'page' : page,
        'size' : size,
        'start_page': start_page,
        'end_page': end_page,
        'has_previous': has_previous,
        'has_next': has_next,
        'user' : user
    })





@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, request: Request,  db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    question = question_crud.get_question(db, question_id=question_id)
    
    return templates.TemplateResponse("test.html", {"request": request,'text' : question, "user" : user})

@router.get("/create_site")
def qestion_site(request: Request , user: dict = Depends(get_current_user)):
     return templates.TemplateResponse("question_site.html", {"request": request, "user" : user})


@router.post("/create")
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create, user=current_user)
    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="수정 권한이 없습니다.")  # 403 코드로 변경
    question_crud.update_question(db=db, db_question=db_question, question_update=_question_update)

    
@router.get("/modify/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, request: Request,  db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    question = question_crud.get_question(db, question_id=question_id)
    
    return templates.TemplateResponse("modify_site.html", {"request": request,'text' : question, "user" : user})

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="삭제 권한이 없습니다.")  # 403 코드로 변경
    question_crud.delete_question(db=db, db_question=db_question)
