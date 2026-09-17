FROM python:3.11-slim

WORKDIR /app

COPY services/publish_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY services/publish_service /app/services/publish_service

ENV PYTHONPATH=/app

CMD ["uvicorn", "services.publish_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
