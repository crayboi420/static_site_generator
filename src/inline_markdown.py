from textnode import *
from htmlnode import *
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodelist = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodelist.append(node)
            continue
        text = node.text
        imagelist = extract_markdown_images(text)
        for image in imagelist:
            [textbefore, text] = text.split(f"![{image[0]}]({image[1]})", 1)
            nodelist.append(TextNode(textbefore, text_type_text))
            nodelist.append(TextNode(image[0], text_type_image, image[1]))
        if len(text) > 0:
            nodelist.append(TextNode(text, text_type_text))
    return nodelist


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodelist = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            nodelist.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        for link in links:
            [textbefore, text] = text.split(f"[{link[0]}]({link[1]})", 1)
            nodelist.append(TextNode(textbefore, text_type_text))
            nodelist.append(TextNode(link[0], text_type_link, link[1]))
        if len(text) > 0:
            nodelist.append(TextNode(text, text_type_text))
    return nodelist


def text_to_textnodes(text: str) -> list[TextNode]:
    l0 = [TextNode(text, text_type_text)]
    # Bold
    l1 = split_nodes_delimiter(l0, "**", text_type_bold)
    # Italic
    l2 = split_nodes_delimiter(l1, "*", text_type_italic)
    # Code
    l3 = split_nodes_delimiter(l2, "`", text_type_code)
    # Image
    l4 = split_nodes_image(l3)
    # Links
    l5 = split_nodes_link(l4)
    return l5


def markdown_to_blocks(markdown: str) -> list[str]:
    return [_.strip() for _ in re.split(r"\n{2,}", markdown)]


def __represents_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


def __check_if_orderedlist(lines):
    i = 1
    for line in lines.split("\n"):
        if (
            len(line) < 3 + i // 10
            or not __represents_int(line[0 : 1 + i // 10])
            or int(line[0 : 1 + i // 10]) != i
            or line[1 + i // 10] != "."
        ):
            return False
        i += 1
    return True


def block_to_block_type(markdown: str) -> str:
    if re.search(r"^\#+ .+", markdown):
        return block_type_heading
    if re.seach(r"^```(?:[^`]|`(?!``))*```$", markdown):
        return block_type_code
    if re.search(r"^(>[^\n]*\n?)*$", markdown):
        return block_type_quote
    if re.search(r"^((\*|-) [^\n]*\n?)*$", markdown):
        return block_type_ulist
    if __check_if_orderedlist(markdown):
        return block_type_olist
    else:
        return block_type_paragraph


def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    blocktypes = list(map(block_to_block_type,markdown_blocks))
    
    
    daddyNode = HTMLNode("div", None, None)
