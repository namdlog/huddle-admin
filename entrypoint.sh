#!/bin/sh
python main.py db migrate
python main.py db upgrade
python main.py runserver 0.0.0.0:5000