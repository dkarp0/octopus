FROM python:3.6-alpine

MAINTAINER danielkarpinski

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

RUN mkdir -p /root/nltk_data
COPY nltk /root/nltk_data

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR $INSTALL_PATH
COPY static static
COPY *.py ./

RUN pytest -v

EXPOSE 8080
CMD python app.py