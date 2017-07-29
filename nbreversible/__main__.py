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
                        exec("".join(map(str, buf)), g)
                except:
                    out.write(traceback.format_exc(limit=5).replace(os.getenv("HOME"), "~"))

                output = out.getvalue().strip()
                if output:
                    print("\n#", "\n# ".join(output.split("\n")))

    yield reaction


@contextlib.contextmanager
def notebook(capture):
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
