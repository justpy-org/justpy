# Justpy Tutorial demo session_test from docs/tutorial/sessions.md
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

# initialize the demo
from examples.basedemo import Demo
Demo("session_test", session_test)
