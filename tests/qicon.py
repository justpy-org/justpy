import justpy as jp


def icon_test():
    wp = jp.QuasarPage()
    c = jp.parse_html("""
    <div class="q-pa-md">
    <div class="text-purple q-gutter-md" style="font-size: 2em">
      <q-icon name="font_download" />
      <q-icon name="warning" />
      <q-icon name="format_size" />
      <q-icon name="print" />
      <q-icon name="today" />
      <q-icon name="style" />
    </div>

    <div class="q-mt-md q-gutter-md">
      <q-icon name="font_download" class="text-primary" style="font-size: 32px;" />
      <q-icon name="warning" class="text-red" style="font-size: 4rem;" />
      <q-icon name="format_size" style="color: #ccc; font-size: 1.4em;" />
      <q-icon name="print" class="text-teal" style="font-size: 4.4em;" />
      <q-icon name="today" class="text-orange" style="font-size: 2em;" />
      <q-icon name="style" style="font-size: 3em;" />
    </div>
  </div>
    """, a=wp)
    c = jp.parse_html("""
<div class="q-pa-md">
    <div class="q-gutter-md">
      <q-btn color="accent" label="Fit Menu" style="width: 280px;">

        <q-menu fit>
          <q-list style="min-width: 100px">
            <q-item clickable>
              <q-item-section>New tab</q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>New incognito tab</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Recent tabs</q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>History</q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>Downloads</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Settings</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Help &amp; Feedback</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>

      <q-btn color="brown" label="Max Height Menu">
        <q-menu max-height="130px">
          <q-list style="min-width: 100px">
            <q-item clickable>
              <q-item-section>New tab</q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>New incognito tab</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Recent tabs</q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>History</q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>Downloads</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Settings</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>Help &amp; Feedback</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>

      <q-btn color="indigo" label="Max Width Menu">
        <q-menu max-width="80px">
          <q-list style="min-width: 100px">
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">New tab</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">New incognito tab</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">Recent tabs</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">History</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">Downloads</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">Settings</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable>
              <q-item-section>
                <q-item-label lines="1">Help & Feedback</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>

    </div>
  </div>
    """, a=wp)
    for i in c.commands:
        print(i)
    jp.Br(a=wp)
    root = jp.Div(name='root', a=wp)
    c17 = jp.Div(classes='q-pa-md', a=root)
    c18 = jp.Div(classes='q-gutter-md', a=c17)
    c19 = jp.QBtn(color='accent', label='Fit Menu', style='width: 280px;', a=c18)
    c20 = jp.QMenu(fit=True, a=c19)
    c21 = jp.QList(style='min-width: 100px', a=c20)
    c22 = jp.QItem(clickable=True, a=c21)
    c23 = jp.QItemSection(a=c22, text='New tab')
    c24 = jp.QItem(clickable=True, a=c21)
    c25 = jp.QItemSection(a=c24, text='New incognito tab')
    c26 = jp.QSeparator(a=c21)
    c27 = jp.QItem(clickable=True, a=c21)
    c28 = jp.QItemSection(a=c27, text='Recent tabs')
    c29 = jp.QItem(clickable=True, a=c21)
    c30 = jp.QItemSection(a=c29, text='History')
    c31 = jp.QItem(clickable=True, a=c21)
    c32 = jp.QItemSection(a=c31, text='Downloads')
    c33 = jp.QSeparator(a=c21)
    c34 = jp.QItem(clickable=True, a=c21)
    c35 = jp.QItemSection(a=c34, text='Settings')
    c36 = jp.QSeparator(a=c21)
    c37 = jp.QItem(clickable=True, a=c21)
    c38 = jp.QItemSection(a=c37, text='Help & Feedback')
    c39 = jp.QBtn(color='brown', label='Max Height Menu', a=c18)
    c40 = jp.QMenu(max_height='130px', a=c39)
    c41 = jp.QList(style='min-width: 100px', a=c40)
    c42 = jp.QItem(clickable=True, a=c41)
    c43 = jp.QItemSection(a=c42, text='New tab')
    c44 = jp.QItem(clickable=True, a=c41)
    c45 = jp.QItemSection(a=c44, text='New incognito tab')
    c46 = jp.QSeparator(a=c41)
    c47 = jp.QItem(clickable=True, a=c41)
    c48 = jp.QItemSection(a=c47, text='Recent tabs')
    c49 = jp.QItem(clickable=True, a=c41)
    c50 = jp.QItemSection(a=c49, text='History')
    c51 = jp.QItem(clickable=True, a=c41)
    c52 = jp.QItemSection(a=c51, text='Downloads')
    c53 = jp.QSeparator(a=c41)
    c54 = jp.QItem(clickable=True, a=c41)
    c55 = jp.QItemSection(a=c54, text='Settings')
    c56 = jp.QSeparator(a=c41)
    c57 = jp.QItem(clickable=True, a=c41)
    c58 = jp.QItemSection(a=c57, text='Help & Feedback')
    c59 = jp.QBtn(color='indigo', label='Max Width Menu', a=c18)
    c60 = jp.QMenu(max_width='80px', a=c59)
    c61 = jp.QList(style='min-width: 100px', a=c60)
    c62 = jp.QItem(clickable=True, a=c61)
    c63 = jp.QItemSection(a=c62)
    c64 = jp.QItemLabel(lines='1', a=c63, text='New tab')
    c65 = jp.QItem(clickable=True, a=c61)
    c66 = jp.QItemSection(a=c65)
    c67 = jp.QItemLabel(lines='1', a=c66, text='New incognito tab')
    c68 = jp.QSeparator(a=c61)
    c69 = jp.QItem(clickable=True, a=c61)
    c70 = jp.QItemSection(a=c69)
    c71 = jp.QItemLabel(lines='1', a=c70, text='Recent tabs')
    c72 = jp.QItem(clickable=True, a=c61)
    c73 = jp.QItemSection(a=c72)
    c74 = jp.QItemLabel(lines='1', a=c73, text='History')
    c75 = jp.QItem(clickable=True, a=c61)
    c76 = jp.QItemSection(a=c75)
    c77 = jp.QItemLabel(lines='1', a=c76, text='Downloads')
    c78 = jp.QSeparator(a=c61)
    c79 = jp.QItem(clickable=True, a=c61)
    c80 = jp.QItemSection(a=c79)
    c81 = jp.QItemLabel(lines='1', a=c80, text='Settings')
    c82 = jp.QSeparator(a=c61)
    c83 = jp.QItem(clickable=True, a=c61)
    c84 = jp.QItemSection(a=c83)
    c85 = jp.QItemLabel(lines='1', a=c84, text='Help & Feedback')
    jp.parse_html("""
    <div class="q-pa-md">
    <div class="q-gutter-y-md column">
      <q-rating
        
        size="3.5em"
        color="green-5"
        icon="star_border"
        icon-selected="star"
      />
    </div>
  </div>
    """, a=wp)
    return wp

jp.justpy(icon_test)