# Sessions in JustPy

JustPy supports secure server based sessions.

To enable sessions, set `SESSIONS` to true. You can also set the name of the cookie JustPy will use by setting the value of `SESSION_COOKIE_NAME`. The default value is `'jp_token'`.  The max age of the cookie in seconds is set using `COOKIE_MAX_AGE`, default is 7 days.

When a request is received and sessions are enabled, JustPy checks if a session cookie already exits. If not a new unique session id is generated (using uuid4()). 

The value of the JustPy cookie is signed using the python package [**itsdangerous**](<https://pythonhosted.org/itsdangerous/ ). To do so a secret_key needs to be provided. Set the secret key by setting the value of `SECRET_KEY`. JustPy comes with a default value but be sure to change this for production. The advantage of signing the cookie is that tampering with the cookie value can be detected. If JustPy detects that the cookie was tampered with, a ''**Bad Cookie**" response is returned to the browser. 

If the cookie is validated, the session inserts the session_id into the request as `request.session_id` 

It can be used as an index, for example, into a server side dictionary keeping session data. If you need the session data to persist between server restarts, then use a shelve or database to hold session data. If your secret key remains the same, the restarted server will be able to un-sign the cookie correctly.

Example:

```python
import justpy as jp

session_dict = {}

def session_test(request):
    wp = jp.WebPage()
    if request.session_id in session_dict:
        session_data = session_dict[request.session_id]
    else:
        session_dict[request.session_id] = {'visits': 0, 'events': 0}
        session_data = session_dict[request.session_id]
    session_data['visits'] += 1
    jp.Div(text=f'My session id: {request.session_id}', classes='m-2 p-1 text-xl', a=wp)
    visits = session_data['visits']
    visits_div = jp.Div(text=f'Number of visits: {visits}', classes='m-2 p-1 text-xl', a=wp)
    events = session_data['events']
    b = jp.Button(text=f'Number of Click Events: {events}', classes='m-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full', a=wp)
    b.visits_div = visits_div

    def click(self, msg):
        session_data = session_dict[msg.session_id]
        session_data['events'] += 1
        events = session_data['events']
        self.text =f'Number of Click Events: {events}'
        visits = session_data['visits']
        self.visits_div.text = f'Number of visits: {visits}'

    b.on('click', click)
    return wp


jp.justpy(session_test)
# Click on button to add events and open page in another tab or browser to add visits
```

