# Static Files

The handling of static files is to be changed in an upcoming justpy
version see https://github.com/justpy-org/justpy/issues/162

## The Basics

Static resources are those that are not generated dynamically by the application. An image is an example of a static resource.

By default, all static resources for JustPy can be found under the `/static` route (this can be changed using the configuration file). 
 
Let's look at a concrete example.

Follow this link : [picture of papillon](https://images.dog.ceo/breeds/papillon/n02086910_7280.jpg)

Save the image in the directory where your programs are under the name "papillon.jpg".

Now, run the following program:

```python
import justpy as jp

def static_test():
    wp = jp.WebPage()
    jp.Img(src='/static/papillon.jpg', a=wp, classes='m-2 p-2')
    return wp

jp.justpy(static_test)
```

You should see the picture on the web page.

If you enter the URL http://127.0.0.1:8000/static/papillon.jpg you will get the picture also.

If want to keep your static resources in a separate directory, the simplest thing to do is to create a subdirectory in the directory your program is in. If you call the directory "my_pictures" for example, and put the image there, you would need to set the `src` attribute of the image to "/static/my_pictures/papillon.jpg".

The line in the code would look like this:
```python
    jp.Img(src='/static/my_pictures/papillon.jpg', a=wp, classes='m-2 p-2')
```

## Advanced Configuration

JustPy uses starlette's [StaticFiles class](https://www.starlette.io/staticfiles/) to serve static files.

The relevant configuration and mounting commands are:
```python
config = Config('justpy.env')

STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=os.getcwd())
STATIC_ROUTE = config('STATIC_MOUNT', cast=str, default='/static')
STATIC_NAME = config('STATIC_NAME', cast=str, default='static')

app.mount(STATIC_ROUTE, StaticFiles(directory=STATIC_DIRECTORY), name=STATIC_NAME)

```

If you want to change JustPy's defaults, change the settings in justpy.env, the configuration file.

!!! note
    STATIC_NAME is used inside JustPy's templates so there is probably no reason to change it in any application unless you change the template files also. 
