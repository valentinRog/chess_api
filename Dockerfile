FROM python

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD python build_db.py puzzles.csv