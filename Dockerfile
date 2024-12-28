FROM python:3.11-slim


RUN apt-get update  \
    && apt-get -y install tesseract-ocr libtesseract-dev  \
    && apt-get -y install ffmpeg libsm6 libxext6


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app
WORKDIR /app


ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

CMD ["python", "main.py"]
