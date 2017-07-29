TARGET?=00output

gen:
	# python
	python -m nbreversible --format=python Untitled.ipynb > ${TARGET}.py
	# markdown
	python -m nbreversible --format=markdown --execute ${TARGET}.py > ${TARGET}.md
	# notebook
	python -m nbreversible --format=notebook --execute ${TARGET}.py | jupyter-nbconvert --to notebook -y --stdin --stdout --execute > ${TARGET}.ipynb
