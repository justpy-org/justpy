import justpy as jp
import os
import psutil

td_class = "py-4 px-6 border-b border-grey-light"

def dir_test():
    wp = jp.WebPage()
    table = jp.Table(a=wp, classes='m-2 p-1')
    tr = jp.Tr(a=table, classes='border-b-4 text-xl')
    tr.add(jp.Th(text='Name', classes='text-left py-4 px-6'), jp.Th(text='Size'))
    with os.scandir() as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                tr = jp.Tr(a=table)
                tr.add(jp.Td(text=entry.name, classes='text-left ' + td_class), jp.Td(text=f'{entry.stat().st_size:,}', classes=td_class + ' text-center'))
    return wp

@jp.SetRoute('/mem')
def test_memory():
    print('in get mem')
    wp = jp.WebPage()
    mem = psutil.virtual_memory()
    for i in ['available', 'free', 'percent', 'total', 'used']:
        jp.Div(text=f'{i:{20}} {getattr(mem,i):,}', a=wp, classes='m-1 p-1 text-xl border')
    return wp

jp.justpy(dir_test)