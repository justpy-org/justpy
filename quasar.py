from justpy import *
import demjson


def load_json(options_string):
    return Dict(demjson.decode(options_string.encode("ascii", "ignore")))

@SetRoute('/q_test')
def q_test():
    wp = WebPage(template_file='quasar.html')
    d = QDiv(classes='text-white bg-yellow text-h3', style='height: 500px; width: 500px', a=wp, text='Tap me',
             v_ripple={'color': 'blue'})
    q = QAvatar(a=wp)
    q.color = 'red'
    q.text_color = 'white'
    q.icon = 'fas fa-ambulance'
    wp.add(q,q)
    q = QAvatar(a=wp)
    Img(src="https://cdn.quasar.dev/img/avatar.png", a=q)
    d= Div(classes="q-pa-md q-gutter-sm", a=wp)
    b = QButton(label='Hello', color='primary', a=d)
    # b1 = parse_html( '<q-btn icon="phone" label="Stacked" stack glossy color="purple"></q-btn>', a=d)
    b1 = parse_html('<q-btn icon="directions" label="Stacked" stack glossy color="purple"/>', a=d)
    s = QSpinner(spinner_type='hourglass', a=d)
    b1.add_scoped_slot('loading', s)
    b1.loading = True
    def click(self, msg):
        b1.loading = not b1.loading
        self.label = 'clicked!'
    b.on('click', click)
    b2 = parse_html('<q-btn color="teal"><q-icon left size="3em" name="map" /><div>Label</div></q-btn>', a=d)
    spinner_types = ['audio', 'ball', 'bars', 'comment', 'cube', 'dots', 'facebook', 'gears', 'grid', 'hearts',
                     'hourglass', 'infinity', 'ios', 'oval', 'pie', 'puff', 'radio', 'rings', 'tail']
    colors = ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light_green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey']
    for i in range(len(spinner_types)):
        s = QSpinner(color=colors[i], a=d, size=f'{(1+i)//2}em', thickness=f'{i}', spinner_type=spinner_types[i])
    d = QDiv(classes='text-white bg-red text-h3', style='height: 500px; width: 500px', a=wp, text='Tap me', v_ripple={'color': 'blue'})
    # setattr(d, 'v-ripple', True)
    return wp


def test_directives():
    wp = WebPage(template_file='quasar.html')
    d = QDiv(classes='text-white bg-blue text-h3', style='height: 500px; width: 500px', a=wp, text='Tap me', v_ripple=True)
    # setattr(d, 'v-ripple', True)
    return wp

@SetRoute('/test_input')
def test_input():
    wp = WebPage(template_file='quasar.html')
    icon = QIcon(name='event', a=wp)
    d = QDiv(classes="q-gutter-md",style="max-width: 300px", a=wp)
    d1 = QDiv(classes="q-pa-md", a=d)
    in1 = QInput(a=d1, color="purple-12", label='Standard')
    in1.add_scoped_slot('prepend', icon)
    in1.value = 1
    in2 = QInput(a=d1, color="orange", label='Second one')
    in1.in2 = in2
    def my_input(self, msg):
        self.in2.value = self.value
    in1.on('input', my_input)

    b = QButton(label='Hello', color='primary', a=d)
    b.in1 = in1
    b.in2 = in2
    def my_click(self, msg):
        print('clicked')
        self.label = 'clicked'
        self.in1.value = 'Hello'
        self.in2.value = 'You'
    b.on('click', my_click)

    # setattr(d, 'v-ripple', True)
    return wp

@SetRoute('/test_model')
def test_model():

    wp = WebPage(template_file='quasar.html') # data={'text': 'EliEli'}
    in5 = QInput(a=wp)
    icon = QIcon(color='red', name='fas fa-dog', a=wp)
    icon1 = QIcon(color='orange', name='fas fa-cat', a=wp)
    s = QSplitter(style="height: 400px", a=wp, value=80, disable=False)
    # d = Div(classes="q-gutter-md", style="max-width: 500px", a=wp)
    d = Div(classes="q-gutter-md", style="max-width: 500px")
    s.before_slot = d
    d1 = Div(classes="q-pa-md", a=d, data={'text': 'EliEli'})
    in1 = QInput(a=d1, color="purple-12", label='Standard', model=[d1, 'text']) # model=[wp, 'text']

    in1.hint_slot = Span(text='try dog span')
    # in1.counter_slot = Div()
    in1.bottom_slots = True
    in1.counter = True
    in1.debounce = 500
    # in1.add_scoped_slot('hint', Div(text='try dog'))
    # in1 = QInput(a=wp, color="purple-12", label='Standard') # model=[wp, 'text']
    in1.add_scoped_slot('append', icon)


    in1.add_scoped_slot('prepend', QIcon(name='favorite', color='blue'))
    def focus_event(self, msg):
        print('Focused-----------------------!')
    def blur_event(self, msg):
        print('bluRREDDD--------------!')
    in1.add_allowed_event('focusin')
    in1.add_allowed_event('focusout')
    # in1.on('focusin', focus_event)
    # in1.on('focusout', blur_event)
    # in1.add_scoped_slot('after', icon1)
    in1.add_scoped_slot('before', icon)
    # in1.add_scoped_slot('append', icon)
    # in1.add_scoped_slot('before', icon1)
    # in1.value = 1
    in2 = QInput(a=d1, color="orange", label='Second one', clearable=True, model=[d1, 'text'], type="text", prefix='$')
    in2.add_scoped_slot('prepend', icon1)
    in3 = parse_html("""
    <q-input standout v-model="email"  prefix="Email:" suffix="@gmail.com" hint="email"></q-input>
    """, a=d1)
    in3.mask = "###/##"
    in3.add_scoped_slot('prepend', QIcon(name='mail'))
    in3.add_scoped_slot('after', Div(text='hello'))
    d2 = Div(classes="q-pa-md", style="max-width: 500px")
    c = parse_html("""
    <q-tabs
        
        inline-label
        class="bg-primary text-white shadow-2"
      >
        <q-tab name="mails" icon="mail" label="Mails" />
        <q-tab name="alarms" icon="alarm" label="Alarms" />
        <q-tab name="movies" icon="movie" label="Movies" />
        <q-tab name="photos" icon="photo" label="Photos" />
        <q-tab name="videos" icon="slow_motion_video" label="Videos" />
        <q-tab name="addressbook" icon="people" label="Address Book" />
      </q-tabs>
    """, a=d2)
    s.after_slot = d2
    c.model = [d1, 'text']
    return wp

