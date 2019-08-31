import justpy as jp

class CalendarDate(jp.Div):

    def __init__(self, **kwargs):
        self.month = 'Jan'
        self.year = '2010'
        self.weekday = 'Sun'
        self.day = '1'
        self.color = 'red'
        super().__init__(**kwargs)

    def react(self, data):
        self.inner_html = f"""
                        <div class="w-24 rounded-t overflow-hidden bg-white text-center m-2 cursor-default">
                            <div class="bg-{data['color']}-500 text-white py-1">
                                {self.month}
                            </div>
                            <div class="pt-1 border-l border-r">
                                <span class="text-4xl font-bold">{self.day}</span>
                            </div>
                            <div class="pb-2 px-2 border-l border-r border-b rounded-b flex justify-between">
                                <span class="text-xs font-bold">{self.weekday}</span>
                                <span class="text-xs font-bold">{self.year}</span>
                            </div>
                        </div>
                        """


def comp_test():
    wp = jp.WebPage()
    year = 2019
    month = 'Feb'
    d = jp.Div(classes='flex flex-wrap', a=wp, data={'color': 'purple'})
    for day in range(1,11):
        CalendarDate(day=day, month=month, year=year, color='teal', a=d)
    d = jp.Div(classes='flex flex-wrap', a=wp, data={'color': 'red'})
    for day in range(5, 26):
        c = CalendarDate(day=day, month='Jul', year='2005', color='yellow', a=d)
        c.day += 1    # Notice how the date starts from 6 and not from 5.
    colors = ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']
    s = jp.Select(classes='w-32 text-xl m-2 p-2 bg-white  border rounded-full', a=wp, value='red',
                  change='self.d.data["color"] = self.value')
    s.d = d
    for color in colors:
        s.add(jp.Option(value=color, text=color, classes=f'bg-{color}-600'))
    return wp

jp.justpy(comp_test)