import argparse
import contextlib
from nbreversible import pytransform
from nbreversible import parselib


@contextlib.contextmanager
def markdown():
    yield lambda event, buf: event.markdown(buf)  # NOQA


@contextlib.contextmanager
def notebook():
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
    args = parser.parse_args()

    t = parselib.parse_file(args.src)
    with globals()[args.format]() as reaction:
        for e, buf in pytransform.cell_events(t):
            reaction(e, buf)


if __name__ == "__main__":
    main()
