from nbreversible import code

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

with code():
    from pydataset import data
    quakes = data('quakes')
    quakes.head()
    quakes.tail()
