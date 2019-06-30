from justpy import *

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
    # in1 = QInput(a=wp, color="purple-12", label='Standard') # model=[wp, 'text']
    in1.add_scoped_slot('append', icon)


    in1.add_scoped_slot('prepend', QIcon(name='favorite', color='blue'))
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

# justpy(q_test)
# justpy(test_directives)
# justpy(test_input)
# justpy(test_model)  # Shows model works also with q-tabs
# justpy(test_comps)
# justpy(test_panel)
justpy(tab_demo)
