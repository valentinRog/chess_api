SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{address}:{port}/{database}".format(
    user="root",
    password="root",
    address="localhost",
    port="3306",
    database="puzzles"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_POOL_TIMEOUT = 20
