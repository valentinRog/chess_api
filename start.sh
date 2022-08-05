#!/bin/sh

python build_database.py
gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:80