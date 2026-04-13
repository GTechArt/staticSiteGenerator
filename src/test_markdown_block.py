import unittest
from markdown_block import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_exessive_newlines(self):
        md = """
# This is a heading



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.




- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_block_to_block_type_heading(self):
        text = "#### Title 4"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_paragraphs_one_line(self):
        md = "This is **bolded** paragraph, text in a p, tag here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph, text in a p, tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_header(self):
        html = markdown_to_html_node("## Title 2").to_html()
        self.assertEqual(html, "<div><h2>Title 2</h2></div>")
        html = markdown_to_html_node("###### Title 6").to_html()
        self.assertEqual(html, "<div><h6>Title 6</h6></div>")

    def test_quote(self):
        html = markdown_to_html_node("> Hello there !").to_html()
        self.assertEqual(html, "<div><blockquote>Hello there !</blockquote></div>")

        text = """
> Hello there !
> another lines !
"""
        html = markdown_to_html_node(text).to_html()
        self.assertEqual(html, "<div><blockquote>Hello there ! another lines !</blockquote></div>")

    def test_unordered_list(self):
        text = """
- Neil Armstrong
- Alan Bean
- Peter Conrad
- Edgar Mitchell
- Alan Shepard
"""
        html = markdown_to_html_node(text).to_html()
        self.assertEqual(html, "<div><ul><li>Neil Armstrong</li><li>Alan Bean</li><li>Peter Conrad</li><li>Edgar Mitchell</li><li>Alan Shepard</li></ul></div>")

    def test_ordered_list(self):
        text = """
1. Mix flour, baking powder, sugar, and salt.
2. In another bowl, mix eggs, milk, and oil.
3. Stir both mixtures together.
4. Fill muffin tray 3/4 full.
5. Bake for 20 minutes.
"""
        html = markdown_to_html_node(text).to_html()
        self.assertEqual(html, "<div><ol><li>Mix flour, baking powder, sugar, and salt.</li><li>In another bowl, mix eggs, milk, and oil.</li><li>Stir both mixtures together.</li><li>Fill muffin tray 3/4 full.</li><li>Bake for 20 minutes.</li></ol></div>")


    #@unittest.skip("test_paragraphs() first !")
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()