@SetRoute('/test_comps')
def test_comps():
    wp = WebPage(template_file='quasar.html')
    c = parse_html("""
    <div class="q-pa-md q-gutter-sm">
    <div class="text-h4">
      <span>Title</span>
      <q-badge align="top">cli v1.0.0</q-badge>
    </div></div>
    """, a=wp)
    c = parse_html("""
      <q-badge color="red">
      12 <q-icon name="warning" color="white" class="q-ml-xs" />
    </q-badge>
       """, a=wp)
    c.text = '15'
    d = Div(classes="q-pa-md q-gutter-sm", a=wp)
    banner = QBanner(classes="bg-primary text-white", text='Unfortunately, the credit card did not go through, please try again.', a=d, inline_actions=False)
    d2 = Span()
    QButton(flat=True, color='white', label='Dismiss', a=d2)
    QButton(flat=True, color='white', label='Update Credit Card', a=d2)
    banner.add_scoped_slot('action', d2)
    banner.add_scoped_slot('avatar', QIcon(name="signal_wifi_off", color="white"))
    Div(classes='text-h2', text='Buttons', a=wp)
    c = parse_html("""
    <div class="q-pa-md q-gutter-sm">
    <q-btn flat color="primary" label="Flat" />
    <q-btn flat rounded color="primary" label="Flat Rounded" />
    <q-btn flat round color="primary" icon="card_giftcard" />
    <br/>
    <q-btn outline color="primary" label="Outline" />
    <q-btn outline rounded color="primary" label="Outline Rounded" />
    <q-btn outline round color="primary" icon="card_giftcard" />
    <br/>
    <q-btn push color="primary" label="Push" />
    <q-btn push color="primary" round icon="card_giftcard" />
    <q-btn push color="white" text-color="primary" label="Push" />
    <q-btn push color="white" text-color="primary" round icon="card_giftcard" />
    <br/>
    <q-btn unelevated color="primary" label="Unelevated" />
    <q-btn unelevated rounded color="primary" label="Unelevated Rounded" />
    <q-btn unelevated round color="primary" icon="card_giftcard" />
    <br/>
    <q-btn no-caps color="primary" label="No caps" />
    <br/>
    <q-btn class="glossy" color="teal" label="Glossy" />
    <q-btn class="glossy" rounded color="deep-orange" label="Glossy Rounded" />
    <q-btn class="glossy" round color="primary" icon="card_giftcard" />
    <q-btn class="glossy" round color="secondary" icon="local_florist" />
    <q-btn class="glossy" round color="deep-orange" icon="local_activity" />
    <br/>
    <q-btn align="left" style="width: 200px;" color="primary" label="Align to left" size="xl" ripple="{ color: 'yellow' }"></q-btn>
    <q-btn align="right" style="width: 200px;" color="secondary" label="Align to right" />
    <q-btn align="between" style="width: 200px;" color="accent" label="Align between" icon="flight_takeoff" />
    <q-btn align="around" style="width: 200px;" color="brown-5" label="Align around" icon="lightbulb_outline" />
  </div>
    """, a=wp)
    c = QButton(align='left',  color='primary', label="Align to left", a=wp, size="xl", ripple={'color': 'yellow' })
    Div(classes='text-h2', text='Button Group', a=wp)
    c = parse_html("""
    <div class="q-pa-md q-gutter-y-md column items-start">
    <q-btn-group push>
      <q-btn push label="First" icon="timeline" />
      <q-btn push label="Second" icon="visibility" />
      <q-btn push label="Third" icon="update" />
    </q-btn-group>

    <q-btn-group push>
      <q-btn color="yellow" glossy text-color="black" push label="First" icon="verified_user" />
      <q-btn color="amber" glossy text-color="black" push label="Second" />
      <q-btn color="orange" glossy text-color="black" push label="Third" />
    </q-btn-group>

    <q-btn-group outline>
      <q-btn outline color="brown" label="First" />
      <q-btn outline color="brown" label="Second" icon-right="watch_later" />
      <q-btn outline color="brown" label="Third" />
    </q-btn-group>

    <q-btn-group>
      <q-btn color="secondary" glossy label="First" />
      <q-btn color="secondary" glossy label="Second" />
      <q-btn color="secondary" glossy label="Third" />
      <q-btn color="secondary" glossy label="Fourth" />
    </q-btn-group>

    <q-btn-group>
      <q-btn color="accent" icon="timeline" />
      <q-btn color="accent" icon="visibility" />
      <q-btn color="accent" icon="update" />
    </q-btn-group>

    <q-btn-group rounded>
      <q-btn color="amber" rounded glossy icon="timeline" />
      <q-btn color="amber" rounded glossy icon="visibility" />
      <q-btn color="amber" rounded glossy icon-right="update" label="Update" />
    </q-btn-group>
  </div>
    """, a=wp)
    Div(classes='text-h4', text='Lists', a=wp)
    c = parse_html("""
    <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered separator>
      <q-item clickable v_ripple>
        <q-item-section>Single line item</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>
          <q-item-label>Item with caption</q-item-label>
          <q-item-label caption>Caption</q-item-label>
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>
          <q-item-label overline>OVERLINE</q-item-label>
          <q-item-label>Item with caption</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
    """, a=wp)
    c= parse_html("""
    <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
      <q-item clickable v-ripple>
        <q-item-section>Icon as avatar</q-item-section>
        <q-item-section avatar>
          <q-icon color="primary" name="bluetooth" />
        </q-item-section>
      </q-item>

      <q-item clickable v_ripple name="list1">
        <q-item-section name="list2">Avatar-type icon click here</q-item-section>
        <q-item-section avatar>
          <q-avatar color="teal" text-color="white" icon="bluetooth" />
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>Rounded avatar-type icon</q-item-section>
        <q-item-section avatar>
          <q-avatar rounded color="purple" text-color="white" icon="bluetooth" />
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>Letter avatar-type</q-item-section>
        <q-item-section avatar>
          <q-avatar color="primary" text-color="white">
            R
          </q-avatar>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-item clickable v-ripple>
        <q-item-section>Image avatar</q-item-section>
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>Image square avatar</q-item-section>
        <q-item-section avatar>
          <q-avatar square>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>Image rounded avatar</q-item-section>
        <q-item-section avatar>
          <q-avatar rounded>
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-avatar>
        </q-item-section>
      </q-item>
      <q-separator></q-separator>
      <q-item clickable v-ripple>
        <q-item-section>List item</q-item-section>
        <q-item-section avatar>
          <q-avatar rounded>
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-avatar>
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section>List item</q-item-section>
        <q-item-section thumbnail>
          <img src="https://cdn.quasar.dev/img/mountains.jpg">
        </q-item-section>
      </q-item>
    </q-list>
  </div>
    """, a=wp)

    print(c.name_dict)
    print(c.name_dict['list1'], c.name_dict['list1'].__class__)
    def click_me(self, msg):
        c.name_dict['list2'][0].text = 'Clicked'
    c.name_dict['list1'].on('click', click_me)
    Div(classes='text-h4', text='Dropdwon Button', a=wp)
    c = parse_html("""
    <div class="q-pa-md">
    <q-btn-dropdown color="primary" label="Dropdown Button">
      <q-list>
        <q-item clickable v_close_popup>
          <q-item-section>
            <q-item-label>Photos</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v_close_popup>
          <q-item-section>
            <q-item-label>Videos</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v_close_popup>
          <q-item-section>
            <q-item-label>Articles</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
    """, a=wp)
    return wp

def test_panel():
    wp = WebPage(template_file='quasar.html')
    c = parse_html("""
    <div class="q-pa-md" style="max-width: 350px">
    <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
    <q-tab-panels
      value="mails"
      animated
      swipeable
      infinite
      class="bg-purple text-white shadow-2 rounded-borders"
    >
      <q-tab-panel name="mails">
        <div class="text-h6">Mails</div>
        <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
      </q-tab-panel>

      <q-tab-panel name="alarms">
        <div class="text-h6">Alarms</div>
        <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
      </q-tab-panel>

      <q-tab-panel name="movies">
        <div class="text-h6">Movies</div>
        <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
      </q-tab-panel>
    </q-tab-panels>
  </div>
    """, a=wp)
    c = parse_html("""
      <div class="q-pa-md">
    <div class="q-gutter-y-md" style="max-width: 600px">
      <q-tabs
        value="Movies"
        class="text-teal"
      >
        <q-tab name="mails" icon="mail" label="Mails" />
        <q-tab name="alarms" icon="alarm" label="Alarms" />
        <q-tab name="movies" icon="movie" label="Movies" />
      </q-tabs>

      <q-tabs
        v-model="tab"
        inline-label
        class="bg-purple text-white shadow-2"
      >
        <q-tab name="mails" icon="mail" label="Mails" />
        <q-tab name="alarms" icon="alarm" label="Alarms" />
        <q-tab name="movies" icon="movie" label="Movies" />
      </q-tabs>

      <q-tabs
        v-model="tab"
        no-caps
        class="bg-orange text-white shadow-2"
      >
        <q-tab name="mails" label="Mails" />
        <q-tab name="alarms" label="Alarms" />
        <q-tab name="movies" label="Movies" />
      </q-tabs>

      <q-tabs
        v-model="tab"
        class="bg-teal text-yellow shadow-2"
      >
        <q-tab name="mails" icon="mail" />
        <q-tab name="alarms" icon="alarm" />
        <q-tab name="movies" icon="movie" />
      </q-tabs>

      <q-tabs
        v-model="tab"
        inline-label
        class="bg-primary text-white shadow-2"
      >
        <q-tab name="mails" icon="mail" label="Mails" />
        <q-tab name="alarms" icon="alarm" label="Alarms" />
        <q-tab name="movies" icon="movie" label="Movies" />
        <q-tab name="photos" icon="photo" label="Photos" />
        <q-tab name="videos" icon="slow_motion_video" label="Videos" />
        <q-tab name="addressbook" icon="people" label="Address Book" />
      </q-tabs>
    </div>
  </div>
    """, a=wp)
    return wp

def tab_demo():
    wp = QuasarPage()
    d = Div(classes="q-pa-md", style="max-width: 900px", a=wp)
    c = parse_html("""
    <q-tabs
        v-model="tab"
        inline-label
        class="bg-primary text-white shadow-2"
      >
        <q-tab name="mails" icon="mail" label="Mails" />
        <q-tab name="alarms" icon="alarm" label="Alarms" />
        <q-tab name="movies" icon="movie" label="Movies" />
        <q-tab name="photos" icon="photo" label="Photos" />
        <q-tab name="videos" icon="slow_motion_video" label="Videos" />
        <q-tab name="addressbook" icon="people" label="Address Book" />
      </q-tabs>
    """, a=d)
    print(c)
    print(c.name_dict.keys())
    print(c.name_dict)
    tabs = ['mails', 'alarms', 'movies', 'photos', 'videos', 'addressbook']
    tab_dict = {}
    for tab in tabs:
        tab_dict[tab] = QDiv(text=tab, classes='text-h2', a=d, show=False)
    tab_dict['alarms'].show = True
    c.tab_dict = tab_dict
    def tab_it(self, msg):
        print(msg)
        for i in tabs:
            if i == self.value:
                self.tab_dict[i].show = True
            else:
                self.tab_dict[i].show = False
    c.on('input', tab_it)
    return wp

