import argparse
from nbreversible import pytransform
from nbreversible import parselib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("--format", default="markdown", choices=["markdown"])
    args = parser.parse_args()

    t = parselib.parse_file(args.src)
    for e, buf in pytransform.cell_events(t):
        getattr(e, args.format)(buf)


if __name__ == "__main__":
    main()
