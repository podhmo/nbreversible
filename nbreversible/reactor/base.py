class Reactor:
    """almost interface"""

    def __init__(self, filename):
        self.filename = filename

    def iterate(self):
        raise NotImplementedError()

    def markdown(self):
        raise NotImplementedError()

    def notebook(self):
        raise NotImplementedError()

    def python(self):
        raise NotImplementedError()
