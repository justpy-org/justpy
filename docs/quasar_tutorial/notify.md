# Notifications

Notifications are created by a special component that does not wrap a quasar component but activates the quasar [notify](https://quasar.dev/quasar-plugins/notify) utility.

!!! warning
    Add an 'after' event to any button that activates the notification that sets the `notify` attribute back to false. Otherwise, the notification will appear every update. Alternatively, await page update in event and then set notify to `False`.

The following is based on [this](https://quasar.dev/quasar-plugins/notify#positioning) example in the Quasar documentation.

```python
import justpy as jp
import datetime


page_html = """
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

        <q-btn round size="sm" color="secondary" name="top-right">
          <q-icon name="arrow_upward" class="rotate-45" />
        </q-btn>

      </div>
    </div>

    <div>
      <div class="row q-gutter-sm">
        <div>

          <q-btn round size="sm" color="accent" name="left">
            <q-icon name="arrow_back" />
          </q-btn>
        </div>
        <div>

          <q-btn round size="sm" color="accent" name="center">
            <q-icon name="fullscreen_exit" />
          </q-btn>
        </div>
        <div>

          <q-btn round size="sm" color="accent" name="right">
            <q-icon name="arrow_forward" />
          </q-btn>

        </div>
      </div>
    </div>

    <div>
      <div class="row q-gutter-sm">
        <div>

          <q-btn round size="sm" color="secondary" name="bottom-left">
            <q-icon name="arrow_forward" class="rotate-135" />
          </q-btn>
        </div>
        <div>

          <q-btn round size="sm" color="accent" name="bottom">
            <q-icon name="arrow_downward" />
          </q-btn>
        </div>
        <div>

          <q-btn round size="sm" color="secondary" name="bottom-right">
            <q-icon name="arrow_forward" class="rotate-45" />
          </q-btn>
        </div>
      </div>
    </div>
  </div>
  </div>
    """

directions = ['top-left', 'top', 'top-right',
              'left', 'center', 'right',
              'bottom-left', 'bottom', 'bottom-right']


def btn_click(self, msg):
    self.notification.notify = True
    self.notification.caption = f'Time: {datetime.datetime.now().strftime("%H:%M:%S, %Y-%m-%d")}'

def btn_after(self, msg):
    self.notification.notify = False

def quasar_notify_test():
    wp = jp.QuasarPage()
    c = jp.parse_html(page_html, a=wp)
    for direction in directions:
        btn = c.name_dict[direction]
        btn.on('click', btn_click)
        btn.on('after', btn_after)
        btn.notification = jp.QNotify(message=f'Notification in/on {direction}', a=wp, position=direction, closeBtn='Close')
    return wp


jp.justpy(quasar_notify_test)

```
