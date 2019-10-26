// {% raw %}
var storage_dict = {}

Vue.component('quasar_component', {

    render: function (h) {
        // console.log(this.jp_props);
        if (this.jp_props.hasOwnProperty('text')) {
            var comps = [this.jp_props.text];
        } else comps = [];

        // console.log(this.jp_props);
        for (var i = 0; i < this.jp_props.object_props.length; i++) {
            //if (this.jp_props.show) {   // (this.jp_props.show)
            if (this.jp_props.object_props[i].show) {   // (this.jp_props.show)
                comps.push(h(this.jp_props.object_props[i].vue_type, {
                    props: {
                        jp_props: this.jp_props.object_props[i]
                    }
                }))
            }
        }

        description_object = {
            // class: this.jp_props.classes,
            style: this.jp_props.style,
            attrs: this.jp_props.attrs,
            domProps: {
                // innerHTML: this.jp_props.inner_html
            },
            on: {
                // click: this.eventFunction,
                // mouseenter: this.eventFunction,
                // mouseleave: this.eventFunction,
                // input: this.eventFunction,
                // change: this.eventFunction,
                // keyup: this.eventFunction
            },
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

               case 'input': fn = this.inputEvent; break;
               case 'change': fn = this.changeEvent; break;
               case 'submit': fn = this.submitEvent; break;
               // For QTree
               case 'update:expanded': fn = this.treeExpandedEvent; break;
               case 'update:selected': fn = this.treeSelectedEvent; break;  // Also for QTable and QChip
               case 'update:ticked': fn = this.treeTickedEvent; break;
               // For QSlideItem
               case 'left': fn = this.leftEvent; break;
               case 'right': fn = this.rightEvent; break;
               case 'action': fn = this.actionEvent; break;
               case 'load': fn = this.loadEvent; break;
               // For Qtable
               case 'update:pagination': fn = this.tablePaginationEvent; break;
               case 'request': fn = this.tableRequestEvent; break;
               case 'selection': fn = this.tableSelectionEvent; break;
               case 'remove': fn = this.removeEvent; break;
               // For QScrollObserver
               case 'scroll': fn = this.scrollEvent; break;

               default: fn = this.defaultEvent;
           }

            // event_description[this.jp_props.events[i]] = this.eventFunction;
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
            //if (true || 'vue_type' in b[slot_name])
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
            // console.log('Event for ' + this.$props.jp_props.html_tag);
            //             console.log(typeof event );
            //             if (event == null) event = '';
                        // if (typeof event === 'string' || typeof event === 'boolean') {
                        new_event = {};
                        // new_event.type = 'input';
                        new_event.type = event_type;
                        new_event.target = {};
                        new_event.currentTarget = {};
                        new_event.target.value = event;
                        if (aux) new_event.aux = aux;
                        this.$props.jp_props.input_type = 'text';
                        eventHandler(this.$props, new_event, false, aux);
                        // } // else event.stopPropagation();
        }),
        defaultEvent: (function (event) {
            console.log('%%%%%% In Default event');
            console.log(event);
            // if (event == null) event = '';
            this.eventFunction(event, event.type);
        }),
        inputEvent: (function (event) {
            console.log('%%%%%% In Input event');
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
            console.log('%%%%%% In change event');
            this.eventFunction(event, 'change');
        }),
        scrollEvent: (function (event) {
            console.log('%%%%%% In scroll event');
            console.log(event);
            this.eventFunction(event, 'scroll');
        }),
        treeExpandedEvent: (function (event) {
            console.log('%%%%%% In Tree Expanded event');
            this.eventFunction(event, 'update:expanded');
        }),
        treeSelectedEvent: (function (event) {
            console.log('%%%%%% In Tree or Table or Qchip Selected event');
            this.eventFunction(event, 'update:selected');
        }),
        treeTickedEvent: (function (event) {
            console.log('%%%%%% In Tree Ticked event');
            this.eventFunction(event, 'update:ticked');
        }),
         tablePaginationEvent: (function (event) {
            console.log('%%%%%% In Table Pagination event');
            this.eventFunction(event, 'update:pagination');
        }),
        tableRequestEvent: (function (event) {
            console.log('%%%%%% In Table Request event');
            this.eventFunction(event, 'request');
        }),
        tableSelectionEvent: (function (event) {
            console.log('%%%%%% In Table selection event');
            this.eventFunction(event, 'selection');
        }),
        removeEvent: (function (event) {
            console.log('%%%%%% In chip remove event');
            this.eventFunction(event, 'remove');
        }),
        leftEvent: (function (event) {
            console.log('%%%%%% In slidetime left event');
            console.log(event);  //{reset: f, side: 'right'}
            storage_dict['r' + this.$props.jp_props.id] = event;
            console.log(storage_dict);
            this.eventFunction(true, 'left');
        }),
        rightEvent: (function (event) {
            console.log('%%%%%% In slidetime right event');
            console.log(event);  //{reset: f, side: 'right'}
            storage_dict['r' + this.$props.jp_props.id] = event;
            console.log(storage_dict);
            this.eventFunction(true, 'right');
        }),
        actionEvent: (function (event) {
            console.log('%%%%%% In slidetime action event');
            console.log(event);  //{reset: f, side: 'right'}
            storage_dict['r' + this.$props.jp_props.id] = event;
            console.log(storage_dict);
            this.eventFunction(event.side, 'action');
        }),
        loadEvent: (function (index, done) {
            console.log('%%%%%% In infinite scroll load event');
            console.log(index, done);  //{reset: f, side: 'right'}
            // if (this.$props.jp_props.initial) {done(); return;}
            storage_dict['r' + this.$props.jp_props.id] = done;
            console.log(storage_dict);
            this.eventFunction(index, 'load');
        }),
        submitEvent: (function (event) {
            console.log('%%%%%% In submit event');
            // if (event == null) event = '';
            // if (event.type == 'submit') {
            if (event.hasOwnProperty('type')) {
                var form_reference = this.$el;
                var props = this.$props;
                event.preventDefault();    //stop form from submitting
                console.log('In submit ' + ' id ' + form_reference.id);
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

                // console.log(event);
                console.log(form_elements_list);
                // var form_data = {'form_data': form_elements_list};
                eventHandler(props, event, form_elements_list);
            }
            // this.eventFunction(event, 'change');
        }),

        eventFunction: (function (event, event_type, aux) {
            console.log('In component eventFunction. ');
            console.log(event);
            console.log(aux);
            console.log(this.$props.jp_props);
            console.log('Tag: ' + this.$props.jp_props.html_tag);
            console.log('Event type: ' + event_type);
            // if (typeof event === 'object') event_type = event.type;
            // console.log(event); console.log(event_type);
            if (!this.$props.jp_props.event_propagation) {
                event.stopPropagation();
            }

            if (event != null && event.hasOwnProperty('type')) {
                eventHandler(this.$props, event, false);
            } else {
                this.createEvent(event, event_type, aux);
            }
        }),
        animateFunction: (function () {
            var animation = this.$props.jp_props.animation;
            var element = this.$el;
                element.classList.add('animated', animation);
            element.addEventListener('animationend', function() { element.classList.remove('animated', animation); });

        }),
        notifyFunction: (function () {
            console.log('In Notify');
            console.log(this.jp_props.attrs.notify);
            console.log(this.jp_props);
            app1.$q.notify({
                message: this.jp_props.attrs.message,
                position: this.jp_props.attrs.position,
                icon: this.jp_props.attrs.icon,
                color: this.jp_props.attrs.color,
                textColor: this.jp_props.attrs.textColor,
                timeout: this.jp_props.attrs.timeout,
                avatar: this.jp_props.attrs.avatar,
                closeBtn: this.jp_props.attrs.closeBtn,
                html: this.jp_props.attrs.html
            });
        })
        ,
        mountedFunction: (function (event) {

        })
    },
    mounted() {
        if (this.$props.jp_props.animation) this.animateFunction();

        switch (this.$props.jp_props.html_tag) {

            case 'q-notify':
                console.log('in mounted notify -----------');
                console.log(this.$props.jp_props.notify);
                if (this.$props.jp_props.notify) {
                    this.$nextTick(() => {
                        this.notifyFunction();
                    });

                    // this.notifyFunction();
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


        if (this.$props.jp_props.input_type) {
            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;
        }

        //storage_dict['r' + this.$props.jp_props.id] = event;

    },
    updated() {
        //console.log('in updated'); console.log(this.$props.jp_props);console.log(this.$props.jp_props.slide_down);
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
                console.log('in updated notify -----------');
                console.log(this.$props.jp_props.notify);
                if (this.$props.jp_props.notify) {
                    this.$nextTick(() => {
                        this.notifyFunction();
                    });

                    // this.notifyFunction();
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


        if (this.$props.jp_props.input_type) {    //this.$props.jp_props.input_type

            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;    //make sure that the input value is the correct one received from server

            if (this.$props.jp_props.input_type == 'radio') {
                // console.log('in radio update'); console.log(this.$props.jp_props);
                if (this.$props.jp_props.checked) {
                    // if (!this.$refs['r' + this.$props.jp_props.id].checked) this.$refs['r' + this.$props.jp_props.id].focus();
                    this.$refs['r' + this.$props.jp_props.id].checked = true;  // This unchecks other radio buttons in group also
                } else {
                    this.$refs['r' + this.$props.jp_props.id].checked = false;
                }
            }


            if (this.$props.jp_props.input_type == 'checkbox') {
                this.$refs['r' + this.$props.jp_props.id].checked = this.$props.jp_props.checked;
            }
        }

        if (this.$props.jp_props.slide_down) {   // Use the jquery slide up and slide down if required
            $('#' + this.$props.jp_props.id).slideDown();
        }

        if (this.$props.jp_props.slide_up) {
            $('#' + this.$props.jp_props.id).slideUp();
        }
    },
    props: {
        jp_props: Object,

    }
});

// {% endraw %}