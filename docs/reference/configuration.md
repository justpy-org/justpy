# Configuration Variables

Please read [configuration in tutorial](/tutorial/configuration) first for an overview of configuration.

The variables below can be set in the justpy.env. The file needs to be located in the directory from which the program is run.
See also [configuration in tutorial](/tutorial/configuration)

```python

config = Config('justpy.env')
# Determines if error is shown in browser when it occurs
DEBUG = config('DEBUG', cast=bool, default=True)

# If set to True, the program terminates if there is an error in an event handler
CRASH = config('CRASH', cast=bool, default=False)

# When True the console displays the memory taken by the program each time a browser tab closes so you check if memory is being reclaimed
# It requires psutil to be installed
MEMORY_DEBUG = config('MEMORY_DEBUG', cast=bool, default=False)
if MEMORY_DEBUG:
    import psutil

# If not 0, the framework simulates a latency between the front end and backend when the program is run
# This is useful in order to asses how latency will affect user experience. The value is the latency in milliseconds.
LATENCY = config('LATENCY', cast=int, default=0)
if LATENCY:
    print(f'Simulating latency of {LATENCY} ms')

# If True sessions are created
SESSIONS = config('SESSIONS', cast=bool, default=True)

# The cookie name to use. Cookie only contains signed session id
SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', cast=str, default='jp_token')

# The secret key is used to sign the session cookies
SECRET_KEY = config('SECRET_KEY', default='$$$my_secret_string$$$')    # Make sure to change when deployed

# The time the cookie is valid for
COOKIE_MAX_AGE = config('COOKIE_MAX_AGE', cast=int, default=60*60*24*7)   # One week in seconds

LOGGING_LEVEL = config('LOGGING_LEVEL', default=logging.WARNING)

HOST = config('HOST', cast=str, default='127.0.0.1')
PORT = config('PORT', cast=int, default=8000)
SSL_VERSION = config('SSL_VERSION', default=PROTOCOL_SSLv23)
SSL_KEYFILE = config('SSL_KEYFILE', default='')
SSL_CERTFILE = config('SSL_CERTFILE', default='')

# current_dir is the directory of the module
TEMPLATES_DIRECTORY = config('TEMPLATES_DIRECTORY', cast=str, default=current_dir + '/templates')
STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=os.getcwd())
STATIC_ROUTE = config('STATIC_MOUNT', cast=str, default='/static')
STATIC_NAME = config('STATIC_NAME', cast=str, default='static')

FAVICON = config('FAVICON', cast=str, default='')  # If False gets value from https://elimintz.github.io/favicon.png

TAILWIND = config('TAILWIND', cast=bool, default=True)
QUASAR = config('QUASAR', cast=bool, default=False)
# If none, latest version is loaded unless NO_INTERNET is Tru in which case the version that comes with the package is loaded
QUASAR_VERSION = config('QUASAR_VERSION', cast=str, default=None)
HIGHCHARTS = config('HIGHCHARTS', cast=bool, default=True)
AGGRID = config('AGGRID', cast=bool, default=True)
AGGRID_ENTERPRISE = config('AGGRID_ENTERPRISE', cast=bool, default=False)

# Set to True for use with no access to the internet. All resources are loaded locally.
# Set to False to load resources from CDN and work from latest version.
NO_INTERNET = config('NO_INTERNET', cast=bool, default=True)
```