# The justpy Command

The `justpy` command starts the web sever and the async loop in which the application runs. Unless the `justpy` command is executed, no web pages will be served.No other command in the file after the `justpy` command will be executed so it should be the last command in the program file. 

`def justpy(func=None, *, start_server=True, websockets=True, host=HOST, port=PORT, startup=None, **kwargs)`

`func` - Function to run if no route assigned functions are available. This is the default function to run if the URL is not recognized as a designated route. If no function is provided, the framework displays the 'Page not found' message.

All other arguments are keyword arguments.

`start_server` - If `False`, the server is not started. Use this if you want to run justpy while the server is already running or you want to deploy with a server other than uvicorn (not tested yet).

`websockets` - If `False`, all pages in the application will use Ajax instead of Websockets by default.

`host` - Set to the configuration file HOST setting by default. If not specified in configuration file, it is `0.0.0.0'

`port` - Set to the configuration file PORT setting by default. If not specified in configuration file, it is 8000

`startup` - The function to run before starting the web server. The async loop has already been started but the web server will not start until the function terminates.

All other keyword arguments are used to set the template options. It is better to set these via the configuration file.

```python
template_options = {'tailwind': TAILWIND, 'quasar': QUASAR, 'highcharts': HIGHCHARTS, 'aggrid': AGGRID, 'static_name': STATIC_NAME}
```

For example, if you don't want Highcharts to be loaded, set the keyword parameter `highcharts` to `False`.