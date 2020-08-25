# Deployment

## Simple Deployment

Launch a Linux Virtual Machine on your preferred cloud service.

If you are not a superuser, become one. 

Update your machine and install pip3:

```
apt update
apt install python3-pip
```


Follow the [getting started](/tutorial/getting_started) instructions. This will prepare your VM to run your JustPY program.

Then, set the `HOST` parameter in the configuration file justpy.env to the public IP address of the VM or to '0.0.0.0' (one should work). If you want to use the default port, set the `PORT` parameter to 80 (otherwise port 8000 will be used). In some cloud services only port 80 is supported by default. In some cloud services, if you are not logged in as root by default, you will need to run the program with sudo.

For example you may add the following two lines to justpy.env:
```python
HOST = '0.0.0.0'
PORT = 80
```

Alternatively, you can use the `host` and `port` parameter in the `justpy` command.

Now, point your browser to your VM using the IP address and port and you should be good to go. If your VM is assigned a domain name, you can use that. 


## More Complex Deployment

For more complex deployments please look at the [uvicorn deployment instructions](https://www.uvicorn.org/deployment/).

Make sure to set the `start_server` keyword argument of the [`justpy`](/reference/justpy) command to`False`, so that uvicorn server is not started.

You also need to expose the starlette app to unvicorn. If test.py is your main program file where you import justpy then you need to add the following line to it after importing justpy:
```python
import justpy as jp
app = jp.app
```

!!! warning
    The following JustPy configuration file params do not get set in this case: HOST, PORT, UVICORN_LOGGING_LEVEL, SSL_KEYFILE, SSL_CERTFILE, SSL_VERSION. You will need to specify the required configuration in the command line or in the Gunicorn configuration file if you want to use a value different than the default one uvicorn uses.
    
    



