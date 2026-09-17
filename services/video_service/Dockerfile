FROM python:3.11-slim

WORKDIR /app

COPY services/video_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY services/video_service /app/services/video_service

ENV PYTHONPATH=/app

CMD ["uvicorn", "services.video_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
