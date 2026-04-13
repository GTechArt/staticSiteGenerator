from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def markdown_to_blocks(markdown_text):
    split_string = markdown_text.split("\n\n")

    blocks = []
    for e in split_string:
        if e != "":
            e = e.strip()
            blocks.append(e)
    return blocks

def block_to_block_type(markdown_block):
    if markdown_block.startswith("#"):
        return BlockType.HEADING

    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    elif markdown_block[0].startswith(">"):
        return BlockType.QUOTE
    
    elif markdown_block.startswith("- "):
        return BlockType.UNORDERED
    
    elif markdown_block[0].isdigit() and markdown_block[1:3] == ". ":
        return BlockType.ORDERED
    
    else:
        return BlockType.PARAGRAPH