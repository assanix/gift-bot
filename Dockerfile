FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Запускаем приложение
CMD ["python", "main.py"]
