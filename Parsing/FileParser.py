import io
import Config

class FileParser():

    def __init__(self, file_path: str, config: Config):
        self.file_path = file_path 
        self.config = config

    def parse(self):
        with open(self.file_path, "r") as data:
            data.readline()

    def parse_line(self):
        pass