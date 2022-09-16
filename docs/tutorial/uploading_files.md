# Downloading and Uploading Files

## Downloading Files

### Static Content

Enabling a file download by users is done by using the JustPy component that corresponds to the [a html tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a). The component has a [`download` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#Attributes) that when set, the file that the `href` attributes links to is downloaded and the name given to it is the value of the `download` attribute.

```python
import justpy as jp
download_link = jp.A(text='Download image', href='/static/image1.png', download='image1.png')
```

In the example above, when the element is clicked, the file 'image1.png' from the directory the server was run (the default static directory) will be downloaded and will be called 'image1.png' on the user's computer. The way JustPy handles static files is explained [here](../static)

### Dynamic Content

The download link does not have to be static. In the example below, the href is a non-static route that responds to a user request and inserts text into the page that is returned. Since the text is assigned to the `html` attribute of the page, this overrides all other page options and just the text is returned.

Run it and look at the files created each time. They will be different based on the time they were downloaded.

```python
import justpy as jp
from datetime import datetime

def change_link_text(self, msg):
    self.set_classes('text-yellow-500')

def download_test1():
    wp = jp.WebPage()
    download_link = jp.A(text='Download File', href='/create_file', download='text_file.txt', a=wp,
             classes='inline-block m-2 p-2 text-white bg-blue-500 text-2xl')
    download_link.on('click', change_link_text)
    return wp

@jp.SetRoute('/create_file')
def create_file():
    wp = jp.WebPage()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    wp.html = f'This text file was generated on {now}'
    return wp

jp.justpy(download_test1)

```

## Uploading Files

Uploading files is a three step process.

1) First the user needs to provide the files to upload using an [Input element of type 'file'](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file). In order to upload files chosen by the user, this Input element **must** be in a Form element and the form **must** have a submit button.

2) When the user submits the form, the content of the files is provided as part of the second argument of the submit event handler (`msg` in this tutorial).

3) Form submission activates the form submit event handler where the file content can be saved on the server.

First, let's look at the isolated behavior of an Input element of type 'file'.

In the program below, one such element is put on the page and after the user selects files, information about the selected files is displayed on the page.

!!! note
    In order to be compatible with all browsers, use the 'change' event with this kind of Input element and not the 'input' event


```python
import justpy as jp

def download_test2():
    wp = jp.WebPage()
    in1 = jp.Input(type='file', classes=jp.Styles.input_classes, a=wp, multiple=True, change=file_input)
    in1.file_div = jp.Div(a=wp)
    return wp

def file_input(self, msg):
    self.file_div.delete_components()
    for f in msg.files:
        jp.Div(text=f'{f.name} | {f.size} | {f.type} | {f.lastModified}', a=self.file_div, classes='font-mono m-1 p-2')


jp.justpy(download_test2)

```

In the case of an Input element for file selection, JustPy adds to `msg` a list `msg.files`, that includes information about all the files selected by the user. For each file there is dictionary in the list with four keys:

* name - the name of the file
* size - the size of the file in bytes
* type - the [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) of the file
* lastModified - time that the file was last modified as milliseconds since the epoch

Run the program above to see some examples of these values.

Note that the content of the files is not available to the change event handler. Only when a form with the element has been submitted, does JustPy actually read the files and insert their content in the `msg` of the submit event handler.

Again the information is found in `msg.files` but with an additional key called `file_content`. The value under this key is the file content in  [base64 format](https://docs.python.org/3/library/base64.html). Files in this format are in printable ASCII characters and can be included in WebSocket messages and HTTP POST requests.

!!! note
    When using Websockets there is currently a 1 MByte limit on total upload size in one request after the base64 conversion. If you want a large limit, run the upload page or the application with `websockets=false`

The program below lets users upload image files and displays thumbnails of the files uploaded. When the thumbnails are clicked, the file that was uploaded is downloaded.

Each user's files are stored in a directory that is unique for each session.

The ThumbNail component defined in the program is an [A component](../html_components?id=html-links) that includes an Img component.
### upload image files and display thumbnails of the files uploaded
```python
import justpy as jp
import base64
import os


class ThumbNail(jp.A):

    def __init__(self, **kwargs):
        self.pic_file = ''
        # If True, files downloaded. If False, they are opened in new browser tab
        self.download_files = True
        super().__init__(**kwargs)
        self.target = '_blank'
        self.img = jp.Img(a=self)
        self.img.style = 'width: 150px'
        self.img.classes = 'p-5 m-1 border-2 rounded-lg border-gray-200 hover:shadow-lg'

    def react(self, data):
        self.img.src = self.pic_file
        self.href = self.pic_file
        if self.download_files:
            self.download = self.href.split('/')[3]    # href is of the form /static/session_id/file_name
        self.set_classes('inline-block')


def pic_submit(self, msg):
    # If directory for session does not exist, create one
    # The name of the directory is the session_id
    if not os.path.isdir(msg.session_id):
        os.mkdir(msg.session_id)
    # Find the element in the form data that contains the file information
    for c in msg.form_data:
        if c.type == 'file':
            break
    # Write the content to a file after decoding the base64 content
    for i, v in enumerate(c.files):
        with open(f'{msg.session_id}/{v.name}', 'wb') as f:
            f.write(base64.b64decode(v.file_content))
    file_list = os.listdir(msg.session_id)
    self.image_div.delete_components()
    if file_list:
        for file in file_list:
            ThumbNail(pic_file=f'/static/{msg.session_id}/{file}', a=self.image_div)
    else:
        jp.Div(text='No images uploaded yet', a=self.image_div, classes='text-3xl')


def upload_test(request):
    wp = jp.WebPage()
    image_div = jp.Div(a=wp, classes='m-2 p-2 overflow-auto border-4 flex flex-wrap content-start', style='height: 80vh')
    file_list = []
    if os.path.isdir(request.session_id):
        file_list = os.listdir(request.session_id)
    if file_list:
        for file in file_list:
            ThumbNail(pic_file=f'/static/{request.session_id}/{file}', a=image_div)
    else:
        jp.Div(text='No images uploaded yet', a=image_div, classes='text-3xl')

    f = jp.Form(a=wp, enctype='multipart/form-data' , submit=pic_submit)
    f.image_div = image_div  # Will be used in submit event handler
    jp.Input(type='file', classes=jp.Styles.input_classes, a=f, multiple=True, accept='image/*')
    jp.Button(type='submit', text='Upload', classes=jp.Styles.button_simple, a=f)
    return wp

jp.justpy(upload_test, websockets=False)

```
