from justpy import Form, Input, Li, Ol, WebPage

# see https://github.com/elimintz/justpy/pull/401
def handle_submit(_c, msg):
    """
    handle submission of a multi upload
    """
    fl = msg.page.file_list
    fl.components.clear()
    for fd in msg.form_data:
        if "files" in fd:
            for f in fd["files"]:
                Li(text=f"File uploaded: {f['name']} of {len(f['file_content'])}", a=fl)


def multiupload():
    """
    show a multi upload
    """
    wp = WebPage()
    WebPage.tailwind = False
    f = Form(submit=handle_submit, a=wp)
    Input(name="f1", type="file", a=f)
    Input(name="f2", type="file", a=f)
    Input(type="submit", value="OK", a=f)
    wp.file_list = Ol(a=wp)
    return wp


from examples.basedemo import Demo

Demo("multi uploads demo", multiupload)
