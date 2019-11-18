# mkdocs.org docsify.js.org
import http.server
import socketserver
import shutil
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def combine_docs(name_list, result_name):
    with open(f'{dir_path}/{result_name}/{result_name}.md', 'wb') as combined_file:
        for name in name_list:
            print(name)
            with open(f'{dir_path}/{result_name}/{name}', 'rb') as f:
                shutil.copyfileobj(f, combined_file)


tutorial_files = ['getting_started.md', 'basic_concepts.md', 'handling_events.md', 'html_components.md', 'routes.md',
                  'request_object.md', 'input.md', 'intermezzo_1.md', 'working_with_html.md', 'pushing_data.md',
                  'ajax.md', 'model_and_data.md', 'sessions.md', 'configuration.md', 'custom_components.md'
                  ]

combine_docs(tutorial_files, 'tutorial')

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving docs http://localhost:{PORT}")
    httpd.serve_forever()

f'{dir_path}/{result_name}/{name}'