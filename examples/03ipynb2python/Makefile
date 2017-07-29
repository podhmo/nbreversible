TARGET?=00display

default:
	TARGET=00display $(MAKE) gen
	TARGET=01graph $(MAKE) gen

gen:
	# python
	python -m nbreversible --format=python ${TARGET}.ipynb > ${TARGET}.py
	# notebook
	python -m nbreversible --format=notebook ${TARGET}.py > ${TARGET}.new.ipynb
	jupyter-nbconvert --inplace -y --execute --to=notebook ${TARGET}.new.ipynb
