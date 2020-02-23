import justpy as jp
import pandas as pd


class AutoTable1(jp.Table):

    td_classes = 'border px-4 py-2 text-center'
    tr_even_classes = 'bg-gray-100 '
    tr_odd_classes = ''
    th_classes = 'px-4 py-2'

    def __init__(self, **kwargs):
        self.values = []
        super().__init__(**kwargs)


    def react(self,data):
        self.set_class('table-auto')
        #First row of values is header
        if self.values:
            headers = self.values[0]
            thead = jp.Thead(a=self)
            tr = jp.Tr(a=thead)
            for item in headers:
                jp.Th(text=item, classes=self.th_classes, a=tr)
            tbody = jp.Tbody(a=self)
            for i, row in enumerate(self.values[1:]):
                if i % 2 == 1:
                    tr = jp.Tr(classes=self.tr_even_classes, a=tbody)
                else:
                    tr = jp.Tr(classes=self.tr_odd_classes, a=tbody)
                for item in row:
                    jp.Td(text=item, classes=self.td_classes, a=tr)


wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_df['Year'] = wm_df['Year'].astype('str')
headers = list(wm_df.columns)
table_data = wm_df.to_numpy().tolist()
table_data.insert(0, headers)

def table_test():
    wp = jp.WebPage()
    d = jp.Div(classes='w-7/8 m-2 p-3 border rounded-lg ', a=wp)
    # jp.AutoTable(values=table_data, a=d, classes='block p-4 overflow-auto', style='height: 90vh')
    wm_df.jp.table(classes='block p-4 overflow-auto', style='height: 90vh', a=d)
    return wp

jp.justpy(table_test)
# ----------------------------------
wp = jp.WebPage(delete_flag=False)
wp.tailwind = False
e = jp.EditorMD(a=wp, debounce=0)

def edit_test(request):
    return wp

# jp.justpy(edit_test)
my_table_data = [['Title', 'Author', 'Views'],
                 ['Intro to CSS', 'Adam', '858'],
                 ['A Long and Winding Tour of the History of UI Frameworks and Tools and the Impact on Design', 'Adam', '112'],
                 ['Intro to Javascript', 'Chris', '1,280'],
                 ['Intro to Javascript', '', '12345'],
                 ['Intro to Javascript', 'Chris', '1,280'],
                 ['Intro to Javascript', 'Chris', '1,280'],
]