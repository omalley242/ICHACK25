#Allow for io processing
import io
import sys
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
#SQLite3 for Django interation
import sqlite3
#allow for running subprocesses from cmdline
import subprocess

from signal import *

global django_proc
global react_proc

def clean(*args):
    django_proc.kill()
    react_proc.kill()
    sys.exit(0)

@click.group()
def cli():
    pass

#default command
def parse_func(configfile_path: str):

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
    database_records = []
    for id, file in enumerate(files_to_parse, start=1):
        database_records.append((id, file.removeprefix("./").replace("/", "->"), file_parser.parse(file)))


    print("Saving Database Records")
    #After strings extracted add to sqlite db and serialize for use by Django
    con = sqlite3.connect("./src/backend/db.sqlite3")
    cur = con.cursor()
    cur.execute("DELETE FROM Anubis_markdowncontent")
    cur.executemany("INSERT INTO Anubis_markdowncontent VALUES(?, ?, ?)", database_records)
    con.commit()  # Remember to commit the transaction after executing INSERT.


@cli.command()
@click.argument('configfile_path')
def parse(configfile_path: str):
    parse_func(configfile_path)

#command to start the server
def runserver_func():

    print("starting servers")
    # run django database server
    django_proc = subprocess.Popen(["python3", "./src/backend/manage.py", "runserver"], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)

    # run react front end server
    react_proc = subprocess.Popen(["npm", "start", "--prefix", "src/frontend/"], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True) 
    
    django_proc.wait()
    react_proc.wait()


@cli.command()
def runserver():
    runserver_func()

@cli.command()
@click.argument('configfile_path')
def all(configfile_path: str):
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, clean)
        
    parse_func(configfile_path)
    runserver_func()

if __name__ == '__main__':
    cli()

