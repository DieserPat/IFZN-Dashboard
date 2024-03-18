1) environment erstellen:
	python -m venv [name_of_env]
2) env aktivieren:
	- cd [name_of_env]/Scripts
	- activate
	- cd ../..
3) requirements installieren
	pip install -r requirements.txt
4) App ausführen
	flask run

Nur für Bearbeitung der App:
0.0) Erstellen von requirements.txt
	pip freeze > requirements.txt
0.1) App exportieren
	- set FLAS_APP=app.py
	- set FLASK_ENV=development
	- set FLASK_DEBUG=1