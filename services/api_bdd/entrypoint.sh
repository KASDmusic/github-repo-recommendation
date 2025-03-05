#!/bin/sh
python init_bdd.py
uvicorn api_bdd:app --host 0.0.0.0 --port 2100
