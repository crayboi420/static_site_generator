import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_leaf_render_a(self):
        leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            leaf1.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_render_p(self):
        leaf1 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf1.to_html(), "<p>This is a paragraph of text.</p>")

    def test_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
