``` python
from nbreversible import code

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
```
``` python
from pydataset import data
quakes = data('quakes')
quakes.head()
quakes.tail()
```
