from enum import Enum

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
