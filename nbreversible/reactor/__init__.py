import os.path


def get_reactor(filename):
    ext = os.path.splitext(filename)[1]
    if ext == ".ipynb":
        from .fromnotebook import IPYNBReactor
        return IPYNBReactor(filename)
    else:
        from .frompython import PyReactor
        return PyReactor(filename)
