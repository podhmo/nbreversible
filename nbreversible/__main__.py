import argparse
from nbreversible.reactor import get_reactor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument(
        "-f", "--format", default="notebook", choices=["markdown", "notebook", "python"]
    )
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    reactor = get_reactor(args.src)
    with getattr(reactor, args.format)(args.execute) as reaction:
        for args in reactor.iterate():
            reaction(*args)


if __name__ == "__main__":
    main()
