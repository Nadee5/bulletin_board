FROM python:3

WORKDIR /bulletin_board

COPY ./requirements.txt /code/

RUN pip install -r /code/requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1