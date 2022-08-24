# General Thoughts

await this.dispatch(event, event_data)  
different than alpine dispatch as there is no bubbling. There is dict of events on the page that has the appropriate component instance and results in run_event.

dispatch must always be awaited.
Currently dict only supports one element per event

Example in card_search.py where the input also captures keydown to make sure it does not propagate to window and also does return True to avoid flicker.

Modifiers: 
* window  put event in window
* once   evaluate expression only once at beginning (good for initialization using python globals)
* stop   stop propagation
* noupdate  add return True at end of init when creating event handler. Does not update page

x-model works just on top direct attributes that are simple types, see task in todo.py. task works but not task[i]. Otherwise, just write it explicitly
