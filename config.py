SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{address}:{port}/{database}".format(
    user="root",
    password="root",
    address="localhost",
    port="3306",
    database="puzzles"
)
# SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{address}:{port}/{database}".format(
#     user="valenbel123",
#     password="mysqlpassword",
#     address="valenbel123.mysql.pythonanywhere-services.com",
#     port="3306",
#     database="valenbel123$puzzles"
# )
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_POOL_TIMEOUT = 20