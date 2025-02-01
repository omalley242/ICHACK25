# Class to represent a comment matching pattern for a file extenstion
class CommentPattern():

    base_comment_pattern: str
    inline_comment_start: str
    inline_comment_end: str
    multiline_comment_start: str
    multiline_comment_end: str

    def __init__(self, base_comment_pattern, inline_comment_start, inline_comment_end, multiline_comment_start, multiline_comment_end):
        self.base_comment_pattern = base_comment_pattern
        self.inline_comment_start = inline_comment_start
        self.inline_comment_end = inline_comment_end
        self.multiline_comment_start = multiline_comment_start
        self.multiline_comment_end = multiline_comment_end