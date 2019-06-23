//{% raw %}


var cached_graph_def = {};
var tooltip_timeout = null;
var tooltip_timeout_flag  = true;
var tooltip_counter  = 0;
var tooltip_timeout_period  = 100;
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
            cached_graph_def['chart'+container] = c;
            var update_dict = {};
            if (this.$props.jp_props.events.indexOf('tooltip') >= 0) {
                var point_array = [];
                update_dict.tooltip = {
                        useHTML: true,
                        formatter: function (tooltip) {

                            var point = this.point;
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
                                'series_name': this.series.name,
                                'series_id': this.series.options.id,
                                'page_id': page_id,
                                'websocket_id': websocket_id
                            };
                            }
                            else {
                                // Tooltip shared or split
                                for (var i=0; i<this.points.length; i++) {
                                    // console.log('shared point');
                                    // console.log(this.points[i]);
                                    var point = {};
                                    point.x = this.points[i].x;
                                    point.y = this.points[i].y;
                                    point.z = this.points[i].z;
                                    point.color = this.points[i].color;
                                    point.percentage = this.points[i].percentage;
                                    point.total = this.points[i].total;
                                    point.series_name = this.points[i].series.name;
                                    point_array.push(point);
                                }
                                var e = {
                                    'event_type': 'tooltip',
                                    'x': this.x,
                                    id: id,
                                    form_data: false,
                                    'points': point_array,
                                    'page_id': page_id,
                                    'websocket_id': websocket_id
                                };
                            }

                            if (use_websockets){


                                // tooltip_timeout = setTimeout(() => socket.send(JSON.stringify({'type': 'event'  ,'event_data': e})), 100);
                                clearTimeout(tooltip_timeout);
                                     tooltip_timeout = setTimeout(function()
                                {
                                    socket.send(JSON.stringify({'type': 'event'  ,'event_data': e}));
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
                            }
                            else return 'Loading...';
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
                                        // This handles click on point. Need to improve. Don't propogate. Only if activated
                                        var p = {
                                            'event_type': 'point_click',
                                            id: id,
                                            form_data: false,
                                            x: e.point.x,
                                            y: e.point.y,
                                            z: e.point.z,
                                            //running_id: rid,
                                            type: e.type,
                                            series_name: e.point.series.name,
                                            page_id: page_id
                                        };
                                        console.log(p);
                                        console.log(e);
                                         if (use_websockets){
                                socket.send(JSON.stringify({'type': 'event'  ,'event_data': p}));
                            }
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
