import os.path


def get_reactor_from_filename(filename):
    ext = os.path.splitext(filename)[1]
    if ext == ".ipynb":
        fmt = "notebook"
    else:
        fmt = "python"
    return get_reactor_factory(fmt)(filename)


def get_reactor_from_format(fmt, *, input_port):
    return get_reactor_factory(fmt)(None, input_port=input_port)


def get_reactor_factory(fmt):
    if fmt == "notebook":
        from .fromnotebook import IPYNBReactor
        return IPYNBReactor
    elif fmt == "python":
        from .frompython import PyReactor
        return PyReactor
    else:
        raise ValueError("invalid format: {}".format(fmt))
