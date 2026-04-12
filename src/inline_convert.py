import re
from textnode import TextNode, TextType
from htmlnode import LeafNode


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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_texts = old_node.text.split(delimiter)

        if len(split_texts) % 2 == 0:
            raise ValueError(f"Closing delimiter : '{delimiter}' is missing !")

        split_nodes = []
        for i in range(len(split_texts)):
            if split_texts[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_texts[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):   
    alt_matches = re.findall(r"\[(.*?)\]", text)
    url_matches = re.findall(r"\(([^\(\)]*)\)", text)

    if len(alt_matches) != len(url_matches):
        raise Exception("alt or url issue")
    
    alt_url_list = []

    for i in range(len(alt_matches)):
        alt_url_list.append((alt_matches[i], url_matches[i]))

    return alt_url_list
    
    
def extract_markdown_links(text):
    descr_matches = re.findall(r"\[(.*?)\]", text)
    url_matches = re.findall(r"\(([^\(\)]*)\)", text)

    if len(descr_matches) != len(url_matches):
        raise Exception("url or description issue")

    descr_url_list = []

    for i in range(len(descr_matches)):
        descr_url_list.append((descr_matches[i], url_matches[i]))

    return descr_url_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(new_nodes)
            continue

        node_text = old_node.text
        images_mk = extract_markdown_images(node_text)
        
        if len(images_mk) == 0:
            return old_nodes

        for image_mk in images_mk:
            image_alt, image_url = image_mk
            split_text = node_text.split(f"![{image_alt}]({image_url})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_url))
            node_text = split_text[1]
        return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(new_nodes)
            continue

        node_text = old_node.text
        links_mk = extract_markdown_links(node_text)
        
        if len(links_mk) == 0:
            return old_nodes

        for link_mk in links_mk:
            link_descr, link_url = link_mk
            split_text = node_text.split(f"[{link_descr}]({link_url})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_descr, TextType.LINK, url=link_url))
            node_text = split_text[1]
        return new_nodes

if __name__ == "__main__":
    unittest.main()