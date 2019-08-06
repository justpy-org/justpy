Parsing HTML
==================

With JustPy it is simple to move from an HTML representation to the JustPy object oriented one.
Two functions provide this support:

::

    parse_html(html_string, **kwargs)
    parse_html_file(html_file, **kwargs)

These function takes an HTML formatted string or file and return a JustPy component. The component is a ``Div``
instance if there are several top level siblings in the HTML string or the topmost HTML element if
there is only one.

Simple example:

``c = parse_html('<div>Hello</div)``

The function adds to important attributes to the object returned.

``name_dict`` is a dictionary that includes the named objects.

::

    c = parse_html('<div><button name="my_button"></button></div')
    my_button = c.name_dict['my_button']
    my_button.on('click', do_something)

``commands`` is a list with string representation of the python commands needed to generate the object.

A ``:`` in front of a parameter in the HTML causes it to be evaluated: ``:percentage="50"`` makes percentage 50.
Any python expression is applicable (the python ``eval`` function is used)

.. DANGER::
   Beware killer rabbits!

.. note:: This is a note admonition.
   This is the second line of the first paragraph.

   - The note contains all indented body elements
     following.
   - It includes this bullet list.

.. code:: python

  def my_function():
      "just a test"
      print 8/2

def my_function(my_arg, my_other_arg):
    """A function just for me.

    :param my_arg: The first of my arguments.
    :param my_other_arg: The second of my arguments.

    :returns: A message (just for me, of course).
    """



