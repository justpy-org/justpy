/***
 * justpy core java script
 */
 
 /**
  * Legacy global variables
  */
 var comp_dict = {};  // Hold components for running methods
 var websocket_id = '';
 var websocket_ready = false;
 var web_socket_closed = false;
 
 // the global app object
 var app1=null; // will be initialized with a Vue component in justpy_core.setup()
 var msg=null; // declare msg - beware aggrid also does this!
 var socket=null;
    
 // @TODO make configurable and put into object oriented part
 let reload_timeout = 2000;
 let reload_started = false;

 /**
  * Non object oriented legacy functions
  */
    function try_reload_site() {
        fetch(window.location)
        .then(function(response) {
            console.log('Site Available, reloading');
            window.location.reload();
        })
        .catch(function(error) {
            console.log('Site Unavailable (', error.message, '), retrying in ', reload_timeout, 'ms');
            setTimeout(try_reload_site, reload_timeout);
            if (reload_timeout < 60000)
                reload_timeout += 1000;
        });
    }

    function reload_site() {
        if (!reload_started) {
            console.log("Reloading site...");
            reload_started = true;
            setTimeout(try_reload_site, reload_timeout);
        }
    }
    
    var crosshairs = [];
 
	function draw_crosshair(chart, series, point) {

        var
            r = chart.renderer,
            left = chart.plotLeft,
            top = chart.plotTop,
            width = chart.plotWidth,
            height = chart.plotHeight,
            x = point.plotX,
            y = point.plotY;

        var crosshair = r.path(['M', left, top + y, 'L', left + width, top + y, 'M', left + x, top, 'L', left + x, top + height])
            .attr({
                'stroke-width': 1,
                stroke: '#D3D3D3'
            })
            .add();
        crosshairs.push(crosshair);
    }

    function comp_replace(comp, comp_list) {
        var m_id = comp['id'];
        for (let i = 0; i < comp_list.length; i++) {
            if (comp_list[i]['id'] == m_id) {
                var spliced = comp_list.splice(i, 1, comp);
            } else {
                if (comp_list[i]['object_props']) {
                    comp_replace(comp, comp_list[i]['object_props']);
                }
            }
        }
    }
    
/***
 * Object Oriented Core
 */
class JustpyCore {
 
  // create a JustpyCore instance
  constructor(window,page_id,title,use_websockets,redirect,display_url,page_ready,result_ready,reload_interval_ms,debug) {
	this.window=window;
	this.page_id=page_id;
    this.setTitle(title);
    this.use_websockets=use_websockets;
    if (redirect) {
		location.href = redirect; 
	}
	if (display_url) {
		window.history.pushState("", "", display_url);
	}
    this.page_ready=page_ready;
    this.result_ready=result_ready;
    this.reload_interval_ms=reload_interval_ms;
    this.debug=debug;
  }
  
  // set the title
  setTitle(title) {
	document.title=title;
	this.title=title;
	// pass
  }
  
  // setup the core functionality
  setup() {
	if (this.use_websockets) {	
		this.setupWebSocket();
	} else {
		this.setupNoWebSocket();
	}
	this.createApp1();
  }
  
  // create the global app1 Vue object
  createApp1() {
	  app1 = new Vue({
        el: '#components',
        data: {
            justpyComponents: justpyComponents
        },
        render: function (h) {
            var comps = [];
            for (var i = 0; i < this.justpyComponents.length; i++) {
                if (this.justpyComponents[i].show) {
                    comps.push(h(this.justpyComponents[i].vue_type, {
                        props: {
                            jp_props: this.justpyComponents[i]
                        }
                    }))
                }
            }
            return h('div', {}, comps);
        }
    });
  }
  
