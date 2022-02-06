FROM tensorflow/tensorflow:latest

RUN apt-get update
RUN apt-get install -y python pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ /opt/app/
WORKDIR /opt/app

EXPOSE 5000
ENV FLASK_APP=app.py

ENTRYPOINT flask run --host=0.0.0.0