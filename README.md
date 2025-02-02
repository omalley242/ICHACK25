# Anubis: Automatic Code Documentation for Any Language

Anubis is a powerful tool that automatically generates documentation for your code, regardless of the programming language. It extracts structured comments and code blocks based on custom delimiters, making it easy to document and share your projects.

---

## How It Works

Anubis scans your source code and identifies documentation blocks using specific markers. These markers allow you to embed markdown-style documentation directly within your code.

### Syntax

- Markdown to be included in the documentation is marked with a `|` character within a comment.
- Code blocks to include in the documentation are surrounded by `#{` and `#}`.
- These characters can be customized in the `anubis_config.json` file.

---

## Example Usage

### Annotated Code

Below is an example of how you can document your code using Anubis:

```python
'''|

# this is a function


|'''

#{

# my random test function
def random_test_function():
    if 1 + 1 == 2:
        return True
    return False

#}

'''|

## Example Python Class 
This is a simple python class that holds a public member that can be accessed using the . operator
A good tutorial for python classes can be seen here [Click Me](https://docs.python.org/3/tutorial/classes.html)

|'''

class SimpleClass():
    # This is a method to initalise member variables
    def __init__(self):
        pass


```
For this Anubis will generate the documentation:

> # this is a function  
>```python
> def random_test_function():
>    if 1 + 1 == 2:
>        return True
>    return False
>```  
>## Example Python Class
>This is a simple python class that holds a public >member that can be accessed using the . operator
>A good tutorial for python classes can be seen here > [Click Me](https://docs.python.org/3/tutorial/classes.html)


