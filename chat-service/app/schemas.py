from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

# 성공 응답 형식
class SuccessResponse(BaseModel):
    success: bool = True          # 기본값으로 True를 가짐. 모든 정상 응답에 필수 포함
    data: Optional[Any] = None    # 결과 데이터, 없을 수도 있어서 Optional 처리
    message: str = "요청 성공"     # 프론트엔드에 띄우는 한글 메시지 기본값

# 채팅방을 만들 때 백엔드로 보내는 데이터
class ChatRoomCreate(BaseModel):
    # '...'은 생략할 수 없는 '필수값'
    post_id: int = Field(..., description="연계된 중고거래 물품 게시글 ID")
    buyer_id: int = Field(..., description="대화를 시작하는 구매 희망자 ID")

# 메시지 포맷
class MessagePayload(BaseModel):
    room_id: int                  # 어떤 채팅방에서 발생한 메시지인지 구분하는 ID
    user_id: int                  # 이 메시지를 보낸 유저가 누구인지 식별하는 ID
    content: str                  # 메시지 텍스트 내용. (추후 이미지 등 확장 가능..)
    message_type: str = "TEXT"    # 기본은 TEXT, 나중에 IMAGE/PAYMENT등 확장
    created_at: datetime = Field(default_factory=datetime.now) # 메시지가 생성될 때 컴퓨터 시스템 시간을 입력