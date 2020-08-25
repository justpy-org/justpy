# Notes

## delete vs remove

There is a difference between remove and delete. Remove is just basically:

`self.components.remove(component)`

It does not remove the component (an instance of a Python class) from memory, only from the list of components of some other component.

Delete removes all references within JustPy to an instance so that the Python garbage collection can reclaim its memory.

When you delete a component before removing it from its parent's component list, you remove all references to it from the internal JustPy data structures but a reference remains in its parent's component list.

The framework automatically deletes all components on a page when a browser tab displaying the page is closed (unless the delete_flag is set to False). Alternatively, you can set their `show` attribute to `False` and then they will be deleted by the framework when the browser tab closes.

If you remove an element from a page, and it closes later, it will not be deleted automatically. So you may first want to remove it and then delete it. In most use cases the memory leak is small so unless you have huge traffic you don't need to worry about deleting components until you see a problem emerging. The worst case is you need to restart the server more often.

The delete method also deletes all components the component contains, therefore you don't need to delete them separately (again, unless a child component as the delete_flag set to False).

Only components that the user interacts with or contain components that user interacts with need to deleted because otherwise the framework does not include any reference to them. The components that need deletion include components that explicitly have been assigned an event (like click for a button) or any component that has an input event to which the framework assigns an event even if the user does not (in order to update the value of the component on the server side in the before event handler).

