FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN apt-get update && \
    apt-get install -y \
        gcc \
        gettext \
        libpq-dev \
        libpcre3 \
        libpcre3-dev \
        zlib1g-dev \
        libjpeg-dev \
        libpng-dev \
        libfreetype6-dev \
        libssl-dev \
        libffi-dev \
        && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]