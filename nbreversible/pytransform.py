import sys
import contextlib
from .parselib import (
    StrictPyTreeVisitor,
    PyTreeVisitor,
)
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
from lib2to3.pytree import Leaf


class _LiftupVisitor(PyTreeVisitor):
    def __init__(self, indent):
        self.indent = indent

    def visit_INDENT(self, node):
        node.value = node.value.replace(self.indent.value, "", 1)

    def visit_DEDENT(self, node):
        node.prefix = node.prefix.replace(self.indent.value, "", 1)


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
            for line in extract_inner_block(node):
                self.collector.collect(line, event=self.collector.events.CODE, new=new)
                if new:
                    new = False
        else:
            self.collector.collect(node, event=self.collector.events.CODE)

    def visit_ENDMARKER(self, node):
        self.collector.consume()


def extract_inner_block(node, *, liftup_visitor=_LiftupVisitor(Leaf(token.INDENT, "    "))):
    found = None
    for c in node.children:
        if c.type == syms.suite:
            found = c
            break

    indent_level = 0
    for subnode in found.children:
        if subnode.type == token.INDENT:
            indent_level += 1
            continue
        if subnode.type == token.DEDENT:
            indent_level -= 1
            if indent_level <= 0:
                break
        if indent_level > 0:
            subnode = subnode.clone()
            indent_space = liftup_visitor.indent.value
            if subnode.prefix:
                subnode.prefix = "\n".join(
                    (line[len(indent_space):] if line.startswith(indent_space) else line)
                    for line in subnode.prefix.split("\n")
                )
            if subnode.type != syms.simple_stmt:
                liftup_visitor.visit(subnode)
            yield subnode


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
            if stmt.prefix.lstrip(" ").startswith("#"):
                stmt = stmt.clone()
                self.current.add(Leaf(token.COMMENT, stmt.prefix))
                stmt.prefix = ""
            self.consume()
            self.current = event()
            self.current.add(stmt)
        elif new or prev_event != event:
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
