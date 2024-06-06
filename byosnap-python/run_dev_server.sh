#!/usr/bin/env bash
export FLASK_APP=jinks_flask
export FLASK_DEBUG=true
export FLASK_ENV=development
# flask run
# For production
flask run --host=0.0.0.0 --port=5003