@SetRoute('/chat')
def chat_test():
    wp = QuasarPage(data={'color': '#695757'})
    d = Div(classes="q-pa-md", style="max-width: 900px", a=wp)
    c = parse_html("""
    <div class="q-gutter-xs">
    <q-chip clickable  color="primary" text-color="white" icon="event" animation="slideInRight">
      Add to calendar
    </q-chip>
      <q-chip  selected  color="primary" text-color="white" icon="cake" name="icecream">
        Ice cream
      </q-chip>
      <q-chip color="teal"  text-color="white" icon="cake" name="cake">
        Eclair
      </q-chip>
      <q-chip  removable color="orange" text-color="white" icon="cake">
        Cupcake
      </q-chip>
      <q-chip    disable removable color="red" text-color="white" icon="cake">
        Gingerbread
      </q-chip>
    </div>
    """, a=d)
    c.name_dict['icecream'].selected = False
    c.name_dict['icecream'].clickable = False
    c.name_dict['icecream'].removable = True
    c.name_dict['cake'].selected = True
    c.name_dict['cake'].clickable = True
    c = parse_html("""
    <div class="q-pa-md row justify-center">
    <div style="width: 100%; max-width: 400px">
      <q-chat-message
        label="Sunday, 19th"
      />

      <q-chat-message
        name="me"
        avatar="https://cdn.quasar.dev/img/avatar4.jpg"
        :text="['hey, how are you?']"
        sent
        stamp="7 minutes ago"
      />
      <q-chat-message
        name="Jane"
        avatar="https://cdn.quasar.dev/img/avatar3.jpg"
        :text="['doing fine, how r you?']"
        stamp="4 minutes ago"
      />
    </div>
  </div>
    """, a=d)
    c = QChatMessage(text=['hey, how are you?'], a=d, name='me', avatar="https://cdn.quasar.dev/img/avatar1.jpg", stamp="1 minutes ago")
    c = parse_html("""
    <q-circular-progress
      indeterminate
      show-value
      font-size="10px"
      class="q-ma-md"
      :value="81"
      size="80px"
      :thickness="0.25"
      color="primary"
      track-color="grey-3"
    >
      <q-avatar size="60px">
        <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
      </q-avatar>
    </q-circular-progress>
    """, a=wp)
    c = parse_html("""
    <div class="q-pa-md flex flex-center">
    <q-circular-progress
      :value="81"
      size="50px"
      :thickness="0.22"
      color="purple"
      track-color="grey-3"
      class="q-ma-md"
    />

    <q-circular-progress
      :angle="90"
      :value="81"
      size="50px"
      :thickness="0.22"
      color="purple"
      track-color="grey-3"
      class="q-ma-md"
    />

    <q-circular-progress
      :angle="180"
      :value="25"
      size="50px"
      :thickness="0.22"
      color="purple"
      track-color="grey-3"
      class="q-ma-md"
    />

    <q-circular-progress
      :angle="270"
      :value="67"
      size="50px"
      :thickness="0.22"
      color="purple"
      track-color="grey-3"
      class="q-ma-md"
    />

    <q-circular-progress
      :angle="52"
      :value="43"
      size="50px"
      :thickness="0.22"
      color="purple"
      track-color="grey-3"
      class="q-ma-md"
    />
  </div>
    """, a=wp)
    c = QColor(a=wp) #, model=[wp, 'color'])
    c = parse_html("""
    <div class="q-pa-md q-gutter-md" style="font-size: 36px">
    <q-icon name="settings_remote" class="text-brown cursor-pointer">
      <q-popup-proxy transition-show="flip-up" transition-hide="flip-down">
        <q-banner class="bg-brown text-white">
          
          You have lost connection to the internet. This app is offline.
        </q-banner>
      </q-popup-proxy>
    </q-icon>

    <q-icon name="perm_data_setting" class="text-purple cursor-pointer">
      <q-popup-proxy :offset="[10, 10]">
        <q-banner class="bg-purple text-white">
          
          You have lost connection to the internet. This app is offline.
        </q-banner>
      </q-popup-proxy>
    </q-icon>
  </div>
    """, a=wp)
    c = QInput(filled=True, style='width: 400px', a=wp, model=[wp, 'color'])
    j = parse_html("""
    <q-icon name="colorize" class="cursor-pointer">
            <q-popup-proxy transition-show="scale" transition-hide="scale">
              <q-color name="color"/>
            </q-popup-proxy>
          </q-icon>
    """)
    c.add_scoped_slot('append', j)
    j.name_dict['color'].model = [wp, 'color']
    return wp

@SetRoute('/dialog')
def dialog_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md q-gutter-sm">
    <q-btn label="Alert" color="primary" name="alert_button" />
    <q-btn label="Confirm" color="primary" name="confirm_button" />
    <q-btn label="Prompt" color="primary" name="prompt_button" />

    <q-dialog name="alert">
      <q-card>
        <q-card-section>
          <div class="text-h6">Alert</div>
        </q-card-section>

        <q-card-section>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v_close_popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog name="confirm" :persistent="True">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="signal_wifi_off" color="primary" text-color="white" />
          <span class="q-ml-sm">You are currently not connected to any network.</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v_close_popup />
          <q-btn flat label="Turn on Wifi" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog name="prompt" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Your address</div>
        </q-card-section>

        <q-card-section>
          <q-input dense  autofocus />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v_close_popup />
          <q-btn flat label="Add address" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
    """, a=wp)

    alert_button = c.name_dict['alert_button']
    alert_button.alert = c.name_dict['alert']
    def alert_click(self, msg):
        print('in alert', msg)
        self.alert.value = True
    alert_button.on('click', alert_click)
    c.name_dict['alert'].value = True
    c.name_dict['confirm'].persistent = True
    # c.name_dict['alert'].value = False

    confirm_button = c.name_dict['confirm_button']
    confirm_button.confirm = c.name_dict['confirm']
    def confirm_click(self, msg):
        print('in confirm', msg)
        self.confirm.value = True

    confirm_button.on('click', confirm_click)
    # return wp
    d = parse_html("""
    <div class="q-pa-md q-gutter-sm">
    <q-btn label="Click Me" color="primary" name="show_button" />

    <q-dialog seamless position="right" name="show">
      <q-card style="width: 350px">
        

        <q-card-section class="row items-center no-wrap">
          <div>
            <div class="text-weight-bold">The Walker</div>
            <div class="text-grey">Fitz & The Tantrums</div>
          </div>

          <q-space />

          <q-btn flat round icon="play_arrow" />
          <q-btn flat round icon="pause" />
          <q-btn flat round icon="close" v_close_popup />
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
    """, a=wp)
    print(d.name_dict)
    b = d.name_dict['show_button']
    b.show_me = d.name_dict['show']
    def show_click(self, msg):
        self.show_me.value = True
        self.e.fullscreen = True
    b.on('click', show_click)
    e = QEditor(a=wp)
    b.e = e
    # e.toolbar = [['print', 'fullscreen']]
    # e.toolbar = QEditor.default_options
    e.kitchen_sink = True
    # print(e.toolbar)
    c = parse_html("""
 <div class="q-pa-md" style="max-width: 350px">
    <q-list>
      <q-expansion-item popup default-opened icon="mail" label="Inbox" caption="5 unread emails">
        <q-separator />
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item popup icon="send" label="Outbox" caption="Empty">
        <q-separator />
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item popup icon="drafts" label="Draft" caption="Draft a new email">
        <q-separator />
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>
  </div>
    """, a=wp)
    c = parse_html("""
      <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
      <q-expansion-item
        group="somegroup"
        icon="explore"
        label="First"
        default-opened
        header-class="text-primary"
      >
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item group="somegroup" icon="perm_identity" label="Second" header-class="text-teal">
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item group="somegroup" icon="shopping_cart" label="Third" header-class="text-purple">
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>

      <q-separator />

      <q-expansion-item
        group="somegroup"
        icon="bluetooth"
        label="Fourth"
        header-class="bg-teal text-white"
        expand-icon-class="text-white"
      >
        <q-card class="bg-teal-2">
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>
    </q-list>
  </div>
    """, a=wp)
    return wp

def image_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-col-gutter-md row items-start">
      <div class="col-4">
        <span>Ratio: 16/9</span>
        <q-img
          src="https://placeimg.com/500/300/nature"
          :ratio="16/9"
        />
      </div>

      <div class="col-4">
        <span>Ratio: 1</span>
        <q-img
          src="https://placeimg.com/500/300/nature"
          :ratio="1"
        />
      </div>

      <div class="col-4">
        <span>Ratio: 4/3</span>
        <q-img
          src="https://placeimg.com/500/300/nature"
          :ratio="4/3"
        />
      </div>
    </div>
  </div>
    """, a=wp)

    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-col-gutter-md row items-start">
      <div class="col-6">
        <q-img
          src="https://placeimg.com/500/300/nature?t=2345"
          style="width: 100%"
          transition="flip-right"
        >
          <div class="absolute-bottom text-subtitle1 text-center q-pa-xs">
            Caption
          </div>
        </q-img>
      </div>

      <div class="col-6">
        <q-img src="https://cdn.quasar.dev/img/parallax2.jpg">
          <div class="absolute-top text-center q-pa-xs">
            Caption
          </div>
        </q-img>
      </div>

      <div class="col-6">
        <q-img src="https://cdn.quasar.dev/img/parallax2.jpg">
          <div class="absolute-bottom-right text-subtitle2">
            Caption
          </div>
        </q-img>
      </div>

      <div class="col-6">
        <q-img src="https://cdn.quasar.dev/img/parallax2.jpg">
          <div class="absolute-full text-subtitle2 flex flex-center">
            Caption
          </div>
        </q-img>
      </div>
    </div>
  </div>
    """, a=wp)
    return wp

def inner_loading_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md q-gutter-md">
    <q-btn color="primary" name="button">
      Show Text Loading
    </q-btn>
<transition appear
          enter-active-class="animated zoomIn slow"
          leave-active-class="animated zoomOut slower"
        >
        <div>
        <span key=0>s1</span>
        <span key=1>s2</span>
        <span key=2>s3</span>
        <span key=3>s4</span>
        </div>
        </transition>
    <q-card class="bg-grey-3 relative-position card-example">
      <q-card-section>
        <div class="text-h6">Lorem Ipsum</div>
      </q-card-section>

      <q-card-section>
        <transition
          
          appear
          enter-active-class="animated zoomIn slow"
          leave-active-class="animated zoomOut slower"
        >
          <div name="text_div">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel magna eu risus laoreet tristique. Nulla ut fermentum elit, nec consequat augue. Morbi et dolor nec metus tincidunt pellentesque. Nullam non semper ante. Fusce pellentesque sagittis felis quis porta. Aenean condimentum neque sed erat suscipit malesuada. Nulla eget rhoncus enim. Duis dictum interdum eros.
          </div>
        </transition>
      </q-card-section>

      <q-inner-loading :showing="False" name="inner">
        <q-spinner spinner_type="gears" size="50px" color="primary" :showing="True"/>
      </q-inner-loading>
    </q-card>
  </div>
    """, a=wp)
    def click(self, msg):
        print(msg)
        self.inner.showing = not self.inner.showing
        self.text_div.show = not self.text_div.show
    b = c.name_dict['button']
    b.inner = c.name_dict['inner']
    b.text_div = c.name_dict['text_div']
    b.on('click', click)

    return wp

def splitter_test():
    wp = QuasarPage()
    s = QSplitter(style="height: 400px", a=wp, value=80, disable=False)
    pane = parse_html("""
     <div class="q-pa-md">
    <div class="text-h4 q-mb-md">After</div>
          <div class="q-my-md">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</div>
          <div class="q-my-md">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</div>
          <div class="q-my-md">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</div>
          <div class="q-my-md">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</div>
          <div class="q-my-md">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</div>
          <div class="q-my-md">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</div>
        </div>
    """)
    s.dark = True
    # s.add_scoped_slot('before', pane)
    s.before_slot = pane
    s.after_slot = pane
    # s.add_scoped_slot('after', pane)
    Div(a=wp, classes='q-ma-lg')
    image1 = QImg(src="https://cdn.quasar.dev/img/parallax1.jpg", ratio=16/9)
    image2 = QImg(src="https://cdn.quasar.dev/img/parallax1-inverted.jpg", ratio=16/9)
    s1 = QSplitter(style="height: 300px", limits=[1, 99], before_class="overflow-hidden", after_class="overflow-hidden", separator_class="bg-black", a=wp)
    s1.before_slot = image1
    s1.after_slot = image2
    return wp

