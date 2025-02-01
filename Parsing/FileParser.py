import io
import jsonpickle

#deserialize config file
class Config():

    anubisignore: list[str] #ignored fnmatch strings
    comment_patterns: dict #dictionary extenstion -> comment token
    accepted_file_types: list[str] #list of accepted file types
    anubis_enable_token: str

    def __init__(self, anubisignore, comment_patterns, accepted_file_types, anubis_enable_token):
        self.anubisignore = anubisignore
        self.comment_patterns = comment_patterns
        self.accepted_file_types = accepted_file_types
        self.anubis_enable_token = anubis_enable_token

    @classmethod
    def from_file(file_path):
        with open(file_path, 'r') as data:
            contents = data.read()
            return jsonpickle.decode(contents)


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



class BlockComments(): 

    def __init__(self, comment):
        self.comment = comment

class FileComments():

    def __init__(self, comments: list[BlockComments]):
        self.comments = comments


class FileParser():

    def __init__(self, file_path: str, config: Config):
        self.file_path = file_path 
        self.config = config

    def parse(self):
        with open(self.file_path, "r") as data:
            data.readline()

    def parse_line(self):
        pass

if __name__ == "__main__":
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    anubisignore = ["venv/**", "Anubis/__pycache__/**"]
    python_comment_pattern = CommentPattern("#", "", "", "\'\'\'", "\'\'\'")
    comment_pattern_dictionary = {".py", python_comment_pattern}
    accepted_file_types = [".py"]
    anubis_enable_token = "*"
    example_config = Config(anubisignore, comment_pattern_dictionary, accepted_file_types, anubis_enable_token)

    print(jsonpickle.encode(example_config))
