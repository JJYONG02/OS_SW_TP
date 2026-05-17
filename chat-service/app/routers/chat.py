# app/routers/chat.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.schemas import SuccessResponse, ChatRoomCreate, MessagePayload
from app.websocket import manager
from app import models

router = APIRouter(prefix="/api/chat", tags=["CampusChat"])

# -------------------------------------------------------------------------
# [HTTP API] 1:1 채팅방 개설 창구 (수정사항 PDF 시나리오 100% 반영)
# -------------------------------------------------------------------------
@router.post("/rooms", response_model=SuccessResponse)
async def create_chat_room(room_data: ChatRoomCreate, db: Session = Depends(get_db)):
    """
    구매자가 게시물을 보고 '채팅방 생성' 버튼을 눌렀을 때의 방어 및 개설 로직
    """
    # [시나리오 1단계] 실제 DB의 posts 테이블에서 해당 물품의 seller_id를 조회한다.
    post = db.query(models.Post).filter(models.Post.post_id == room_data.post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "error": {"code": "POST_NOT_FOUND", "message": "존재하지 않는 상품 게시글입니다."}}
        )
        
    # [시나리오 2-2단계] 만약 구매자의 user_id와 그 게시물의 seller_id가 같다면, 채팅방 만들기 실패.
    if room_data.buyer_id == post.seller_id:
        return SuccessResponse(
            success=False,
            message="채팅방 개설 실패",
            data={"error_code": "SELF_TRANSACTION_FORBIDDEN", "reason": "자신이 올린 판매글에서는 대화방을 만들 수 없습니다."}
        )

    # [시나리오 2-1단계] 다를 경우, 기존에 동일한 post_id와 buyer_id로 개설된 방이 있는지 확인.
    existing_room = db.query(models.ChatRoom).filter(
        models.ChatRoom.post_id == room_data.post_id,
        models.ChatRoom.buyer_id == room_data.buyer_id
    ).first()

    # [시나리오 3-2단계] 만약 이미 채팅방을 만든 적이 있다면, 기존 방 정보를 넘겨주며 이동시킨다.
    if existing_room:
        return SuccessResponse(
            success=True,
            data={
                "room_id": existing_room.room_id,
                "post_id": existing_room.post_id,
                "buyer_id": existing_room.buyer_id,
                "seller_id": existing_room.seller_id,
                "created_at": existing_room.created_at
            },
            message="이미 개설된 대화방이 존재하므로 기존 채팅방으로 이동합니다."
        )

    # [시나리오 3-1단계] 만든 적이 없다면, 판매자 ID(seller_id)를 매칭하여 실제 DB에 저장 (성공)
    new_room = models.ChatRoom(
        post_id=room_data.post_id,
        buyer_id=room_data.buyer_id,
        seller_id=post.seller_id
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return SuccessResponse(
        success=True,
        data={
            "room_id": new_room.room_id,
            "post_id": new_room.post_id,
            "buyer_id": new_room.buyer_id,
            "seller_id": new_room.seller_id,
            "created_at": new_room.created_at
        },
        message="새로운 1:1 중고거래 채팅방이 성공적으로 개설되었습니다!"
    )

# -------------------------------------------------------------------------
# [HTTP API] 참여 중인 채팅방 목록 모아보기 (구매자/판매자 통합 조회)
# -------------------------------------------------------------------------
@router.get("/rooms/{user_id}", response_model=SuccessResponse)
async def get_user_chat_rooms(user_id: int, db: Session = Depends(get_db)):
    """
    내가 구매자이거나 판매자로 등록되어 있는 모든 실제 DB 채팅방 목록을 긁어온다.
    """
    rooms = db.query(models.ChatRoom).filter(
        (models.ChatRoom.buyer_id == user_id) | (models.ChatRoom.seller_id == user_id)
    ).all()
    
    user_rooms = []
    for r in rooms:
        user_rooms.append({
            "room_id": r.room_id,
            "post_id": r.post_id,
            "buyer_id": r.buyer_id,
            "seller_id": r.seller_id,
            "created_at": r.created_at
        })
        
    return SuccessResponse(data=user_rooms, message="참여 중인 채팅방 목록 조회가 완료되었습니다.")

# -------------------------------------------------------------------------
# [실시간 웹소켓] 대화방 입장 및 실시간 메시지 송수신 + 실제 DB 누적 저장
# -------------------------------------------------------------------------
@router.websocket("/ws/{room_id}/{user_id}")
async def chat_websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int):
    # 연결 검증: 실제 DB에 개설된 채팅방이 맞는지 체크하고 없으면 차단
    db_check = SessionLocal()
    room_exists = db_check.query(models.ChatRoom).filter(models.ChatRoom.room_id == room_id).first()
    db_check.close()
    
    if not room_exists:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 정식 세션 입장
    await manager.connect(room_id, websocket)
    
    try:
        while True:
            # 1. 프론트엔드로부터 실시간 메시지 텍스트 수신
            raw_text = await websocket.receive_text()
            
            if not raw_text.strip():
                continue
                
            # 2. 실제 DB의 chat_messages 테이블에 대화 내용 영구 저장 
            db_save = SessionLocal() # 메시지 저장용 독립 DB 세션 가동
            try:
                db_message = models.ChatMessage(
                    room_id=room_id,
                    user_id=user_id,
                    content=raw_text,
                    message_type="TEXT"
                )
                db_save.add(db_message)
                db_save.commit()  # 🔴 하드디스크에 대화 내용 각인 완료!
                db_save.refresh(db_message)
                
                # 브로드캐스트용 데이터 페이로드 구성
                payload = MessagePayload(
                    room_id=db_message.room_id,
                    user_id=db_message.user_id,
                    content=db_message.content,
                    message_type=db_message.message_type,
                    created_at=db_message.created_at
                )
            finally:
                db_save.close() # 저장 처리가 끝나면 즉시 세션 반환 (커넥션 풀 관리)
            
            # 3. 방에 붙어있는 상대방과 나에게 실시간 메시지 동시 배달
            await manager.broadcast_to_room(room_id, payload.model_dump(mode="json"))
            
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)