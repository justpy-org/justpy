# Justpy Tutorial demo joint_edit from docs/tutorial/pushing_data.md
import justpy as jp

wp = jp.QuasarPage(delete_flag=False)
editor = jp.QEditor(a=wp, kitchen_sink=True, height='94vh')

def joint_edit():
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("joint_edit",joint_edit)