def dropdown_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-btn-dropdown color="primary" label="Eli Dropdown Button" name="button">
      <q-list>
        <q-item clickable v-close-popup>
          <q-item-section>
            <q-item-label>Photos</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable  name="videos">
          <q-item-section>
            <q-item-label name="videos_label">Videos</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-close-popup>
          <q-item-section>
            <q-item-label>Articles</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
    """, a=wp)
    videos = c.name_dict['videos']
    videos_label = c.name_dict['videos_label']
    button = c.name_dict['button']
    videos.videos_label = videos_label
    videos.button = button
    def click(self, msg):
        self.videos_label.text += 'Clicked on Videos'
        # self.button.value = False
    videos.on('click', click)
    c = parse_html("""
    <div class="q-pa-md">
    <q-btn-dropdown
      split
      color="orange"
      push
      glossy
      no-caps
      icon="folder"
      label="Dropdown Button"
    >
      <q-list>
        <q-item clickable v-close-popup >
          <q-item-section avatar>
            <q-avatar icon="folder" color="primary" text-color="white" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Photos</q-item-label>
            <q-item-label caption>February 22, 2016</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-icon name="info" color="amber" />
          </q-item-section>
        </q-item>

        <q-item clickable v-close-popup >
          <q-item-section avatar>
            <q-avatar icon="assignment" color="secondary" text-color="white" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Vacation</q-item-label>
            <q-item-label caption>February 22, 2016</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-icon name="info" color="amber" />
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
    """, a=wp)
    return wp


def slider_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-badge color="secondary">
      Model: Will go here
    </q-badge>

    <q-slider
      v-model="value"
      :min="-20"
      :max="20"
      :step="4"
      label
      color="light-green"
    />
  </div>
    """, a=wp)
    d = Div(classes='q-pa-md bg-grey-10', data={'value': 4}, a=wp)
    badge1 = QBadge(color='secondary', a=d)
    Span(text='Model: ', a=badge1)
    Space(a=badge1, num=35)
    Span(model=[d, 'value'], a=badge1)
    Span(text='&nbsp;', a=badge1, temp=True)
    Span(text='&nbsp;', a=badge1, temp=True)
    Span(text='&nbsp;', a=badge1, temp=True)
    Span(text='&nbsp;', a=badge1, temp=True)
    Span(text='&nbsp;', a=badge1, temp=True)
    Span(text=' (-20 to 20, step 4)', a=badge1)
    slider1 = QSlider(min=-20, max=20, step=4, label=True,  label_always=True, color='red', a=d, model=[d, 'value'], dark=True, label_suffix=' px')
    badge2 = QBadge(color='secondary', a=d, model=[d, 'value'])
    slider2 = QSlider(min=-20, max=20, step=4, label=True,  label_always=True, color='purple', a=d, model=[d, 'value'], dark=True)
    d = Div(classes="q-pa-md", a=wp)
    range1 = QRange(min=-200, max=200,  label=True, color='purple', a=d, drag_range=True)
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-sm">
      <q-checkbox  label="Teal" />
    </div>
    <div class="q-gutter-sm">
      <q-checkbox left-label  label="Orange" name="orange"/>
    </div>
  </div>
    """, a=wp)
    # c.name_dict['orange'].value = True
    c = parse_html("""
    <div class="q-gutter-sm">
      <q-checkbox toggle-indeterminate  label="Did you eat lunch today?" />
    </div>
    """, a=wp)
    QInput(a=wp)
    c = parse_html("""
    <div class="q-ma-md">
    <div class="q-gutter-sm">
      <q-checkbox  val="teal" label="Teal" color="teal" name="test"/>
      <q-checkbox  val="orange" label="Orange" color="orange" name="test" />
      <q-checkbox  val="red" label="Red" color="red" name="test" />
      <q-checkbox  val="cyan" label="Cyan" color="cyan" name="test" />
    </div>

    <div class="q-px-sm">
      The model data: 
    </div>
  </div>
    """, a=wp)
    print(c.name_dict)
    for i in c.name_dict['test']:
        i.value = True
    c = parse_html("""
    <div class="q-pa-md q-gutter-sm">
    <div>
      <q-toggle
        
        icon="alarm"
      />
      <q-toggle
        
        color="pink"
        icon="mail"
        label="Same Icon for each state"
      />
    </div>

    <div>
      <q-toggle
        
        checked-icon="check"
        color="green"
        unchecked-icon="clear"
      />
      <q-toggle
        
        checked-icon="check"
        color="red"
        label="Different icon for each state"
        unchecked-icon="clear"
      />
    </div>
  </div>
    """, a=wp)
    return wp

def qmenu_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-md row items-center">

      <q-btn color="primary" label="Click me">
        <q-menu>
          <q-list dense style="min-width: 100px">
            <q-item clickable v-close-popup>
              <q-item-section>Open...</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>New</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Preferences</q-item-section>
              <q-item-section side>
                <q-icon name="keyboard_arrow_right" />
              </q-item-section>

              <q-menu anchor="top right" self="top left">
                <q-list>
                  <q-item
                    
                    dense
                    clickable
                  >
                    <q-item-section>Submenu Label</q-item-section>
                    <q-item-section side>
                      <q-icon name="keyboard_arrow_right" />
                    </q-item-section>
                    <q-menu auto-close anchor="top right" self="top left">
                      <q-list>
                        <q-item
                          dense
                          clickable
                        >
                          <q-item-section>3rd level Label</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-item>
                </q-list>
              </q-menu>

            </q-item>
            <q-separator />
            <q-item clickable v-close-popup>
              <q-item-section>Quit</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>

      <q-bar style="min-width: 250px;" class="bg-teal text-white rounded-borders">
        <div class="cursor-pointer non-selectable">
          <span>File</span>
          <q-menu>
            <q-list dense style="min-width: 100px">
              <q-item clickable v-close-popup>
                <q-item-section>Open...</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section>New</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable>
                <q-item-section>Preferences</q-item-section>
                <q-item-section side>
                  <q-icon name="keyboard_arrow_right" />
                </q-item-section>

                <q-menu anchor="top right" self="top left">
                  <q-list dense>
                    <q-item
                      
                      clickable
                    >
                      <q-item-section>Submenu Label</q-item-section>
                      <q-item-section side>
                        <q-icon name="keyboard_arrow_right" />
                      </q-item-section>
                      <q-menu auto-close anchor="top right" self="top left">
                        <q-list dense>
                          <q-item
                           
                            clickable
                          >
                            <q-item-section>3rd level Label</q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-item>
                  </q-list>
                </q-menu>

              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section>Quit</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </div>
        <div class="cursor-pointer non-selectable">
        <span>Edit</span>
          <q-menu>
            <q-list dense style="min-width: 100px">
              <q-item clickable v-close-popup>
                <q-item-section>Cut</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section>Copy</q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section>Paste</q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section>Select All</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </div>
        <q-space />
        <q-btn dense flat icon="minimize" />
        <q-btn dense flat icon="crop_square" />
        <q-btn dense flat icon="close" />
      </q-bar>
    </div>
  </div>
    """, a=wp)
    return wp

@SetRoute('/option')
def optiongroup_test():
    wp = QuasarPage(data = {'check':  ['op1', 'op3'], 'radio': 'op3'})
    b = QBtn(label='hello', a=wp)
    options = [
        {
            'label': 'Option 1',
            'value': 'op1'
        },
        {
            'label': 'Option 2',
            'value': 'op2'
        },
        {
            'label': 'Option 3',
            'value': 'op3'
        }
    ]
    og1 = QOptionGroup(color='primary', a=wp, inline=True, model =[wp, 'radio'])
    og1.options = options
    og2 = QOptionGroup(color='primary', a=wp, inline=True, value='op2', model =[wp, 'radio'])
    og2.options = options
    og1 = QOptionGroup(color='primary', a=wp, inline=True, type='checkbox', model =[wp, 'check'])
    og1.options = options
    og2 = QOptionGroup(color='primary', a=wp, inline=True, type='toggle', model =[wp, 'check'])
    og2.options = options
    def my_input(self, msg):
        print(wp.data)
    og1.on('input', my_input)
    b.og1 = og1
    b.og2 = og2
    def my_click(self, msg):
        # self.og1.value = []
        wp.data['check'] = []
    b.on('click', my_click)
    return wp

@SetRoute('/select')
def select_test():
    wp = QuasarPage()
    option_string = """
    [
        {
          label: 'Google',
          value: 'Google',
          description: 'Search engine',
          category: '1'
        },
        {
          label: 'Facebook',
          value: 'Facebook',
          description: 'Social media',
          category: '1'
        },
        {
          label: 'Twitter',
          value: 'Twitter',
          description: 'Quick updates',
          category: '2'
        },
        {
          label: 'Apple',
          value: 'Apple',
          description: 'iStuff',
          category: '2'
        },
        {
          label: 'Oracle',
          value: 'Oracle',
          disable: true,
          description: 'Databases',
          category: '3'
        }
      ]
    """
    d = Div(classes="q-pa-md", style="max-width: 300px", a=wp)
    d1 = Div(classes="q-gutter-md", a=d)
    # s1 = QSelect(label='Standard', a=d1, emit_value=False, multiple=True, use_chips=True)
    s1 = QSelect(label='Label', a=d1, color='orange', clearable=True, standout=True, bottom_slots=True, counter=True, hint='My hint')
    s1.prepend_slot = QIcon(name='place')
    s1.append_slot = QIcon(name='favorite')
    s1.before_slot = QIcon(name='event')
    s1.options = ['Google', 'Facebook', 'Twitter', 'Apple', 'Oracle']
    # s1.value = []
    # options = s1.load_json(option_string)
    # print(s1.options)

    return wp

