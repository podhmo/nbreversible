from nbreversible import (
    code
)
import sys

sys.stderr.write("this is stderr\n")
sys.stdout.write("this is stdout\n")


with code():
    sys.stderr.write("err\n")
    sys.stderr.write("err\n")
    sys.stdout.write("out\n")
