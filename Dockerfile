FROM python:3.12

WORKDIR /app
COPY ./requirements.txt /requirements.txt
COPY ./app /app

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8666

CMD ["python", "/app/main.py"]

