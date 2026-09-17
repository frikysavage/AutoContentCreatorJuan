FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY services/assembly_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared
COPY services/assembly_service /app/services/assembly_service

ENV PYTHONPATH=/app

CMD ["uvicorn", "services.assembly_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
