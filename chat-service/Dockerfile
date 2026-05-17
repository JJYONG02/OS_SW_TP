FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app 폴더를 포함한 현재 위치의 모든 파일을 도커 내부로 복사
COPY . .

EXPOSE 8000

# app.main:app 으로 경로가 바뀐 점 주의!
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]