//{% raw %}


var cached_graph_def = {};
Vue.component('chart', {

    template:
        `<div v-bind:id="jp_props.container" :class="jp_props.classes"  :style="jp_props.style" >
    </div>`,
    methods: {

        graph_change() {

            cached_graph_def[this.$props.jp_props.container] = JSON.stringify(this.$props.jp_props.def);
            if (this.$props.jp_props.stock) {
                var c = Highcharts.stockChart(this.$props.jp_props.container.toString(), this.$props.jp_props.def);
            } else {
                var c = Highcharts.chart(this.$props.jp_props.container.toString(), this.$props.jp_props.def);
            }
            var id = this.$props.jp_props.id;
            var rid = this.$props.jp_props.running_id;
            //var container = this.$props.jp_props.container.toString();
            var container = this.$props.jp_props.id.toString();
            // var graph_id = parseInt(container.replace('chart', ''));
            cached_graph_def['chart'+container] = c;
            if (!this.$props.jp_props.stock)
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
                                'running_id': rid,
                                'series_name': this.series.name,
                                'series_id': this.series.options.id,
                                'page_id': page_id
                            }; //'running_id': this.$props.basic_card_props.running_id};
                            if (use_websockets){
                                // setTimeout(function(){ socket.send(JSON.stringify({'type': 'event'  ,'event_data': e})); }, 2);
                                socket.send(JSON.stringify({'type': 'event'  ,'event_data': e}));
                            }

                            return '<span style="color:' + this.point.color + '">\u25CF</span>' + this.series.name + ': <b>' + this.point.y + '</b><br/>';

                        },
                    }, plotOptions: {
                        series: {
                            cursor: 'pointer',
                            point: {
                                events: {
                                    click: function (e) {
                                        var p = {
                                            x: e.point.x,
                                            y: e.point.y,
                                            z: e.point.z,
                                            running_id: rid,
                                            type: e.type,
                                            name: e.point.series.name,
                                            page_id: page_id
                                        };
                                        console.log(p);
                                        console.log(e);
                                        socket.emit('events', p);
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
        if (JSON.stringify(this.$props.jp_props.def) == cached_graph_def[this.$props.jp_props.container]) {
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