def toggle_button_test():
    wp = QuasarPage()
    d = Div(classes="q-pa-md q-gutter-md", a=wp)

    option_string = """
    [
          {label: 'One', value: 'one'},
          {label: 'Two', value: 'two'},
          {label: 'Three', value: 'three'}
        ]
    """
    b1 = QBtnToggle(push=True, glossy=True, toogle_color='primary', a=d, options=option_string)
    b1.value = 'one'

    g = Pie([1,2,3], ['one', 'two', 'three'], a=d)
    print(g.options)
    b1.g = g
    def my_input(self, msg):
        v = {'one': 1, 'two': 2, 'three': 3}
        print('in my input')
        print(self.g.options.chart)
        self.g.options.title.text = msg.value
        # {'name': 'one', 'y': 1}
        self.g.options.series[0].data.append({'name': 'added ' + msg.value, 'y': v[msg.value] })
    b1.on('input', my_input)

    # b1.load_json(option_string)
    return wp

def tooltip_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-md">

      <q-btn label="Hover me" color="primary">
        <q-tooltip name="t1">
          Some text as content of Tooltip
        </q-tooltip>
      </q-btn>

      <div
        class="inline bg-amber rounded-borders cursor-pointer"
        style="max-width: 300px"
      >
        <div class="fit flex flex-center text-center non-selectable q-pa-md">
          I am groot!<br>(Hover me!)
        </div>

        <q-tooltip>
          I am groot!
        </q-tooltip>
      </div>
      
      <q-btn color="primary" label="Yeah">
        
        <q-tooltip content-class="bg-purple" content-style="font-size: 16px" :offset="[30, 30]" anchor="center left" self="center right" transition-show="scale"
          transition-hide="scale">
          Here I am!
        </q-tooltip>
      </q-btn>

    </div>
  </div>
    """, a=wp)
    t1 = c.name_dict['t1']
    t1.disable_events = True
    return wp

def stepper_test():
    wp = QuasarPage()
    c = parse_html("""
     <div class="q-pa-md">
    <q-btn label="Reset" push color="white" text-color="primary"  class="q-mb-md" name="reset_button"/>

    <q-stepper
      :value="1"
      header-nav
      ref="stepper"
      color="primary"
      animated
    >
      <q-step
        :name="1"
        title="Select campaign settings"
        icon="settings"
      >
        <span>For each ad campaign that you create, you can control how much youre willing to
        spend on clicks and conversions, which networks and geographical locations you want
        your ads to show on, and more.</span>

        <q-stepper-navigation>
          <q-btn color="primary" label="Continue" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="2"
        title="Create an ad group"
        caption="Optional"
        icon="create_new_folder"
      >
        <span>An ad group contains one or more ads which target a shared set of keywords.</span>

        <q-stepper-navigation>
          <q-btn color="primary" label="Continue" />
          <q-btn flat color="primary" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>

      <q-step
        :name="3"
        title="Create an ad"
        icon="add_comment"
      >
        <span>Try out different ad text to see what brings in the most customers, and learn how to
        enhance your ads using features like ad extensions. If you run into any problems with
        your ads, find out how to tell if they're running and how to resolve approval issues.</span>

        <q-stepper-navigation>
          <q-btn color="primary" label="Finish" />
          <q-btn flat  color="primary" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </div>
    """,)
    s = QStepper(color='primary', animated=True, a=wp)
    step = QStep(name="step1", title="Select campaing settings", icon='settings', done=False, a=s)
    Span(text='For each ad campaign that you create, you can control how much youre willing tospend on clicks and conversions', a=step)

    return wp

def slide_transition_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md" style="max-width: 500px;">
    <q-toggle  label="Visible image" class="q-mb-md" name="toggle" />

    <q-slide-transition appear name="trans">
      <div v-show="visible">
        <img 
          class="responsive"
          src="https://cdn.quasar.dev/img/quasar.jpg"
        >
      </div>
    </q-slide-transition>
  </div>
    """, a=wp)
    tog = c.name_dict['toggle']
    tog.value = True
    trans = c.name_dict['trans']
    tog.trans = trans
    def my_input(self, msg):
        if msg.value:
            # self.trans.style = 'display: block;'
            self.trans.show = True
        else:
            # self.trans.style = 'display: none;'
            self.trans.show = False
            # self.trans.slide_up = True
    tog.on('input', my_input)
    return wp

@SetRoute('/timeline')
def timeline_test():
    wp = QuasarPage()
    b = QBtn(label='change layout', a=wp, color='primary')
    c = parse_html("""
    <div class="q-px-lg q-pb-md">
    <q-timeline color="secondary" name="timeline">
      <q-timeline-entry heading>
        Timeline heading
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 22, 1986"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 21, 1986"
        icon="delete"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>

      <q-timeline-entry heading>
        November, 2017
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 22, 1986"
        avatar="https://cdn.quasar.dev/img/avatar2.jpg"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 22, 1986"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 22, 1986"
        color="orange"
        icon="done_all"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 22, 1986"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>

      <q-timeline-entry
        title="Event Title"
        subtitle="February 22, 1986"
      >
        <div>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </q-timeline-entry>
    </q-timeline>
  </div>
    """, a=wp)
    b.timeline = c.name_dict['timeline']
    def my_click(self, msg):
        self.timeline.layout = 'comfortable'
    b.on('click', my_click)
    return wp

def time_picker_test():
    wp = QuasarPage(data={'time': '2019-06-06 05:21'})
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-md">
      <q-time  />

      <q-time
        landscape
        with-seconds
        format24h
        now-btn
      />
    </div>
  </div>
    """, a=wp)

    q1 = parse_html("""
    <q-icon name="access_time" class="cursor-pointer">
            <q-popup-proxy transition-show="scale" transition-hide="scale">
              <q-time mask="YYYY-MM-DD HH:mm" name="time"/>
            </q-popup-proxy>
          </q-icon>
    """)
    in1 = QInput(style='width: 400px', filled=True, a=wp, model=[wp, 'time'])
    in1.append_slot = q1
    q1.name_dict['time'].model = [wp, 'time']
    q2 = parse_html("""
    <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy transition-show="scale" transition-hide="scale">
            <q-date mask="YYYY-MM-DD HH:mm" name="date"/>
          </q-popup-proxy>
        </q-icon>
    """)
    in1.prepend_slot = q2
    q2.name_dict['date'].model = [wp, 'time']
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-md">
      <q-date
        
        color="orange"
      />

      <q-date
        
        color="yellow"
        text-color="black"
      />
    </div>
  </div>
    """, a=wp)
    return wp

def knob_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md flex flex-center">
    <q-knob
      show-value
      class="text-light-blue q-ma-md"
      
      size="50px"
      color="light-blue"
    />

    <q-knob
      show-value
      class="text-white q-ma-md"
      v-model="value"
      size="90px"
      :thickness="0.2"
      color="orange"
      center-color="grey-8"
      track-color="transparent"
    >
      <q-icon name="volume_up" />
    </q-knob>

    <q-knob
      show-value
      font-size="12px"
      v-model="value"
      size="50px"
      
      color="teal"
      track-color="grey-3"
      class="q-ma-md"
    >
    </q-knob>

    <q-knob
      show-value
      font-size="16px"
      class="text-red q-ma-md"
      v-model="value"
      size="60px"
      :thickness="0.05"
      color="red"
      track-color="grey-3"
    >
      <q-icon name="volume_up" class="q-mr-xs" />
      
    </q-knob>

    <q-knob
      show-value
      font-size="10px"
      class="q-ma-md"
      v-model="value"
      size="80px"
      :thickness="0.25"
      color="primary"
      track-color="grey-3"
    >
      <q-avatar size="60px">
        <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
      </q-avatar>
    </q-knob>
  </div>
    """, a=wp)
    return wp

@SetRoute('/pagination')
def pagination_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-lg flex flex-center">
    <q-pagination
      
      :max="5"
    >
    </q-pagination>
  </div>
  <div class="q-pa-lg flex flex-center">
    <q-pagination
      :max="5"
      :input="True"
    >
    </q-pagination>
  </div>
  <div class="q-pa-lg flex flex-center">
    <q-pagination
      :max="5"
      input
      input-class="text-orange-10"
    />
  </div>
   <div class="q-pa-lg flex flex-center">
    <q-pagination
      color="black"
      :max="10"
      :max-pages="6"
      :boundary-numbers="False"
    >
    </q-pagination>
  </div>
  <div class="q-pa-lg flex flex-center">
    <q-pagination
      color="purple"
      :max="10"
      :max-pages="3"
      :boundary-numbers="True"
      :boundary-links="True"
    >
    </q-pagination>
  </div>
  <div class="q-pa-lg flex flex-center">
    <q-pagination
      color="deep-orange"
      :max="5"
      :boundary-links="True"
    >
    </q-pagination>
  </div>
    """, a=wp)
    d = Div(classes="q-pa-lg flex flex-center", a=wp)
    p1 = QPagination(color='deep-orange', max=5, boundary_links=True, a=d)
    return wp

