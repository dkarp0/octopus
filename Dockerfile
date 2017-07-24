FROM python:3.6-alpine

MAINTAINER danielkarpinski

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR $INSTALL_PATH
COPY app.py app.py

EXPOSE 8080
CMD python app.py