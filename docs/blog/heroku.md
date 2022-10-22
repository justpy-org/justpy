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
justpy>=0.10.1
# install dependencies for examples
bokeh
matplotlib
pandas
plotly
pydeck
pygments
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
rsync -avz justpy/examples $pwd
```
#### get the justpy examples
```bash
./getjustpy
git add examples
```
#### commit and push
```
git commit -am "initial check in"
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

###restart
```bash
heroku restart
``

### Configs
```bash
heroku config:set PYTHONPATH=.
``

# Demo
http://justpy-demo.herokuapp.com/