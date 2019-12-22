# Deployment

## Introduction

Deployment is a complex issue and contributions to making this easier to explain and do would be appreciated.
Hosting instructions for other platforms and vendors would be appreciated as well.

For reference, the uvicorn deployment instructions can be found [here](https://www.uvicorn.org/deployment/).


## Hosting instructions for a DigitalOcean droplet

Create: Ubuntu 18.04.3 (LTS) x64, Standard plan, $5/month (1Gb/25Gb/1Tb), no block storage authentication with one-time password. Pick a location closest to you or your users.  (If using SSH keys instead of one-time password, follow Digital Ocean's instructions and modify step 2 below accordingly).

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

Clone the repository:
`# git clone https://github.com/elimintz/TestPy.git`

Install the required packages:
```python
# cd TestPy
# pip3 install -r requirements.txt
```

Run a JustPy test:
```python
# cat > hello.py
import justpy as jp
def hello_world():
    wp = jp.WebPage()
    p = jp.P(text='Hello World!', a=wp)
    return wp
jp.justpy(hello_world)
<Ctrl-D>

# python3 hello.py
```


Open a browser, navigate to http://<droplet IP address>:8000


## Adding HTTPS

It is possible to conduct local HTTPS development and testing using self-issued certificates ([see for example](https://woile.github.io/posts/local-https-development-in-python-with-mkcert/)). Remote browsers don’t like this however, so the instructions below concentrate on using a proper host/domain name and a certificate issued by Let’s Encrypt https://letsencrypt.org/ .

If a new domain name is needed, consider [freenom.com](https://freenom.com) . It provides domains such as .tk, .ml, .ga for free.

Follow [Digital Ocean instructions](https://www.digitalocean.com/docs/networking/dns/how-to/add-domains/) to add a fully qualified domain name (FQDN) to your droplet . Make sure you’re able to invoke your JustPy app with http://<droplet FQDN>:8000 . 

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

Open a browser, navigate to https://<droplet FQDN>:8443