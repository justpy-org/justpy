import justpy as jp
import datetime, asyncio
from justpy import WebPage, DivJP, Button, InputJP

def before_click(self, msg):
    self.clicked = 100

def my_click1(self, msg):
    for i in range(1):
        # await asyncio.sleep(1)
        try:
            self.clicked += 1
        except:
            self.clicked = 1
        self.text = f'{self.text} Clicked {str(self.clicked)} times'
    print(msg['page'].to_html(indent=0, indent_step=3, format=True))

async def test(request):
    # s = str(datetime.datetime.now().time())
    jp.print_request(request)
    num = int(request.query_params.get('num', 10))
    # if jp.WebPage.instances:
    #     return jp.WebPage.instances[0]
    wp = jp.WebPage(url='test')
    in1 = jp.InputJP(a=wp)
    b = jp.Button(text='My Button1', a=wp, classes='m-1 p-1 text-xl text-white bg-blue-500 hover:bg-green-500')
    c = jp.Sub(text='test', a=b)
    async def my_click(self, msg):
        for i in range(10):
            # await asyncio.sleep(0.1)
            try:
                self.clicked += 1
            except:
                self.clicked = 1
            self.text = f'Clicked {str(self.clicked)} times'
            await msg['page'].delayed_update(0.01)
            # await asyncio.sleep(2)

    b.on('click', my_click)
    # b.on('before', before_click)
    for i in range(num):
        d = jp.DivJP(text=f'{str(i)}) test div', a=wp, classes='m-1 p-1 text-xl text-white bg-blue-500 hover:bg-green-500 w-1/4')
        c = jp.Sub(text='test', a=d)
        c = jp.IconJP(icon='dog', a=d)
        c = jp.IconJP(icon='cat', a=d)
        c = jp.IconJP(icon='dog', a=d)
    return wp

def calculator_click(self, msg):
    # print('In calculator click')
    # print(self, msg, ' calculator click')
    wp = msg['page']
    if self.text == 'C':
        wp.result.value = '0'
        wp.tape.value = ' '
    elif self.text == '=':
        wp.result.value = str(eval(wp.tape.value))
        wp.tape.value = ' '
    else:
        if wp.tape.value[-1] in '*+-/' or self.text in '*+-/':
            wp.tape.value += ' ' + self.text
        else:
            wp.tape.value +=  self.text
        try:
            wp.result.value = str(eval(wp.tape.value))
        except:
            pass


def calculator(request):
    wp = WebPage(name='calculator')
    tape = InputJP(classes='block p-2 m-2 w-1/3 border text-right text-sm bg-gray-200', a=wp, readonly=True, value=' ')
    result = InputJP(classes='block p-2 m-2 w-1/3 border text-2xl text-right', a=wp, readonly=True, value='0')
    btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-yellow-500 shadow-md'
    layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'],['1', '2', '3', '+'],['C', '0', '.', '=']]
    for line in layout_text:
        d = DivJP(classes='flex w-1/3 ml-2', a=wp)
        for b in line:
            Button(text=b, a=d, classes=btn_classes, click=calculator_click)
    wp.result = result
    wp.tape = tape
    return wp

def test1(request):
    wp = WebPage(name='c')
    d = DivJP(text='hello', a=wp, classes='text-5xl hover:text-lg text-red-500 hover:font-bold bg-yellow-500 m-2 p-2')
    jp.get_tag('sub',text='sub text', a=d)
    jp.get_tag('sup',text='sup text', a=d)
    # d = jp.Sub(text='hello', a=wp, classes='m-1 p-1 text-yellow-500 bg-blue-500  hover:bg-gray-500')
    d.set_class('bg-blue-500')
    d.set_class('text-orange-500', 'hover')
    d.set_class('font-thin', 'hover')
    d.set_class('text-xl', 'hover')
    return wp


