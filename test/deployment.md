# Deployment

## Introduction

Deployment can get complicated and contributions to making this easier to explain and do would be appreciated.
Hosting instructions for other platforms and vendors would be appreciated as well.

For reference, the uvicorn deployment instructions can be found [here](https://www.uvicorn.org/deployment/).


## Hosting instructions for a DigitalOcean droplet

Create an Ubuntu 18.04.3 (LTS) x64 droplet, no block storage authentication with one-time password. Pick a location closest to you or your users.  

The Standard $5/month (1Gb/25Gb/1Tb) plan is good enough to start with. You can upgrade your droplet as the need arises.

If using SSH keys instead of one-time password, follow Digital Ocean's instructions and modify step 2 below accordingly.

Once the email with the IP address and root password is received, ssh into the droplet and follow the prompts to change the root password.

Once in root prompt confirm availability of python3:
```
# python3 --version
Python 3.6.8
```

If the output is “Command ‘python3’ not found…”, then “something went wrong”

Install pip3:
```python
# apt update
# apt install python3-pip
```

!> `apt` will want to install/update multiple packages, answer Y


To test the installation, create a file called 'hello.py' with the following:
```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp

jp.justpy(hello_world, host='<droplet IP address>')
```

Then run the program:
```
# python3 hello.py
```

Alternatively, instead of specifying the `host` keyword in the `justpy` command, you can create a justpy.env file and insert the line:
```python
HOST = '<droplet IP address>' 
```

Open a browser, navigate to http://<droplet IP address>:8000

You should get the Hello component on the page if the setup was successful.


## Adding HTTPS

It is possible to conduct local HTTPS development and testing using self-issued certificates ([see for example](https://woile.github.io/posts/local-https-development-in-python-with-mkcert/)). Remote browsers don’t like this however, so the instructions below concentrate on using a proper host/domain name and a certificate issued by Let’s Encrypt https://letsencrypt.org/ .

If a new domain name is needed, consider [freenom.com](https://freenom.com) . It provides domains such as .tk, .ml, .ga for free.

Follow [Digital Ocean instructions](https://www.digitalocean.com/docs/networking/dns/how-to/add-domains/) to add a fully qualified domain name (FQDN) to your droplet . Make sure you’re able to invoke your JustPy app with http://\<droplet FQDN\>:8000 . 

Follow [LetsEncrypt instructions for certbot](https://certbot.eff.org/lets-encrypt/ubuntubionic-other) to create your certificate: 

In the root TestPy directory, create a JustPy config file to specify the paths to the key file and the certificate file. Optionally, change the port setting.
 ```
# cd TestPy
# cat > justpy.env
SSL_KEYFILE="/path/to/letsencrypt/live/<hostname>/privkey.pem"
SSL_CERTFILE="/home/justpy/letsencrypt/live/<hostname>/cert.pem"
PORT=8443
```
 

Re-run the JustPy test:
`# python3 hello.py`

Open a browser, navigate to https://\<droplet FQDN\>:8443