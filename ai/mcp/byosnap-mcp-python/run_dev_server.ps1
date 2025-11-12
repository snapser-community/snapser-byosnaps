# run_server.ps1

$env:FLASK_APP = "app"
$env:FLASK_DEBUG = "true"
$env:FLASK_ENV = "development"

# Run via Waitress for production use
flask run --host=0.0.0.0 --port=5003