def panel_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-y-md" style="max-width: 350px">
      <q-option-group name="og"
        
        inline
        options="[
          { label: 'Mails', value: 'mails' },
          { label: 'Alarms', value: 'alarms' },
          { label: 'Movies', value: 'movies' }
        ]"
      />

      <q-tab-panels value="alarms" animated class="shadow-2 rounded-borders" name="panel" style="width: 500px; height: 400px;">
        <q-tab-panel name="mails">
          <div class="text-h6">Mails</div>
          <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
        </q-tab-panel>

        <q-tab-panel name="alarms">
          <div class="text-h6">Alarms</div>
          <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
        </q-tab-panel>

        <q-tab-panel name="movies">
          <div class="text-h6">Movies</div>
          <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
    """, a=wp)
    panel = c.name_dict['panel']
    panel.value = 'alarms'
    # panel.keep_alive = False
    og = c.name_dict['og']
    og.value = 'alarms'
    og.panel = panel
    def my_input(self, msg):
        print('in Input', msg.value)
        self.panel.value = msg.value
    og.on('input', my_input)
    Div(text='stam', a=wp)

    return wp


def tree_test():
    wp = QuasarPage()
    d = Div(classes="q-pa-md q-gutter-sm", a=wp)
    node_string = """
    [
        {
          label: 'Satisfied customers (with avatar)',
          avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
          children: [
            {
              label: 'Good food (with icon)',
              icon: 'restaurant_menu',
              children: [
                { label: 'Quality ingredients', icon: 'favorite' },
                { label: 'Good recipe' }
              ]
            },
            {
              label: 'Good service (disabled node with icon)',
              icon: 'room_service',
              disabled: true,
              children: [
                { label: 'Prompt attention' },
                { label: 'Professional waiter' }
              ]
            },
            {
              label: 'Pleasant surroundings (with icon)',
              icon: 'photo',
              children: [
                {
                  label: 'Happy atmosphere (with image)',
                  img: 'https://cdn.quasar.dev/img/logo_calendar_128px.png'
                },
                { label: 'Good table presentation' },
                { label: 'Pleasing decor' }
              ]
            }
          ]
        }
      ]
    """
    node = []
    for i in range(100):
        temp = {'label': 'Good service (disabled node with icon)', 'icon': 'room_service' }
        temp['label'] = f"{i} {temp['label']}"
        node.append(temp)

    node = [{
          'label': 'Satisfied customers (with avatar)',
          'avatar': 'https://cdn.quasar.dev/img/boy-avatar.png',
          'children': node}]
    tree = QTree(a=d, node_key='label', nodes=node, tick_strategy="leaf")
    # tree = QTree(a=d, node_key='label', nodes=node_string, tick_strategy="leaf")
    print(tree.nodes)
    d1 = Div(text='stam', a=d)
    def my_updated(self, msg):
        print('in my updated')
        d1.text = str(msg.value)
    tree.on('update:ticked', my_updated)
    return wp

def animate_test():
    wp = WebPage()
    base_classes = 'absolute  bg-blue-300 text-red-500'
    b = Button(text='Slide Out', classes='m-1 p-1 bg-blue-500 text-white', a=wp)
    b1 = Button(text='Slide In', classes='m-1 p-1 bg-blue-500 text-white', a=wp)
    b2 = Button(text='Slide In Left', classes='m-1 p-1 bg-blue-500 text-white', a=wp)
    outer = Div(a=wp, classes='text-2xl m-1', style="width: 500px; height: 300px; overflow: hidden; position: relative;")
    d = Div(text='OUT', classes=base_classes, style=' height: 300px;  width: 100%;  z-index: 10;', a=outer)
    d1 = Div(text='in', classes='absolute  bg-red-300 text-red-500', style=' height: 300px; width: 100%;  ', a=outer)
    d.base_classes = base_classes
    b.d = d
    b1.d = d
    b2.d = d
    def in_click(self, msg):
        self.d.classes = self.d.base_classes + ' animated slideInRight faster'
    def out_click(self, msg):
        self.d.classes = self.d.base_classes + ' animated slideOutLeft faster '
    def slide_in_left_click(self, msg):
        self.d.classes = self.d.base_classes + ' animated slideInLeft faster'
    b.on('click', out_click)
    b1.on('click', in_click)
    b2.on('click', slide_in_left_click)


    return wp


import time
@SetRoute('/slide')
def slide_item_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md" style="max-width: 350px">
    <q-list bordered separator>

      <q-slide-item name="item1">
        <q-item>
          <q-item-section avatar>
            <q-avatar color="primary" text-color="white" icon="bluetooth" />
          </q-item-section>
          <q-item-section>Icons only</q-item-section>
        </q-item>
      </q-slide-item>

      <q-slide-item >
        <q-item>
          <q-item-section avatar>
            <q-avatar>
              <img src="https://cdn.quasar.dev/img/avatar6.jpg">
            </q-avatar>
          </q-item-section>
          <q-item-section>Text only</q-item-section>
        </q-item>
      </q-slide-item>

      <q-slide-item >

        <q-item>
          <q-item-section avatar>
            <q-avatar>
              <img src="https://cdn.quasar.dev/img/avatar4.jpg">
            </q-avatar>
          </q-item-section>
          <q-item-section>Text and icons</q-item-section>
        </q-item>
      </q-slide-item>

    </q-list>
  </div>
    """, a=wp)
    item1 = c.name_dict['item1']
    done_icon = QIcon(name='done')
    alarm_icon = QIcon(name='alarm')
    item1.left_slot = done_icon
    # item1.left_slot = Div(text='hello')
    # item1.add_scoped_slot('left', done_icon)
    item1.right_slot = alarm_icon
    # item1.add_scoped_slot('right', alarm_icon)
    def left_change(self, msg):
        print(msg)
        time.sleep(3)
        self.reset = True
    item1.on('left', left_change)
    return wp

def infinite_scroll_test():
    wp = QuasarPage()
    s = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore'
    dstam = Div(a=wp, classes='row')
    d = Div(classes="q-pa-md q-ma-md scroll", a=wp, style=' width: 700px; height: 500px;') # style='width: 700px; height: 700px; '
    q = QInfiniteScroll(a=d, classes='')
    q.offset = 250
    for i in range(30):
        q.add(Div(text=f'{i} {s}', classes='text-body1'))
    c = parse_html("""
    <div class="row justify-center q-my-md">
          <q-spinner spinner_type="ball" class="color: blue;" style="font-size: 50px; color: blue" />
        </div>
    """)
    # c1 = parse_html('<q-spinner color="primary"  style="font-size: 50px"/>')
    c.spinner_type = 'ball'
    q.loading_slot = c
    def load_event(self, msg):
        print(msg)
        time.sleep(2)
        for i in range(10):
            q.add(Div(text=f'{i} {s}', classes='text-body1'))
        self.done = True
    q.on('load', load_event)
    return wp

@SetRoute('/scroll')
def scroll_area_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="row q-ma-md">
    <div class="col-12">
      <q-scroll-area style="height: 500px; max-width: 300px;" name="scroll">
        
      </q-scroll-area>
    </div>
  </div>
    """, a=wp)
    scroll = c.name_dict['scroll']
    observe_scroll = QScrollObserver(a=scroll)
    observe_scroll.scroll = scroll
    s = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    for i in range(100):
        Div(classes="q-py-xs", text=f'{i} {s}', a=scroll)
    b = QBtn(label='scroll more', a=wp)
    b.scroll = scroll
    scroll.offset = 500
    scroll.duration = 500
    def my_click(self, msg):
        self.scroll.offset += 500
        scroll.duration = 500
    b.on('click', my_click)
    def scroll_event(self, msg):
        print('in scroll', msg)
        self.position = msg.value.position
        print(self.position)
        if self.position > 6000:
            self.scroll.offset = 5000
            return
        else:
            return False
    observe_scroll.on('scroll', scroll_event)
    return wp

def notifiy_test():
    wp = QuasarPage()
    c = parse_html("""
    <div style="display: flex; align-items: center; justify-content: center; height: 100vh">
    <div class="q-pa-md q-gutter-y-sm column  items-center" >
    <div>
      <div class="row q-gutter-sm">
        <q-btn round size="sm" color="secondary" name="top-left">
          <q-icon name="arrow_back" class="rotate-45" />
        </q-btn>
        <q-btn round size="sm" color="accent" name="top">
          <q-icon name="arrow_upward" />
        </q-btn>
        <q-btn round size="sm" color="secondary" @click="showNotif('top-right')">
          <q-icon name="arrow_upward" class="rotate-45" />
        </q-btn>
      </div>
    </div>

    <div>
      <div class="row q-gutter-sm">
        <div>
          <q-btn round size="sm" color="accent" @click="showNotif('left')">
            <q-icon name="arrow_back" />
          </q-btn>
        </div>
        <div>
          <q-btn round size="sm" color="accent" @click="showNotif('center')">
            <q-icon name="fullscreen_exit" />
          </q-btn>
        </div>
        <div>
          <q-btn round size="sm" color="accent" @click="showNotif('right')">
            <q-icon name="arrow_forward" />
          </q-btn>
        </div>
      </div>
    </div>

    <div>
      <div class="row q-gutter-sm">
        <div>
          <q-btn round size="sm" color="secondary" @click="showNotif('bottom-left')">
            <q-icon name="arrow_forward" class="rotate-135" />
          </q-btn>
        </div>
        <div>
          <q-btn round size="sm" color="accent" @click="showNotif('bottom')">
            <q-icon name="arrow_downward" />
          </q-btn>
        </div>
        <div>
          <q-btn round size="sm" color="secondary" @click="showNotif('bottom-right')">
            <q-icon name="arrow_forward" class="rotate-45" />
          </q-btn>
        </div>
      </div>
    </div>
  </div>
  </div>
    """, a=wp)
    b = c.name_dict['top-left']
    b1 = c.name_dict['top']
    n1 = QNotify(color= 'negative', message= 'Woah! Danger! You are getting good at this!', icon= 'report_problem', a=wp, position='top', closeBtn='Dismiss')
    n2 = QNotify(color='secondary', message='Hello!', a=wp, closeBtn='Bye', textColor='yellow')
    n3 = QNotify(message='<div style="font-size: 50px;">test</div><div style="font-size: 30px;">stam</div><q-btn label="click"></q-btn>', a=wp, html=True, closeBtn='Dismiss')
    b.notification = n1
    b1.notification = n3
    def b_click(self, msg):
        print(msg)
        self.notification.notify = True
    def b_after(self, msg):
        self.notification.notify = False
        print('in after')
        print(self.notification.notify)
    b.on('click', b_click)
    b.on('after', b_after)
    b1.on('click', b_click)
    b1.on('after', b_after)
    return wp

def parallax_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md q-gutter-md">
    <div class="row justify-between">

    <q-parallax
      src="https://cdn.quasar.dev/img/parallax2.jpg"
    >
      <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg" style="width: 150px; height: 150px">
          <div class="text-h3 text-white text-center">Quasar Framework</div>
    </q-parallax>

    </div>
  </div>
    """)
    d = Div(classes='scroll', style='height: 600px; width: 50%', a=wp)
    for i in range(5):
        d.add(c)
    return wp

