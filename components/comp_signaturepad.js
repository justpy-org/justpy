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