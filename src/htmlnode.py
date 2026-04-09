class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # <p>, <a>...
        self.value = value # text, img ...
        self.children = children # HTMLNode List representating children of this Node
        self.props = props # representing the attributes html tag, ex: "href"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        html_text = ""
        for key in self.props.keys():
            html_text += " " + key + '="' + self.props[key] + '"'

        return html_text
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        #return super().to_html()
        if self.value is None:
            raise ValueError("value is 'None'")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is 'None'")
        
        if self.children is None:
            raise ValueError("children is missing or None")
        
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            if child is None:
                raise ValueError("child is missing or None")
            html_string += child.to_html()

        html_string += f"</{self.tag}>"

        return html_string
    

    
        
