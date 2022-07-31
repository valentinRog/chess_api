FROM python

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "build_database.py"]