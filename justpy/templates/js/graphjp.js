//{% raw %}


var cached_graph_def = {};
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
            console.log('events');
            console.log(this.$props.jp_props.events);
            if (this.$props.jp_props.events.indexOf('tooltip') >= 0) {
                console.log('in updating tooltip');
                update_dict.tooltip = {
                        useHTML: true,
                        formatter: function () {
                            console.log('formatter: ');
                            console.log(this.point);
                            console.log(this.series);
                            var point = this.point;
                            var e = {
                                'event_type': 'tooltip',
                                id: id,
                                form_data: false,
                                'x': this.x,
                                'y': this.y,
                                'z': this.z,
                                color: this.point.color,
                                //'running_id': rid,
                                'series_name': this.series.name,
                                'series_id': this.series.options.id,
                                'page_id': page_id,
                                'websocket_id': websocket_id
                            };
                            if (use_websockets){
                                // setTimeout(function(){ socket.send(JSON.stringify({'type': 'event'  ,'event_data': e})); }, 2);
                                socket.send(JSON.stringify({'type': 'event'  ,'event_data': e}));
                            }

                            return '<span style="color:' + this.point.color + '">\u25CF</span>' + this.series.name + ': <b>' + this.point.y + '</b><br/>';

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
                                // setTimeout(function(){ socket.send(JSON.stringify({'type': 'event'  ,'event_data': e})); }, 2);
                                socket.send(JSON.stringify({'type': 'event'  ,'event_data': p}));
                            }
                                    }
                                }
                            }
                        }
                    }
            }
            console.log(update_dict);
            c.update(update_dict);
            if (false)
                c.update({
                    tooltip: {
                        useHTML: true,
                        formatter: function () {
                            //return '5';
                            //return '<span style="color:'+this.point.color+'">\u25CF</span>'+this.series.name+': <b>'+this.point.y+'</b><br/>';
                            console.log('formatter:');

                            console.log(this.point);
                            console.log(this.series);
                            var point = this.point;


                            var e = {
                                'event_type': 'tooltip',
                                id: id,
                                form_data: false,
                                'x': this.x,
                                'y': this.y,
                                'z': this.z,
                                color: this.point.color,
                                //'running_id': rid,
                                'series_name': this.series.name,
                                'series_id': this.series.options.id,
                                'page_id': page_id,
                                'websocket_id': websocket_id
                            };
                            if (use_websockets){
                                // setTimeout(function(){ socket.send(JSON.stringify({'type': 'event'  ,'event_data': e})); }, 2);
                                socket.send(JSON.stringify({'type': 'event'  ,'event_data': e}));
                            }

                            return '<span style="color:' + this.point.color + '">\u25CF</span>' + this.series.name + ': <b>' + this.point.y + '</b><br/>';

                        },
                    },
                    plotOptions: {
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
                                // setTimeout(function(){ socket.send(JSON.stringify({'type': 'event'  ,'event_data': e})); }, 2);
                                socket.send(JSON.stringify({'type': 'event'  ,'event_data': p}));
                            }
                                    }
                                }
                            }
                        }
                    }
                });

        }
    },
    mounted() {
        console.log('mounted chart');
        console.log(this.$props);
        this.graph_change();
    },
    updated() {
        console.log('updated');
        if (JSON.stringify(this.$props.jp_props.def) == cached_graph_def[this.$props.jp_props.id]) {
            console.log('Not updated because cache');
            return;
        }
        //var chart_old = $("#" + this.$props.jp_props.container).highcharts();
        //chart_old.destroy();
        console.log('updating...');
        this.graph_change();


    },
    props: {
        jp_props: Object
    }
});

//   {% endraw %}
