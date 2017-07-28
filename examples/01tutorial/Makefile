TARGET=01controlflow

default:
	# markdown
	python -m nbreversible --format=markdown ${TARGET}.py > ${TARGET}.md
	# notebook
	python -m nbreversible --format=notebook ${TARGET}.py > ${TARGET}.ipynb
	jupyter-nbconvert --inplace -y --execute --to=notebook ${TARGET}.ipynb
