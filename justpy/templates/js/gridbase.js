// {* raw *}

var cached_grid_def = {};
Vue.component('grid', {

  template:
      `<div  v-bind:id="jp_props.container" :class="jp_props.classes"  :style="jp_props.style"  >
    </div>`,
     methods: {
         grid_change() {
            // lookup the container we want the Grid to use
            console.log('#'+ this.$props.jp_props.container);
            j = JSON.stringify(this.$props.jp_props.def);
            console.log(j);
             var eGridDiv = document.querySelector('#'+ this.$props.jp_props.container);

                // create the grid passing in the div to use together with the columns & data we want to use

    cached_grid_def[this.$props.jp_props.container] = j;
    //new agGrid.Grid($('#'+ this.$props.jp_props.container), this.$props.jp_props.def);
             console.log('defs:');
             console.log(this.$props.jp_props.def);
        var    grid_def = JSON.parse(j);
    grid_def.onGridReady = grid_ready;
        new agGrid.Grid(eGridDiv, grid_def);  // the api calls are added to grid_def
    console.log('2defs:');
             console.log(this.$props.jp_props.def);

var rid = this.$props.jp_props.running_id;
var container = this.$props.jp_props.container;
var grid_id = parseInt(container.replace('grid',''));
cached_graph_def[rid] = grid_def;  // you need to retrieve this to call the api
function grid_ready(event) {
    console.log('grid is ready');
    grid_def.columnApi.autoSizeColumns();

}
//grid_def.api.addEventListener('gridReady', grid_ready);
console.log('grid_def'); console.log(grid_def);
  }
  },
    mounted() {
    console.log('mounted');
    console.log(this.$props.jp_props);
    console.log('kelli');
    this.grid_change();
  },
    updated() {
    // api.setRowData(newData)  this changes the data only, doesn't do whole graph
      console.log('updated');
    if (JSON.stringify(this.$props.jp_props.def) == cached_grid_def[this.$props.jp_props.container]) {
        console.log('Not updated because cache');
        return;
    }
    //var chart_old = $("#" + this.$props.chart_props.container).highcharts();
    //chart_old.destroy();
        console.log('updating...');
    grid_to_destroy = cached_graph_def[this.$props.jp_props.running_id];
    grid_to_destroy.api.destroy();
    this.grid_change(); // may need to change to check difference and update with api instead of redraw.


  },
        props: {
        jp_props: Object
  }
});

// {* endraw *}