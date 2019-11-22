# Configuration

JustPy is configured by settings in the justpy.env file. The file is not strictly required, as there are defaults for all settings.

Here is an example of a configuration file:

```python
HIGHCHARTS = True
AGGRID = True
LOGGING_LEVEL = DEBUG
LATENCY = 50
SECRET_KEY = '$$$my_secret_string$$$'
```

Since the default for wheter to include the Highcharts library is `True`, the first line is not required (neither are the second or fifth).

The `LATENCY` option is one I like to work with. When it is specified, JustPy adds the specified milliseconds to each communication between the server and the web pages. In this way you can simulate locally the effect of network latency and see if it hinders the user experience.