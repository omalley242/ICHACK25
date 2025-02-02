# Class to represent a comment matching pattern for a file extenstion
class CommentPattern():

    base_comment_pattern: str
    multiline_comment_start: str
    multiline_comment_end: str
    language_name: str
    
    def __init__(self, base_comment_pattern, multiline_comment_start, multiline_comment_end, language_name):
        self.base_comment_pattern = base_comment_pattern
        self.multiline_comment_start = multiline_comment_start
        self.multiline_comment_end = multiline_comment_end
        self.language_name = language_name