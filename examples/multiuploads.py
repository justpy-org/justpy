from justpy import *

def handle_submit(c, msg):
  fl=msg.page.file_list
  fl.components.clear()
  for fd in msg.form_data:
    if "files" in fd:
      for f in fd["files"]:
        Li(text=f"File uploaded: {f['name']} of {len(f['file_content'])}", a=fl)

def p1():
  wp=WebPage()
  f=Form(submit=handle_submit, a=wp)
  Input(name="f1", type="file", a=f)
  Input(name="f2", type="file", a=f)
  Input(type="submit", value="OK", a=f)
  wp.file_list=Ol(a=wp)
  return wp
  

WebPage.tailwind=False
justpy(p1, start_server=(__name__=="__main__"))
