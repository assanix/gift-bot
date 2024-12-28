FROM python:3.11-slim


RUN apt-get update  \
    && apt-get -y install tesseract-ocr libtesseract-dev  \
    && apt-get -y install ffmpeg libsm6 libxext6


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .


ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

CMD ["python", "main.py"]
