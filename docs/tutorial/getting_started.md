# Getting Started

In order to take full advantage of this tutorial some knowledge of Python is required including an understanding
of [object oriented programming](https://docs.python.org/3/tutorial/classes.html) in Python. 
In addition, a basic understanding of HTML is required ([HTML - Getting Started](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)). 
The examples in this guide will use Python f-strings ([Python f-strings](https://realpython.com/python-f-strings/) provides a good introduction).

First, make sure that the version of `python3` you have is 3.6 or higher:
`$ python3 --version`

If not, upgrade your Python interpreter.

It is probably best to run the programs in this tutorial in a virtual environment so that your system wide Python interpreter is not affected, though this is not a requirement.
Create a directory for this tutorial, create a virtual environment named jp and activate it. Finally install justpy:

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

!> You can easily copy the code by hovering over it and then clicking 'Copy to clipboard' in the upper right corner

###### Run

To run the program execute the following command:

```
$ python3 test.py`
```

Then, direct your browser to http://localhost:8000/ or http://127.0.0.1:8000  (this refers to port 8000 on the local machine, one of these should work no matter your operating system). You should see 'Hello!' in your browser.  Click it a few times also. It should report the number of times it has been clicked. 
In this tutorial, when asked to "run the program", it means following the two steps above. 



