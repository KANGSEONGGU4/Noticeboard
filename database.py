import contextlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:BOTSU3sXDyMJ1aI@test-notepad-db.flycast:5432"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:BOTSU3sXDyMJ1aI@127.0.0.1:5432/postgres"

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost/test"

# 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# autocommit : 자동 커밋 / autoflush : 자동 플러시 / bind : 세션과 연결할 엔진 지정
# 플러시는 SQLAlchemy에서 세션에 대한 변경 내용을 데이터베이스에 반영하는 작업
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base 클래스를 상속받은 클래스는 데이터베이스 테이블에 대한 매핑을 나타내는 모델 클래스입니다
Base = declarative_base()


# db 세션 객체를 생성한 후에 db.close()를 수행하지 않으면
# SQLAlchemy가 사용하는 컨넥션 풀에 db 세션이 반환되지 않아 문제가 생긴다.
# 파이썬의 contextlib 모듈에 있는 데코레이터
# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        