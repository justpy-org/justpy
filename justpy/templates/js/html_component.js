// {% raw %}


Vue.component('html_component', {

    render: function (h) {
        if (this.jp_props.hasOwnProperty('text')) {
            var comps = [this.jp_props.text];
        } else comps = [];
        //console.log(this.jp_props);
        for (var i = 0; i < this.jp_props.object_props.length; i++) {

            if (this.jp_props.show) {   // (this.jp_props.show)
                comps.push(h(this.jp_props.object_props[i].vue_type, {
                    props: {
                        jp_props: this.jp_props.object_props[i]
                    }
                }))
            }
        }

        description_object  = {
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
            directives: [
                {
                    name: 'tooltip',    // https://www.npmjs.com/package/v-tooltip
                    content: 'hello there',
                    //value: (this.jp_props.tooltip ? {content: this.jp_props.tooltip} : null),
                    value: (function (o) {
                        if (o.jp_props.tooltip) {
                            return {content: o.jp_props.tooltip}
                        } else {
                            return null
                        }
                    })(this),
                    placement: 'auto'

                }
            ],
            slot: this.jp_props.slot,
            ref: 'r' + this.jp_props.id
        };

        if (this.jp_props.classes) {
            description_object['class'] = this.jp_props.classes;
        }

        event_description = {};
        for (i = 0; i < this.jp_props.events.length; i++) {
            event_description[this.jp_props.events[i]] = this.eventFunction
        }
        description_object['on'] = event_description;


        if (this.jp_props.inner_html) {
            description_object['domProps'] = {innerHTML: this.jp_props.inner_html};
        }

        return h(this.jp_props.html_tag, description_object, comps);

    },
    methods: {

        eventFunction: (function (event) {
            // console.log('In component eventFunction');
            // console.log(event);
            if (!this.$props.jp_props.event_propagation) {
                event.stopPropagation();
            }
            if (event.type=='submit') {
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
                    for (var j=0; j<attributes.length; j++) {
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
            else {
                eventHandler(this.$props, event, false);
            }
        }),
        mountedFunction: (function (event) {

        })
    },
    mounted() {

        if (this.$props.jp_props.input_type) {    //this.$props.jp_props.input_type
            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;
        }

    },
    updated() {
        //console.log('in updated'); console.log(this.$props.jp_props);console.log(this.$props.jp_props.slide_down);
        if (this.$props.jp_props.input_type) {    //this.$props.jp_props.input_type

            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;    //make sure that the input value is the correct one received from server

            if (this.$props.jp_props.input_type=='radio') {
                if (this.$props.jp_props.checked) {
                  // if (!this.$refs['r' + this.$props.jp_props.id].checked) this.$refs['r' + this.$props.jp_props.id].focus();
                  this.$refs['r' + this.$props.jp_props.id].checked = true;  // This unchecks other radio buttons in group also
                }
                else {
                    this.$refs['r' + this.$props.jp_props.id].checked = false;
                }
            }


             if (this.$props.jp_props.input_type=='checkbox') {
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