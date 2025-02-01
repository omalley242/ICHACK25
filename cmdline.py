#Allow for io processing
import io
#For processing Yaml Files
import yaml
#For creating CLI utils
import click
#Glob library for searching for files recursively
from glob import glob
#tool for matching file paths for anubisignore
import pathspec
#Custom Parsing Library
from Parsing.Config import *
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

    for filename in glob(f'{base_dir}/*', recursive=True):

        if ignore_spec.match_file(filename):
            continue
        
        files_to_parse.append(filename)


    print(files_to_parse)



#command to start the server
@cli.command()
def runserver():
    print("runserver")



if __name__ == '__main__':
    cli()