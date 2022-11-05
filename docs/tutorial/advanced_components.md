# Advanced Components

!!! warning
    Work in progress. The example works but requires much more elucidation

## Introduction

In most cases, components can be defined using Python only as previously described in this tutorial. In some cases however, in parallel to the Python definition, a Vue.js component also needs to be created.

In this chapter, we will create a signing pad component based on [signature_pad](https://github.com/szimek/signature_pad)

!!! info
    If you are not familiar with Vue.js, this chapter will not be very useful to you.

## The Components Directory

Under your applications [static](https://justpy.io/tutorial/static/) directory (the default is the directory the application is run form) create another directory called `components`. Put the your JavaScript component definition there. Files must all have the extension `.js`.

The application will load these files automatically. 

## Python 

### Try [pad_test live demo]({{demo_url}}/pad_test)

```python
import justpy as jp

class SignaturePad(jp.JustpyBaseComponent):

    vue_type = 'signaturepad'

    def __init__(self, **kwargs):

        self.options = jp.Dict()
        self.classes = ''
        self.style = ''
        self.width = 400
        self.height = 200
        self.clear = False
        self.show = True
        self.event_propagation = True
        self.pages = {}
        kwargs['temp'] = False  # Force an id to be assigned to pad
        super().__init__(**kwargs)
        self.allowed_events = ['onEnd', 'onBegin']
        if type(self.options) != jp.Dict:
            self.options = jp.Dict(self.options)
        self.initialize(**kwargs)


    def add_to_page(self, wp: jp.WebPage):
        wp.add_component(self)

    def react(self, data):
        pass


    def convert_object_to_dict(self):
        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        d['show'] = self.show
        d['classes'] = self.classes
        d['style'] = self.style
        d['event_propagation'] = self.event_propagation
        d['def'] = self.options
        d['events'] = self.events
        d['width'] = self.width
        d['height'] = self.height
        d['clear'] = self.clear
        d['options'] = self.options
        return d


def my_end(self, msg):
    print(msg)
    self.data = msg.data

async def clear_pad(self, msg):
    self.pad.clear = True
    await msg.page.update()
    self.pad.clear = False
    return True


def pad_test():
    wp = jp.WebPage()
    wp.head_html = '<script src="https://cdn.jsdelivr.net/npm/signature_pad@2.3.2/dist/signature_pad.min.js"></script>'
    pad = SignaturePad(a=wp, style = 'background-color: white; border: 1px solid;', classes='m-2', onEnd=my_end)
    pad.options = {'penColor': 'blue'}
    clear_btn = jp.Button(text='Clear Pad', classes=jp.Styles.button_simple + ' m-2', a=wp, click=clear_pad)
    clear_btn.pad = pad
    return wp

jp.justpy(pad_test)
```
 
## Vue.js Component
 
```javascript
var signature_pads = {};
    Vue.component('signaturepad', {
        template:
            `<canvas  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style" :width="jp_props.width" height="jp_props.height"></canvas>`,
        methods: {
            pad_change() {
                var id = this.$props.jp_props.id.toString();
                var canvas = document.getElementById(id);
                var signaturePad = new SignaturePad(canvas, this.$props.jp_props.options);
                signature_pads[id] = signaturePad;
                var events = this.$props.jp_props.events;
                var props = this.$props;

                function onEnd() {
                    if (events.includes('onEnd')) {
                        var data = signaturePad.toDataURL('image/png');
                        var point_data = signaturePad.toData();
                        var e = {
                            'event_type': 'onEnd',
                            'id': props.jp_props.id,
                            'class_name': props.jp_props.class_name,
                            'html_tag': props.jp_props.html_tag,
                            'vue_type': props.jp_props.vue_type,
                            'page_id': page_id,
                            'websocket_id': websocket_id,
                            'data': data,
                            'point_data': point_data
                        };
                        send_to_server(e, 'event');
                    }
                }

                signaturePad.onEnd = onEnd;

            }
        },
        mounted() {
            this.pad_change();
        },
        updated() {

            if (this.$props.jp_props.clear) {
                signature_pads[this.$props.jp_props.id.toString()].clear();
            }
        },
        props: {
            jp_props: Object
        }
    });

```

## FullCalendar Example

[FullCalendar](https://fullcalendar.io/) is a full featured JavaScript Calendar

The following implementation does not support all the features and events but is a sound basis to build on.

Python file:

```python
import justpy as jp


class FullCalendar(jp.JustpyBaseComponent):
    vue_type = 'fullcalendar'

    def __init__(self, **kwargs):
        self.options = jp.Dict()
        self.classes = ''
        self.style = ''
        self.show = True
        self.event_propagation = True
        self.pages = {}
        kwargs['temp'] = False  # Force an id to be assigned
        super().__init__(**kwargs)
        self.allowed_events = ['eventClick', 'eventDrop']
        if type(self.options) != jp.Dict:
            self.options = jp.Dict(self.options)
        self.initialize(**kwargs)

    def add_to_page(self, wp: jp.WebPage):
        wp.add_component(self)

    def react(self, data):
        pass

    async def run_method(self, command, websocket):
        await websocket.send_json({'type': 'run_method', 'data': command, 'id': self.id})
        # So the page itself does not update, return True not None
        return True

    def convert_object_to_dict(self):
        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        d['show'] = self.show
        d['classes'] = self.classes
        d['style'] = self.style
        d['event_propagation'] = self.event_propagation
        d['events'] = self.events
        d['options'] = self.options
        return d


