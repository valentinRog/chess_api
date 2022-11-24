FROM python

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD gunicorn -w 2 -b 0.0.0.0:80 app:app