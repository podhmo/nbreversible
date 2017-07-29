TARGET=testv3

default:
	# python
	python -m nbreversible --format=python ${TARGET}.ipynb > ${TARGET}.py
	# notebook
	python -m nbreversible --format=notebook ${TARGET}.py > ${TARGET}.new.ipynb
	jupyter-nbconvert --inplace -y --execute --to=notebook ${TARGET}.new.ipynb
