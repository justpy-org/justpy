from justpy import *

wp = QuasarPage()
editor = QEditor(a=wp, kitchen_sink=True, height='100vh')

def joint_edit():
    return wp

justpy(joint_edit)