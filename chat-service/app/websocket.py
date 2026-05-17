from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        # { 1(채팅방ID): [A 웹소켓, B 웹소켓] } 구조
        self.active_connections: Dict[int, List[WebSocket]] = {}

    # 1. [유저가 채팅방 입장을 시도할 때 연결을 수락하고 명단에 등록]
    async def connect(self, room_id: int, websocket: WebSocket):
        await websocket.accept()  # 유저의 웹소켓 연결 요청을 수락
        
        # 만약 처음 생성된 방이면, 딕셔너리에 추가
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            
        # 방 리스트 안에 현재 접속한 유저의 웹소켓 추가
        self.active_connections[room_id].append(websocket)

    # 2. [유저가 창을 닫거나 나가서 연결이 끊어졌을 때 명단에서 지워줌]
    def disconnect(self, room_id: int, websocket: WebSocket):
        if room_id in self.active_connections:
            # 해당 방 리스트에서 유저 세션을 제거
            self.active_connections[room_id].remove(websocket)
            
            # 방에 아무도 업어서 리스트가 비었다면, 메모리 절약을 위해 방 자체를 딕셔너리에서 지움
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    # 3. [방에 메시지를 브로드캐스트]
    async def broadcast_to_room(self, room_id: int, message: dict):
        # 메시지를 보낼 방이 명단에 존재하는지 확인
        if room_id in self.active_connections:
            # 그 방의 리스트에 담겨있는 모든 유저의 웹소켓 통로를 꺼냄
            for connection in self.active_connections[room_id]:
                # 꺼내온 통로를 통해 JSON 형태의 데이터를 실시간으로 전송
                await connection.send_json(message)

# 인스턴스 미리 생성
manager = ConnectionManager()