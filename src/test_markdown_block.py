import unittest
from markdown_block import BlockType, markdown_to_blocks, block_to_block_type

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

    def test_block_to_block_type_code(self):
        text = "```stdout(hello!)\nreturn test```"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        text = ">Hello there !"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered(self):
        text = "- One\n- Two\n- Three"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.UNORDERED)

    def test_block_to_block_type_ordered(self):
        text = "1. One\n2. Two\n3. Three"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.ORDERED)

    def test_block_to_block_type_paragraph(self):
        text = "I'm a simple paragraph...\nYes, just simple !"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()