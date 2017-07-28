default:
	# markdown
	python -m nbreversible --format=markdown 00pretty.py > 00pretty.md
	# notebook
	python -m nbreversible --format=notebook 00pretty.py > 00pretty.ipynb
	jupyter-nbconvert --inplace -y --execute --to=notebook 00pretty.ipynb
