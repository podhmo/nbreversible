class Reactor:
    """almost interface"""

    def __init__(self, filename, *, input_port=None):
        self.filename = filename
        self.input_port = input_port

    def iterate(self):
        raise NotImplementedError()

    def markdown(self):
        raise NotImplementedError()

    def notebook(self):
        raise NotImplementedError()

    def python(self):
        raise NotImplementedError()
