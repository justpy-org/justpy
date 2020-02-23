import justpy as jp

wp = jp.QuasarPage(delete_flag=False)
editor = jp.QEditor(a=wp, kitchen_sink=True, height='94vh')

def joint_edit():
    return wp

jp.justpy(joint_edit)