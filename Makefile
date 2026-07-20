.PHONY: install pipeline test coverage lint validate dashboard

install:
	python -m pip install -r requirements-dev.txt

pipeline:
	python run_pipeline.py

test:
	python -m pytest -q

coverage:
	python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80

lint:
	python -m ruff check .

validate:
	python validate_project.py

dashboard:
	python -m streamlit run app.py