  // prepare WebSocket handling
  setupWebSocket() {
    console.log(location.protocol + ' Domain: ' + document.domain);
    if (location.protocol === 'https:') {
        var protocol_string = 'wss://'
    } else {
        protocol_string = 'ws://'
    }
    var ws_url = protocol_string + document.domain;
    if (location.port) {
        ws_url += ':' + location.port;
    }
    socket = new WebSocket(ws_url);

    socket.addEventListener('open', function (event) {
        console.log('Websocket opened');
        socket.send(JSON.stringify({'type': 'connect', 'page_id': page_id}));
    });

    socket.addEventListener('error', function (event) {
        reload_site();
    });

    socket.addEventListener('close', function (event) {
        console.log('Websocket closed');
        web_socket_closed = true;
        reload_site()
    });

    socket.addEventListener('message', function (event) {
        msg = JSON.parse(event.data);
        if (justpy_core.debug) {
            console.log('Message received from server ', msg);
            console.log(event);
        }
        let e = {};
        switch (msg.type) {
            case 'page_update':
                if (msg.page_options.redirect) {
                    location.href = msg.page_options.redirect;
                    break;
                }
                if (msg.page_options.open) {
                    window.open(msg.page_options.open, '_blank');
                }
                if (msg.page_options.display_url !== null)
                    window.history.pushState("", "", msg.page_options.display_url);
                document.title = msg.page_options.title;
                if (msg.page_options.favicon) {
                    var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
                    link.type = 'image/x-icon';
                    link.rel = 'shortcut icon';
                    if (msg.page_options.favicon.startsWith('http')) {
                        link.href = msg.page_options.favicon;
                    } else {
                        link.href = '{{ url_for(options.static_name, path='/') }}' + msg.page_options.favicon;
                    }
                    document.getElementsByTagName('head')[0].appendChild(link);
                }

                app1.justpyComponents = msg.data;

                break;
            case 'page_mode_update':
                Quasar.Dark.set(msg.dark);
                break;
            case 'websocket_update':
                websocket_id = msg.data;
                websocket_ready = true;
                if (justpy_core.page_ready) {     
                    e = {
                        'event_type': 'page_ready',
                        'visibility': document.visibilityState,
                        'page_id': page_id,
                        'websocket_id': websocket_id
                    };
                    send_to_server(e, 'page_event', false);
                }    
                break;
            case 'component_update':
                // update just specific component on the page
                comp_replace(msg.data, app1.justpyComponents);
                break;
            case 'run_javascript':
                // let js_result = eval(msg.data);
                let js_result;

            function eval_success() {
                e = {
                    'event_type': 'result_ready',
                    'visibility': document.visibilityState,
                    'page_id': page_id,
                    'websocket_id': websocket_id,
                    'request_id': msg.request_id,
                    'result': js_result //JSON.stringify(js_result)
                };
                if (justpy_core.result_ready) {   
                    if (msg.send) send_to_server(e, 'page_event', false);
                }
            }

                const jsPromise = (new Promise(function () {
                    js_result = eval(msg.data);
                })).then(eval_success());

                break;
            case 'run_method':
                // await websocket.send_json({'type': 'run_method', 'data': command, 'id': self.id})
                eval('comp_dict[' + msg.id + '].' + msg.data);
                break;
            case 'draw_crosshair':
                // Remove previous crosshairs
                for (let i = 0; i < crosshairs.length; i++) {
                    crosshairs[i].destroy();
                }
                crosshairs = [];
                for (let i = 0; i < msg.data.length; i++) {
                    const m = msg.data[i];
                    const chart_index = document.getElementById(m.id.toString()).getAttribute('data-highcharts-chart');
                    const chart = Highcharts.charts[chart_index];
                    const point = chart.series[m.series].data[m.point];
                    draw_crosshair(chart, chart.series[m.series], point);
                }
                break;
            case 'select_point':
                for (let i = 0; i < msg.data.length; i++) {
                    const m = msg.data[i];
                    const chart_index = document.getElementById(m.id.toString()).getAttribute('data-highcharts-chart');
                    const chart = Highcharts.charts[chart_index];
                    chart.series[m.series].data[m.point].select();
                }
                break;
            case 'chart_update':
                const chart = cached_graph_def['chart' + msg.id];
                chart.update(msg.data);
                break;
            case 'tooltip_update':
                // https://github.com/highcharts/highcharts/issues/6824
                var chart_on = cached_graph_def['chart' + msg.id];

                if (chart_on.options.tooltip.split) {
                    chart_on.tooltip.tt.attr({
                        text: msg.data[0]
                    });

                    var j = 1;
                    for (let i = 0; i < chart_on.tooltip.chart.series.length; i++) {
                        if (chart_on.tooltip.chart.series[i].visible &&
                            (chart_on.tooltip.chart.series[i].tt != null)) {
                            chart_on.tooltip.chart.series[i].tt.attr({
                                text: msg.data[j++]
                            });

                        }
                    }

                } else {
                    chart_on.tooltip.label.attr({
                        text: msg.data
                    });
                }
                break;
            default: {

            }
        }
    });
  }
  
  setupNoWebSocket() {
     window.addEventListener('beforeunload', function (event) {
        e = {
            'event_type': 'beforeunload',
            'page_id': page_id,
        };
        send_to_server(e);
    });
  }
  
  // setup the reload interval
  setupReloadInterval() {
	if (this.reload_interval_ms >0) {
        setInterval(function () {
            $.ajax({
                type: "POST",
                url: "/zzz_justpy_ajax",
                data: JSON.stringify({
                    'type': 'event',
                    'event_data': {'event_type': 'page_update', 'page_id': this.page_id}
                }),
                success: function (msg) {
                    if (msg) app1.justpyComponents = msg.data;
                },
                dataType: 'json'
            });
        }, this.reload_interval_ms);
    }    
  }
}