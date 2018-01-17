import re
import sys
import contextlib
from .parselib import StrictPyTreeVisitor
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
from lib2to3.pytree import Leaf


class Visitor(StrictPyTreeVisitor):
    def __init__(self, consume, *, marker="code", collector=None):
        self.marker = marker
        self.collector = collector or Collector(consume)

    def visit_file_input(self, node):
        # iterate only toplevel
        for c in node.children:
            self.visit(c)

    def visit_simple_stmt(self, node):
        self.collector.collect(node)

    def visit_decorated(self, node):
        self.collector.collect(node, event=self.collector.events.CODE)

    visit_for_stmt = visit_try_stmt = visit_if_stmt = visit_funcdef = visit_classdef = visit_decorated

    def visit_with_stmt(self, node):
        if getattr(node.children[1].children[0], "value", None) == self.marker:
            new = True
            for line in squash_block(node):
                self.collector.collect(line, event=self.collector.events.CODE, new=new)
                if new:
                    new = False
        else:
            self.collector.collect(node, event=self.collector.events.CODE)

    def visit_ENDMARKER(self, node):
        self.collector.consume()


class DedentNode:
    type = -1  # dummy for pytree.Node

    def __init__(self, node):
        self.node = node

    @property
    def prefix(self):
        return self.node.prefix

    def __str__(self, rx=re.compile("^ +")):
        internal_string = str(self.node)
        m = rx.search(internal_string.lstrip("\n"))
        if m is None:
            return internal_string
        indent = m.group(0)
        indent_size = len(indent)
        return "\n".join(
            [
                line[indent_size:] if line.startswith(indent) else line
                for line in internal_string.split("\n")
            ]
        )


def squash_block(node):
    found = None
    for c in node.children:
        if c.type == syms.suite:
            found = c
            break

        # rescue comment.
        if c.type == token.NAME:
            if c.prefix:
                yield Leaf(token.COMMENT, "", prefix=c.prefix)

    yield DedentNode(found)


def _surround_with(s, wrapper):
    return s.startswith(wrapper) and s.endswith(wrapper)


class PyCellEvent:
    name = "python"

    def __init__(self, buf=None):
        self.buf = buf or []

    def add(self, stmt):
        self.buf.append(stmt)

    @contextlib.contextmanager
    def markdown(self, buf, file=sys.stdout):
        print("``` {}".format(self.name), file=file)
        print("".join(map(str, buf)).strip(), file=file)
        yield
        print("```", file=file)


class MarkdownCellEvent:
    name = "markdown"

    def __init__(self, buf=None):
        self.buf = buf or []

    def add(self, stmt):
        self.buf.append(stmt)

    @contextlib.contextmanager
    def markdown(self, buf, file=sys.stdout):
        print("", file=file)
        print("".join(map(str, buf)).strip().strip("'").strip('"'), file=file)
        yield
        print("", file=file)


class Collector:
    class events:
        MARKDOWN = MarkdownCellEvent
        CODE = PyCellEvent
        DEFAULT = PyCellEvent

    def __init__(self, cont, events=events):
        self.cont = cont
        self.prev = None
        self.events = events
        self.current = self.events.DEFAULT()

    def guess_event(self, stmt):
        node = stmt.children[0]
        if node.type == token.STRING and (
            _surround_with(node.value, "'''") or _surround_with(node.value, '"""')
        ):
            return self.events.MARKDOWN
        else:
            return self.events.CODE

    def consume(self):
        if self.current.buf and not getattr(self.current, "_used", False):
            self.current._used = True
            self.cont(self.current, self.current.buf)

    def collect(self, stmt, event=None, new=False):
        event, prev_event = (event or self.guess_event(stmt)), self.prev
        self.prev = event
        if event == self.events.MARKDOWN:
            if stmt.prefix.lstrip().startswith("#"):
                if prev_event == event:
                    self.consume()
                    self.current = self.events.CODE()
                stmt = stmt.clone()
                self.current.add(Leaf(token.COMMENT, "", prefix=stmt.prefix))
                stmt.prefix = ""
            self.consume()
            self.current = event()
            self.current.add(stmt)
        elif new or prev_event != event:
            if stmt.type == token.COMMENT:
                # rescue comment.
                self.consume()
                self.current.add(stmt)
                self.current = event()
            else:
                self.consume()
                self.current = event()
                self.current.add(stmt)
        else:
            self.current.add(stmt)


def cell_events(t):
    r = []

    def consume(p, buf):
        r.append((p, buf))

    v = Visitor(consume)
    v.visit(t)
    return iter(r)
