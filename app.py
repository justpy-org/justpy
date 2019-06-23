import justpy as jp
import datetime, asyncio
from justpy import WebPage, DivJP, Button, Input
import requests
from justpy.tailwind import Tailwind

def inp(self, msg):
    # print(self.parent.components)
    self.value = msg.value
    print(msg)
    for i in self.parent.components:
        i.value = self.value


async def test(request):
    # s = str(datetime.datetime.now().time())
    jp.print_request(request)
    print('in test')
    num = int(request.query_params.get('num', 10))
    wp = WebPage()
    outer_div = jp.Div(classes='flex flex-col w-1/3', a=wp)
    for i in range(num):
        d = jp.TextArea(a=outer_div, classes='form-textarea block m-1 p-1 ', placeholder='test' ,parent=outer_div) # text-white bg-blue-500 hover:bg-blue-200
        # d.parent = outer_div
        jp.Br(a=outer_div)
        d.on('input', inp)
    s = '''
    <div class="flex flex-row-reverse bg-gray-200">
  <div class="text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">1</div>
  <div class="text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">2</div>
  <div class="text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">3</div>
</div>
    '''
    jp.Div(inner_html=s, a=outer_div)
    jp.CalendarDateJP(a=outer_div, month='Feb')
    f = jp.Form(a=outer_div)
    r = jp.Input(type='radio', name='cat1', value='volvo', a=f, classes='form-radio')
    jp.Span(text='Volvo', a=f)
    r = jp.Input(type='radio', name='cat1', value='volvo 12', a=f, classes='form-radio')
    jp.Span(text='Volvo1', a=f)
    r = jp.Input(type='radio', name='cat1', value='volvo 13', a=f)
    jp.Span(text='Volvo2', a=f)
    r = jp.Input(type='checkbox', name='cat1123', value='volvocheck', a=f)
    for t in ['button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'image']:
        r = jp.Input(type=t, name=t, value=t, a=f)
    return wp

async def get_dog(self, msg):
    # breed = msg['page'].breed
    breed = msg.page.breed
    # print(breed, f'https://dog.ceo/api/{breed}/boxer/images/random')
    # r = requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    # result = await jp.JustPy.loop.run_in_executor(None, requests.get, f'https://dog.ceo/api/breed/{breed}/images/random')
    # d = result.json()
    d = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    # d = r.json()
    if self.html_tag == 'img':
        self.src=d['message']
        # return update_only(self)
        # return update_only(self)
    else:
        self.image.src=d['message']
        # return update_only(self.image)

async def change_breed(self, msg):

    print('in change breed')
    print(msg)
    # WebPage.instances[msg['page_id']].breed = self.value
    msg.page.breed = self.value

    # msg.page.breed = self.value
    return await get_dog(self.image, msg)
    # return update_only(self)

async def papillon_demo(request):
    select_html = '''
    <select><option value="affenpinscher" >affenpinscher</option><option value="african" selected>african</option><option value="airedale">airedale</option><option value="akita">akita</option><option value="appenzeller">appenzeller</option><option value="basenji">basenji</option><option value="beagle">beagle</option><option value="bluetick">bluetick</option><option value="borzoi">borzoi</option><option value="bouvier">bouvier</option><option value="boxer">boxer</option><option value="brabancon">brabancon</option><option value="briard">briard</option><option value="bulldog-boston">boston bulldog</option><option value="bulldog-french">french bulldog</option><option value="bullterrier-staffordshire">staffordshire bullterrier</option><option value="cairn">cairn</option><option value="cattledog-australian">australian cattledog</option><option value="chihuahua">chihuahua</option><option value="chow">chow</option><option value="clumber">clumber</option><option value="cockapoo">cockapoo</option><option value="collie-border">border collie</option><option value="coonhound">coonhound</option><option value="corgi-cardigan">cardigan corgi</option><option value="cotondetulear">cotondetulear</option><option value="dachshund">dachshund</option><option value="dalmatian">dalmatian</option><option value="dane-great">great dane</option><option value="deerhound-scottish">scottish deerhound</option><option value="dhole">dhole</option><option value="dingo">dingo</option><option value="doberman">doberman</option><option value="elkhound-norwegian">norwegian elkhound</option><option value="entlebucher">entlebucher</option><option value="eskimo">eskimo</option><option value="frise-bichon">bichon frise</option><option value="germanshepherd">germanshepherd</option><option value="greyhound-italian">italian greyhound</option><option value="groenendael">groenendael</option><option value="hound-afghan">afghan hound</option><option value="hound-basset">basset hound</option><option value="hound-blood">blood hound</option><option value="hound-english">english hound</option><option value="hound-ibizan">ibizan hound</option><option value="hound-walker">walker hound</option><option value="husky">husky</option><option value="keeshond">keeshond</option><option value="kelpie">kelpie</option><option value="komondor">komondor</option><option value="kuvasz">kuvasz</option><option value="labrador">labrador</option><option value="leonberg">leonberg</option><option value="lhasa">lhasa</option><option value="malamute">malamute</option><option value="malinois">malinois</option><option value="maltese">maltese</option><option value="mastiff-bull">bull mastiff</option><option value="mastiff-tibetan">tibetan mastiff</option><option value="mexicanhairless">mexicanhairless</option><option value="mix">mix</option><option value="mountain-bernese">bernese mountain</option><option value="mountain-swiss">swiss mountain</option><option value="newfoundland">newfoundland</option><option value="otterhound">otterhound</option><option value="papillon" selected="selected">papillon</option><option value="pekinese">pekinese</option><option value="pembroke">pembroke</option><option value="pinscher-miniature">miniature pinscher</option><option value="pointer-german">german pointer</option><option value="pointer-germanlonghair">germanlonghair pointer</option><option value="pomeranian">pomeranian</option><option value="poodle-miniature">miniature poodle</option><option value="poodle-standard">standard poodle</option><option value="poodle-toy">toy poodle</option><option value="pug">pug</option><option value="puggle">puggle</option><option value="pyrenees">pyrenees</option><option value="redbone">redbone</option><option value="retriever-chesapeake">chesapeake retriever</option><option value="retriever-curly">curly retriever</option><option value="retriever-flatcoated">flatcoated retriever</option><option value="retriever-golden">golden retriever</option><option value="ridgeback-rhodesian">rhodesian ridgeback</option><option value="rottweiler">rottweiler</option><option value="saluki">saluki</option><option value="samoyed">samoyed</option><option value="schipperke">schipperke</option><option value="schnauzer-giant">giant schnauzer</option><option value="schnauzer-miniature">miniature schnauzer</option><option value="setter-english">english setter</option><option value="setter-gordon">gordon setter</option><option value="setter-irish">irish setter</option><option value="sheepdog-english">english sheepdog</option><option value="sheepdog-shetland">shetland sheepdog</option><option value="shiba">shiba</option><option value="shihtzu">shihtzu</option><option value="spaniel-blenheim">blenheim spaniel</option><option value="spaniel-brittany">brittany spaniel</option><option value="spaniel-cocker">cocker spaniel</option><option value="spaniel-irish">irish spaniel</option><option value="spaniel-japanese">japanese spaniel</option><option value="spaniel-sussex">sussex spaniel</option><option value="spaniel-welsh">welsh spaniel</option><option value="springer-english">english springer</option><option value="stbernard">stbernard</option><option value="terrier-american">american terrier</option><option value="terrier-australian">australian terrier</option><option value="terrier-bedlington">bedlington terrier</option><option value="terrier-border">border terrier</option><option value="terrier-dandie">dandie terrier</option><option value="terrier-fox">fox terrier</option><option value="terrier-irish">irish terrier</option><option value="terrier-kerryblue">kerryblue terrier</option><option value="terrier-lakeland">lakeland terrier</option><option value="terrier-norfolk">norfolk terrier</option><option value="terrier-norwich">norwich terrier</option><option value="terrier-patterdale">patterdale terrier</option><option value="terrier-russell">russell terrier</option><option value="terrier-scottish">scottish terrier</option><option value="terrier-sealyham">sealyham terrier</option><option value="terrier-silky">silky terrier</option><option value="terrier-tibetan">tibetan terrier</option><option value="terrier-toy">toy terrier</option><option value="terrier-westhighland">westhighland terrier</option><option value="terrier-wheaten">wheaten terrier</option><option value="terrier-yorkshire">yorkshire terrier</option><option value="vizsla">vizsla</option><option value="weimaraner">weimaraner</option><option value="whippet">whippet</option><option value="wolfhound-irish">irish wolfhound</option></select>
    '''
    wp = WebPage(name='papillon')
    d1 = DivJP(text='Dog Pics', classes='text-3xl text-teal  m-5 p-3', a=wp)

    # r = requests.get('https://dog.ceo/api/breed/papillon/images/random')
    # d = r.json()
    # result = await jp.JustPy.loop.run_in_executor(None, requests.get, 'https://dog.ceo/api/breed/papillon/images/random')
    # d = result.json()
    d = await jp.get('https://dog.ceo/api/breed/papillon/images/random')
    print(d)
    i = jp.Img(src=d['message'], classes='mr-2 p-2 cursor-pointer', tooltip='Click to get new image')
    wp.add_component(i)
    # return wp
    # wp.add_component(BrJP())
    b = Button(text='Get Another Pic', classes='m-2 p-2 text-blue-500 bg-white hover:bg-blue-200 hover:text-blue-500 border')
    b.add_component(jp.Icon(icon='dog', classes='ml-3'))
    b.image = i
    b.on('click', get_dog)
    i.on('click', get_dog)
    wp.add_component(b)
    # return wp
    select_tag = jp.parse_html(select_html)
    select_tag.value = 'papillon'   # the first component is select because the outer is a div
    select_tag.classes = 'inline m-2 p-2 bg-white hover:bg-blue-dark border rounded-full'
    select_tag.on('change', change_breed)
    select_tag.image = i
    wp.add_component(select_tag)
    wp.breed = 'papillon'
    # print(select_tag.components[0].id, select_tag.components[0].html_tag)
    return wp


def key_test(request):
    wp = WebPage()
    d = jp.TextArea(a=wp, classes='block m-1 p-1 text-white bg-blue-500 hover:bg-blue-700', placeholder='test')
    d.allowed_events += ['keypress']
    # d.on_before = False
    my_div = jp.Div(text='My text', a=wp, classes='m-1 p-1')
    d.my_div = my_div
    def key_event(self, msg):
        # self.value = msg['value']
        print('value', self.value)
        # print(msg['key_data'])
        # d.my_div.text = msg['key_data']['key'] +  ' ' + self.value
        self.my_div.text = self.value
    d.on('keydown', key_event)
    return wp


s = '''
<div class="max-w-sm rounded overflow-hidden shadow-lg">
  <img class="w-full" src="https://tailwindcss.com/img/card-top.jpg" alt="Sunset in the mountains">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">The Coldest Sunset</div>
    <p class="text-gray-700 text-base">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.
    </p>
  </div>
  <div class="px-6 py-4">
    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">#photography</span>
    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">#travel</span>
    <span class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">#winter</span>
  </div>
</div>
'''

s1 = '''
<div class="max-w-sm w-full lg:max-w-full lg:flex">
  <div class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" style="background-image: url('https://tailwindcss.com/img/card-left.jpg')" title="Woman holding a mug">
  </div>
  <div class="border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t lg:border-gray-400 bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
    <div class="mb-8">
      <p class="text-sm text-gray-600 flex items-center">
        <svg class="fill-current text-gray-500 w-3 h-3 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M4 8V6a6 6 0 1 1 12 0v2h1a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-8c0-1.1.9-2 2-2h1zm5 6.73V17h2v-2.27a2 2 0 1 0-2 0zM7 6v2h6V6a3 3 0 0 0-6 0z" />
        </svg>
        Members only
      </p>
      <div class="text-gray-900 font-bold text-xl mb-2">Can coffee make you a better developer?</div>
      <p class="text-gray-700 text-base">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.</p>
    </div>
    <div class="flex items-center">
      <img class="w-10 h-10 rounded-full mr-4" src="https://tailwindcss.com/img/jonathan.jpg" alt="Avatar of Jonathan Reinink">
      <div class="text-sm">
        <p class="text-gray-900 leading-none">Jonathan Reinink</p>
        <p class="text-gray-600">Aug 18</p>
      </div>
    </div>
  </div>
</div>
'''

s2 = '''
<form class="w-full max-w-lg">
  <div class="flex flex-wrap -mx-3 mb-6">
    <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
        First Name
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="grid-first-name" type="text" placeholder="Jane">
      <p class="text-red-500 text-xs italic">Please fill out this field.</p>
    </div>
    <div class="w-full md:w-1/2 px-3">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-last-name">
        Last Name
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-last-name" type="text" placeholder="Doe">
    </div>
  </div>
  <div class="flex flex-wrap -mx-3 mb-6">
    <div class="w-full px-3">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-password">
        Password
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-password" type="password" placeholder="******************">
      <p class="text-gray-600 text-xs italic">Make it as long and as crazy as you'd like</p>
    </div>
  </div>
  <div class="flex flex-wrap -mx-3 mb-2">
    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-city">
        City
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-city" type="text" placeholder="Albuquerque">
    </div>
    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-state">
        State
      </label>
      <div class="relative">
        <select class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-state">
          <option>New Mexico</option>
          <option>Missouri</option>
          <option>Texas</option>
        </select>
        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
          <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
        </div>
      </div>
    </div>
    <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
      <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-zip">
        Zip
      </label>
      <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-zip" type="text" placeholder="90210">
    </div>
  </div>
</form>
'''


s3 = '''
<div class="block">
  <span class="text-gray-700">Checkboxes</span>
  <div class="mt-2">
    <div>
      <label class="inline-flex items-center">
        <input type="checkbox" class="form-checkbox text-indigo-600" checked>
        <span class="ml-2">Option 1</span>
      </label>
    
    </div>
    <br>
    <div>
      <label class="inline-flex items-center">
        <input type="checkbox" class="form-checkbox text-gray-800"/>
        <span class="ml-2">Option 2</span>
      </label>
    </div>
    <br/>
    <div>
      <label class="inline-flex items-center">
        <input type="checkbox" class="form-checkbox text-gray-800"/>
        <span class="ml-2">Option 3</span>
      </label>
    </div>
  </div>
</div>
'''


s4 = '''
<div class="block">
  <span class="text-gray-700">Radio Buttons</span>
  <div class="mt-2">
    <div>
      <label class="inline-flex items-center">
        <input type="radio" class="form-radio text-yellow-800" name="radio-direct" value="1" checked/>
        <span class="ml-2">Option 1</span>
      </label>
    </div>
    <div>
      <label class="inline-flex items-center">
        <input type="radio" class="form-radio text-gray-800" name="radio-direct" value="2"/>
        <span class="ml-2">Option 2</span>
      </label>
    </div>
    <div>
      <label class="inline-flex items-center">
        <input type="radio" class="form-radio text-gray-800" name="radio-direct" value="3"/>
        <span class="ml-2">Option 3</span>
      </label>
    </div>
  </div>
</div>
'''

s5 = '''
<div><span>First text nbsp &nbsp;&nbsp;</span> <span> span text</span> <span>second text </span></div>
'''

s6= '''
<form name="form1">
<input name="shalom" value="hello">
<div>
  <input type="checkbox"  name="my_check" value="checky">
  <label >Check me</label>
</div>
<p>Select a maintenance drone:</p>

<div>
  <input type="radio" id="huey" name="drone" value="huey">
  <label for="huey">Huey</label>
</div>

<div>
  <input type="radio" id="dewey" name="drone" value="dewey" class="form-radio text-blue-500">
  <label for="dewey">Dewey</label>
</div>

<div>
  <input type="radio" id="louie" name="drone" value="louie" checked>
  <label for="louie">Louie</label>
</div>
<select value="saab">
  <option value="volvo">Volvo</option>
  <option value="saab" selected="true">Saab</option>
  <option value="mercedes">Mercedes</option>
  <option value="audi">Audi</option>
</select>
<div>
    <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" >Submit</button>
  </div>
</form>
'''

s7 = '''
<div class="antialiased bg-gray-200 font-sans">
    <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-center min-h-screen">
            <div class="max-w-md w-full px-3">
                <div class="bg-white shadow-xl rounded-lg overflow-hidden">
                    <div class="bg-cover bg-top h-40" style="background-image: url(https://images.unsplash.com/photo-1518296736038-a6ab5e1488fc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1267&q=80)">
                    </div>
                    <div class="flex pt-2 p-5">
                        <div class="bg-cover bg-center w-32 h-32 -mt-16 rounded-full border-4 border-white" style="background-image: url(https://images.unsplash.com/photo-1520366914631-d250fd86eed2?ixlib=rb-1.2.1&auto=format&fit=crop&w=334&q=80)">
                        </div>
                        <div class="ml-3">
                            <div class="font-bold text-2xl">Babs and Lori</div>
                            <div class="flex items-start">
                                <span>
                                    <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                        <path class="fill-current text-gray-500" d="M4.34 14.66a8 8 0 1 1 11.32 0L11.4 18.9a2 2 0 0 1-2.82 0l-4.25-4.24zm1.42-1.42L10 17.5l4.24-4.25a6 6 0 1 0-8.48 0zM10 12a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0-2a1 1 0 1 0 0-2 1 1 0 0 0 0 2z" /></svg>
                                </span>
                                <span class="text-gray-700 ml-2">New York, NY</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex px-5 mt-2 mb-6 -mx-2">
                        <button class="leading-relaxed rounded-full mx-2 font-bold py-1 w-1/2 bg-blue-500 hover:bg-blue-600 text-white">Follow</button>
                        <button class="leading-relaxed rounded-full mx-2 font-bold py-1 w-1/2 text-gray-900 bg-white border-2 border-gray-400 hover:border-gray-500">Message</button>
                    </div>
                    <div class="border-t-2 border-gray-200 p-5">
                        <div class="flex items-start">
                            <span>
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                    <path class="fill-current text-gray-500" d="M10 11a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 19a1 1 0 0 1-2 0c0-3.84 2.8-7 6.33-7h5.34c3.52 0 6.33 3.16 6.33 7a1 1 0 0 1-2 0c0-2.79-1.97-5-4.33-5H7.33C4.97 14 3 16.21 3 19z" /></svg>
                            </span>
                            <div class="relative">
                                <span class="font-bold text-gray-900 ml-2">12</span>
                                <span class="inline text-gray-700">Followers you know</span>
                            </div>
                        </div>
                        <div class="flex justify-between items-center mt-3">
                            <div class="flex flex-row-reverse justify-end">
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white" style="background-image: url(https://images.unsplash.com/photo-1458071103673-6a6e4c4a3413?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1518806118471-f28b20a1d79d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=80)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1470406852800-b97e5d92e2aa?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1473700216830-7e08d47f858e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1543610892-0b1f7e6d8ac1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1502323777036-f29e3972d82f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=60)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1530424426433-967ce567454d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=100&q=60)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1525879000488-bff3b1c387cf?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=60)">
                                </div>
                                <div class="bg-cover bg-center w-12 h-12 rounded-full border-4 border-white -mr-3" style="background-image: url(https://images.unsplash.com/photo-1521132293557-5b908a59d1e1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=60)">
                                </div>
                            </div>
                            <div class="w-10 h-10 rounded-full border-2 border-gray-400 text-sm font-bold text-gray-700 flex justify-center items-center">+3</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''

# https://stackoverflow.com/questions/17066875/how-to-inspect-formdata
def radio_change(self, msg):
    print('Radio change', self.checked)
    print(self.name, self.components)
    print_name(self.name, msg['page'])
    return True


def print_name(name, container):
    # print(name, container, container.components)
    for c in container.components:
        # print(c,c.id)
        if hasattr(c, 'name'):
            if c.name == name:
                try:
                    print('****** Succes',c.name, c.value, c.checked)
                except:
                    print('problem', c.name)
        # print(name, c.components)
        try:
            print_name(name, c)
        except:
            print('No self.components', c)
    # print('done')

async def test_parse(request):
    jp.print_request(request)
    wp = WebPage()
    # if request.url =

    print(request.query_params)
    for key, value in request.query_params.items():
        print(key, value)

    for i in range(1):
        c = await jp.parse_html_file_async('html/calculator.html')
        c.classes='m-1'
        for i in range(1):
            wp.add(c)
        return wp
        print(c.name_dict)
        for i in []: #c.name_dict['drone']:
            print(i.name, i.value, i.checked)
            i.on('change', radio_change)
        #    print(c.to_html(indent_step=2))
        # c = jp.Div(text='hello')
        wp.add(c)
        wp.add(jp.Br())

    return wp


def test_check(request):
    jp.print_request(request)
    wp = WebPage()
    in1 = jp.Input(type='checkbox', classes='m-2 form-checkbox', a=wp, value='hello')
    d = jp.Div(text='div in middle', a=wp)
    l = jp.Label(text='Checkbox label', for_component=in1, a=wp)
    return wp

d = jp.Div(classes='m-2 h-1/2 border')

async def comp_update_test(request):
    global d
    wp = WebPage()
    jp.Div(text='Chat', classes='text-3xl', a=wp)
    in1 = jp.Input(placeholder='Enter text', a=wp, classes='m-2')
    b = jp.Button(text='Add', a=wp, classes='m-2 p-2 text-blue-500 bg-white hover:bg-blue-200 hover:text-blue-500 border')

    wp.add(d)
    d.pages.append(wp)
    print(d.pages)
    b.in1 = in1
    b.d = d
    async def b_click(self, msg):
        jp.Div(text=self.in1.value, a=self.d)
        await self.d.update()
        return True
    b.on('click', b_click)
    return wp

def simple_input(self, msg):
    print('simple input' ,msg.page.data['initial'])
    print('event change', msg.page.data['initial'])
    # self.d.text = self.value

    self.d.text = msg['page'].data['initial']

def b_click(self, msg):
    # msg['page'].data['initial'] = 'Hello'
    msg.page.data['initial'] = 'Hello'

def simple(request):
    wp = WebPage(data={'initial': 'Initial text'})
    in1 = jp.TextArea(placeholder='test', classes='m-1 p-1 border text-xl', a=wp, model=[wp, 'initial'])
    b1 = jp.Button(classes='m-2 p-2 text-blue-500 bg-white hover:bg-blue-200 hover:text-blue-500 border', a=wp, text='My Button')
    b1.on('click', b_click)
    # in1.on('input', simple_input)
    for i in range(10):
        d = jp.Div(text=wp.data['initial'], a=wp, model=[wp, 'initial'])
    # in1.d = d
    return wp

input_types = ['button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'file', 'hidden', 'image',
        'month', 'number', 'password', 'radio', 'range', 'reset', 'search', 'submit', 'tel', 'text', 'time', 'url', 'week']

def input_test(request):
    wp = WebPage()
    jp.Div(text='Input types', classes='m-1 p-1 text-3xl', a=wp)
    for t in input_types:
        jp.Div(text=t, a=wp, classes='m-1 p-1 text-xl text-red-500')
        in1 = jp.Input(type=t, a=wp)
        if t=='button':
            in1.value='Button'
    return wp

def exec_test(request):
    wp = WebPage()
    e = jp.EditorJP(a=wp)
    b = Button(text='switch', a=wp)

    def b_click(self, msg):
        jp.justpy(simple, False)
    b.on('click', b_click)
    return wp

def inners(request):
    wp = WebPage()
    with open('html/svg_tiger.html', encoding="utf-8") as f:
        s = f.read()
    d = DivJP()
    for i in range(10):
        wp.add(d)
    d.inner_html = s
    return wp

def b_simple(request):
    wp = WebPage()
    b = jp.Button(text='click me', classes='text-white bg-blue-500 text-2xl m-1 p-1', a=wp)
    d = jp.Div(text='Not clicked', a=wp)
    b.d = d
    def click_me(self, msg):
        self.text = 'I was clicked'
        self.d.text = 'Yes, there was a click'
    b.on('click', click_me)
    return wp


from timeit import default_timer as timer

async def change_text(self, msg):
    msg.page.data['text'] = self.value
    self.result.inner_html = self.r.to_html()

async def colors_test(request):
    wp = WebPage(data={'text': 'o'})
    in1 = jp.Input(placeholder='text goes here', a=wp, classes='m-2')
    result = jp.Div(a=wp)
    outer = jp.Div(classes='flex flex-col items-stretch')
    print('length', len(Tailwind.tw_dict['background_color'])*len(Tailwind.tw_dict['text_color']))
    for bg in Tailwind.tw_dict['background_color'][:]:
        r = jp.Div(a=outer)
        for color in Tailwind.tw_dict['text_color'][:]:
            d = jp.Div( classes=f'{color} {bg} inline', a=r, model=[wp, 'text'])
        # jp.Div(a=r, classes='h-0')
    start = timer()
    result.inner_html = outer.to_html()
    end = timer()
    print('elapsed time',end - start)
    in1.result = result
    in1.r = outer
    in1.on('input', change_text)
    return wp

async def colors_test1(request):
    wp = WebPage(data={'text': 'o'})
    in1 = jp.Input(placeholder='text goes here', a=wp, classes='m-2')
    result = jp.Div(a=wp)
    r = jp.Div(a=wp)
    print('length', len(Tailwind.tw_dict['background_color'])*len(Tailwind.tw_dict['text_color']))
    for bg in Tailwind.tw_dict['background_color'][:]:
        for color in Tailwind.tw_dict['text_color'][:]:
            d = jp.Span( classes=f'{color} {bg}', a=r, model=[wp, 'text'])
        jp.Div(a=r)
    # start = timer()
    # result.inner_html = r.to_html()
    # end = timer()
    # print('elapsed time',end - start)
    in1.result = result
    in1.r = r
    in1.on('input', change_text)
    return wp





def my_click(self, msg):
    print('in click')
    print(msg)
    self.text = 'I was clicked'

def very_simple(request):
    wp = WebPage()
    d = jp.Div(a=wp)
    # small_div = jp.Div(text='hello', a=d, classes='text-xl m-1 p-1 text-white bg-yellow-500')
    # d.add(*[small_div]*3000)
    for i in range(30):
        c = jp.Div(text='hello', a=d, classes='w-1/3 text-xl m-1 p-1 text-white bg-yellow-500', onclick=lambda self, msg: print('Lambda click!'))
        # d.add(small_div)
    # d1 = jp.Div(a=wp)
    # d1.inner_html = d.to_html()
    return wp


def form_test(request):
    wp = WebPage()
    f = jp.Form(a=wp)
    r = jp.Input(type='radio', name='cat1', value='volvo', a=f, classes='form-radio')
    jp.Span(text='Volvo', a=f)
    r = jp.Input(type='radio', name='cat1', value='volvo 12', a=f, classes='form-radio')
    jp.Span(text='Volvo1', a=f)
    r = jp.Input(type='radio', name='cat1', value='volvo 13', a=f)
    jp.Span(text='Volvo2', a=f)
    r = jp.Input(type='checkbox', name='cat1123', value='volvocheck', a=f)
    b = Button(text='Click me now', a=f)
    return wp


# jp.justpy(comp_update_test)
jp.justpy(papillon_demo)
# jp.justpy(very_simple)
# jp.justpy(form_test)
# jp.justpy(simple, websockets=True)
# jp.justpy(test)
# jp.justpy(colors_test, websockets=True)
# jp.justpy(clock_test)