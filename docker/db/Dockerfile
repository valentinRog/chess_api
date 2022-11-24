FROM python

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT python build_db.py puzzles.csv