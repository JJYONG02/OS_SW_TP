# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. .env 파일에 있는 환경 변수들을 파이썬으로 불러오기
load_dotenv()

# 2. 하드코딩 금지! os.getenv를 통해 안전하게 DB 주소 가져오기
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# DB와 통신하는 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 데이터베이스 세션을 생성하는 공장
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델들을 정의할 때 상속받을 베이스 클래스
Base = declarative_base()

# FastAPI 라우터에서 DB 연결을 안전하게 주입받기 위한 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()