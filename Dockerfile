FROM python:3.10


COPY . /KamranProject
COPY ./requirements.txt /temp/requirements.txt

WORKDIR /KamranProject
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


