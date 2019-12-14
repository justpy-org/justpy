# Chart Events

## General

The HighCharts component supports events that allow making charts more interactive:
- **point_click** - fires when a point is clicked
- **point_select** - fires when a point is selected
- **point_unselect** - fires when point is unselected
- **series_hide** - fires when series is hidden
- **series_show** - fires when series is shown
- **series_click** - fires when series is clicked
- **tooltip** - fires when chart requests a tootltip (covered in its own [chapter](charts_tutorial/tooltips.md) in the tutorial)


For all chart events, JustPy adds the following fields to the second argument of the event handler (`msg` in this tutorial): 
- `msg.x` - the x value of the point
- `msg.y` - the y value of the point
- `msg.category` - the category value of the point
- `msg.color` - the point's color
- `msg.series_name` - the name of the series the point is in
- `msg.series_index` - the index of the series the point is in
- `msg.point_index` - the index of the point in the series

## point_click




## draw_crosshair Method
 
 
 ## point_click Event and select_point Method
 
 Let's look into the event handler `click_point` above.
 ```python
async def click_point(self, msg):
    print(msg)
    return await self.select_point([{'id': chart_id, 'series': msg.series_index, 'point': msg.point_index} for chart_id in self.chart_list if self.id != chart_id], msg.websocket)
```
 
The event handler is bound to the point_click event of the chart, the event that occurs when a point is clicked.

JustPy adds the following fields to `msg` when event handlers for point_click are activated:
- `msg.x` - the x value of the point
- `msg.y` - the y value of the point
- `msg.category` - the category value of the point
- `msg.color` - the point's color
- `msg.series_name` - the name of the series the point is in
- `msg.series_index` - the index of the series the point is in
- `msg.point_index` - the index of the point in the series



 
## select_point Method

## Series events https://api.highcharts.com/highcharts/plotOptions.series.events

