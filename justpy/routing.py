import starlette.routing 
import typing

class JpRoute(starlette.routing.Route):
    '''
    extends starlette Routing
    
    see 
       https://www.starlette.io/routing/
    
       https://github.com/encode/starlette/blob/master/starlette/routing.py
    '''
    # map for all routes that are defined
    routesByPath={}
    
    @classmethod
    def reset(cls):
        JpRoute.routesByPath={}
        
    @classmethod
    def getFuncForRequest(cls,request):
        '''
        get the function for the given request
        
        Args:
            request: the starlette request
            
        Returns:
            Callable: the function that is bound to the path of the given request
        '''
        scope=request.scope
        return JpRoute.getFuncForScope(scope)
    
    @classmethod
    def getFuncForScope(cls,scope):
        '''
        get the function (endpoint in starlette jargon) for the given scope
        
        Args:
            path: the path to check
        Returns:
            Callable: the function that is bound to the given path 
        '''
        for _path,route in JpRoute.routesByPath.items():
            match,_matchScope=route.matches(scope)
            if match is not starlette.routing.Match.NONE:
                func_to_run=route.endpoint
                return func_to_run
        return None
     
    def __init__(self, path: str, endpoint: typing.Callable,**kwargs):
        '''
        constructor
        '''
        # call super constructor
        starlette.routing.Route.__init__(self, path=path,endpoint=endpoint,**kwargs)
        # remember my routes 
        JpRoute.routesByPath[path]=self
        
    def __repr__(self):
        return f'{self.__class__.__name__}(name: {self.name}, path: {self.path}, format: {self.path_format}, func: {self.endpoint.__name__}, regex: {self.path_regex})'
  
class Route(JpRoute):
    '''
    legacy compatibility layer - use JpRoute instead
    '''
    def __init__(self, path: str, endpoint: typing.Callable,**kwargs):
        JpRoute.__init__(self,path,endpoint,**kwargs)
    
class SetRoute:
    '''
    Justpy specific route annotation
    '''

    def __init__(self, route, **kwargs):
        '''
        constructor
        
        Args:
            route(Route): the starlette route to set
            **kwargs: Arbitrary keyword arguments.
        '''
        self.route = route
        self.kwargs = kwargs

    def __call__(self, fn, **_instance_kwargs):
        '''
        Args:
            fn(Callable): the function
            **_instance_kwargs: Arbitrary keyword arguments (ignored).
        
        '''
        # create a new route
        JpRoute(path=self.route, endpoint=fn,  name=self.kwargs.get('name', None))
        return fn