calendar_options = {
    'plugins': ['dayGrid', 'interaction'],
    'editable': True,
    'header': {'left': '',
               'center': 'title',
               'right': 'today prev,next'},
    'defaultDate': '2020-05-15',
    'events': [
        {
            'title': 'This is an event',
            'start': '2020-05-02',
            'end': '2020-05-12',
            'color': 'red',
            'editable': True
        },
        {
            'title': 'event with a URL',
            'url': 'https://www.google.com/',
            'start': '2020-05-03'
        }
    ]
}
# https://fullcalendar.io/docs/plugin-index
head_html = """
<link rel="stylesheet" href="https://unpkg.com/@fullcalendar/core@4.4.0/main.min.css">
<link rel="stylesheet" href="https://unpkg.com/@fullcalendar/daygrid@4.4.0/main.min.css">
<script src="https://unpkg.com/@fullcalendar/core@4.4.0/main.min.js"></script>
<script src="https://unpkg.com/@fullcalendar/daygrid@4.4.0/main.min.js"></script>
<script src="https://unpkg.com/@fullcalendar/interaction@4.4.0/main.min.js"></script>
"""

async def add_event(self, msg):
    print(msg)
    self.calendar.options['events'].append({'title': 'Very new event', 'start': '2020-05-02', 'end': '2020-05-05', 'color': 'green', 'editable': True})

def event_click(self, msg):
    print(msg)

def event_drop(self, msg):
    print(msg)
    print(msg.all_events)
    self.options['events'] = msg.all_events

def calendar_test():
    wp = jp.QuasarPage()
    wp.head_html = head_html
    calendar = FullCalendar(a=wp, classes='q-ma-lg', style='width: 700px;')
    calendar.options = calendar_options
    calendar.on('eventClick', event_click)
    calendar.on('eventDrop', event_drop)
    b = jp.QBtn(label='Add Event', a=wp, classes='q-ma-lg', click=add_event)
    b.calendar = calendar
    return wp


jp.justpy(calendar_test)

```

Vue.js component:

```javascript
var full_calendars = {};
Vue.component('fullcalendar', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style" ></div>`,

    methods: {
        get_all_events(calendar) {
            let all_events = [];
            for (let event_obj of calendar.getEvents()) {
                all_events.push(this.create_object_from_event(event_obj))
            }
            return all_events;
        },
        create_object_from_event(event_obj) {
            // https://fullcalendar.io/docs/event-object
            const event_properties = ['id', 'groupId', 'allDay', 'start', 'end', 'title', 'url', 'classNames',
                'editable', 'startEditable', 'durationEditable', 'resourceEditable', 'rendering', 'overlap',
                'constraint', 'backgroundColor', 'borderColor', 'textColor', 'extendedProps'];
            let event_data = {};
            for (let i of event_properties) {
                event_data[i] =event_obj[i];
            }
            return event_data;
        },
        calendar_change() {
            var id = this.$props.jp_props.id.toString();
            var events = this.$props.jp_props.events;
            var props = this.$props;
            var calendarEl = document.getElementById(id);
            var calendar = new FullCalendar.Calendar(calendarEl, this.$props.jp_props.options);
            const parent_comp = this;
            if (events.includes('eventClick'))
                // https://fullcalendar.io/docs/eventClick
                calendar.on('eventClick', function (info) {
                    var e = {
                        'event_type': 'eventClick',
                        'id': props.jp_props.id,
                        'class_name': props.jp_props.class_name,
                        'html_tag': props.jp_props.html_tag,
                        'vue_type': props.jp_props.vue_type,
                        'page_id': page_id,
                        'websocket_id': websocket_id,
                        'event_data': parent_comp.create_object_from_event(info.event),
                        'all_events': parent_comp.get_all_events(calendar)
                    };
                    send_to_server(e, 'event');
                });

            if (events.includes('eventDrop'))
                // https://fullcalendar.io/docs/eventDrop
                calendar.on('eventDrop', function (info) {
                    var e = {
                        'event_type': 'eventDrop',
                        'id': props.jp_props.id,
                        'class_name': props.jp_props.class_name,
                        'html_tag': props.jp_props.html_tag,
                        'vue_type': props.jp_props.vue_type,
                        'page_id': page_id,
                        'websocket_id': websocket_id,
                        'event_data': parent_comp.create_object_from_event(info.event),
                        'old_event_data': parent_comp.create_object_from_event(info.oldEvent),
                        'delta': info.delta,
                        'all_events': parent_comp.get_all_events(calendar)
                    };
                    send_to_server(e, 'event');
                });
            full_calendars[id] = calendar;
            comp_dict[this.$props.jp_props.id] = calendar;

            calendar.render();
        },

    },

    mounted() {
        this.calendar_change();
    },
    updated() {
        var calendar = comp_dict[this.$props.jp_props.id];
        calendar.destroy();
        this.calendar_change();

    },
    props: {
        jp_props: Object
    }
});


```