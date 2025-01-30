.PHONY: test install_requirements run_scraper

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/

run:
	python -m src.main --query "Software Engineer in Ethiopia"