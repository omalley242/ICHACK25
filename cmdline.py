#Allow for io processing
import io
#For processing Yaml Files
import yaml
#For creating CLI utils
import click
#Custom Parsing Library
from Parsing import FileParser


@click.group()
def cli():
    pass

#default command
@cli.command()
def parse():
    print("parsing")


#command to start the server
@cli.command()
def runserver():
    print("runserver")



if __name__ == '__main__':
    cli()