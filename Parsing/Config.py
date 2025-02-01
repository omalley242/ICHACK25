import jsonpickle

#deserialize config file
class Config():

    anubisignore: list[str] #ignored fnmatch strings
    comment_patterns: dict #dictionary extenstion -> comment token
    anubis_enable_token: str

    def __init__(self, anubisignore, comment_patterns, anubis_enable_token):
        self.anubisignore = anubisignore
        self.comment_patterns = comment_patterns
        self.anubis_enable_token = anubis_enable_token

    @classmethod
    def from_file(self, file_path):
        with open(file_path, 'r') as data:
            contents = data.read()
            return jsonpickle.decode(contents)