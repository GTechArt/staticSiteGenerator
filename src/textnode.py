from enum import Enum
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, content, textType, url=None):
        self.text = content
        self.text_type = textType
        #if url == None:
        #    self.url = None
        #else:    
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            raise ValueError(f"ERROR : {other} isn't not TextNode Class")
        
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":""})

        case _:
            raise Exception ("text_type is missing or not recognizing")
            
