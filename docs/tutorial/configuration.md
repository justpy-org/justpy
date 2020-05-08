# Configuration

## Introduction

JustPy is configured by settings in the justpy.env file. The file is not strictly required, as there are defaults for all settings.

Here is an example of a configuration file:

```python
HIGHCHARTS = True
AGGRID = True
LOGGING_LEVEL = DEBUG
LATENCY = 50
SECRET_KEY = '$$$my_secret_string$$$'
```

Since the default for whether to include the Highcharts library is `True`, the first line is not required (neither are the second or fifth).

## Simulating Latency

The `LATENCY` option is one I like to work with. When it is set, JustPy adds the specified milliseconds to each communication between the server and the web pages. In this way you can simulate locally the effect of network latency and see if it hinders the user experience.

## Working Locally without an Internet Connection

If you set the option `NO_INTERNET` to `True`, JustPy will not attempt to use the internet to retrieve the JavasScript libraries it needs, and will use instead copies that are part of the package.
The downside is that between versions of JustPy, the JavaScript libraries will not be updated to the latest version.

Since version 0.1.0 the default for this option is `True`.

## Quasar Version

New in version 0.1.0

You can specify the Quasar version to use:

```python
QUASAR_VERSION = '1.9.4'
``` 

When `NO_INTERNET` is true, version 1.9.4 is used.