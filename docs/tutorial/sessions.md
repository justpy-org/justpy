# Sessions in JustPy


JustPy supports secure, server based sessions.

Sessions are supported by default. If you want to disable them, add the line:
 ```python
SESSIONS = False
```
to the configuration file, justpy.env

In the configuration file. You can also set the name of the cookie JustPy will use by setting the value of
`SESSION_COOKIE_NAME`. The default value is 'jp_token'. The max age of the cookie in seconds is set using `COOKIE_MAX_AGE`, default is 7 days.

Your justpy.env file could include for example:
```python
SESSIONS = True
SESSION_COOKIE_NAME = "my_cookie_name"
COOKIE_MAX_AGE = 108000
SECRET_KEY = "my_very_secret_key_that_only_I_know"
```

When a request is received and sessions are enabled, JustPy checks if a session cookie already exits. If not, a new unique session id is generated (using [uuid4](https://docs.python.org/3/library/uuid.html)).

The value of the JustPy cookie is signed using the python package [`itsdangerous`](https://palletsprojects.com/p/itsdangerous/).  In order to do so, a secret key needs to be provided. Set the secret key by setting the value of `SECRET_KEY` in the configuration file justpy.env. JustPy comes with a default value ("$$$my_secret_string$$$") but be sure to change this for production. 

The advantage of signing the cookie is that cookie tampering  can be detected. If JustPy detects that the cookie was tampered with, a  **Bad Cookie** response is returned to the browser. 

!> If you get a **Bad Cookie** response while testing you site, it may mean that you changed your secret key and your cookie is signed with the previous one. Just erase the cookie in your browser and try again. 

If the cookie is validated, the session inserts the session id into the `request` object as `request.session_id`.

!> The JustPy cookie **ONLY** holds the signed session id. There is no other information in the cookie.

!> The JustPy cookie is an [HttpOnly](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#Creating_cookies) cookie and is inaccessible to JavaScript on the page.

## Example

The session id can be used as an index or key to store information about a session. In the example below we define a dictionary called `session_dict` and hold the information there. If you need the session data to persist between
server restarts, you would use a permanent data store like a a shelve or database to hold session data.

In this example, for each session, a tally is kept of the number of visits and the number of clicks.
JustPy provides the session id as part of the information that event handlers receive. If the standard `msg` argument is used, then the session id can be found in `msg.session_id`.

```python
import justpy as jp

session_dict = {}

def session_test(request):
   wp = jp.WebPage()
   if request.session_id not in session_dict:
        session_dict[request.session_id] = {'visits': 0, 'events': 0}
   session_data = session_dict[request.session_id]
   session_data['visits'] += 1
   jp.Div(text=f'My session id: {request.session_id}', classes='m-2 p-1 text-xl', a=wp)
   visits_div = jp.Div(text=f'Number of visits: {session_data["visits"]}', classes='m-2 p-1 text-xl', a=wp)
   b = jp.Button(text=f'Number of Click Events: {session_data["events"]}', classes='m-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full', a=wp)
   b.visits_div = visits_div

   def my_click(self, msg):
       session_data = session_dict[msg.session_id]
       session_data['events'] += 1
       self.text =f'Number of Click Events: {session_data["events"]}'
       self.visits_div.text = f'Number of visits: {session_data["visits"]}'

   b.on('click', my_click)
   return wp

jp.justpy(session_test)
```

Run the program above. Close, open and reload browser tabs and click the button. The session information persists.