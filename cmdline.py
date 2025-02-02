#Allow for io processing
import io
#For creating CLI utils
import click
#Glob library for searching for files recursively
from glob import glob
#tool for matching file paths for anubisignore
import pathspec
#Custom Parsing Library
from Parsing.Config import Config
from Parsing.FileParser import FileParser
#enables it to be effectively decoded
from Parsing.CommentPattern import CommentPattern
#allow for path manipulation
import os.path


@click.group()
def cli():
    pass

#default command
@cli.command()
@click.argument('configfile_path')
def parse(configfile_path: str):

    #Load the config file from the supplied directory
    print(f"Loading Config File from {configfile_path}")
    try:
        config = Config.from_file(configfile_path)
    except:
        print("Unable to read the supplied path")

    #Retrieve base path from which to recurse from (using the config file location as root)
    base_dir = os.path.dirname(configfile_path)
    
    #Compile our Anubis ignore patterns
    ignore_spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, config.anubisignore)

    #files to parse worklist
    files_to_parse = []

    #Extract all files
    for filename in glob(f'{base_dir}/**/*.*', recursive=True):

        #Skip file if within anubisignore
        if ignore_spec.match_file(filename):
            continue
        
        #Add to worklist
        files_to_parse.append(filename)

    #create a new file parser
    file_parser = FileParser(config)

    #Process Worklist iteratively
    extracted_text = []
    for file in files_to_parse:
        extracted_text += file_parser.parse(file)

    print("".join(extracted_text))


#command to start the server
@cli.command()
def runserver():
    print("runserver")



if __name__ == '__main__':
    cli()