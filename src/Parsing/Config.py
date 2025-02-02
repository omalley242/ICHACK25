import jsonpickle
from .CommentPattern import *

#deserialize config file
class Config():

    anubisignore: list[str] #ignored fnmatch strings
    comment_patterns: dict[str, CommentPattern] #dictionary extenstion -> comment token
    anubis_enable_token: str
    anubis_multiline_start_token: str
    anubis_multiline_end_token: str
    code_start_token: str
    code_end_token: str

    def __init__(self, anubisignore, comment_patterns, anubis_enable_token, anubis_multiline_start_token, anubis_multiline_end_token, code_start_token, code_end_token):
        self.anubisignore = anubisignore
        self.comment_patterns = comment_patterns
        self.anubis_enable_token = anubis_enable_token
        self.anubis_multiline_start_token = anubis_multiline_start_token
        self.anubis_multiline_end_token = anubis_multiline_end_token
        self.code_start_token = code_start_token
        self.code_end_token = code_end_token

    @classmethod
    def from_file(self, file_path):
        with open(file_path, 'r') as data:
            contents = data.read()
            return jsonpickle.decode(contents)
            