SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{address}:{port}/{database}".format(
    user="root",
    password="root",
    address="10.0.0.5",
    port="3306",
    database="puzzles"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
PUZZLES_CSV_FILE = "puzzles.csv"
