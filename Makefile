install:
	@pip install -e .

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -rf */.ipynb_checkpoints
	@rm -Rf build
	@rm -Rf */__pycache__
	@rm -Rf */*.pyc
	@echo "🧽 Cleaned up successfully!"

all: install clean

test:
	@pytest -v tests


git_merge:
	$(MAKE) clean
	$(MAKE) lint
	@python auto_git/git_merge.py

git_push:
	$(MAKE) clean
	$(MAKE) lint
	@python auto_git/git_push.py


lint:
	@black .

