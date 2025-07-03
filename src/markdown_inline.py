import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        new_nodes_text = node.text.split(delimiter)
        if len(new_nodes_text) % 2 == 0:
            raise ValueError("improperly closed markdown tag")
        for i in range(len(new_nodes_text)):
            if new_nodes_text[i] == "":
                continue
            new_type = text_type
            if i % 2 == 0:
                new_type = node.text_type
            split_nodes.append(TextNode(new_nodes_text[i], new_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        images = extract_markdown_images(node.text)
        new_nodes_text = [node.text]
        for image in images:
            new_nodes_text.extend(new_nodes_text.pop().split(f"![{image[0]}]({image[1]})"))
        for i in range(len(new_nodes_text)):
            if new_nodes_text[i] != "":
                split_nodes.append(TextNode(new_nodes_text[i], node.text_type))
            if i < len(images):
                split_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        links = extract_markdown_links(node.text)
        new_nodes_text = [node.text]
        for link in links:
            new_nodes_text.extend(new_nodes_text.pop().split(f"[{link[0]}]({link[1]})"))
        for i in range(len(new_nodes_text)):
            if new_nodes_text[i] != "":
                split_nodes.append(TextNode(new_nodes_text[i], node.text_type))
            if i < len(links):
                split_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)