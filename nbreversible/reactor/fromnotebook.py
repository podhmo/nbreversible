import contextlib
import nbformat
from .base import Reactor
from prestring.python import Module


class IPYNBReactor(Reactor):
    """convert ipynb file to something"""

    def iterate(self):
        with open(self.filename) as rf:
            nb = nbformat.read(rf, as_version=4)
        for cell in nb["cells"]:
            yield (cell, )

    @contextlib.contextmanager
    def markdown(self, need_execute):
        raise NotImplementedError(">_<")

    @contextlib.contextmanager
    def python(self, need_execute):
        prev = None
        m = Module()
        sm = m.submodule()

        def reaction(cell):
            nonlocal prev
            typ = cell["cell_type"]

            if prev is not None:
                m.sep()

            if typ == "markdown":
                m.stmt('"""')
                m.stmt(cell["source"])
                m.stmt('"""')
            elif typ == "code":  # xxx: see cell["language"]
                if prev is None or prev == typ:
                    sm.stmt("from nbreversible import code")
                    with m.with_("code"):
                        for line in (cell["source"]):
                            m.append(line)
                for line in (cell["source"]):
                    m.append(line)
            prev = typ

        yield reaction
        print(m)
