FLIP = {
    "left": "right",
    "right": "left",
    "up": "down",
    "down": "up",
}


class Link:
    """Two-dimensional doubly-linked list element, with an associated column.
    Only column-type Link instances have a size (the number of child Links)
    and a name (for pretty printing)."""

    __slots__ = [
        "left",
        "right",
        "up",
        "down",
        "column",
        "size",
        "name",
    ]

    def __init__(self, column=None, name=""):
        self.column = column
        self.name = name

        self.size = 0
        self.left = self.right = self.up = self.down = None

    def __str__(self):
        return "".join(map(str, self.name))

    def loop(self, direction, include=False):
        """Traverse doubly-linked-list Links in a loop of a certain direction."""
        if include:
            yield self

        link = getattr(self, direction)
        while link != self:
            yield link
            link = getattr(link, direction)

    def attach(self, other, direction):
        """Attach a Link on one side."""
        link = getattr(self, direction)

        setattr(self, direction, other)
        setattr(other, FLIP[direction], self)

        if link is not None:
            setattr(link, FLIP[direction], other)
            setattr(other, direction, link)

    def cover(self):
        """In the set cover problem sense: consider the column-type Link as
        being covered and thus remove it from the Matrix of Links which remain
        to be covered."""
        self.left.right = self.right
        self.right.left = self.left

        for row in self.loop("down"):
            for link in row.loop("right"):
                link.down.up = link.up
                link.up.down = link.down
                link.column.size -= 1

    def uncover(self):
        """The reverse of cover.  In the set cover problem sense: consider the
        column-type Link as not being covered and thus add it to the Matrix of
        Links which remain to be covered."""
        for row in self.loop("up"):
            for link in row.loop("left"):
                link.column.size += 1
                link.down.up = link
                link.up.down = link

        self.right.left = self
        self.left.right = self
