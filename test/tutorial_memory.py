import justpy as jp

wp = jp.WebPage(delete_flag=False)
header = jp.Div(text='header', classes='text-2xl m-2 p-2', delete_flag=False, a=wp)
main_div = jp.Div(a=wp)
footer = jp.Div(text='footer', classes='text-2xl m-2 p-2', delete_flag=False, a=wp)

def memory_test():
    hello = jp.Hello(a=main_div)
    return wp

jp.justpy(memory_test)