``` python
from nbreversible import (
    code
)
import sys

sys.stderr.write("this is stderr\n")
sys.stdout.write("this is stdout\n")

# this is stdout
#! this is stderr
```
``` python
sys.stderr.write("err\n")
sys.stderr.write("err\n")
sys.stdout.write("out\n")

# out
#! err
#! err
```