def video_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md q-gutter-md">
      <div class="q-video">
        <iframe
          src="https://www.youtube.com/embed/k3_tw44QsZQ?rel=0"
          frameborder="0"
          allowfullscreen
        />
      </div>
  </div>
    """, a=wp)

    return wp

def icon_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="text-purple q-gutter-md" style="font-size: 2em" name="icon-div">
      <q-icon name="font_download" />
      <q-icon name="warning" />
      <q-icon name="format_size" />
      <q-icon name="print" />
      <q-icon name="today" />
      <q-icon name="style" />
    </div>
    </div>
    """, a=wp)
    QIcon(name='wifi', a=wp, style="font-size: 2em")
    QIcon(name='fas fa-dog', a=wp, color='primary', style="font-size: 2em")
    QIcon(name='far fa-bell', a=wp, style="font-size: 2em")
    QIcon(name='fab fa-apple', a=wp,  style="font-size: 2em")
    QIcon(name='far fa-grin-squint-tears', a=wp, color='primary', style="font-size: 2em")
    QIcon(name='fas fa-ambulance', a=wp, style="font-size: 20px")
    QIcon(name='ion-md-airplane', a=wp, style="font-size: 2em")
    QIcon(name='mdi-alert-circle-outline', a=wp, style="font-size: 2em")
    QIcon(name='ti-hand-point-up', a=wp, style="font-size: 2em")
    QIcon(name='wifi', a=wp, style="font-size: 2em")

    QIcon(name='format_align_justify', a=wp)
    return wp
    with open('icons.txt', 'r') as f:
        l = f.readline()
        while l:
            l = l.split()
            q = QIcon(name=l[0], a=c.name_dict['icon-div'], temp=True)
            # q = QIcon(name='r_'+l[0], a=c.name_dict['icon-div'], temp=True)
            l = f.readline()

    return wp

def table_test():
    wp = QuasarPage()
    columns = """
     [
        {
          name: 'name',
          required: true,
          label: 'Dessert (100g serving)',
          align: 'left',
          field: 'name',
          
          sortable: true
        },
        { name: 'calories', align: 'center', label: 'Calories', field: 'calories', sortable: true },
        { name: 'fat', label: 'Fat (g)', field: 'fat', sortable: true },
        { name: 'carbs', label: 'Carbs (g)', field: 'carbs' },
        { name: 'protein', label: 'Protein (g)', field: 'protein' },
        { name: 'sodium', label: 'Sodium (mg)', field: 'sodium' },
        { name: 'calcium', label: 'Calcium (%)', field: 'calcium', sortable: true },
        { name: 'iron', label: 'Iron (%)', field: 'iron', sortable: true}
      ]
    """
    data = """
    [
        {
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          sodium: 87,
          calcium: '14%',
          iron: '1%'
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          sodium: 129,
          calcium: '8%',
          iron: '1%'
        },
        {
          name: 'Eclair',
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          sodium: 337,
          calcium: '6%',
          iron: '7%'
        },
        {
          name: 'Cupcake',
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          sodium: 413,
          calcium: '3%',
          iron: '8%'
        },
        {
          name: 'Gingerbread',
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          sodium: 327,
          calcium: '7%',
          iron: '16%'
        },
        {
          name: 'Jelly bean',
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          sodium: 50,
          calcium: '0%',
          iron: '0%'
        },
        {
          name: 'Lollipop',
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          sodium: 38,
          calcium: '0%',
          iron: '2%'
        },
        {
          name: 'Honeycomb',
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          sodium: 562,
          calcium: '0%',
          iron: '45%'
        },
        {
          name: 'Donut',
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          sodium: 326,
          calcium: '2%',
          iron: '22%'
        },
        {
          name: 'KitKat',
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          sodium: 54,
          calcium: '12%',
          iron: '6%'
        }
      ]
    """
    d = Div(classes='q-pa-md', a=wp, style='height: 300px')
    t = QTable(title='Treats', data=data, columns=columns, row_key='name', a=d, dense=True, selection="single", fullscreen=False)
    def selection_event(self, msg):
        print('in selection EVENT')
        print(msg)
    t.on('selection', selection_event)
    return wp

def markup_table_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-markup-table dark class="bg-indigo-8" dense>
      <thead>
        <tr>
          <th class="text-left">Dessert (100g serving)</th>
          <th class="text-right">Calories</th>
          <th class="text-right">Fat (g)</th>
          <th class="text-right">Carbs (g)</th>
          <th class="text-right">Protein (g)</th>
          <th class="text-right">Sodium (mg)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left">Frozen Yogurt</td>
          <td class="text-right">159</td>
          <td class="text-right">6</td>
          <td class="text-right">24</td>
          <td class="text-right">4</td>
          <td class="text-right">87</td>
        </tr>
        <tr>
          <td class="text-left">Ice cream sandwich</td>
          <td class="text-right">237</td>
          <td class="text-right">9</td>
          <td class="text-right">37</td>
          <td class="text-right">4.3</td>
          <td class="text-right">129</td>
        </tr>
        <tr>
          <td class="text-left">Eclair</td>
          <td class="text-right">262</td>
          <td class="text-right">16</td>
          <td class="text-right">23</td>
          <td class="text-right">6</td>
          <td class="text-right">337</td>
        </tr>
        <tr>
          <td class="text-left">Cupcake</td>
          <td class="text-right">305</td>
          <td class="text-right">3.7</td>
          <td class="text-right">67</td>
          <td class="text-right">4.3</td>
          <td class="text-right">413</td>
        </tr>
        <tr>
          <td class="text-left">Gingerbread</td>
          <td class="text-right">356</td>
          <td class="text-right">16</td>
          <td class="text-right">49</td>
          <td class="text-right">3.9</td>
          <td class="text-right">327</td>
        </tr>
      </tbody>
    </q-markup-table>
  </div>
  <div class="q-pa-md">
  <q-btn name="b1"
      
      :percentage="50"
      color="primary"
      
      style="width: 100px"
    >
    
    </q-btn>
    <q-btn color="primary" class="block" icon="alarm" label="Block" :loading="True" :percentage="50" />
    <q-btn color="teal" class="block q-mt-md" label="Block" />

    <q-btn color="black" class="full-width q-mt-md" label="Full-width" dark-percentage :percentage="50"/>

    <q-btn color="primary" label="With Tooltip" class="q-mt-md">
      <q-tooltip>I'm a tooltip</q-tooltip>
    </q-btn>
  </div>
    """, a=wp)
    b1 = c.name_dict['b1']
    b1.default_slot = Span(text='hello')
    s1 = Span()
    QSpinner(spinner_type='gears', a=s1, classes='on-left')
    Span(text='Hello', a=s1, classes='on-left')

    b1.loading_slot = s1
    b1.loading = True
    b1.fab = False
    return wp

def toolbar_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-toolbar class="bg-primary text-white q-my-md shadow-2">
      <q-btn flat round dense icon="menu" class="q-mr-sm" />
      <q-separator dark vertical inset />
      <q-btn stretch flat label="Link" />

      <q-space />

      <q-btn-dropdown stretch flat label="Dropdown">
        <q-list>
          <q-item-label header>Folders</q-item-label>
          <q-item  clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="folder" color="secondary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Photos</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
          <q-item  clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="folder" color="secondary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Photos</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
          <q-item  clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="folder" color="secondary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Photos</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
          <q-separator inset spaced />
          <q-item-label header>Files</q-item-label>
          <q-item  clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="assignment" color="primary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Vacation</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
          <q-item  clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="assignment" color="primary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Vacation</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
          <q-item  clickable v-close-popup tabindex="0">
            <q-item-section avatar>
              <q-avatar icon="assignment" color="primary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Vacation</q-item-label>
              <q-item-label caption>February 22, 2016</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="info" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <q-separator dark vertical />
      <q-btn stretch flat label="Link" />
      <q-separator dark vertical />
      <q-btn stretch flat label="Link" />
    </q-toolbar>
  </div>
    """, a=wp)
    return wp

