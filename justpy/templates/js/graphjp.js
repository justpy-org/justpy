//{% raw %}


var cached_graph_def = {};
var tooltip_timeout = null;
var tooltip_timeout_period = 100;
Vue.component('chart', {

    template:
        `<div v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style" >
    </div>`,
    methods: {

        graph_change() {

            cached_graph_def[this.$props.jp_props.id] = JSON.stringify(this.$props.jp_props.def);
            var container = this.$props.jp_props.id.toString();
            if (this.$props.jp_props.stock) {
                var c = Highcharts.stockChart(container, this.$props.jp_props.def);
            } else {
                var c = Highcharts.chart(container, this.$props.jp_props.def);
            }
            var id = this.$props.jp_props.id;
            //var rid = this.$props.jp_props.running_id;
            cached_graph_def['chart' + container] = c;
            var update_dict = {};
            if (this.$props.jp_props.events.indexOf('tooltip') >= 0) {
                var point_array = [];
                update_dict.tooltip = {
                    useHTML: true,
                    shape: 'callout',
                    positioner: function (boxWidth, boxHeight, point) {
                        return {
                            x: point.plotX + 0,
                            y: point.plotY - 2 * boxHeight
                        };
                    },
                    formatter: function (tooltip) {
                        if (this.point != null) {
                            // Tootltip not shared or split
                            var e = {
                                'event_type': 'tooltip',
                                id: id,
                                form_data: false,
                                'x': this.point.x,
                                'y': this.point.y,
                                'z': this.point.z,
                                'color': this.point.color,
                                'percentage': this.point.percentage,
                                'total': this.point.total,
                                'point_index': this.point.index,
                                'series_name': this.series.name,
                                'series_index': this.series.index,
                                'page_id': page_id,
                                'websocket_id': websocket_id
                            };
                        } else {
                            // Tooltip shared or split
                            for (let i = 0; i < this.points.length; i++) {
                                let point = {};
                                point.x = this.points[i].x;
                                point.y = this.points[i].y;
                                point.z = this.points[i].z;
                                point.color = this.points[i].color;
                                point.percentage = this.points[i].percentage;
                                point.total = this.points[i].total;
                                point.point_index = this.points[i].index;
                                point.series_name = this.points[i].series.name;
                                point.series_index = this.points[i].series.index;
                                point_array.push(point);
                            }
                            var e = {
                                event_type: 'tooltip',
                                x: this.x,
                                id: id,
                                form_data: false,
                                points: point_array,
                                page_id: page_id,
                                websocket_id: websocket_id
                            };
                        }

                        if (use_websockets) {
                            // Wait 100ms before sending tooltip information to server.
                            // This allows new tooltip event delete old one if it arrives less than 100ms
                            // after the previous one.
                            clearTimeout(tooltip_timeout);
                            tooltip_timeout = setTimeout(function () {
                                    //socket.send(JSON.stringify({'type': 'event', 'event_data': e}));
                                    send_to_server(e);
                                }
                                , tooltip_timeout_period);
                        }
                        point_array = [];
                        if (tooltip.split) {
                            var return_array = [];
                            for (var i = 0; i < tooltip.chart.series.length + 1; i++) {
                                return_array.push('Loading...');
                            }
                            return return_array;
                        } else return 'Loading...';
                    },
                }
            }

            if (this.$props.jp_props.events.indexOf('point_click') >= 0) {
                update_dict.plotOptions = {
                    series: {
                        cursor: 'pointer',
                        point: {
                            events: {
                                click: function (e) {
                                    // May need to add additional fields to p
                                    console.log(e);
                                    var p = {
                                        event_type: 'point_click',
                                        id: id,
                                        form_data: false,
                                        x: e.point.x,
                                        y: e.point.y,
                                        z: e.point.z,
                                        color: e.point.color,
                                        percentage: e.point.percentage,
                                        total: e.point.total,
                                        point_index: e.point.index,
                                        type: e.type,
                                        series_name: e.point.series.name,
                                        series_index: e.point.series.index,
                                        page_id: page_id,
                                        websocket_id: websocket_id
                                    };
                                    console.log(p);
                                    console.log(e);
                                    send_to_server(p);
                                }
                            }
                        }
                    }
                }
            }
            // console.log(update_dict);
            c.update(update_dict);


        }
    },
    mounted() {
        this.graph_change();
    },
    updated() {
        if (JSON.stringify(this.$props.jp_props.def) == cached_graph_def[this.$props.jp_props.id]) {
            console.log('Not updated because cache');
            return;
        }
        // console.log('updating graph');
        this.graph_change();


    },
    props: {
        jp_props: Object
    }
});

//   {% endraw %}

