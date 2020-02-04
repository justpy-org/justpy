from starlette.routing import compile_path
import typing


class Route:

    # Modified code from Starlette routing.py: https://github.com/encode/starlette/blob/master/starlette/routing.py
    # Copyright © 2018, Encode OSS Ltd. All rights reserved.
    # You may obtain a copy of the License at: https://github.com/encode/starlette/blob/master/LICENSE.md

    instances = []
    id = 0

    def __init__(self, path: str, func_to_run: typing.Callable, last=False, **kwargs):

        assert path.startswith("/"), "Routed paths must start with '/'"
        self.path = path
        self.func_to_run = func_to_run
        self.name = kwargs.get('name', None)
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        self.id = Route.id
        Route.id += 1
        if last:
            Route.instances.append(self)
        else:
            Route.instances.insert(0, self)

    def matches(self, path, request):
        match = self.path_regex.match(path)
        if match:
            matched_params = match.groupdict()
            for key, value in matched_params.items():
                matched_params[key] = self.param_convertors[key].convert(value)
            request.path_params.update(matched_params)
            return self.func_to_run
        else:
            return False

    def __repr__(self):
        return f'{self.__class__.__name__}(name: {self.name}, id: {self.id}, path: {self.path}, format: {self.path_format}, func: {self.func_to_run.__name__}, regex: {self.path_regex})'


class SetRoute:

    def __init__(self, route, **kwargs):
        self.route = route
        self.kwargs = kwargs


    def __call__(self, fn, **kwargs):
        Route(self.route, fn,  name=self.kwargs.get('name', None))
        return fn


