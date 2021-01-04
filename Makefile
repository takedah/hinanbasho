.PHONY: init
init:
	pip install -r requirements.txt
	python import_opendata.py
	python import_post_office_csv.py
