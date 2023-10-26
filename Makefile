dirs := lkdlt

check:
	black --check $(dirs)
	isort --check-only $(dirs)
	mypy $(dirs)
	flake8 --count
	pylint $(dirs)

.PHONY: check
