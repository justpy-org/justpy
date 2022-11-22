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
