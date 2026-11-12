class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = tuple(state)
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h

    def reconstruct_path(self):
        path = []
        current = self
        while current is not None:
            path.append({
                "state": list(current.state),
                "move": current.action,
                "g": current.g,
                "h": current.h,
                "f": current.f
            })
            current = current.parent
        return path[::-1]
