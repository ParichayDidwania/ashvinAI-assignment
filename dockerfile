FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    gcc

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "__init__.py" ]
