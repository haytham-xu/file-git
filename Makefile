
run:
	python3 main.py
test:
	python3 -m unittest discover -p "*.py"
	# python -m unittest FOLDER.CLASS.FUNCTION
freeze:
	pip3 freeze > requirements.txt
install:
	pip3 install -r requirements.txt
