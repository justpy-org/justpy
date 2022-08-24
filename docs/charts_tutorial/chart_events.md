# Chart Events and Methods

## Events

The HighCharts component supports events that allow making charts more interactive:

- **point_click** - fires when a point is clicked
- **point_select** - fires when a point is selected
- **point_unselect** - fires when point is unselected
- **series_hide** - fires when series is hidden
- **series_show** - fires when series is shown
- **series_click** - fires when series is clicked
- **tooltip** - fires when chart requests a tooltip (covered in its own [chapter](../tooltips) in the tutorial)


For all chart events, JustPy adds the following fields to the second argument of the event handler (`msg` in this tutorial): 
- `msg.x` - the x value of the point
- `msg.y` - the y value of the point
- `msg.category` - the category value of the point
- `msg.color` - the point's color
- `msg.series_name` - the name of the series the point is in
- `msg.series_index` - the index of the series the point is in
- `msg.point_index` - the index of the point in the series

## Methods

### `async def draw_crosshair(self, point_list, websocket)`

Draw crosshairs for designated points.

```python
    async def draw_crosshair(self, point_list, websocket):
        # data is list of of dictionaries  whose keys are:
        # 'id': the chart id 
        # 'series': the series index
        # 'point': the point index 
        #  Values are  all integers
        # Example:
        # {'id': chart_id, 'series': msg.series_index, 'point': msg.point_index}
        await websocket.send_json({'type': 'draw_crosshair', 'data': point_list})
        # So the page itself does not update, only the tooltip, return True not None
        return True
```

See example of usage in [Iris Flower Dataset Visualization](../iris)


### `async def select_point(self, point_list, websocket)`

Selects designated points.

```python
async def select_point(self, point_list, websocket):
    # data is list of of dictionaries  whose keys are:
    # 'id': the chart id 
    # 'series': the series index
    # 'point': the point index 
    #  Values are  all integers
    # Example:
    # {'id': chart_id, 'series': msg.series_index, 'point': msg.point_index}
    await websocket.send_json({'type': 'select_point', 'data': point_list})
    # So the page itself does not update, only the tooltip, return True not None
    return True
```
 
 See example of usage in [Iris Flower Dataset Visualization](../iris)
 
 