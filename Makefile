test:
	python -m pytest .

publish: test
	rm dist/ -r
	python setup.py sdist
	python setup.py bdist_wheel
	python -m twine upload dist/*

.PHONY: test publish
