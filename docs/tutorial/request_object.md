# The Request Object

JustPy request handlers (functions that handle requests) can receive an optional argument, the [request object](https://www.starlette.io/requests/). Whenever JustPy needs to run a request handler, it checks first if it is defined with an argument and if that is the case, JustPy provides the request object as the argument.

## URL Parameters

URLs may include a [query string](https://en.wikipedia.org/wiki/Query_string) with parameters: www.example.com/?num=4&name=Joe
In this example the URL includes two parameters, `num` and `name` with values of 4 and 'Joe'.

The request object includes (among other things) information about the URL parameters. 
Below is a simple program that displays a page with the parameters in the URL. Try http://127.0.0.1:8000/?number=5&name=Smith for example. 
```python
import justpy as jp

def demo_function(request):
    wp = jp.WebPage()
    if len(request.query_params) > 0:
        for key, value in request.query_params.items():
            jp.P(text=f'{key}: {value}', a=wp, classes='text-xl m-2 p-1')
    else:
        jp.P(text='No URL paramaters present', a=wp, classes='text-xl m-2 p-1')
    return wp

jp.justpy(demo_function)
```

The request object has several attributes. One of them is the Python dictionary `request.query_params` which includes the keys and values of the URL parameters. In the program above we iterate over this dictionary and add to the page all the keys and their corresponding values.

## Dog Example

Let's do something a little more useful (well, at least more entertaining). The site https://dog.ceo provides pictures of dogs using a simple [API](https://en.wikipedia.org/wiki/Application_programming_interface). Please run the following program and load a browser page without any parameters in the URL:

```python
import justpy as jp

async def dog_pic1(request):
    wp = jp.WebPage()
    breed = request.query_params.get('breed', 'papillon' )
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2')
    return wp

jp.justpy(dog_pic1)
```

After a few seconds, you should see a picture of a [papillon](https://www.akc.org/dog-breeds/papillon/). That is the default dog breed to show (now you know the breed of my two dogs). Each time you reload the page you will get a different picture as we are asking the site for a random image. Try changing the breed of the dogs in the picture by specifying the breed parameter in the URL, for example: http://127.0.0.1:8000/?breed=corgi

Let's examine the program. First, notice how we define `dog_pic` as an `async` function (if you don't know what `async` functions are in Python just skip this paragraph and the next). JustPy uses [starlette.io](https://www.starlette.io/), "a lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services".  To shield users from the complexities of async programming in Python, JustPy allows both functions that handle requests and functions that handle events to be either `async` or not. The framework checks if a function is a coroutine and runs it accordingly. 

When a request or event handler require I/O operations over the internet (or to access a local database or even file), it is recommended that they be of type `async` and that all I/O and database operations be non-blocking (this means they are run as a coroutine or in another thread). Otherwise, the application will not scale. To help with the simple case of using an API with the HTTP GET method, JustPy provides a helper function conveniently called `get`. The function asynchronously retrieves information which (by default in JSON format) and converts it to a Python dictionary.
 
In the program above we call the `get` function with the appropriate URL. We are requesting the URL for a random image of dog with a certain breed. That URL can be found under the 'message' key in the dictionary `r`. We then add an image to the page using the `Img` class which corresponds to the HTML img tag. The `src` attribute is then set to the URL of the image. Finally, we return the page which the framework will then render. 

## Dog Example with Image Click

As the program is currently written, to get a new image we need to reload the page. Let's change this so that by clicking on the image, a new one is loaded:

```python
import justpy as jp

async def get_image1(self, msg):
    r = await jp.get(f'https://dog.ceo/api/breed/{msg.page.breed}/images/random')
    self.src = r['message']


async def dog_pic2(request):
    wp = jp.WebPage()
    breed = request.query_params.get('breed', 'papillon')
    wp.breed = breed
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2 cursor-pointer', click=get_image1)
    return wp

jp.justpy(dog_pic2)
```

We added the function `get_image` and assigned the image's click event to it . We also made a small design change by adding 'cursor-pointer' to the classes of the image. When the mouse cursor enters the image, it will change its shape to indicate that the image can be interacted with. Notice how we also assigned the breed to a page attribute so that `get_image` will have direct access to it via `msg.page.breed`.

## Path Parameters

JustPy also supports [path parameters](https://www.starlette.io/routing/#path-parameters) in addition to URL query parameters. Let's change the example above so that the breed is determined by the path in the URL:

```python
import justpy as jp

async def get_image2(self, msg):
    r = await jp.get(f'https://dog.ceo/api/breed/{msg.page.breed}/images/random')
    self.src = r['message']

@jp.SetRoute('/breed/{breed}')
async def dog_pic3(request):
    wp = jp.WebPage()
    breed = request.path_params.get('breed', 'papillon')
    wp.breed = breed
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2 cursor-pointer', click=get_image2)
    return wp

jp.justpy(dog_pic3)
```

Try going to http://127.0.0.1:8000/breed/borzoi or http://127.0.0.1:8000/breed/boxer
 
Path parameters are defined by surrounding them with {} in the path. If JustPy can match the path to the URL, it executes the function and provides the path parameters in the dictionary `request.path_params`. To learn more about the different options with path parameters go to https://www.starlette.io/routing/
