// {* raw *}

var cached_grid_def = {};
Vue.component('grid', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  >
    </div>`,
    methods: {
        grid_change() {
            console.log('in grid change');
            console.log(this.$props);
            console.log(this.$props.jp_props.def);
            var j = JSON.stringify(this.$props.jp_props.def);
            var grid_def = JSON.parse(j);
            console.log(grid_def);
            cached_grid_def[this.$props.jp_props.id] = j;
            grid_def.onGridReady = grid_ready;
            console.log(grid_def);
            console.log(document.getElementById(this.$props.jp_props.id.toString()));
            //new agGrid.Grid(document.querySelector('#' + this.$props.jp_props.id), grid_def);  // the api calls are added to grid_def
            new agGrid.Grid(document.getElementById(this.$props.jp_props.id.toString()), grid_def);  // the api calls are added to grid_def
            cached_grid_def['g' + this.$props.jp_props.id] = grid_def;
            var auto_size = this.$props.jp_props.auto_size;

            function grid_ready(event) {
                // grid_def.columnApi.autoSizeColumns();
                if (auto_size) {
                    var allColumnIds = [];
                    grid_def.columnApi.getAllColumns().forEach(function (column) {
                        allColumnIds.push(column.colId);
                    });
                    grid_def.columnApi.autoSizeColumns(allColumnIds);
                }
            }

            grid_def.api.addGlobalListener(global_listener);
            var events = this.$props.jp_props.events;
            var props = this.$props;

            function global_listener(event_name, event_obj) {
                // console.log(event_name, event_obj);
                if (events.includes(event_name)) {
                    console.log(event_name, event_obj);
                    //getDataAsCsv
                    //console.log(JSON.stringify(event_obj));
                    var event_fields = ['data', 'rowIndex', 'type', 'value']; // for cellClicked and rowClicked
                    var e = {
                        'event_type': event_name,
                        'grid': 'ag-grid',
                        'id': props.jp_props.id,
                        'class_name': props.jp_props.class_name,
                        'html_tag': props.jp_props.html_tag,
                        'vue_type': props.jp_props.vue_type,
                        'colId': (typeof event_obj.column === "undefined") ? null : event_obj.column.colId,
                        'page_id': page_id,
                        'websocket_id': websocket_id
                    };
                    var more_properties = ['value', 'oldValue', 'newValue', 'context', 'rowIndex', 'data', 'toIndex'];
                    for (let i=0; i<more_properties.length; i++ ) {
                        let property = more_properties[i];
                        //if (event_obj.hasOwnProperty(property)) {
                        if (!(typeof event_obj[property] === "undefined"))  {
                            e[property] = event_obj[property];
                        }
                    }
                    if (!(typeof event_obj.column === "undefined")) {
                        e.colId = event_obj.column.colId;
                    }
                    if (['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd'].includes(event_name)) {
                        e.data = grid_def.api.getDataAsCsv();
                    }
                    send_to_server(e);
                }
            }
        }
    },
    mounted() {
        this.grid_change();
    },
    updated() {
        console.log('updated');
        if (JSON.stringify(this.$props.jp_props.def) == cached_grid_def[this.$props.jp_props.id]) {
            console.log('Not updated because cache');
            return;
        }
        console.log('updating...');
        grid_to_destroy = cached_graph_def['g' + this.$props.jp_props.id];
        grid_to_destroy.api.destroy();
        this.grid_change(); // may need to change to check difference and update with api instead of redraw.
    },
    props: {
        jp_props: Object
    }
});

// {* endraw *}