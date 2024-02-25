FROM python:3.10


COPY . /KAMRAN
COPY ./requirements.txt /temp/requirements.txt
WORKDIR /KAMRAN
EXPOSE 8000

RUN  pip install --upgrade pip

RUN pip install -r /temp/requirements.txt


