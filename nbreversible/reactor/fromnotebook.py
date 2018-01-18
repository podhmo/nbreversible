import contextlib
import nbformat
from .base import Reactor
from prestring.python import Module


class IPYNBReactor(Reactor):
    """convert ipynb file to something"""
    default_format = "python"

    def iterate(self):
        if self.input_port is not None:
            nb = nbformat.read(self.input_port, as_version=4)
        else:
            with open(self.filename) as rf:
                nb = nbformat.read(rf, as_version=4)
        for cell in nb["cells"]:
            yield (cell, )

    @contextlib.contextmanager
    def markdown(self, *, need_execute):
        raise NotImplementedError(">_<")

    @contextlib.contextmanager
    def python(self, *, need_execute):
        prev = None
        m = Module(import_unique=True)
        sm = None
        prepared = False

        def _emit_code(m, source):
            for line in source.strip().split("\n"):
                if line.startswith("%"):
                    m.stmt("# {}".format(line))
                else:
                    m.stmt(line)

        def reaction(cell):
            nonlocal prev, sm, prepared
            typ = cell["cell_type"]

            if prev is not None:
                m.sep()

            source = cell["source"]

            if typ == "markdown":
                m.stmt('"""')
                m.stmt(source.strip())
                m.append('"""')
            elif typ == "code":  # xxx: see cell["language"]
                if sm is None:
                    sm = m.submodule()

                if "import" in source and "nbreversible" in source and "code" in source and "from" in source:
                    prepared = True
                    sm.clear()

                if prev is None or prev != typ:
                    _emit_code(m, source)
                else:
                    if not prepared:
                        sm.from_("nbreversible", "code")

                    cm = m.submodule(newline=False)
                    with cm.with_("code()"):
                        _emit_code(cm, source)
                    if "\n" not in str(cm):
                        cm.clear()

            prev = typ

        yield reaction
        print(m)
