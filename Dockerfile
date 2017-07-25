FROM gcr.io/google-appengine/python

MAINTAINER danielkarpinski

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

RUN mkdir -p /root/nltk_data
COPY nltk /root/nltk_data

RUN pip3.6 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3.6 install -r requirements.txt

WORKDIR $INSTALL_PATH
COPY static static
COPY templates templates
COPY *.py ./
COPY public.pem public.pem

RUN pytest -v

EXPOSE 8080
CMD python3.6 app.py