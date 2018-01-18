TARGET=01controlflow

default:
	# markdown
	python -m nbreversible --execute --format=markdown ${TARGET}.py > ${TARGET}.md
	# # notebook
	python -m nbreversible --format=notebook ${TARGET}.py > ${TARGET}.ipynb
	jupyter-nbconvert --inplace -y --execute --to=notebook ${TARGET}.ipynb
