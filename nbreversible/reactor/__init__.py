from .frompython import PyReactor


def get_reactor(filename):
    return PyReactor(filename)
