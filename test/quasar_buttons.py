import justpy as jp


def q_test():
    wp = jp.QuasarPage()
    p = jp.parse_html("""
    <div>
    <div class="q-pa-md q-gutter-sm">
    <q-btn color="white" text-color="black" label="Standard" />
    <q-btn color="primary" label="Primary" />
    <q-btn color="secondary" label="Secondary" />
    <q-btn color="amber" glossy label="Amber" />
    <q-btn color="brown-5" label="Brown 5" />
    <q-btn color="deep-orange" glossy label="Deep Orange" />
    <q-btn color="purple" label="Purple" />
    <q-btn color="black" label="Black" />
    <br/>
    <q-btn style="background: #FF0080; color: white" label="Fuchsia" />
    <q-btn flat style="color: #FF0080" label="Fuchsia Flat" />
    <q-btn style="background: goldenrod; color: white" label="Goldenrod" />
    <q-btn outline style="color: goldenrod;" label="Goldenrod" />
    <q-btn color="grey-4" text-color="purple" glossy unelevated icon="camera_enhance" label="Purple text" />
    <q-btn color="primary" icon="mail" label="On Left" />
    <q-btn color="secondary" icon-right="mail" label="On Right" />
    <q-btn color="red" icon="mail" icon-right="send" label="On Left and Right" />
    <br/>
    <q-btn icon="phone" label="Stacked" stack glossy color="purple" />
    <q-btn round color="primary" icon="shopping_cart" />
    <q-btn round color="secondary" icon="navigation" />
    <q-btn round color="amber" glossy text-color="black" icon="layers_clear" />
    <q-btn round color="brown-5" icon="directions" />
    <q-btn round color="deep-orange" icon="edit_location" />
    <q-btn round color="purple" glossy icon="local_grocery_store" />
    <q-btn round color="black" icon="my_location" />
    <div class="q-pa-md q-gutter-md">
    <q-btn color="teal">
      <q-icon left size="3em" name="map" />
      <div>Label</div>
    </q-btn>

    <q-btn round>
      <q-avatar size="42px">
        <img src="https://cdn.quasar.dev/img/avatar2.jpg">
      </q-avatar>
    </q-btn>

    <q-btn color="indigo" no-caps>
      Multiline<br>Button
    </q-btn>
<br/>
    <q-btn color="deep-orange" push>
      <div class="row items-center no-wrap">
        <q-icon left name="map" />
        <div class="text-center">
          <span>Custom</span><br/><span>content</span>
        </div>
      </div>
    </q-btn>
  </div>

  </div>
  <div class="q-pa-md q-gutter-sm">
    <q-btn color="primary" style="width: 200px">
      <div class="ellipsis">
        This is some very long text that is expected to be truncated
      </div>
    </q-btn>
  </div>
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
  </div>
  <div class="q-pa-md q-gutter-sm">
    <q-btn align="left" style="width: 200px" class="btn-fixed-width" color="primary" label="Align to left" />
    <q-btn align="right" style="width: 200px" class="btn-fixed-width" color="secondary" label="Align to right" />
    <q-btn align="between" style="width: 300px" class="btn-fixed-width" color="accent" label="Align between" icon="flight_takeoff" />
    <q-btn align="around" style="width: 300px" class="btn-fixed-width" color="brown-5" label="Align around" icon="lightbulb_outline" />
  </div>
  <div class="q-pa-md q-gutter-sm">
  <q-btn
      size="10px"
      color="black"
      label="Text height: 10px"
    />
    <q-btn
      size="22px"
      class="q-px-xl q-py-xs"
      color="purple"
      label="Custom"
    />
    <q-btn
      size="35px"
      round
      color="teal"
      icon="map"
    />
  </div>
  </div>
    """, a=wp)
    wp.dark = True
    for i in p.commands:
        print(i)
        jp.Div(text=i, classes='q-ml-md', style='font-family: monospace', a=wp)
    return wp


jp.justpy(q_test)