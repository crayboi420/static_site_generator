class HTMLNode:
    def __init__(self, tag: str, value: str, children: list = [], props: dict = {}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"Tag: {self.tag}, Value: {self.value}, Properties: {self.props.keys()}, No. of children: {len(self.children)}"

    def to_html(self):
        raise NotImplementedError("lule")

    def props_to_html(self) -> str:
        output = ""
        for key, item in self.props.items():
            output += f' {key}="{item}"'
        return output


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):

        if value is None:
            raise ValueError("Pls gib value")

        # Don't allow for children
        super().__init__(tag, value, [], props)

    def to_html(self):
        output = ""
        if self.tag is None:
            return self.value
        return f"<{self.tag}{str(self.props_to_html())}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = {}):

        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Pls gib tag")
        if len(self.children) < 1:
            raise ValueError("No Children wtf")
        output = ""
        output += f"<{self.tag}{str(self.props_to_html())}>"
        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"
        return output
