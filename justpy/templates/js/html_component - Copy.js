// {% raw %}


Vue.component('html_component', {

    render: function (h) {
        if (this.jp_props.hasOwnProperty('text')) {
            var comps = [this.jp_props.text];
        } else var comps = [];
        //console.log(this.jp_props);
        for (var i = 0; i < this.jp_props.object_props.length; i++) {

            if (this.jp_props.show) {   // (this.jp_props.show)
                comps.push(h(this.jp_props.object_props[i].type, {
                    props: {
                        jp_props: this.jp_props.object_props[i]
                    }
                }))
            }
        }

        //console.log(this.groupedCharts);
        return h(this.jp_props.html_tag, {
            class: this.jp_props.classes,
            style: this.jp_props.style,
            attrs: this.jp_props.attrs,
            domProps: {
                // innerHTML: this.jp_props.inner_html
            },
            on: {
                click: this.eventFunction,
                mouseenter: this.eventFunction,
                mouseleave: this.eventFunction,
                input: this.eventFunction,
                change: this.eventFunction,
                keyup: this.eventFunction
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
        }, comps);


    },
    methods: {

        eventFunction: (function (event) {
            console.log('raw');
            console.log(event);
            if (!this.$props.jp_props.event_propagation) {
                event.stopPropagation();
            }

            eventHandler(this.$props, event);
        }),
        mountedFunction: (function (event) {
            //eventHandler(this.$props, event);
        })
    },
    mounted() {


        //console.log('buttongroup mounted');
        //console.log(this.$props.jp_props);
    },
    updated() {
        //console.log('in updated'); console.log(this.$props.jp_props);console.log(this.$props.jp_props.slide_down);
        if (this.$props.jp_props.input_type) {    //this.$props.jp_props.input_type

            this.$refs['r' + this.$props.jp_props.id].value = this.$props.jp_props.value;    //make sure that the input value is the correct one received from server
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