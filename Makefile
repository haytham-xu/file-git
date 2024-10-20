
run:
	python main.py
test:
	python -m unittest discover -p "*.py" -v -f
	# python -m unittest uttest.test_command_push.TestCommandPush.test_command_push_encrypted -v -f
freeze:
	pip3 freeze > requirements.txt
install:
	pip3 install -r requirements.txt
