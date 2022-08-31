/***
 * justpy core java script
 */
 
 /**
  * Legacy global variables
  */
 var comp_dict = {};  // Hold components for running methods
 var websocket_ready = false;
    
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
  constructor(page_options) {
    this.page_options=page_options
  }
  
}