# run_server.ps1

$env:FLASK_APP = "app"
$env:FLASK_DEBUG = "true"
$env:FLASK_ENV = "development"

# Run via Waitress for production use
python app.py
