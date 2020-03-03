class Null(object):

    def __init__(self, alliance=None, position=None):
        self.alliance = alliance
        self.position = position

    def to_string(self):
        return "-"
