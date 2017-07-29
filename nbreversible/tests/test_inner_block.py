import unittest
import textwrap


def _file_node(nodes):
    from lib2to3.pytree import Node, Leaf
    from lib2to3.pygram import python_symbols as syms
    from lib2to3.pgen2 import token
    return Node(syms.file_input, [*list(nodes), Leaf(token.ENDMARKER, "")])


class Tests(unittest.TestCase):
    def _callFUT(self, node):
        from nbreversible.pytransform import extract_inner_block
        return extract_inner_block(node)

    def _parse(self, code):
        from nbreversible.parselib import parse_string
        return parse_string(code).children[0]

    def test_simple(self):
        code = textwrap.dedent(
            """
        with code():
            two = 1 + 1
            print(two)
        """
        )

        t = self._parse(code)
        inner = self._callFUT(t)

        expected = textwrap.dedent("""
        two = 1 + 1
        print(two)
        """)
        self.assertEqual(str(_file_node(inner)).strip(), expected.strip())

    def test_simple_with_as(self):
        code = textwrap.dedent(
            """
        with code() as x:
            two = 1 + 1
            print(two)
        """
        )

        t = self._parse(code)
        inner = self._callFUT(t)

        expected = textwrap.dedent("""
        two = 1 + 1
        print(two)
        """)
        self.assertEqual(str(_file_node(inner)).strip(), expected.strip())

    def test_with_other_control_flow(self):
        code = textwrap.dedent(
            """
        with code() as x:
            if random.random() > 0.5:
                print("big")
            else:
                print("small")
        """
        )

        t = self._parse(code)
        inner = self._callFUT(t)

        expected = textwrap.dedent("""
        if random.random() > 0.5:
            print("big")
        else:
            print("small")
        """)
        self.assertEqual(str(_file_node(inner)).strip(), expected.strip())

    def test_with_other_control_flow2(self):
        code = textwrap.dedent(
            """
        with code() as x:
            if random.random() > 0.5:
                if random.random() > 0.5:
                    return "TT"
                else:
                    return "TF"
            else:
                if random.random() > 0.5:
                    return "FT"
                else:
                    return "FF"
        """
        )

        t = self._parse(code)
        inner = self._callFUT(t)

        expected = textwrap.dedent("""
        if random.random() > 0.5:
            if random.random() > 0.5:
                return "TT"
            else:
                return "TF"
        else:
            if random.random() > 0.5:
                return "FT"
            else:
                return "FF"
        """)
        self.assertEqual(str(_file_node(inner)).strip(), expected.strip())

    def test_nested(self):
        code = textwrap.dedent(
            """
        with code() as x:
            with open("foo.json") as rf:
                data = json.load(rf)
            print(data)
        """
        )

        t = self._parse(code)
        inner = self._callFUT(t)

        expected = textwrap.dedent("""
        with open("foo.json") as rf:
            data = json.load(rf)
        print(data)
        """)
        self.assertEqual(str(_file_node(inner)).strip(), expected.strip())
