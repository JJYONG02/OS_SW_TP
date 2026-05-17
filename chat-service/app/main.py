from fastapi import FastAPI
from app.routers import chat

app = FastAPI(
    title="Campus Used Marketplace - Chatting Service",
    version="1.0.0"
)

# chat 라우터 코드를 메인 시스템에 마운트
app.include_router(chat.router)

# 서버가 살아있는지 확인
@app.get("/")
def health_check():
    return {"status": "healthy", "service": "chat-service"}