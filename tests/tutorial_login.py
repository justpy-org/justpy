import justpy as jp

users = {}

login_form_html = """
<div class="w-full max-w-xs">
  <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <div class="mb-4">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
        Username
      </label>
      <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username" name="user_name">
    </div>
    <div class="mb-6">
      <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
        Password
      </label>
      <input class="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" name="password" type="password" placeholder="******************">
      <p class="text-red-500 text-xs italic">The password is 'password'</p>
    </div>
    <div class="flex items-center justify-between">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" name="sign_in_btn">
        Sign In
      </button>
    </div>
  </form>
  <p class="text-center text-gray-500 text-xs">
    Example from https://tailwindcss.com/components/forms
  </p>
</div>
"""

alert_html = """
<div role="alert" class="m-1 p-1 w-1/3">
  <div class="bg-red-500 text-white font-bold rounded-t px-4 py-2">
    Password is incorrect
  </div>
  <div class="border border-t-0 border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700">
    <p>Please enter password again.</p>
  </div>
</div>
"""

def login_test(request):
    wp = jp.WebPage()
    session_id = request.session_id
    d = jp.Div(a=wp, text=f'Your session id is: {session_id}', classes='m-1 p-1 text-xl')
    if session_id in users:
        if users[session_id]['logged_in']:
            d = jp.Div(a=wp, text=f'You are already logged in...', classes='m-1 p-1 text-2l')
            logged_in = True
        else:
            logged_in = False
    else:
        users[session_id] = {}
        users[session_id]['logged_in'] = False
        logged_in = False
    if not logged_in:
        # login_form = jp.parse_html(login_form_html, a=wp)
        return login_page(request)
    return wp

@jp.SetRoute('/login')
def login_page(request):
    try:
        if users[request.session_id]['logged_in']:
            return login_test(request)
    except:
        pass
    wp = jp.WebPage()
    wp.display_url = 'login_page'  # Sets the url to display in browser without reloading page
    login_form = jp.parse_html(login_form_html, a=wp, classes='m-2 p-2')
    alert = jp.parse_html(alert_html)
    wp.add(alert)
    alert.show = False
    session_div = jp.Div(text='Session goes here', classes='m-1 p-1 text-xl', a=wp)
    sign_in_btn = login_form.name_dict['sign_in_btn']
    sign_in_btn.user_name = login_form.name_dict['user_name']
    sign_in_btn.session_id = request.session_id
    sign_in_btn.alert = alert
    def sign_in_click(self, msg):
        # self.alert.show = not self.alert.show
        alert.show = not alert.show
        if login_form.name_dict['password'].value == 'password':
            session_div.text = request.session_id + ' logged in succesfuly'
            return login_successful(wp, request.session_id)
        else:
            session_div.text = request.session_id + ' login not successful'
    sign_in_btn.on('click', sign_in_click)
    return wp

def login_successful(wp, s_id):
    wp.delete_components()
    users[s_id]['logged_in'] = True
    wp.display_url = 'login_succesful'
    jp.Div(text='Login successful. You are now logged in', classes='m-1 p-1 text-2xl', a=wp)


jp.justpy(login_test)