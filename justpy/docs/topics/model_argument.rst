The Model Argument
==================

The `model`  argument creates two way data bindings for `Input`, `Textarea`, and `Select` components. It creates a one way data binding for the `text` attribute in the `Div`component and most other components who inherit from `Div`. All this will be explained with many examples so don't worry if at this stage things are not clear.

The `model` argument is based on the `data` attribute. Any `WebPage` or `Div` component has a `data` attribute as well as any component that inherits from them. The `data` attribute is a dictionary of the form `{'my_text': 'This is some text'}`