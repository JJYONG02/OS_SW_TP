# app/models.py
from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

# 1. 회원 테이블 매핑 (태규/재현 로그인 연동용)
class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)

# 2. 중고거래 게시글 테이블 매핑 (재현이 posts 스크립트 완벽 일치)
class Post(Base):
    __tablename__ = "posts"
    post_id = Column(BigInteger, primary_key=True, index=True)
    seller_id = Column(BigInteger, nullable=False)  # 물품 판매자 ID
    title = Column(String(255), nullable=False)

# 3. 1:1 중고거래 채팅방 테이블
class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    room_id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, nullable=False)     # 어떤 물품글에서 시작되었는가
    buyer_id = Column(BigInteger, nullable=False)    # 대화를 건 구매자 ID
    seller_id = Column(BigInteger, nullable=False)   # 자동 추출된 판매자 ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 4. [추가] 실시간 대화 기록을 저장할 채팅 메시지 테이블
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    message_id = Column(BigInteger, primary_key=True, index=True)
    room_id = Column(BigInteger, nullable=False)     # 소속된 채팅방 ID
    user_id = Column(BigInteger, nullable=False)     # 발신자 ID
    content = Column(Text, nullable=False)           # 대화 내용
    message_type = Column(String(20), default="TEXT") # 2차 확장용 (TEXT, IMAGE, PAYMENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())