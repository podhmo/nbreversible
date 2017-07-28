import os
import argparse
import contextlib
import traceback
from nbreversible import pytransform
from nbreversible import parselib


@contextlib.contextmanager
def markdown(capture):
    from io import StringIO

    g = {}

    def reaction(event, buf):
        with event.markdown(buf):
            if capture and event.name == "python":
                out = StringIO()
                try:
                    with contextlib.redirect_stdout(out):
                        exec("".join(buf), g)
                except:
                    out.write(traceback.format_exc(limit=5).replace(os.getenv("HOME"), "~"))

                output = out.getvalue().strip()
                if output:
                    print("\n#", "\n# ".join(output.split("\n")))

    yield reaction


@contextlib.contextmanager
def notebook(capture):
    from nbformat.v4 import new_code_cell, new_notebook, writes_json

    notebook = new_notebook()
    i = 0

    def reaction(event, buf):
        nonlocal i
        i += 1
        notebook["cells"].append(new_code_cell("".join(buf), execution_count=i))

    yield reaction
    print(writes_json(notebook))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("-f", "--format", default="notebook", choices=["markdown", "notebook"])
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()

    t = parselib.parse_file(args.src)
    with globals()[args.format](args.capture) as reaction:
        for e, buf in pytransform.cell_events(t):
            reaction(e, buf)


if __name__ == "__main__":
    main()
