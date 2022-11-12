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
var app1 = null; // will be initialized with a Vue component in justpy_core.setup()
var msg = null; // declare msg - beware aggrid also does this!
var socket = null;

// @TODO make configurable and put into object oriented part
let reload_timeout = 2000;
let reload_started = false;


/**
 * Non-object-oriented legacy functions
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

/**
 * reload side
 */
function reload_site() {
	if (!reload_started) {
		console.log("Reloading site...");
		reload_started = true;
		setTimeout(try_reload_site, reload_timeout);
	}
}

var crosshairs = [];

/**
 *
 * @param chart
 * @param series
 * @param point
 */
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
			let spliced = comp_list.splice(i, 1, comp);
		} else {
			if (comp_list[i]['object_props']) {
				comp_replace(comp, comp_list[i]['object_props']);
			}
		}
	}
}

/***
 * Object-Oriented Core
 */
class JustpyCore {

	/**
	 * create a JustpyCore instance
	 * @param window
	 * @param {number} page_id - id of the page
	 * @param title - title of the document
	 * @param {boolean} use_websockets - If true use web sockets for communication otherwise ajax is used
	 * @param redirect
	 * @param display_url
	 * @param page_ready
	 * @param result_ready
	 * @param reload_interval_ms
	 * @param {string[]} events - event types the page should listen to
	 * @param {string} staticResourcesUrl - Url to static resources
	 * @param {boolean} debug - If true show debug messages
	 */
	constructor(window,
		page_id,
		title,
		use_websockets,
		redirect,
		display_url,
		page_ready,
		result_ready,
		reload_interval_ms,
		events,
		staticResourcesUrl,
		debug) {
		this.window = window;
		this.page_id = page_id;
		this.setTitle(title);
		this.use_websockets = use_websockets;
		if (redirect) {
			location.href = redirect;
		}
		if (display_url) {
			window.history.pushState("", "", display_url);
		}
		this.page_ready = page_ready;
		this.result_ready = result_ready;
		this.reload_interval_ms = reload_interval_ms;
		this.events = events;
		this.staticResourcesUrl = staticResourcesUrl;
		this.debug = debug;
	}

	/**
	 * set the title
	 * @param title - title of the document
	 */
	setTitle(title) {
		document.title = title;
		this.title = title;
	}

	/**
	 * setup the core functionality
	 */
	setup() {
		if (this.use_websockets) {
			this.setupWebSocket();
		} else {
			this.setupNoWebSocket();
		}
		app1 = createApp();
		this.registerAllEvents();


	}

	/**
	 * prepare WebSocket handling
	 */
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

		socket.addEventListener('open', function(event) {
			console.log('Websocket opened');
			socket.send(JSON.stringify({ 'type': 'connect', 'page_id': page_id }));
		});

		// on error reload site
		socket.addEventListener('error', function(event) {
			reload_site();
		});

		// if side closed → close websocket
		socket.addEventListener('close', function(event) {
			console.log('Websocket closed');
			web_socket_closed = true;
			reload_site()
		});

