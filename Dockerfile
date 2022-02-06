FROM tensorflow/tensorflow:latest

RUN apt-get update
RUN apt-get install -y python pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ /opt/app/
WORKDIR /opt/app

ENTRYPOINT FLASK_APP=app.py flask run --host=0.0.0.0