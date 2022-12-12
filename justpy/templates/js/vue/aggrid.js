// {* raw *}

var cached_grid_def = {};

Vue.component('grid', {
    template:
        `<div  v-bind:id="jp_props.id" :class="jp_props.classes"  :style="jp_props.style"  ></div>`,
    methods: {
        evaluate_formatters(def) {
            if (Array.isArray(def)) {
                for (const element of def) {
                    this.evaluate_formatters(element);
                }
            } else if (typeof def == "object" && def !== null) {
                for (const [key, value] of Object.entries(def)) {
                    if (key.toLowerCase().includes('formatter')) {
                        eval('def[key] = ' + def[key]);
                    }
                    this.evaluate_formatters(value);
                }
            }
        },
        grid_change() {
            let jp_props = this.$props.jp_props;
            let jp_component_id = jp_props.id;
            let jp_grid_id = 'g' + jp_component_id
            let j = JSON.stringify(jp_props.def);
            let grid_def = JSON.parse(j);  // Deep copy the grid definition
            // Define a default cell renderer if none is defined
            for (const column of jp_props.html_columns) {
                if (grid_def.columnDefs[column].cellRenderer === undefined){
                    grid_def.columnDefs[column].cellRenderer = function (params) {
                        return params.value ? params.value : '';
                    };
                }

            }
            cached_grid_def[jp_component_id] = j;
            grid_def.onGridReady = grid_ready;
            grid_def.popupParent = document.querySelector('body');
            // @FIXME causes https://github.com/justpy-org/justpy/issues/467
            // and https://github.com/justpy-org/justpy/issues/369
            // this.evaluate_formatters(grid_def);
            for (const field of jp_props.evaluate) {
                eval('grid_def[field] = ' + grid_def[field]);
            }
            // Code for CheckboxRenderer https://blog.ag-grid.com/binding-boolean-values-to-checkboxes-in-ag-grid/
            function CheckboxRenderer() {
            }

            CheckboxRenderer.prototype.init = function (params) {
                this.params = params;

                this.eGui = document.createElement('input');
                this.eGui.type = 'checkbox';
                this.eGui.checked = params.value;

                this.checkedHandler = this.checkedHandler.bind(this);
                this.eGui.addEventListener('click', this.checkedHandler);
            };

            CheckboxRenderer.prototype.checkedHandler = function (e) {
                let checked = e.target.checked;
                let colId = this.params.column.colId;
                this.params.node.setDataValue(colId, checked);
            };

            CheckboxRenderer.prototype.getGui = function (params) {
                return this.eGui;
            };

            CheckboxRenderer.prototype.destroy = function (params) {
                this.eGui.removeEventListener('click', this.checkedHandler);
            };

            grid_def.components = {
                checkboxRenderer: CheckboxRenderer
            };

            let jp_component_element = document.getElementById(jp_component_id.toString())
            new agGrid.Grid(jp_component_element, grid_def);  // the api calls are added to grid_def
            cached_grid_def[jp_grid_id] = grid_def;

            function grid_ready(event) {
				// handle the grid_ready event
                if (jp_props.auto_size) {
					// array of all column Ids
                    let allColumnIds = [];
                    // get all columns - might be null
                    let allColumns=grid_def.columnApi.getAllColumns()
                    // loop if there are any columns
                    if (allColumns) {
                    	allColumns.forEach(function (column) {
                        	allColumnIds.push(column.colId);
                      	});
                      	grid_def.columnApi.autoSizeColumns(allColumnIds);
                    }
                }
            }

            grid_def.api.addGlobalListener(global_listener);

            /**
             * Global event listener for the grid
             * only listens to events included in $props.jp_props.events
             * @param {string} event_name - name of the event
             * @param event_obj
             */
            function global_listener(event_name, event_obj) {
                if (jp_props.events.includes(event_name)) {
                    let e = {
                        'event_type': event_name,
                        'grid': 'ag-grid',
                        'id': jp_props.id,
                        'class_name': jp_props.class_name,
                        'html_tag': jp_props.html_tag,
                        'vue_type': jp_props.vue_type,
                        'page_id': page_id,
                        'websocket_id': websocket_id
                    };
                    const more_properties = ['value', 'oldValue', 'newValue', 'context', 'rowIndex', 'data', 'toIndex',
                        'firstRow', 'lastRow', 'clientWidth', 'clientHeight', 'started', 'finished', 'direction', 'top',
                        'left', 'animate', 'keepRenderedRows', 'newData', 'newPage', 'source', 'visible', 'pinned',
                        'filterInstance', 'rowPinned', 'forceBrowserFocus'];
                    for (let property of more_properties) {
                        if (typeof event_obj[property] !== "undefined") {
                            e[property] = event_obj[property];
                        }
                    }
                    // add column properties to event message
                    if (typeof event_obj.column !== "undefined") {
                        e.colId = event_obj.column.colId;
                    }
                    // add node properties to event message
                    if (typeof event_obj.node !== "undefined") {
                        let node_properties = ['selected', 'rowHeight'];
                        for (let property of node_properties) {
                            if (!(typeof event_obj.node[property] === "undefined")) {
                                e[property] = event_obj.node[property];
                            }
                        }
                        e.selected = event_obj.node.selected;
                        e.row_id = event_obj.node.id;
                    }
                    // add row data to event message
                    const dataChangeEvents = ['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd'];
                    if (dataChangeEvents.includes(event_name)) {
                        e.data = grid_def.api.getDataAsCsv();
                    }
                    delete e.source;   // the source property cannot be stringified see https://github.com/justpy-org/justpy/issues/304
                    send_to_server(e, 'event');
                }
            }
        }
    },
    mounted() {
        this.grid_change();
    },
    updated() {
        if (JSON.stringify(this.$props.jp_props.def) !== cached_grid_def[this.$props.jp_props.id]) {
            let grid_to_destroy = cached_grid_def['g' + this.$props.jp_props.id];
            grid_to_destroy.api.destroy();
            this.grid_change(); // Explore option to check difference and update with api instead of destroying and creating new grid
        }
    },
    props: {
        jp_props: Object
    }
});