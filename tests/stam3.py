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
    # The names of the directory is the session_id
    if not os.path.isdir(msg.session_id):
        os.mkdir(msg.session_id)
    # Find the files in in form_data
    for c in msg.form_data:
        if c.type == 'file':
            break
    for i, v in enumerate(c.files):
        # print(i, v.name, v.size, v.lastModified)
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



# uploading file: Need to use filereader https://developer.mozilla.org/en-US/docs/Web/API/FileReader
# The file list is in event.target.files of an input field with type='file'
#


print('hello')
html_string = """
<div class="q-pa-md">
    <q-card style="max-width: 300px">
      <q-item>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" />
        </q-item-section>

        <q-item-section>
          <q-item-label>
            <q-skeleton type="text" animation="wave"/>
          </q-item-label>
          <q-item-label caption>
            <q-skeleton type="text" />
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-skeleton height="200px" square />

      <q-card-actions align="right" class="q-gutter-md">
        <q-skeleton type="QBtn" />
        <q-skeleton type="QBtn" />
      </q-card-actions>
    </q-card>
  </div>
"""

html_string1 = """
<div class="q-pa-md row items-start q-gutter-md">
    <q-card class="my-card">
      <q-card-section>
        lorem 
      </q-card-section>
    </q-card>

    <q-card
      class="my-card text-white"
      style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
    >
      <q-card-section>
        <div class="text-h6">Our Changing Planet</div>
        <div class="text-subtitle2">by John Doe</div>
      </q-card-section>

      <q-card-section>
        lorem 
      </q-card-section>
    </q-card>

    <q-card dark bordered class="bg-grey-9 my-card">
      <q-card-section>
        <div class="text-h6">Our Changing Planet</div>
        <div class="text-subtitle2">by John Doe</div>
      </q-card-section>

      <q-separator dark inset />

      <q-card-section>
        lorem 
      </q-card-section>
    </q-card>

    <q-card flat bordered class="my-card">
      <q-card-section>
        <div class="text-h6">Our Changing Planet</div>
      </q-card-section>

      <q-card-section>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua.
      </q-card-section>

      <q-separator inset />

      <q-card-section>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua.
      </q-card-section>
    </q-card>
  </div>
"""

html_string = """
<div class="q-pa-md">
    <q-card flat bordered style="max-width: 300px">
      <q-item>
        <q-item-section avatar>
          <q-skeleton type="QAvatar" animation="fade" />
        </q-item-section>

        <q-item-section>
          <q-item-label>
            <q-skeleton type="text" animation="fade" />
          </q-item-label>
          <q-item-label caption>
            <q-skeleton type="text" animation="fade" />
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-skeleton height="200px" square animation="fade" />

      <q-card-section>
        <q-skeleton type="text" class="text-subtitle2" animation="fade" />
        <q-skeleton type="text" width="50%" class="text-subtitle2" animation="fade" />
      </q-card-section>
    </q-card>
  </div>
"""

def option_group_test():
    wp = jp.QuasarPage()
    d = jp.parse_html(html_string, a=wp)
    for i in d.commands:
        print(i)
    return wp


# jp.justpy(option_group_test)


import justpy as jp

def key_down(self, msg):
    print(msg.key_data)

def color_demo(request):
    wp = jp.QuasarPage(data={'text': 'click to edit'})
    d1 = jp.Div(classes='q-pa-md', a=wp, keydown=key_down,)
    d2 = jp.Div(classes='cursor-pointer', a=d1, model=[wp, 'text'], style='width: 100px')
    qp = jp.QPopupEdit(a=d2, buttons=False, debounce=0)
    in1 = jp.QInput(dense=True, autofocus=True, counter=True, a=qp, model=[wp, 'text'], debounce=0)
    # in1.add_event('keydown')
    # in1.on('keydown', key_down)
    after_div = jp.Div()
    b1 = jp.QBtn(flat=True, dense=True, color='negative', icon='cancel', a=after_div)
    b2 = jp.QBtn(flat=True, dense=True, color='positive', icon='check_circle', a=after_div)
    in1.after_slot = after_div
    d3 = jp.Input(value='key test', a=d1, event_propagation=True)
    # d3.debounce = 0
    # d3.on('keydown', key_down)
    return wp


# jp.justpy(color_demo)


