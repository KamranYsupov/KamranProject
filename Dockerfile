FROM python:3.10


COPY . /KAMRAN
WORKDIR /KAMRAN
EXPOSE 8000

#RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r ./requirements.txt

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]