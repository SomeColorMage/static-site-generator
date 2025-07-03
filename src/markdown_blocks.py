import re
from enum import Enum
from htmlnode import ParentNode
from markdown_inline import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(ParentNode("p", text_to_children(" ".join(block.split("\n")))))
        if block_type == BlockType.HEADING:
            level = block_to_heading_level(block)
            children.append(ParentNode(f"h{level}", text_to_children(block[level + 1:])))
        if block_type == BlockType.CODE:
            raw_text = TextNode(block[4:-3], TextType.TEXT)
            code_block = ParentNode("code", [text_node_to_html_node(raw_text)])
            children.append(ParentNode("pre", [code_block]))
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line.lstrip("> "))
            children.append(ParentNode("blockquote", text_to_children(" ".join(stripped_lines))))
        if block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            grandchildren = []
            for line in lines:
                grandchildren.append(ParentNode("li", text_to_children(line[2:])))
            children.append(ParentNode("ul", grandchildren))
        if block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            grandchildren = []
            for line in lines:
                grandchildren.append(ParentNode("li", text_to_children(line[3:])))
            children.append(ParentNode("ol", grandchildren))

    return ParentNode("div", children, None)

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"#{1,6} ", block):
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
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_to_heading_level(block):
    if block[0] != "#":
        raise ValueError("block is not a heading")
    for i in range(1, 7):
        if block[i] == " ":
            return i
        if block[i] != "#":
            raise ValueError("block is not a heading")
    raise ValueError("block is not a heading")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("no title found")