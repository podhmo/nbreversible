import os
import traceback
import contextlib
from .. import parselib
from .. import pytransform
from .base import Reactor


class PyReactor(Reactor):
    """convert python code to something"""
    default_format = "notebook"

    def iterate(self):
        t = parselib.parse_file(self.filename)
        return pytransform.cell_events(t)

    @contextlib.contextmanager
    def markdown(self, need_execute):
        from io import StringIO

        g = {}

        def reaction(event, buf):
            with event.markdown(buf):
                if need_execute and event.name == "python":
                    out = StringIO()
                    err = StringIO()
                    try:
                        with contextlib.redirect_stdout(out):
                            with contextlib.redirect_stderr(err):
                                exec("".join(map(str, buf)), g)
                    except:
                        out.write(traceback.format_exc(limit=5).replace(os.getenv("HOME"), "~"))

                    output = out.getvalue().strip()
                    if output:
                        print("\n#", "\n# ".join(output.split("\n")))
                    erroutput = err.getvalue().strip()
                    if erroutput:
                        if not output:
                            print("")
                        print("#!", "\n#! ".join(erroutput.split("\n")))

        yield reaction

    @contextlib.contextmanager
    def notebook(self, need_execute):
        from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, writes_json

        notebook = new_notebook()
        i = 0

        def reaction(event, buf):
            nonlocal i
            if event.name == "markdown":
                output = "".join(map(str, buf)).strip().strip("'").strip('"')
                notebook["cells"].append(new_markdown_cell(output))
            elif event.name == "python":
                i += 1

                # for jupyter's magic commands (e.g. `# %matplotlib inline`)
                for node in buf:
                    if node.prefix and node.prefix.lstrip().startswith("#"):
                        newline = node.prefix.lstrip().lstrip("#").lstrip(" ")
                        if newline.startswith("%"):
                            node.prefix = newline

                notebook["cells"].append(new_code_cell("".join(map(str, buf)), execution_count=i))
            else:
                raise NotImplemented(event.name)

        yield reaction

        if need_execute:
            from nbconvert.preprocessors.execute import executenb
            notebook = executenb(notebook)
        print(writes_json(notebook))