html_string = """
<div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-icon color="primary" name="bluetooth" />
        </q-item-section>

        <q-item-section>Icon as avatar</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar color="teal" text-color="white" icon="bluetooth" />
        </q-item-section>

        <q-item-section>Avatar-type icon</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar rounded color="purple" text-color="white" icon="bluetooth" />
        </q-item-section>

        <q-item-section>Rounded avatar-type icon</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar color="primary" text-color="white">
            R
          </q-avatar>
        </q-item-section>

        <q-item-section>Letter avatar-type</q-item-section>
      </q-item>

      <q-separator />

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
        <q-item-section>Image avatar</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar square>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
        <q-item-section>Image square avatar</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar rounded>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
        <q-item-section>Image rounded avatar</q-item-section>
      </q-item>

      <q-separator />

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar rounded>
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-avatar>
        </q-item-section>
        <q-item-section>List item</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section thumbnail>
          <img src="https://cdn.quasar.dev/img/mountains.jpg">
        </q-item-section>
        <q-item-section>List item</q-item-section>
      </q-item>
    </q-list>
  </div>
"""

html_string = """
<div>

<p>Please select your gender:</p>
  <label class="inline-block mb-1 p-1"><input type="radio" name="gender" value="male"><span class="ml-1">Male</span></label>
  <label class="inline-block mb-1 p-1"><input type="radio" name="gender" value="female"><span class="ml-1">Female</span></label>
  <label class="inline-block mb-1 p-1"><input type="radio" name="gender" value="other"><span class="ml-1">Other</span></label>

  <br>

<p>Please select your age:</p>
  <label class="inline-block mb-1 p-1"><input type="radio" name="age" value="30"><span class="ml-1"> 0 - 30 </span></label><br>
  <label class="inline-block mb-1 p-1"><input type="radio" name="age" value="60"><span class="ml-1"> 31 - 60 </span></label><br>
  <label class="inline-block mb-1 p-1"><input type="radio" name="age" value="100"><span class="ml-1"> 61 - 100 </span></label><br>

<br>
  <input type="submit" value="Submit Form">

</div>
"""
# d = jp.parse_html(html_string, classes='m-2 p-2')
# for i in d.commands:
#     print(i)


def radio_test1():
    wp = jp.WebPage()
    root = jp.Div(name='root', classes='m-2 p-2', a=wp)
    c1 = jp.Div(a=root)

    c2 = jp.P(a=c1, text='Please select your gender:')

    c3 = jp.Label(classes='inline-block mb-1 p-1', a=c1)
    c4 = jp.Input(type='radio', name='gender', value='male', a=c3)
    c5 = jp.Span(classes='ml-1', a=c3, text='Male')

    c6 = jp.Label(classes='inline-block mb-1 p-1', a=c1)
    c7 = jp.Input(type='radio', name='gender', value='female', a=c6)
    c8 = jp.Span(classes='ml-1', a=c6, text='Female')

    c9 = jp.Label(classes='inline-block mb-1 p-1', a=c1)
    c10 = jp.Input(type='radio', name='gender', value='other', a=c9)
    c11 = jp.Span(classes='ml-1', a=c9, text='Other')

    c12 = jp.Br(a=c1)

    c13 = jp.P(a=c1, text='Please select your age:')
    c14 = jp.Label(classes='inline-block mb-1 p-1', a=c1)
    c15 = jp.Input(type='radio', name='age', value='30', a=c14)
    c16 = jp.Span(classes='ml-1', a=c14, text='0 - 30')
    c17 = jp.Br(a=c1)
    c18 = jp.Label(classes='inline-block mb-1 p-1', a=c1)
    c19 = jp.Input(type='radio', name='age', value='60', a=c18)
    c20 = jp.Span(classes='ml-1', a=c18, text='31 - 60')
    c21 = jp.Br(a=c1)
    c22 = jp.Label(classes='inline-block mb-1 p-1', a=c1)
    c23 = jp.Input(type='radio', name='age', value='100', a=c22)
    c24 = jp.Span(classes='ml-1', a=c22, text='61 - 100')
    c25 = jp.Br(a=c1)
    c26 = jp.Br(a=c1)
    # c27 = jp.Input(type='submit', value='Submit Form', a=c1)
    return wp
