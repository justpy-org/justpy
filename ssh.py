from fabric import *
import os
# http://docs.fabfile.org/en/2.4/


def upload_digital_ocean():
    print('Uploading to DigitalOcean...')
    p = {"password": "d$$5Fg1tt"}
    python_files =['app.py', 'newcomponents.py', 'graphcomponents.py', 'gridcomponents.py', 'jpstart.py', 'htmlparser.py', 'JPQuery.py', 'parsedcomponents.py',
                   'womenmajors.py', 'quasarcomponents.py', 'materialcomponents.py', 'pandasgraphs.py']
    # Go in templates directory (also js files)
    template_files =['tailwindsbase.html', 'server_render.html', 'quasarbase.html']
    js_files = ['js/EventHandlerJP.js', 'js/basejp.js', 'js/rowjp.js', 'js/htmljp.js', 'js/graphjp.js', 'js/gridbase.js', 'js/editorjp.js',
                'js/calendardate.js', 'js/m-rowjp.js','js/m-basejp.js',]
    # Goes in static
    css_files = ['css/tooltip.css']
    theme_files = ['themes/sand-signika.js']
    data_files = ['women_majors.csv']
    base_directory = '/root/justpy/'
    with Connection('198.199.81.28', user='root', port=22, connect_kwargs=p) as c:
        for f in python_files:
            print(f)
            r = c.put(f, base_directory + f)
            print(f)

        for f in template_files + js_files:
            print(base_directory + 'templates/' + f)
            r = c.put('templates/' + f, base_directory + 'templates/' + f)
            print(f, r)

        for f in css_files + theme_files:
            r = c.put('static/' + f, base_directory + 'static/' + f)
            print(f, r)

        for f in data_files:
            r = c.put('data/' + f, base_directory + 'data/' + f)
            print(f, r)

        for f in os.listdir('static/html'):
            r = c.put('static/html/' + f, base_directory + 'static/html/' + f)
            print(f, r)

        #r = c.run('source jp')
        print('++++++++++++++++++++++++++++++++++++++++++++++++')
        # print(r.stdout)
        print('++++++++++++++++++++++++++++++++++++++++++++++++')

# upload_digital_ocean()


def deploy_digital_ocean():
    p = {"password": "d$$5Fg1tt"}
    python_files =['app.py', 'newcomponents.py', 'graphcomponents.py', 'gridcomponents.py', 'jpstart.py', 'htmlparser.py', 'JPQuery.py', 'parsedcomponents.py', 'womenmajors.py']
    # Go in templates directory (also js files)
    template_files =['tailwindsbase.html', 'server_render.html']
    js_files = ['js/EventHandlerJP.js', 'js/basejp.js', 'js/rowjp.js', 'js/htmljp.js', 'js/graphjp.js', 'js/gridbase.js', 'js/calendardate.js']
    # Goes in static
    css_files = ['css/tooltip.css']
    theme_files = ['themes/sand-signika.js']
    base_directory = 'root/justpy/'
    with Connection('198.199.81.28', user='root', port=22, connect_kwargs=p) as c:
        c.run('ls -l')
        c.put('app.py', '/root/justpy/' + 'app.py')

# test_digital_ocean()

# connect_webfaction()

# connect_codeanywhere()
# print(os.getcwd())
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

def list_files():
    print(os.listdir('static/html'))



def walk_dir():
    for root, dirs, files in os.walk('C:\\Users\\eli\\PycharmProjects\\StarPy\\justpy'):
        print(root, dirs, files)

# walk_dir()


def upload_starpy():
    print(os.getcwd())
    print('Uploading to DigitalOcean...')
    p = {"password": "d$$5Fg1tt"}

    base_directory = '/root/starpy/justpy/'
    with Connection('198.199.81.28', user='root', port=22, connect_kwargs=p) as c:
        for f in ['classcreator.py', 'htmlcomponents.py', 'justpy.py', 'tailwind.py', 'utilities.py', '__init__.py', 'chartcomponents.py']:
            print(f)
            r = c.put('justpy/' + f, base_directory + f)
            print(f)

        for f in ['tailwind.html', '__init__.py']:
            print(f)
            r = c.put('justpy/templates/' + f, base_directory + 'templates/' + f)
            print(f)

        for f in ['editorjp.js', 'EventHandlerJP.js', 'graphjp.js', 'gridbase.js', 'htmljp.js', 'html_component.js']:
            print(f)
            r = c.put('justpy/templates/js/' + f, base_directory + 'templates/js/' + f)
            print(f)

        for f in ['form.css']:
            print(f)
            r = c.put('justpy/templates/css/' + f, base_directory + 'templates/css/' + f)
            print(f)

        for f in ['favicon.ico', 'favicon-16x16.png', 'favicon-32x32.png']:
            print(f)
            r = c.put('justpy/static/' + f, base_directory + 'static/' + f)
            print(f)

        for f in ['bubble.txt', 'histogram.txt', 'streamgraph.txt']:
            print(f)
            r = c.put('highcharts/' + f, '/root/starpy/' + 'highcharts/' + f)
            print(f)

        #r = c.run('source jp')
        print('++++++++++++++++++++++++++++++++++++++++++++++++')
        # print(r.stdout)
        print('++++++++++++++++++++++++++++++++++++++++++++++++')

# upload_starpy()


def upload_starpy_just_apps():
    print(os.getcwd())
    print('Uploading to DigitalOcean...')
    p = {"password": "d$$5Fg1tt"}

    base_directory = '/root/starpy/'
    with Connection('198.199.81.28', user='root', port=22, connect_kwargs=p) as c:
        for f in ['clock.py', 'chartapp.py']:
            print(f)
            r = c.put( f, base_directory + f)
            print(f)

# upload_starpy_just_apps()

def upload_tailwind():
    print(os.getcwd())
    print('Uploading to DigitalOcean...')
    p = {"password": "d$$5Fg1tt"}

    base_directory = '/root/starpy/justpy/'
    with Connection('198.199.81.28', user='root', port=22, connect_kwargs=p) as c:

        for f in ['tailwind.html', '__init__.py']:
            print(f)
            r = c.put('justpy/templates/' + f, base_directory + 'templates/' + f)
            print(f)

upload_tailwind()
# C:\Users\eli\PycharmProjects\StarPy
# C:\Users\eli\PycharmProjects\StarPy\justpy ['static', 'templates', '__pycache__'] ['classcreator.py', 'htmlcomponents.py', 'justpy.py', 'tailwind.py', 'utilities.py', '__init__.py']
# C:\Users\eli\PycharmProjects\StarPy\justpy\static [] []
# C:\Users\eli\PycharmProjects\StarPy\justpy\templates ['css', 'js'] ['tailwind.html', '__init__.py']
# C:\Users\eli\PycharmProjects\StarPy\justpy\templates\css [] ['form.css']
# C:\Users\eli\PycharmProjects\StarPy\justpy\templates\js [] ['editorjp.js', 'EventHandlerJP.js', 'graphjp.js', 'gridbase.js', 'htmljp.js', 'html_component - Copy.js', 'html_component.js']