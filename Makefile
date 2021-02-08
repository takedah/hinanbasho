.PHONY: init
init:
	pip install -r requirements.txt
	python import_opendata.py
	python import_post_office_csv.py

formatter:
	isort --force-single-line-imports .
	autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables .
	black .
	isort --multi-line 3 .