def click1(self, msg):
    c = '''
            <svg width="500px" height="500px" viewBox="0 0 150 360"
        preserveAspectRatio="xMidYMid meet"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink">

      <!-- ref -->
      <defs>
        <g id="circles">
          <circle cx="30" cy="30" r="20" fill="blue" fill-opacity="0.5" />
          <circle cx="20" cy="50" r="20" fill="green" fill-opacity="0.5" />
          <circle cx="40" cy="50" r="20" fill="red" fill-opacity="0.5" />
        </g>
      </defs>
      <use href="#circles" />
      <text x="70" y="50">Reference</text>

      <!-- matrix -->
      <filter id="colorMeMatrix">
        <feColorMatrix in="SourceGraphic"
            type="matrix"
            values="0 0 0 0 0
                    1 1 1 1 0
                    0 0 0 0 0
                    0 0 0 1 0" />
      </filter>
      <use href="#circles" transform="translate(0 70)" filter="url(#colorMeMatrix)" />
      <text x="70" y="120">matrix</text>

      <!-- saturate -->
      <filter id="colorMeSaturate">
        <feColorMatrix in="SourceGraphic"
            type="saturate"
            values="0.2" />
      </filter>
      <use href="#circles" transform="translate(0 140)" filter="url(#colorMeSaturate)" />
      <text x="70" y="190">saturate</text>

      <!-- hueRotate -->
      <filter id="colorMeHueRotate">
        <feColorMatrix in="SourceGraphic"
            type="hueRotate"
            values="180" />
      </filter>
      <use href="#circles" transform="translate(0 210)" filter="url(#colorMeHueRotate)" />
      <text x="70" y="260">hueRotate</text>

      <!-- luminanceToAlpha -->
      <filter id="colorMeLTA">
        <feColorMatrix in="SourceGraphic"
            type="luminanceToAlpha" />
      </filter>
      <use href="#circles" transform="translate(0 280)" filter="url(#colorMeLTA)" />
      <text x="70" y="320">luminanceToAlpha</text>
    </svg>
            '''
    self.inner_html = c
def test2(request):
    wp = WebPage(name='g')

    for i in range (10):
        d = DivJP(text=f'{str(i)}) This is my div', classes='m-1 p-1 ', a=wp)
        c = '''
        <svg width="500px" height="500px" viewBox="0 0 150 360"
    preserveAspectRatio="xMidYMid meet"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">

  <!-- ref -->
  <defs>
    <g id="circles">
      <circle cx="30" cy="30" r="20" fill="blue" fill-opacity="0.5" />
      <circle cx="20" cy="50" r="20" fill="green" fill-opacity="0.5" />
      <circle cx="40" cy="50" r="20" fill="red" fill-opacity="0.5" />
    </g>
  </defs>
  <use href="#circles" />
  <text x="70" y="50">Reference</text>

  <!-- matrix -->
  <filter id="colorMeMatrix">
    <feColorMatrix in="SourceGraphic"
        type="matrix"
        values="0 0 0 0 0
                1 1 1 1 0
                0 0 0 0 0
                0 0 0 1 0" />
  </filter>
  <use href="#circles" transform="translate(0 70)" filter="url(#colorMeMatrix)" />
  <text x="70" y="120">matrix</text>

  <!-- saturate -->
  <filter id="colorMeSaturate">
    <feColorMatrix in="SourceGraphic"
        type="saturate"
        values="0.2" />
  </filter>
  <use href="#circles" transform="translate(0 140)" filter="url(#colorMeSaturate)" />
  <text x="70" y="190">saturate</text>

  <!-- hueRotate -->
  <filter id="colorMeHueRotate">
    <feColorMatrix in="SourceGraphic"
        type="hueRotate"
        values="180" />
  </filter>
  <use href="#circles" transform="translate(0 210)" filter="url(#colorMeHueRotate)" />
  <text x="70" y="260">hueRotate</text>

  <!-- luminanceToAlpha -->
  <filter id="colorMeLTA">
    <feColorMatrix in="SourceGraphic"
        type="luminanceToAlpha" />
  </filter>
  <use href="#circles" transform="translate(0 280)" filter="url(#colorMeLTA)" />
  <text x="70" y="320">luminanceToAlpha</text>
</svg>
        '''
        # d.inner_html = c
        d.on('click', click1)



    # d.text = 'hello'

    return(wp)
# jp.justpy(test1)
jp.justpy(test)

# if __name__ == '__main__':
#     jp.uvicorn.run(jp.app, host='0.0.0.0', port=8000)