@SetRoute('/layout')
def layout_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-layout view="lhh LpR lff" container style="height: 300px" class="shadow-2 rounded-borders">
      <q-header reveal class="bg-black">
        <q-toolbar>
          <q-btn flat round dense icon="menu" />
          <q-toolbar-title>Header</q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-page-container>
        <q-page padding>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
            <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <q-page-sticky position="bottom-right" :offset="[18, 18]">
            <q-fab
              icon="add"
              direction="up"
              color="accent"
            >
              <q-fab-action  color="primary" icon="person_add" name="action1"/>
              <q-fab-action  color="primary" icon="mail" name="action2"/>
            </q-fab>
          </q-page-sticky>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
    """)
    c = parse_html("""
    <div class="q-pa-md">
    <q-layout view="lhh LpR lff" container style="height: 500px" class="shadow-2 rounded-borders">
      <q-header reveal class="bg-black">
        <q-toolbar>
          <q-btn flat @click="drawerLeft = !drawerLeft" round dense icon="menu" />
          <q-toolbar-title>Header</q-toolbar-title>
          <q-btn flat @click="drawerRight = !drawerRight" round dense icon="menu" />
        </q-toolbar>
      </q-header>

      <q-footer>
        <q-toolbar>
          <q-toolbar-title>Footer</q-toolbar-title>
        </q-toolbar>
      </q-footer>

      <q-drawer
        v-model="drawerLeft"
        :width="200"
        :breakpoint="700"
        bordered
        content-class="bg-grey-3"
      >
        <q-scroll-area class="fit">
          <div class="q-pa-sm">
            <div >Drawer 1 / 50</div>
          </div>
        </q-scroll-area>
      </q-drawer>

      <q-drawer
        side="right"
        v-model="drawerRight"
        bordered
        :width="200"
        :breakpoint="500"
        content-class="bg-grey-3"
      >
        <q-scroll-area class="fit">
          <div class="q-pa-sm">
            <div>Drawer right / 50</div>
          </div>
        </q-scroll-area>
      </q-drawer>

      <q-page-container>
        <q-page style="padding-top: 60px" class="q-pa-md">
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>

          <q-page-sticky position="top-left" :offset="[18, 68]">
            <q-btn round color="primary" icon="arrow_back" class="rotate-45" />
          </q-page-sticky>
          <q-page-sticky position="top-right" :offset="[18, 68]">
            <q-btn round color="primary" icon="arrow_upward" class="rotate-45" />
          </q-page-sticky>
          <q-page-sticky position="bottom-left" :offset="[18, 18]">
            <q-btn round color="primary" icon="arrow_forward" class="rotate-135" />
          </q-page-sticky>
          <q-page-sticky position="bottom-right" :offset="[18, 18]">
            <q-btn round color="primary" icon="arrow_forward" class="rotate-45" />
          </q-page-sticky>

          <q-page-sticky position="top" expand class="bg-accent text-white">
            <q-toolbar>
              <q-btn flat round dense icon="map" />
              <q-toolbar-title>Title</q-toolbar-title>
            </q-toolbar>
          </q-page-sticky>
        </q-page>

        <q-page-scroller position="bottom">
          <q-btn fab icon="keyboard_arrow_up" color="red" />
        </q-page-scroller>
      </q-page-container>
    </q-layout>
  </div>
    """)
    c = parse_html("""
    <div class="q-pa-md">
    <q-layout view="lHh Lpr lFf" container style="height: 400px" class="shadow-2 rounded-borders">
      <q-header elevated>
        <q-toolbar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg">
          </q-avatar>
          <q-toolbar-title>
            <strong>Quasar</strong> Framework
          </q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-page-container>
        <q-page padding>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
<p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>

          <!-- place QPageScroller at end of page -->
          <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
            <q-btn fab icon="keyboard_arrow_up" color="accent" />
          </q-page-scroller>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
    """, a=wp)
    return wp

def drawer_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-layout view="hHh Lpr lff" container style="height: 300px" class="shadow-2 rounded-borders">
      <q-header elevated class="bg-black">
        <q-toolbar>
          <q-btn flat  round dense icon="menu" name="header_button"/>
          <q-toolbar-title>Header</q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-drawer name="drawer"
        :width="200"
        :breakpoint="500"
        show-if-above
        bordered
        content-class="bg-grey-3"
      >
        <q-scroll-area class="fit">
          <q-list padding>
            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="inbox" />
              </q-item-section>

              <q-item-section>
                Inbox
              </q-item-section>
            </q-item>

            <q-item active clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="star" />
              </q-item-section>

              <q-item-section>
                Star
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                Send
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="drafts" />
              </q-item-section>

              <q-item-section>
                Drafts
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>

        <div class="q-mini-drawer-hide absolute" style="top: 15px; right: -17px" >
          <q-btn name="mini_button"
            dense
            round
            unelevated
            color="accent"
            icon="chevron_left"
            
          />
        </div>
      </q-drawer>

      <q-page-container>
        <q-page class="q-px-lg q-py-md">
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
    """, a=wp)
    print(c.name_dict)
    hb = c.name_dict['header_button']
    mb = c.name_dict['mini_button']
    mb.event_propagation = False
    drawer = c.name_dict['drawer']
    # drawer.event_propagation = False
    hb.drawer = drawer
    hb.mb = mb
    mb.drawer = drawer
    # drawer.add_event('!click')
    def toggle_drawer(self, msg):
        self.drawer.value = not self.drawer.value
        if not self.drawer.value:
            self.drawer.mini = False
            self.mb.show = False
        else:
            self.mb.show = True

    hb.on('click', toggle_drawer)

    def mini_false(self, msg):
        self.mini = False
        self.remove_event('click')


    def mini_true(self, msg):
        self.drawer.mini = True
        self.drawer.on('click', mini_false)

    mb.on('click', mini_true)
    # drawer.on('click', mini_false)

    return wp

@SetRoute('/drawer')
def drawer1_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <q-layout view="hHh Lpr lff" container style="height: 90vh" class="shadow-2 rounded-borders">
      <q-header elevated class="bg-black">
        <q-toolbar>
          <q-btn flat  round dense icon="menu" name="header_button"/>
          <q-toolbar-title>Header</q-toolbar-title>
        </q-toolbar>
      </q-header>

      <q-drawer name="drawer"
        :value="True"

        :mini="True"

        :width="200"
        :breakpoint="500"
        show-if-above
        bordered
        content-class="bg-grey-3"
      >
        <q-scroll-area class="fit">
          <q-list padding>
            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="inbox" />
              </q-item-section>

              <q-item-section>
                Inbox
              </q-item-section>
            </q-item>

            <q-item active clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="star" />
              </q-item-section>

              <q-item-section>
                Star
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                Send
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="drafts" />
              </q-item-section>

              <q-item-section>
                Drafts
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container>
        <q-page padding>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?
          </p>
        </q-page>
      </q-page-container>
    </q-layout>
  </div>
    """, a=wp)
    hb = c.name_dict['header_button']
    drawer = c.name_dict['drawer']
    hb.drawer = drawer
    def toggle_drawer(self, msg):
        self.drawer.value = not self.drawer.value
    hb.on('click', toggle_drawer)
    def mini_false(self, msg):
        self.mini = False
    def mini_true(self, msg):
        self.mini = True
    drawer.on('mouseover', mini_false)
    drawer.on('mouseout', mini_true)
    return wp


@SetRoute('/helloeli/{user:path}', name='my_route')
def test_eli_params(request):
    user = request.path_params['user']
    wp = WebPage()
    Div(text=f'Hello {user}!', classes='m-1 p-1 text-5xl hover:bg-yellow-200', a=wp)
    return wp


def get_routes(request):
    wp = WebPage()
    d = Div(classes='flex flex-wrap', a=wp)
    for route in Route.instances:
        A(text=route.path, url=route.path, a=d, classes='m-1 p-2 text-2xl text-white bg-blue-500')
    return wp


@SetRoute('/rating')
def rating_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-y-md column">
      <q-rating
        v-model="ratingModel"
        size="1.5em"
        icon="thumb_up"
      />
      <q-rating
        v-model="ratingModel"
        size="2em"
        color="red-7"
        icon="favorite_border"
      />
      <q-rating
        v-model="ratingModel"
        size="2.5em"
        color="purple-4"
        icon="create"
      />
      <q-rating
        v-model="ratingModel"
        size="3em"
        color="brown-5"
        icon="pets"
      />
      <q-rating
        v-model="ratingModel"
        size="3.5em"
        color="green-5"
        icon="star_border"
        :max="10"
      />
    </div>
  </div>
    """, a=wp)
    return wp


@SetRoute('/frame')
def iframe_test():
    wp = WebPage()
    d = Div(a=wp, style=' border: 2px solid; padding: 20px; width: 300px; resize: both; overflow: auto;')
    d1 = Hello(a=wp)
    d2 = Div(a=wp)
    # d.inner_html = '<iframe src="http://vixcentral.com" style="padding: 20px; width: 100%; height: 100%"></iframe>'
    d2.inner_html = '<script>console.log("Hello JavaScript!")</script>'
    d2.inner_html = 'hello'
    # Iframe(src='http://vixcentral.com', a=wp)
    return wp

@SetRoute('/svg')
def svg_test():
    wp = WebPage()
    c = parse_html("""
    <div class="bg-indigo-900 text-center py-4 lg:px-4">
  <div class="p-2 bg-indigo-800 items-center text-indigo-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
    <span class="flex rounded-full bg-indigo-500 uppercase px-2 py-1 text-xs font-bold mr-3">New</span>
    <span class="font-semibold mr-2 text-left flex-auto">Get the coolest t-shirts from our brand new store</span>
    <svg class="fill-current opacity-75 h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.95 10.707l.707-.707L8 4.343 6.586 5.757 10.828 10l-4.242 4.243L8 15.657l4.95-4.95z"/></svg>
  </div>
</div>
    """, a=wp)
    return wp

justpy(get_routes)
# justpy(q_test)
# justpy(test_directives)
# justpy(test_input)
# justpy(test_model)  # Shows model works also with q-tabs
# justpy(test_comps)
# justpy(test_panel)
# justpy(tab_demo)
# justpy(chat_test)
# justpy(dialog_test)
# justpy(image_test)
# justpy(inner_loading_test)
# justpy(splitter_test)
# justpy(dropdown_test)
# justpy(slider_test)
# justpy(qmenu_test)
# justpy(optiongroup_test)
# justpy(select_test)
# justpy(toggle_button_test)
# justpy(tooltip_test)
# justpy(stepper_test) # Not working, same problem as panels and carousel and so on.
# justpy(slide_transition_test)
# justpy(timeline_test)
# justpy(time_picker_test)
# justpy(knob_test)
# justpy(pagination_test)
# justpy(panel_test)
# justpy(tree_test)
# justpy(animate_test)
# justpy(slide_item_test)
# justpy(infinite_scroll_test)
# justpy(scroll_area_test)
# justpy(notifiy_test)
# justpy(parallax_test)
# justpy(video_test)
# justpy(icon_test)
# justpy(table_test)
# justpy(markup_table_test)
# justpy(toolbar_test)
# justpy(layout_test)
# justpy(drawer_test)
# justpy(drawer1_test)
# justpy(get_routes)