		socket.addEventListener('message', function(event) {
			this.handleMessageEvent(event);
		}.bind(this));  // handover the class context to the event listener function
	}

	/**
	 * Handles the message event
	 * https://developer.mozilla.org/en-US/docs/Web/API/MessageEvent
	 * @param event
	 */
	handleMessageEvent(event) {
		msg = JSON.parse(event.data);
		if (this.debug) {
			console.log('Message received from server ', msg);
			console.log(event);
		}
		switch (msg.type) {
			case 'page_update':
				this.handlePageUpdateEvent(msg);
				break;
			case 'page_mode_update':
				Quasar.Dark.set(msg.dark);
				break;
			case 'websocket_update':
				this.handleWebsocketUpdateEvent(msg);
				break;
			case 'component_update':
				// update just specific component on the page
				comp_replace(msg.data, app1.justpyComponents);
				break;
			case 'run_javascript':
				this.handleRunJavascriptEvent(msg);
				break;
			case 'run_method':
				// await websocket.send_json({'type': 'run_method', 'data': command, 'id': self.id})
				eval('comp_dict[' + msg.id + '].' + msg.data);
				break;
			case 'draw_crosshair':
				// Remove previous crosshairs
				this.handleDrawCrosshairEvent(msg);
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
				this.handleTooltipUpdate(msg);
				break;
			default: {
				if (this.debug) {
					console.log("Message type " + msg.type + " has no registered event handler");
				}
			}
		}
	}

	/**
	 * handles the page_update event
	 */
	handlePageUpdateEvent(msg) {
		if (msg.page_options.redirect) {
			location.href = msg.page_options.redirect;
			return;
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
				link.href = this.staticResourcesUrl + msg.page_options.favicon;
			}
			document.getElementsByTagName('head')[0].appendChild(link);
		}
		app1.justpyComponents = msg.data;
	}

	/**
	 * Handles the websocket_update event
	 * @param msg
	 */
	handleWebsocketUpdateEvent(msg) {
		websocket_id = msg.data;
		websocket_ready = true;
		if (this.page_ready) {
			const e = {
				'event_type': 'page_ready',
				'visibility': document.visibilityState,
				'page_id': page_id,
				'websocket_id': websocket_id
			};
			send_to_server(e, 'page_event', false);
		}
	}

	/**
	* handle Error
	*/
	handleError(error) {
		if (this.debug) {
			console.log(error);
		}
		this.send_result("Error in javascript")
	}

	/**
	 * send javascript eval result back to server
	 * @param js_result - the javascript result to send
	 */
	send_result(js_result) {
		let e = {
			'event_type': 'result_ready',
			'visibility': document.visibilityState,
			'page_id': this.page_id,
			'websocket_id': websocket_id,
			'request_id': msg.request_id,
			'result': js_result //JSON.stringify(js_result)
		};
		if (this.result_ready) {
			if (msg.send) {
				send_to_server(e, 'page_event', false);
			}
		}
	}

	/**
	 * Handles the run_javascript event
	 * @param msg
	 */
	handleRunJavascriptEvent(msg) {
		/**
		 * callback to send javascript result back to server
		 */
		const jsPromise = new Promise((resolve, reject) => {
			try {
				let eval_result = eval(msg.data)
				resolve(eval_result)
			} catch (error) {
				reject(error)
			}
		});
		jsPromise.then((value) => {
			this.send_result(value);
		}).catch((error) => {
			this.handleError(error);
		});
	}


	/**
	 * Handle the draw_crosshair event
	 * @param msg
	 */
	handleDrawCrosshairEvent(msg) {
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
	}

	/**
	 * Handles the tooltip_update event
	 * @param msg
	 */
	handleTooltipUpdate(msg) {
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
	}

	/**
	 * setup page without websockets
	 * https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event
	 */
	setupNoWebSocket() {
		window.addEventListener('beforeunload', function(event) {
			let e = {
				'event_type': 'beforeunload',
				'page_id': page_id,
			};
			send_to_server(e);
		});
	}

	/**
	 * setup the reload interval
	 */
	setupReloadInterval() {
		if (this.reload_interval_ms > 0) {
			setInterval(function() {
				$.ajax({
					type: "POST",
					url: "/zzz_justpy_ajax",
					data: JSON.stringify({
						'type': 'event',
						'event_data': { 'event_type': 'page_update', 'page_id': this.page_id }
					}),
					success: function(msg) {
						if (msg) app1.justpyComponents = msg.data;
					},
					dataType: 'json'
				});
			}, this.reload_interval_ms);
		}
	}

	/**
	 * register all events
	 */
	registerAllEvents() {
		for (const event of this.events) {
			this.registerEventListener(event);
		}
	}

	/**
	 * adds an event listener to the given event that sends the event with key data to the server
	 * @param {string} event - event type to add the event listener to
	 */
	registerEventListener(event) {
		document.addEventListener(event, function(evt) {
			console.log(evt);
			const e = {
				'event_type': event,
				'visibility': document.visibilityState,
				'page_id': page_id,
				'websocket_id': websocket_id
			};
			if (evt instanceof KeyboardEvent) {
				// https://developer.mozilla.org/en-US/docs/Web/Events/keydown   keyup, keypress
				e['key_data'] = {
					altKey: evt.altKey,
					ctrlKey: evt.ctrlKey,
					shiftKey: evt.shiftKey,
					metaKey: evt.metaKey,
					code: evt.code,
					key: evt.key,
					location: evt.location,
					repeat: evt.repeat,
					locale: evt.locale
				}
			}
			send_to_server(e, 'page_event', false);
		});
	}
}
