import sys
import argparse
from nbreversible.reactor import (
    get_reactor_from_filename,
    get_reactor_from_format,
)


def main():
    parser = argparse.ArgumentParser()

    src_group = parser.add_mutually_exclusive_group()
    src_group.add_argument("src", nargs="?")
    src_group.add_argument("-i", "--input-format", default=None, choices=["notebook", "python"])

    parser.add_argument("-f", "--format", default=None, choices=["markdown", "notebook", "python"])
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    if args.input_format is not None:
        reactor = get_reactor_from_format(args.input_format, input_port=sys.stdin)
    else:
        reactor = get_reactor_from_filename(args.src)

    format = args.format
    if format is None:
        format = reactor.default_format
    with getattr(reactor, format)(need_execute=args.execute) as reaction:
        for args in reactor.iterate():
            reaction(*args)


if __name__ == "__main__":
    main()
