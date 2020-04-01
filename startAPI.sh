#! /bin/bash
source .venv/flaskdev/bin/activate
cd api/
FLASK_APP=bandwidthAPI.py flask run