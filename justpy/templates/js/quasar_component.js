// {% raw %}
var storage_dict = {};

Vue.component('quasar_component', {

    render: function (h) {
        if (this.jp_props.hasOwnProperty('text')) {
            var comps = [this.jp_props.text];
        } else comps = [];

        for (var i = 0; i < this.jp_props.object_props.length; i++) {
            if (this.jp_props.object_props[i].show) {
                comps.push(h(this.jp_props.object_props[i].vue_type, {
                    props: {
                        jp_props: this.jp_props.object_props[i]
                    }
                }))
            }
        }

        if (this.jp_props.evaluate_prop && (this.jp_props.evaluate_prop.length > 0)) {
            for (i = 0; i < this.jp_props.evaluate_prop.length; i++) {
                const evaluated_prop = this.jp_props.evaluate_prop[i];
                if (this.jp_props.attrs[evaluated_prop]) {
                    if (typeof this.jp_props.attrs[evaluated_prop] == 'string') {
                        this.jp_props.attrs[evaluated_prop] = eval(this.jp_props.attrs[evaluated_prop])
                    } else {
                        for (let j = 0; i < this.jp_props.attrs[evaluated_prop].length; i++) {
                            this.jp_props.attrs[evaluated_prop][j] = eval(this.jp_props.attrs[evaluated_prop][j]);
                        }
                    }
                }
            }
        }

        description_object = {
            style: this.jp_props.style,
            attrs: this.jp_props.attrs,
            domProps: {
                // innerHTML: this.jp_props.inner_html
            },
            on: {},
            directives: [],
            slot: this.jp_props.slot,
            scopedSlots: {},
            ref: 'r' + this.jp_props.id
        };

        if (this.jp_props.classes) {
            description_object['class'] = this.jp_props.classes;
        }

        var event_description = {};
        var fn;
        for (i = 0; i < this.jp_props.events.length; i++) {
            switch (this.jp_props.events[i]) {

                case 'input':
                    fn = this.inputEvent;
                    break;
                case 'change':
                    fn = this.changeEvent;
                    break;
                case 'submit':
                    fn = this.submitEvent;
                    break;
                // For QTree
                case 'update:expanded':
                    fn = this.treeExpandedEvent;
                    break;
                case 'update:selected':
                    fn = this.treeSelectedEvent;
                    break;  // Also for QTable and QChip
                case 'update:ticked':
                    fn = this.treeTickedEvent;
                    break;
                // For QSlideItem
                case 'left':
                    fn = this.leftEvent;
                    break;
                case 'right':
                    fn = this.rightEvent;
                    break;
                case 'action':
                    fn = this.actionEvent;
                    break;
                case 'load':
                    fn = this.loadEvent;
                    break;
                // For QTable
                case 'update:pagination':
                    fn = this.tablePaginationEvent;
                    break;
                case 'request':
                    fn = this.tableRequestEvent;
                    break;
                case 'selection':
                    fn = this.tableSelectionEvent;
                    break;
                case 'remove':
                    fn = this.removeEvent;
                    break;
                // For QScrollObserver
                case 'scroll':
                    fn = this.scrollEvent;
                    break;

                // For QPopupEdit
                case 'save':
                    fn = this.saveEvent;
                    break;
                case 'cancel':
                    fn = this.cancelEvent;
                    break;


                default:
                    fn = this.defaultEvent;
            }
            event_description[this.jp_props.events[i]] = fn;
        }
        description_object['on'] = event_description;

        if (this.jp_props.inner_html) {
            description_object['domProps'] = {innerHTML: this.jp_props.inner_html};
        }

        var directives = [];   // Directives are a list of objects
        for (const directive_name in this.jp_props.directives) {
            directives.push({name: directive_name, value: this.jp_props.directives[directive_name]});
        }
        description_object['directives'] = directives;

        var scoped_slots = {};
        var b = {};
        for (slot_name in this.jp_props.scoped_slots) {
            b[slot_name] = this.jp_props.scoped_slots[slot_name];
            var vue_type = this.jp_props.vue_type;
            scoped_slots[slot_name] = (function (v, e) {
                return function () {
                    return h(v, {props: {jp_props: b[e]}});
                }
            })(vue_type, slot_name);
        }
        description_object['scopedSlots'] = scoped_slots;

        return h(this.jp_props.html_tag, description_object, comps);

    },
    methods: {
        createEvent: (function (event, event_type, aux) {
            new_event = {};
            new_event.type = event_type;
            new_event.target = {};
            new_event.currentTarget = {};
            new_event.target.value = event;
            if (aux) new_event.aux = aux;
            eventHandler(this.$props, new_event, false, aux);
        }),
        defaultEvent: (function (event) {
            this.eventFunction(event, event.type);
        }),
        inputEvent: (function (event) {
            if (arguments.length == 1) {
                aux = false;
            } else {
                var aux = [];
                for (var i = 1; i < arguments.length; i++) {
                    aux.push(arguments[i]);
                }
            }
            if (event == null && this.$props.jp_props.html_tag == 'q-input') event = '';
            this.eventFunction(event, 'input', aux);
        }),
        changeEvent: (function (event) {
            this.eventFunction(event, 'change');
        }),
        scrollEvent: (function (event) {
            this.eventFunction(event, 'scroll');
        }),
        treeExpandedEvent: (function (event) {
            this.eventFunction(event, 'update:expanded');
        }),
        treeSelectedEvent: (function (event) {
            this.eventFunction(event, 'update:selected');
        }),
        treeTickedEvent: (function (event) {
            this.eventFunction(event, 'update:ticked');
        }),
        tablePaginationEvent: (function (event) {
            this.eventFunction(event, 'update:pagination');
        }),
        tableRequestEvent: (function (event) {
            this.eventFunction(event, 'request');
        }),
        tableSelectionEvent: (function (event) {
            this.eventFunction(event, 'selection');
        }),
        removeEvent: (function (event) {
            this.eventFunction(event, 'remove');
        }),
        saveEvent: (function (event) {
            this.eventFunction(event, 'save');
        }),
        cancelEvent: (function (event, event1) {
            this.eventFunction(event, 'cancel');
        }),
        leftEvent: (function (event) {
            storage_dict['r' + this.$props.jp_props.id] = event;
            this.eventFunction(true, 'left');
        }),
        rightEvent: (function (event) {
            storage_dict['r' + this.$props.jp_props.id] = event;
            this.eventFunction(true, 'right');
        }),
        actionEvent: (function (event) {
            storage_dict['r' + this.$props.jp_props.id] = event;
            this.eventFunction(event.side, 'action');
        }),
        loadEvent: (function (index, done) {
            storage_dict['r' + this.$props.jp_props.id] = done;
            this.eventFunction(index, 'load');
        }),
        submitEvent: (function (event) {
            if (event.hasOwnProperty('type')) {
                var form_reference = this.$el;
                var props = this.$props;
                event.preventDefault();    //stop form from submitting
                var form_elements_list = [];
                var formData = new FormData(form_reference);
                var form_elements = form_reference.elements;

                for (var i = 0; i < form_elements.length; i++) {
                    var attributes = form_elements[i].attributes;
                    var attr_dict = {};
                    attr_dict['html_tag'] = form_elements[i].tagName.toLowerCase();
                    for (var j = 0; j < attributes.length; j++) {
                        var attr = attributes[j];
                        attr_dict[attr.name] = attr.value;
                    }
                    attr_dict['value'] = form_elements[i].value;
                    attr_dict['checked'] = form_elements[i].checked;
                    attr_dict['id'] = form_elements[i].id;
                    form_elements_list.push(attr_dict);
                }

                eventHandler(props, event, form_elements_list);
            }
        }),

        eventFunction: (function (event, event_type, aux) {
            if (!this.$props.jp_props.event_propagation) {
                event.stopPropagation();
            }

            if (event instanceof Event) {
                eventHandler(this.$props, event, false);
            } else {
                this.createEvent(event, event_type, aux);
            }
        }),
        animateFunction: (function () {
            var animation = this.$props.jp_props.animation;
            var element = this.$el;
            element.classList.add('animated', animation);
            element.addEventListener('animationend', function () {
                element.classList.remove('animated', animation);
            });
        }),
        notifyFunction: (function () {
            var attr_list = ['message', 'position', 'icon', 'color', 'textColor', 'timeout', 'avatar',
                'caption', 'closeBtn', 'html'];
            var notify_object = {};
            for (let i = 0; i < attr_list.length; i++) {
                notify_object[attr_list[i]] = this.jp_props.attrs[attr_list[i]];
            }
            if (this.jp_props.attrs.reply) {
                // Todo: Add actions
                notify_object.actions = [{
                    label: 'reply', handler: () => {
                    }
                }];
            }
            app1.$q.notify(notify_object);
        })
        ,
        mountedFunction: (function (event) {

        })
    },
    mounted() {
        if (this.$props.jp_props.id) {
            comp_dict[this.$props.jp_props.id] = this.$refs['r' + this.$props.jp_props.id];
        }

        if (this.$props.jp_props.animation) this.animateFunction();

        switch (this.$props.jp_props.html_tag) {

            case 'q-notify':
                if (this.$props.jp_props.notify) {
                    this.$nextTick(() => {
                        this.notifyFunction();
                    });
                }
                break;
            case 'q-tree':
                var tree = comp_dict[this.$props.jp_props.id];
                // Add attribute expand_at_start
                if (true) {
                    this.$nextTick(() => {
                        setTimeout(function () {
                            tree.expandAll();
                        }, 200);
                    });
                }
                break;
            case 'q-scroll-area':
                if (this.$props.jp_props.offset) {
                    this.$nextTick(() => {
                        if (this.$props.jp_props.duration)
                            this.$refs['r' + this.$props.jp_props.id].setScrollPosition(this.$props.jp_props.offset, this.$props.jp_props.duration);
                        else
                            this.$refs['r' + this.$props.jp_props.id].setScrollPosition(this.$props.jp_props.offset);
                    });
                }
                break;
        }


        if (this.$props.jp_props.input_type && (this.$props.jp_props.input_type != 'file')) {
            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;
        }

        if (this.$props.jp_props.set_focus) {
            this.$nextTick(() => this.$refs['r' + this.$props.jp_props.id].focus())
        }
    },
    updated() {
        if (this.$props.jp_props.animation) this.animateFunction();

        switch (this.$props.jp_props.html_tag) {

            case 'q-slide-item':
                if (this.$props.jp_props.reset) {
                    storage_dict['r' + this.$props.jp_props.id].reset();
                }
                break;
            case 'q-infinite-scroll':
                if (this.$props.jp_props.done) {
                    storage_dict['r' + this.$props.jp_props.id]();
                }
                break;
            case 'q-notify':
                if (this.$props.jp_props.notify) {
                    this.$nextTick(() => {
                        this.notifyFunction();
                    });
                }
                break;
            case 'q-scroll-area':
                if (this.$props.jp_props.offset) {
                    this.$nextTick(() => {
                        if (this.$props.jp_props.duration)
                            this.$refs['r' + this.$props.jp_props.id].setScrollPosition(this.$props.jp_props.offset, this.$props.jp_props.duration);
                        else
                            this.$refs['r' + this.$props.jp_props.id].setScrollPosition(this.$props.jp_props.offset);
                    });
                }
                break;
        }


        if (this.$props.jp_props.input_type && (this.$props.jp_props.input_type != 'file')) {

            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;    //make sure that the input value is the correct one received from server

            if (this.$props.jp_props.input_type == 'radio') {
                if (this.$props.jp_props.checked) {
                    this.$refs['r' + this.$props.jp_props.id].checked = true;  // This un-checks other radio buttons in group also
                } else {
                    this.$refs['r' + this.$props.jp_props.id].checked = false;
                }
            }

            if (this.$props.jp_props.input_type == 'checkbox') {
                this.$refs['r' + this.$props.jp_props.id].checked = this.$props.jp_props.checked;
            }
        }

        if (this.$props.jp_props.set_focus) {
            this.$nextTick(() => this.$refs['r' + this.$props.jp_props.id].focus())
        }
    },
    props: {
        jp_props: Object,

    }
});

// {% endraw %}