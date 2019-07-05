from justpy import *
import demjson


def load_json(options_string):
    return Dict(demjson.decode(options_string.encode("ascii", "ignore")))

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

def test_model():
    wp = WebPage(template_file='quasar.html') # data={'text': 'EliEli'}
    icon = QIcon(color='red', name='fas fa-dog', a=wp)
    icon1 = QIcon(color='orange', name='fas fa-cat', a=wp)
    d = Div(classes="q-gutter-md", style="max-width: 500px", a=wp)
    d1 = Div(classes="q-pa-md", a=d, data={'text': 'EliEli'})
    in1 = QInput(a=d1, color="purple-12", label='Standard', model=[d1, 'text']) # model=[wp, 'text']
    in1.hint = 'try dog'
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
    <q-input standout v-model="email" type="email" prefix="Email:" suffix="@gmail.com"></q-input>
    """, a=d1)
    in3.add_scoped_slot('prepend', QIcon(name='mail'))
    in3.add_scoped_slot('after', Div(text='hello'))
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
    """, a=d1)
    c.model = [d1, 'text']
    return wp


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
    c.name_dict['list1'][0].on('click', click_me)
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

def chat_test():
    wp = QuasarPage(data={'color': '#695757'})
    d = Div(classes="q-pa-md", style="max-width: 900px", a=wp)
    #TODO: Document how : in front of an attribute causes it to be evaluated by parse_html
    c = parse_html("""
    <div class="q-gutter-xs">
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
    s.before = pane
    s.after = pane
    # s.add_scoped_slot('after', pane)
    return wp

# justpy(q_test)
# justpy(test_directives)
# justpy(test_input)
# justpy(test_model)  # Shows model works also with q-tabs
# justpy(test_comps)
# justpy(test_panel)
# justpy(tab_demo)
# justpy(chat_test)
justpy(dialog_test)
# justpy(image_test)
# justpy(inner_loading_test)
# justpy(splitter_test)