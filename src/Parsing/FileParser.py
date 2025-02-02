import io
import os
from .Config import Config
from .CommentPattern import CommentPattern
from enum import Enum
import jsonpickle

class parsing_state(Enum):
    IGNORE = 0              #we are not within a marked section
    SINGLE_LINE = 1         #we are within a single line section (add all till newline)
    MULTILINE = 2           #we are within a multiline comment (add till multiline stop token)

class FileParser():
    # Internal State of the parser
    comment_state: parsing_state
    markdown_state: parsing_state
    comment_pattern: CommentPattern

    # Start with the inital state as IGNORE
    def __init__(self, config: Config):
        self.config = config
        self.comment_state = parsing_state.IGNORE
        self.markdown_state = parsing_state.IGNORE
        self.code_state = parsing_state.IGNORE

    # Function to parse a supplied file
    def parse(self, file_path: str) -> str:

        #Locate the config for this file type to enable parsing
        _, file_extension = os.path.splitext(file_path)
        self.comment_pattern = self.config.comment_patterns.get(file_extension)
        self.comment_state = parsing_state.IGNORE
        self.markdown_state = parsing_state.IGNORE
        self.code_state = parsing_state.IGNORE

        if self.comment_pattern == None:
            raise(BaseException(f"Could not find comment pattern requried for {file_extension} please review the config file"))
        
        with open(file_path, "r") as data:
            lines = data.readlines()

            file_markdown = ""
            for line in lines:
                file_markdown += self.parse_line(line)

        return file_markdown

        
    def parse_line(self, line: str):        
        scanning_head_index = 0
        line_markdown = ""
        if self.code_state == parsing_state.IGNORE and line[:-1] == self.comment_pattern.base_comment_pattern + self.config.code_start_token:
            self.code_state = parsing_state.MULTILINE
            return "```" + self.comment_pattern.language_name + "\n"

        elif self.code_state == parsing_state.MULTILINE and line[:-1] == self.comment_pattern.base_comment_pattern + self.config.code_end_token:
            self.code_state = parsing_state.IGNORE
            return "```\n"

        elif self.code_state == parsing_state.MULTILINE:
            return line

        else:

            #iterate over line full
            while scanning_head_index != len(line):

                #check current state not within comment block
                if self.comment_state == parsing_state.IGNORE:

                    #find length of pattern were trying to match (so if its too long for the rest of line we can early exit)
                    base_pattern_length = len(self.comment_pattern.base_comment_pattern)
                    multi_pattern_length = len(self.comment_pattern.multiline_comment_start)

                    if scanning_head_index < len(line) - base_pattern_length and line[scanning_head_index:scanning_head_index + base_pattern_length] == self.comment_pattern.base_comment_pattern:
                        #update state to single line
                        self.comment_state = parsing_state.SINGLE_LINE
                        scanning_head_index+=base_pattern_length

                    elif scanning_head_index < len(line) - multi_pattern_length and line[scanning_head_index:scanning_head_index + multi_pattern_length] == self.comment_pattern.multiline_comment_start:
                        #update state to multi line
                        self.comment_state = parsing_state.MULTILINE
                        scanning_head_index+=multi_pattern_length
                    else:
                        scanning_head_index+=1

                #currently within a comment block so can start looking for markdown marked sections
                else:

                    #we are not in markdown state so look for opening markdown and closing comment
                    if self.markdown_state == parsing_state.IGNORE:
                        markdown_multi_token_len = len(self.config.anubis_multiline_start_token)
                        markdown_token_len = len(self.config.anubis_enable_token)
                        comment_pattern_mutli_len = len(self.comment_pattern.multiline_comment_end)

                        if scanning_head_index < len(line) - comment_pattern_mutli_len and line[scanning_head_index:scanning_head_index + comment_pattern_mutli_len] == self.comment_pattern.multiline_comment_end:
                            #update state to reset both as comment is no longer open
                            self.comment_state = parsing_state.IGNORE
                            self.markdown_state = parsing_state.IGNORE
                            scanning_head_index+=comment_pattern_mutli_len

                        elif scanning_head_index < len(line) - markdown_multi_token_len and line[scanning_head_index:scanning_head_index + markdown_multi_token_len] == self.config.anubis_multiline_start_token:
                            #update state to multi line
                            self.markdown_state = parsing_state.MULTILINE
                            scanning_head_index+=markdown_multi_token_len
                        
                        elif scanning_head_index < len(line) - markdown_token_len and line[scanning_head_index:scanning_head_index + markdown_token_len] == self.config.anubis_enable_token:
                            #update state to multi line
                            self.markdown_state = parsing_state.SINGLE_LINE
                            scanning_head_index+=markdown_token_len
                        else:
                            scanning_head_index+=1

                    #we are in both markdown and comment state therefore add strings and look for closing
                    else:   

                        comment_pattern_mutli_len = len(self.comment_pattern.multiline_comment_end)
                        markdown_pattern_mutli_len = len(self.config.anubis_multiline_end_token)

                        #if both are single line we can early exit
                        if self.comment_state == parsing_state.SINGLE_LINE and self.markdown_state == parsing_state.SINGLE_LINE:
                            self.comment_state = parsing_state.IGNORE
                            self.markdown_state = parsing_state.IGNORE
                            
                            return line_markdown + line[scanning_head_index:] #-1 such that the newline is not included
                        
                        #If the markdown multi line closes change to ignore
                        elif scanning_head_index < len(line) - markdown_pattern_mutli_len and line[scanning_head_index:scanning_head_index + markdown_pattern_mutli_len] == self.config.anubis_multiline_end_token:
                            self.markdown_state = parsing_state.IGNORE
                            scanning_head_index+=markdown_pattern_mutli_len

                        #if the comment closes change both to ignore
                        elif scanning_head_index < len(line) - comment_pattern_mutli_len and line[scanning_head_index:scanning_head_index + comment_pattern_mutli_len] == self.comment_pattern.multiline_comment_end:
                            self.markdown_state = parsing_state.IGNORE
                            self.comment_state = parsing_state.IGNORE
                            scanning_head_index+=comment_pattern_mutli_len

                        else:
                            #Add string to markdown total
                            line_markdown += line[scanning_head_index]
                            scanning_head_index+=1
            
            #Reset single line states at end of line 
            if self.comment_state == parsing_state.SINGLE_LINE:
                self.comment_state = parsing_state.IGNORE

            if self.markdown_state == parsing_state.SINGLE_LINE:
                self.markdown_state = parsing_state.IGNORE

            if len(line_markdown) == 0:
                return ""
            
            return line_markdown + "\n"
