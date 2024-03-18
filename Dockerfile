FROM python:3.10


COPY . /kamranproject
COPY ./requirements.txt /temp/requirements.txt
WORKDIR /kamranproject
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  pip install --upgrade pip
RUN pip install -r /temp/requirements.txt


