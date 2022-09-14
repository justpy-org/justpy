import typing
from jpcore.justpy_app import JustpyApp

class SetRoute:
    """
    Justpy specific route annotation
    
    """

    def __init__(self, route, **kwargs):
        """
        Constructor

        Args:
            route(Route): the starlette route to set
            **kwargs: Arbitrary keyword arguments.
        """
        self.route = route
        self.kwargs = kwargs

    def __call__(self, wpfunc:typing.Callable, **_instance_kwargs):
        """
        Args:
            wpfunc(Callable): a WebPage returning function
            **_instance_kwargs: Arbitrary keyword arguments (ignored).

        """
        # Create a new route
        app=JustpyApp.app
        app.add_jproute(path=self.route, wpfunc=wpfunc, name=self.kwargs.get("name", None))
        return wpfunc
