

bringup: venv
	docker-compose up

venv:
	python3 -m venv venv
	. ./activate && pip install -r requirements.txt


