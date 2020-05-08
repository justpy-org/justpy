# Getting Started

In order to take full advantage of this tutorial some knowledge of Python is required including an understanding
of [object oriented programming](https://docs.python.org/3/tutorial/classes.html) in Python. 
In addition, a basic understanding of HTML is required ([HTML - Getting Started](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)). 

!!! info
    The examples in this tutorial use [Python f-strings](https://realpython.com/python-f-strings/) which were added in Python 3.6

!!! tip
    If you have a question about JustPy please open an issue in the [JustPy Github repository](https://github.com/elimintz/justpy) or post a question with the tag `[justpy]` to [stack overflow](https://stackoverflow.com/). I will try to answer promptly.

## Installation

First, make sure that the version of `python3` you have is 3.6 or higher:
`$ python3 --version`

If not, upgrade your Python interpreter.

It is probably best to run the programs in this tutorial in a virtual environment so that your system wide Python interpreter is not affected, though this is not a requirement.
The following commands create a directory for this tutorial, then create a virtual environment named jp and activate it and finally install JustPy and its dependencies:

```
$ mkdir jptutorial
$ cd jptutorial
$ python3 -m venv jp
$ source jp/bin/activate
(jp) $ pip install justpy
```

On Microsoft Windows, the activation command for the virtual environment is `jp\Scripts\activate` instead of the source command above.

Now, using your favorite code editor, create a file in the jptutorial directory called test.py that includes the following code:

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp

jp.justpy(hello_world)
```

!!! note
    You can easily copy the code by hovering over it and then clicking 'Copy to clipboard' in the upper right corner

## Running the Program

To run the program execute the following command:

```
$ python3 test.py
```

Then, direct your browser to http://127.0.0.1:8000 or http://localhost:8000/ 

This refers to port 8000 on the local machine and should work in most environments. 

You should see 'Hello!' in your browser. Click it a few times also. It should report the number of times it has been clicked. 

In this tutorial, when asked to "run the program", follow the two steps above (there is no need to name the file "test.py", you can use any name you like). 



