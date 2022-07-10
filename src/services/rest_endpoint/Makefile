.PHONY: deps

run: setup
	. .venv/bin/activate && DATABASE_HOST=localhost uvicorn src.main:app --reload --host 0.0.0.0 --port 5000


setup: .venv deps

.venv:
	python3 -m venv .venv

deps:
	. .venv/bin/activate && pip install -r requirements.txt


distclean:
	rm -rf .venv/
