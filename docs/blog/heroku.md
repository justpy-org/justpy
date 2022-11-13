# Using justpy with heroku

## Installation
```bash
npm install -g heroku
```
## Getting started with python in general
If you'd like to try out how python apps work in general in heroku
you might want to check
https://devcenter.heroku.com/articles/getting-started-with-python

## Credentials
see $HOME/.netrc after
```bash
heroku login
```

## Create personal heroku justpy demo app

### create an app in heroku and check it out with git
https://dashboard.heroku.com/apps
New/Create new app
choose an available name by adding your initials or
any other available suffix to justpy-demo in my case
Wolfgang Fahl=wf

justpy-demo-wf
follow the instructions to get your git repository

### add files
see https://github.com/justpy-org/justpy/tree/master/tutorial/heroku
#### Procfile
```bash
web: python examples/demo_browser.py --heroku -d 
```
#### requirements.txt
```bash
# WF 2022-10-19
# heroku  justpy demo browser dependencies
#
# install justpy
# check for latest version at https://pypi.org/project/justpy/
justpy>=0.10.5
# install dependencies for examples
altair
bokeh
matplotlib
pandas
pandas_datareader
plotly
pydeck
pygments
scipy
seaborn
vega_datasets
# debugging
pydevd
```
#### getjustpy 
```bash
#!/bin/bash
# WF 2022-10-19
# get the justpy examples and tutorial files
# remember the current directory
pwd=$(pwd)
# url of justpy repository
giturl=https://github.com/justpy-org/justpy
# get a temporary directory
gitdir=$(mktemp -u)
mkdir -p $gitdir
# switch to the temporary directory
cd $gitdir
if [ ! -d justpy ]
then
  echo "cloning to $gitdir"
  git clone --depth=1 $giturl
fi
rm -rf justpy/.git
rsync -avz justpy/examples $pwd --delete
```
#### get the justpy examples
```bash
# make script executable
chmod +x getjustpy
# git clone justpy and rsync examples directory to local directory
./getjustpy
# add justpy examples copy
git add examples
```
#### change PYTHONPATH via config (see also below)
```bash
heroku config:set PYTHONPATH=.
```

#### commit and push
```
git commit -am "initial check in"
# try with "main" if it won't work with "master"
git push heroku master
```

### try out
replace "wf" with you own suffix
http://justpy-demo-wf.herokuapp.com/

## Further commands
### Status Log
```bash
heroku logs --tail
```

### restart
```bash
heroku restart
```

### Configs
```bash
heroku config:set PYTHONPATH=.
```

### Cancelling builds
E.g. in case you see Your account has reached its concurrent builds limit.
see https://stackoverflow.com/a/60215424/1497139
```
heroku plugins:install heroku-builds
heroku builds:cancel
``


# Demo
http://justpy-demo.herokuapp.com/
