import justpy as jp
import subprocess

def top_test(request):
    wp = jp.WebPage()
    command = request.query_params.get('command', 'echo Command not specified')
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    jp.Pre(text=f'> {command}', style='margin: 1rem', a=wp)
    jp.Pre(text=output, a=wp, style='margin: 1rem')
    return wp

jp.justpy(top_test)


# Sines to dev.to