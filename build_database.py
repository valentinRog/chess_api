import pymongo
import csv
import chess

client = pymongo.MongoClient("mongodb://db:27017")
client.drop_database("puzzles")
db = client["puzzles"]
collection = db["puzzles"]

buffer = []

with open('puzzles.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["Rating"] = int(row["Rating"])
        row["RatingDeviation"] = int(row["RatingDeviation"])
        row["Popularity"] = int(row["Popularity"])
        row["NbPlays"] = int(row["NbPlays"])
        row["NbPieces"] = len(chess.Board(row["FEN"]).piece_map())
        buffer.append(row)
        if not reader.line_num % 10000:
            collection.insert_many(buffer)
            buffer = []
    collection.insert_many(buffer)
