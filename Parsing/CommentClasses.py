class BlockComments(): 

    def __init__(self, comment):
        self.comment = comment

class FileComments():

    def __init__(self, comments: list[BlockComments]):
        self.comments = comments