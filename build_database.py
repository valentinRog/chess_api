import pymongo
import csv
import chess

client = pymongo.MongoClient("mongodb://db:27017")
db = client["puzzles"]
collection = db["puzzles"]

csvfile = open('puzzles.csv', 'r')
reader = csv.reader(csvfile)

with open('puzzles.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["Rating"] = int(row["Rating"])
        row["RatingDeviation"] = int(row["RatingDeviation"])
        row["Popularity"] = int(row["Popularity"])
        row["NbPlays"] = int(row["NbPlays"])
        row["NbPieces"] = len(chess.Board(row["FEN"]).piece_map())
        collection.insert_one(row)
