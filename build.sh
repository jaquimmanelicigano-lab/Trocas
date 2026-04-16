#!/bin/bash
pip install --upgrade pip
pip install -r requirements.txt
python -m gunicorn app:app --workers 1 --timeout 120