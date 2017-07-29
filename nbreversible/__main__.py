import argparse
from nbreversible.reactor import get_reactor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("-f", "--format", default=None, choices=["markdown", "notebook", "python"])
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    reactor = get_reactor(args.src)
    format = args.format
    if format is None:
        format = reactor.default_format
    with getattr(reactor, format)(args.execute) as reaction:
        for args in reactor.iterate():
            reaction(*args)


if __name__ == "__main__":
    main()
