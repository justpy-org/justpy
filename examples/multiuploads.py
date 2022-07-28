from justpy import *

def on_submit(c, msg):
    print(len(msg.form_data[0]["files"][0]["file_content"]))
    print(len(msg.form_data[1]["files"][0]["file_content"]))

def multi_uploads():
    wp=WebPage()
    form=Form(a=wp, submit=on_submit)
    Input(type="file", name="f1", a=form)
    Input(type="file", name="f2", a=form)
    Input(type="submit", value="OK", a=form)
    return wp

justpy(multi_uploads)