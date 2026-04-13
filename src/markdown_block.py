from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_convert import text_to_textnodes, text_node_to_html_node, TextNode, TextType

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

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown_text) -> ParentNode:
    # Create a root HTMLNode
    html_node_root = ParentNode("div", [])

    markdown_blocks = markdown_to_blocks(markdown_text)

    # Create HTMLNode for each blocks
    for block in markdown_blocks:
        node = text_to_children(block)
        html_node_root.children.append(node)

    return html_node_root
    

def text_to_children(markdown_block):
    # 1. Detect the block type of markdown
    # 2. Create a parent_node (with tag correspond block type) for append child LeafNode(HTMLNode)
    # 3. get all text nodes since markdown block text
    # 4. append for each text node convert in leafNode (HTMLNode)
    # 5. and return parent_node    

    match block_to_block_type(markdown_block):
        case BlockType.PARAGRAPH:                
            text_nodes = text_to_textnodes(markdown_block.replace("\n", " "))
            parent_node = ParentNode("p", [])

            for text_node in text_nodes:
                parent_node.children.append(text_node_to_html_node(text_node))

            return parent_node

        case BlockType.HEADING:
            text_nodes = text_to_textnodes(markdown_block)
            head_number = None
            for i in range(len(markdown_block)):
                if markdown_block[i] != "#":
                    head_number = i
                    break
            
            if head_number is None:
                raise ValueError("Issue with header number")
                    
            parent_node = ParentNode(f"h{head_number}", [])

            for text_node in text_nodes:
                new_text = text_node.text[head_number + 1:]
                text_node.text = new_text
                parent_node.children.append(text_node_to_html_node(text_node))

            return parent_node

        case BlockType.CODE:
            split_text = markdown_block.split("\n")[1:-1]
            text = "\n".join(split_text) + "\n"     

            text_node = TextNode(text, TextType.CODE)            
            parent_node = ParentNode("pre", [])
            parent_node.children.append(text_node_to_html_node(text_node))            

            return parent_node

        
        case BlockType.QUOTE:
            split_text = markdown_block.replace("> ", "").split("\n")
            text = " ".join(split_text)
            text_nodes = text_to_textnodes(text)
            parent_node = ParentNode("blockquote", [])

            for text_node in text_nodes:
                parent_node.children.append(text_node_to_html_node(text_node))

            return parent_node
        

        case BlockType.UNORDERED:
            split_text = markdown_block.replace("- ", "").split("\n")
            text = ""
            for e in split_text:
                text += "<li>" + e + "</li>"

            text_nodes = text_to_textnodes(text)
            parent_node = ParentNode("ul", [])
            for text_node in text_nodes:
                parent_node.children.append(text_node_to_html_node(text_node))

            return parent_node

        case BlockType.ORDERED:
            split_text = markdown_block.split("\n")
            text = ""
            for e in split_text:
                text += "<li>" + e[3:] + "</li>"

            text_nodes = text_to_textnodes(text)
            parent_node = ParentNode("ol", [])
            for text_node in text_nodes:
                parent_node.children.append(text_node_to_html_node(text_node))

            return parent_node

        case _:
            raise Exception("Can't found correspondance text to node!")
