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
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        split_texts = old_node.text.split(delimiter)

        if len(split_texts) % 2 == 0:
            raise Exception(f"Closing delimiter : '{delimiter}' is missing !")

        for i in range(len(split_texts)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_texts[i], text_type))

    return new_nodes
        


    