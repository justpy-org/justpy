# Adding a Context Menu

The example below shows how to add a custom context menu to a grid.

!!! warning
    This only works with the [ag-grid enterprise version](/blog/ag-grid_to_web_page/#ag-grid-enterprise)

```python
import justpy as jp

grid_options = {
    'columnDefs': [
      {'headerName': "Make", 'field': "make"},
      {'headerName': "Model", 'field': "model"},
      {'headerName': "Price", 'field': "price"}
    ],
    'rowData': [
      {'row_id': 0, 'make': "Toyota", 'model': "Celica", 'price': 35000},
      {'row_id': 1, 'make': "Ford", 'model': "Mondeo", 'price': 32000},
      {'row_id': 2, 'make': "Porsche", 'model': "Boxter", 'price': 72000}
    ],
    'getRowNodeId': '''function (data) {
          return data.row_id;
      }''',    
    'getContextMenuItems': '''function getContextMenuItems(params) {
          if (!websocket_ready && use_websockets) return;
          var e = {page_id: page_id, websocket_id: websocket_id, event_type: 'result_ready'};
          var result = [
            {
              // menu item 1
              name: 'New Row',
              subMenu: [
                  {
                    name: 'Chevy',
                    action: function () {
                        e.result = {menu_action: "new", make: "Chevy"};
                        send_to_server(e, 'page_event', false);
                    }
                  },
                  {
                    name: 'Honda',
                    action: function () {
                        e.result = {menu_action: "new", make: "Honda"};
                        send_to_server(e, 'page_event', false);
                    }
                  },                  
                ]
            },
            {
              // menu item 2
              name: 'Copy Row',
              action: function () {   
                if (params.node) {   
                  e.result = {menu_action: "copy", row_data: params.node.data};
                  send_to_server(e, 'page_event', false);
                }
              },
            },   
            {
              // menu item 3
              name: 'Delete Row',
              action: function () {
                if (params.node) {       
                  e.result = {menu_action: "delete", row_data: params.node.data};
                  send_to_server(e, 'page_event', false);
                }
              },
            },                   

          ];
          return result;
        }'''
}

async def result_ready(self, msg):
    wp = msg.page

    if msg.result['menu_action'] == 'new':
      row_data = {'row_id': wp.next_row_id}   
      row_data['make'] = msg.result['make']
      row_data['model'] = f'test {wp.next_row_id}'
      row_data['price'] = wp.next_row_id * 98765   
      wp.next_row_id += 1
      await wp.run_javascript(f"""cached_grid_def['g' + {wp.grid.id}].api.applyTransaction({{  add: [{row_data}] }})""")       

    elif msg.result['menu_action'] == 'copy':
      row_data = msg.result['row_data']
      row_data['row_id'] = wp.next_row_id
      wp.next_row_id += 1
      await wp.run_javascript(f"""cached_grid_def['g' + {wp.grid.id}].api.applyTransaction({{  add: [{row_data}] }})""")

    elif msg.result['menu_action'] == 'delete':
      row_data = msg.result['row_data']
      await wp.run_javascript(f"""cached_grid_def['g' + {wp.grid.id}].api.applyTransaction({{  remove: [{row_data}] }})""")

def grid_test_context():
    wp = jp.WebPage()
    wp.on('result_ready', result_ready)
    wp.grid = jp.AgGrid(a=wp, options=grid_options)
    wp.next_row_id = len(grid_options['rowData'])
    wp.grid.evaluate = ['getContextMenuItems', 'getRowNodeId']
    return wp

jp.justpy(grid_test_context)

```
