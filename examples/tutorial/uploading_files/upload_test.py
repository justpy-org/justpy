# Justpy Tutorial demo upload_test from docs/tutorial/uploading_files.md
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

# initialize the demo
from examples.basedemo import Demo
Demo("upload_test", upload_test, websockets=False)
